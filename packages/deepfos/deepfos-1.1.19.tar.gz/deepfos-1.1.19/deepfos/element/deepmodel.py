from contextlib import asynccontextmanager, contextmanager
from contextvars import ContextVar
from typing import List, TYPE_CHECKING, Any, Dict, Union, NamedTuple, Iterable, Optional

import edgedb
import pandas as pd
from loguru import logger
from pydantic import BaseModel, parse_obj_as, ValidationError, Field

from deepfos import OPTION
from deepfos.api.deepmodel import DeepModelAPI
from deepfos.api.models.deepmodel import ObjectBasicDTO, ObjectParam
from deepfos.db.edb import create_async_client
from deepfos.element.base import ElementBase, SyncMeta
from deepfos.exceptions import RequiredFieldUnfilled, ObjectNotExist, ExternalObjectReadOnly, RelationRequired, \
    MultiLinkTargetNotUnique, SingleLinkInRelation
from deepfos.lib import serutils
from deepfos.lib.asynchronous import future_property, evloop
from deepfos.lib.decorator import flagmethod
from deepfos.lib.utils import AliasGenerator

__all__ = ['AsyncDeepModel', 'DeepModel', 'to_fields', 'QueryWithArgs']


OBJECT_QUERY = \
    """
     with module schema
     select ObjectType {
         name,
         links: {
             name,
             cardinality,
             required,
             properties: { name, target: {name} } filter .name not in {'source', 'target'},
             target: { name, external, annotations: {name, value := @value} },
             expr,
             constraints: { name, expr, params: { name, value := @value } },
         } filter .name != '__type__',
         properties: {
             name,
             cardinality,
             required,
             target: { name },
             expr,
             constraints: { name, expr, params: { name, value := @value } },
         },
         annotations: {name, value := @value},
         external
     }
    """
BUSINESS_KEY = 'business_key'
BATCH_INSERT_KW = 'data'

# 由于json number最大至int32或int64的数字
# 为避免精度缺失，如下类型需转换为string
# 相应Note见:
# https://www.edgedb.com/docs/stdlib/numbers#type::std::bigint
# https://www.edgedb.com/docs/stdlib/numbers#type::std::decimal
NEED_CAST_STR = ['std::bigint', 'std::decimal', 'std::int64']

DOC_ARGS_KWARGS = """
        Hint:
        
            kwargs语法:
            
                select User{name, is_active} filter .name=<std::str>$name and is_active=<std::bool>$active
            
            .. admonition:: 使用示例
            
                .. code-block:: python
                
                    dm = DeepModel()
                    
                    dm.execute('delete User filter .name=<std::str>$name and is_active=<std::bool>$active', 
                                name='Alice', active='True')
            
            此处 `$` 为以kwargs的方式指定参数的特殊符号，且需在参数前增加相应类型提示
"""


class ObjectElement(ObjectParam):
    @property
    def links(self):
        return {link.code: link for link in self.linkParamList}


class QueryWithArgs(BaseModel):
    commands: str
    kwargs: Dict[str, Any] = Field(default_factory=dict)


class MainField(NamedTuple):
    business_key: str
    is_multi: bool
    props: Iterable[Optional[str]]
    # 目前业务主键创建的类型只会为std::str
    type: str = 'std::str'


class TargetField(BaseModel):
    name: str
    external: bool = False
    annotations: List[Dict[str, str]] = Field(default_factory=list)

    @property
    def is_scalar(self) -> bool:
        return self.name.startswith('std::') or self.name == 'cal::local_datetime'

    @property
    def info(self):
        return {e['name'].rpartition('::')[-1]: e['value'] for e in self.annotations}


class LinkPropField(BaseModel):
    name: str
    target: TargetField

    @property
    def type(self) -> str:
        return self.target.name


class FieldInfo(BaseModel):
    name: str
    target: TargetField
    properties: List[LinkPropField] = Field(default_factory=list)
    expr: str = None
    required: bool = False
    cardinality: str = None

    @property
    def type(self):
        return self.target.name

    @property
    def is_link(self):
        return not self.target.is_scalar

    @property
    def is_multi_link(self):
        return self.is_link and self.cardinality == 'Many'

    @property
    def computable(self):
        return self.expr is not None

    @property
    def external(self):
        return self.target.external

    @property
    def props(self):
        return [p.name for p in self.properties]
    
    @property
    def prop_type(self):
        return {p.name: p.type for p in self.properties}


class ObjectTypeFrame(BaseModel):
    name: str
    links: List[FieldInfo] = Field(default_factory=list)
    properties: List[FieldInfo] = Field(default_factory=list)
    external: bool
    annotations: List[Dict[str, str]] = Field(default_factory=list)

    @property
    def fields(self):
        return {ptr.name: ptr for ptr in [*self.links, *self.properties]}

    @property
    def info(self):
        return {e['name'].rpartition('::')[-1]: e['value'] for e in self.annotations}


def _format_link(df: pd.DataFrame, link_name: str):
    if all(pd.isnull(df['target'])):
        return {'target': pd.NA}

    record = df.drop(columns=['source']).set_index('target')

    if not record.index.is_unique:
        raise MultiLinkTargetNotUnique(f'Multi Link: [{link_name}] relation dataframe中source与target对应存在不唯一性')

    record = record.to_dict(orient='index')
    return {'prop': record, 'target': list(record.keys())}


class BaseField(FieldInfo):
    def fit(self, df: pd.DataFrame, field_name: str):
        """使 :class:`Dataframe` 对应的列符合字段的限制条件

        Args:
            df: 待转换的 :class:`Dataframe`
            field_name: 需要转化的列名
        """
        self.extra_fit(df, field_name)

    def extra_fit(self, df: pd.DataFrame, field_name: str):
        # df[self.col_name] = df[self.col_name].astype(self.dtype, errors='ignore')
        pass


class FieldDateTime(BaseField):
    @staticmethod
    def format_datetime(dt):
        if pd.isna(dt):
            return pd.NA
        return pd.to_datetime(dt).strftime("%Y-%m-%dT%H:%M:%S")

    def extra_fit(self, df: pd.DataFrame, field_name: str):
        df[field_name] = df[field_name].apply(self.format_datetime)


class FieldString(BaseField):
    def format_string(self, data):
        if pd.isna(data):
            return pd.NA
        if self.type in ['std::int64', 'std::bigint']:
            return str(int(data))
        return str(data)

    def extra_fit(self, df: pd.DataFrame, field_name: str):
        df[field_name] = df[field_name].apply(self.format_string)


class FieldFactory:
    field_map = {
        'std::int64': FieldString,
        'std::bigint': FieldString,
        'std::decimal': FieldString,
        'cal::local_datetime': FieldDateTime,
    }

    def __new__(cls, field: Union[FieldInfo, LinkPropField]):
        field_class = cls.field_map.get(field.type, BaseField)
        return field_class(**field.dict())


class ObjectStructure:
    fields: Dict[str, BaseField]
    
    def __init__(self, name, structure: Iterable[FieldInfo]):
        self.name = name
        self.fields = {
            field.name: FieldFactory(field)
            for field in structure
            if not field.computable and field.name != 'id' and not field.external
        }
        self.self_link_fields = []
        for name, field in list(self.fields.items()):
            if field.type == self.name:
                self.self_link_fields.append(name)
            if field.is_multi_link:
                continue
            if not field.is_link:
                continue
            for prop in field.properties:
                self.fields[f'{name}@{prop.name}'] = FieldFactory(prop)

    def fit(self, df: pd.DataFrame):
        """
        对传入的DataFrame的指定数据列执行fit操作。
        直接影响DataFrame数据。

        Args:
            df: 数据源

        """
        valid_fields = []
        for field in df.columns:
            if field in self.fields:
                valid_fields.append(field)
                self.fields[field].fit(df, field)

        return df[valid_fields]


def _iter_link_prop_assign(link, business_key, prop_name, prop_type, is_multi):
    assign_string = f"@{prop_name} := <{prop_type}>"
    if prop_type in NEED_CAST_STR:
        assign_string += '<std::str>'
    if is_multi:
        return f"{assign_string}(json_get(item, '{link}', 'prop', .{business_key}, '{prop_name}'))"

    return f"{assign_string}(json_get(item, '{link}@{prop_name}'))"


def _iter_single_assign(
    field: FieldInfo,
    cast_type: str,
    target_main_field: Dict[str, MainField]
):
    assign_string = f"{field.name} := "
    # 设置标量值
    if field.name not in target_main_field:
        assign_string += f"<{cast_type}>"

        if cast_type in NEED_CAST_STR:
            assign_string += '<std::str>'
            
        return assign_string + f"item['{field.name}']"

    # 设置link target值
    link = field.name
    main_field = target_main_field[link]

    if main_field.props:
        target = (
            cast_type + "{" +
            ",".join(
                _iter_link_prop_assign(link, main_field.business_key, name, field.prop_type[name], main_field.is_multi)
                for name in main_field.props
            ) + "}"
        )
    else:
        target = cast_type
        
    if main_field.is_multi:
        assign_string += f"""(
            select detached {target}
            filter contains(
                <array<{main_field.type}>>(json_get(item, '{link}', 'target')),
                .{main_field.business_key}
            )
        )"""
    else:
        assign_string += f"""(
            select detached {target}
            filter .{main_field.business_key} = <{main_field.type}>(json_get(item, '{link}'))
        )"""

    return assign_string


def bulk_insert_by_fields(
    object_name: str,
    field_type: List[FieldInfo],
    target_main_field: Dict[str, MainField],
):
    insert_assign_body = ','.join(
        [
            _iter_single_assign(field, field.type, target_main_field)
            for field in field_type
        ]
    )

    return f"""
    with raw_data := <json>to_json(<std::str>${BATCH_INSERT_KW}),
    for item in json_array_unpack(raw_data) union (
        insert {object_name} {{
            {insert_assign_body}
        }}
    )
    """


def bulk_update_by_fields(
    object_name: str,
    business_key: str,
    field_type: List[FieldInfo],
    target_main_field: Dict[str, MainField],
    update_fields: Iterable[str] = None,
):
    update_assign_body = ','.join(
        [
            _iter_single_assign(field, field.type, target_main_field)
            for field in field_type if field.name in update_fields
        ]
    )

    return f"""
        with raw_data := <json>to_json(<std::str>${BATCH_INSERT_KW}),
        for item in json_array_unpack(raw_data) union (
            update {object_name} 
            filter .{business_key} = <std::str>item['{business_key}']
            set {{
                {update_assign_body}
            }}
        )
        """


def format_obj(obj: edgedb.Object) -> ObjectTypeFrame:
    if not isinstance(obj, edgedb.Object):
        raise TypeError("预期obj为edgedb.Object")

    serialized = serutils.serialize(obj)

    try:
        return parse_obj_as(ObjectTypeFrame, serialized)
    except ValidationError:
        raise TypeError("预期obj为ObjectType查询得到的结构信息")


def to_fields(obj: edgedb.Object) -> Dict[str, FieldInfo]:
    return format_obj(obj).fields


txn_support = flagmethod('_txn_support_')


class _TxnConfig:
    __slots__ = ('qls', 'in_txn', 'txn_support')

    def __init__(self):
        self.qls = []
        self.in_txn = False
        self.txn_support = False


if OPTION.edgedb.dsn:
    ONLINE_MODE = True
else:
    ONLINE_MODE = False


# -----------------------------------------------------------------------------
# core
class AsyncDeepModel(ElementBase[DeepModelAPI]):
    """DeepModel"""

    def __init__(self): # noqa
        self._txn_ = ContextVar('QLTXN')
        self.appmodule = f"app{OPTION.api.header['app']}"
        self.spacemodule = f"space{OPTION.api.header['space']}"
        if ONLINE_MODE:
            self.client = create_async_client(default_module=self.appmodule)
        else:
            self.client = None
        self.alias = AliasGenerator()

    @future_property
    async def element_info(self):
        """元素信息"""
        from deepfos.api.space import SpaceAPI
        from deepfos.api.models.app import ElementRelationInfo
        from deepfos.exceptions import ElementTypeMissingError
        modules = await SpaceAPI(sync=False).module.get_usable_module()
        target_module = ['MAINVIEW', 'DM']
        for mdl in modules:
            if mdl.moduleType in target_module and mdl.status == 1:
                return ElementRelationInfo.construct_from(mdl)
        raise ElementTypeMissingError('DeepModel组件在空间内不可用')

    @future_property
    async def async_api(self):
        """异步API对象"""
        return await self._init_api()

    def _safe_get_txn_conf(self) -> _TxnConfig:
        try:
            config = self._txn_.get()
        except LookupError:
            config = _TxnConfig()
            self._txn_.set(config)
        return config

    @property
    def _txn_support_(self):
        return self._safe_get_txn_conf().txn_support

    @_txn_support_.setter
    def _txn_support_(self, val):
        self._safe_get_txn_conf().txn_support = val

    @future_property(on_demand=True)
    async def model_objects(self) -> Dict[str, ObjectParam]:
        """MainView中的所有对象详情"""
        api = await self.wait_for('async_api')
        res = await api.object.get_all()
        return {obj.code: obj for obj in res.objectList}

    @future_property(on_demand=True)
    async def model_object_list(self) -> List[ObjectBasicDTO]:
        """MainView中的所有对象列表"""
        api = await self.wait_for('async_api')
        return await api.object.list()

    @future_property(on_demand=True)
    async def user_objects(self) -> Dict[str, edgedb.Object]:
        """当前app下所有的用户对象"""
        objects = await AsyncDeepModel.query_object(
            self,
            f"{OBJECT_QUERY} filter .name like '{self.appmodule}::%'",
        )
        return {
            obj.name.rpartition('::')[-1]: obj
            for obj in objects
        }

    @future_property(on_demand=True)
    async def system_objects(self) -> Dict[str, edgedb.Object]:
        """当前space下所有的系统对象"""
        objects = await AsyncDeepModel.query_object(
            self,
            f"{OBJECT_QUERY} filter .name like '{self.spacemodule}::%'",
        )
        return {
            obj.name.rpartition('::')[-1]: obj
            for obj in objects
        }

    @staticmethod
    def _prepare_variables(kwargs):
        variables = {}
        for k, v in kwargs.items():
            variables[str(k)] = v
        return variables

    async def query_object(self, ql: str, **kwargs) -> List[Any]:
        """执行ql查询语句，得到原始结果返回

        如有变量，以kwargs的方式提供

        Args:
            ql: 执行的ql
        
        See Also:
        
            :func:`query`, 执行ql查询语句，得到序列化后的结果
            :func:`query_df`, 执行ql查询语句，获取DataFrame格式的二维表
            
        """

        if ONLINE_MODE:
            logger.opt(lazy=True).debug(f"Query: [{ql}], \nkwargs: [{kwargs}].")
            return await self.client.query(ql, **kwargs)

        result = await AsyncDeepModel.query(self, ql, **kwargs)
        return serutils.deserialize(result)

    async def query(self, ql: str, **kwargs) -> List[Any]:
        """执行ql查询语句，得到序列化后的结果

        如有变量，以args, kwargs的方式提供

        Args:
            ql: 执行的ql


        .. admonition:: 示例

            .. code-block:: python

                dm = DeepModel()

                # 以变量name 查询User对象
                dm.query('select User{name, is_active} filter .name=<std::str>$name', name='Alice')

        See Also:
        
            :func:`query_df`, 执行ql查询语句，获取DataFrame格式的二维表
            :func:`query_object`, 执行ql查询语句，得到原始结果返回

        """
        if ONLINE_MODE:
            result = await self.query_object(ql, **kwargs)
            return serutils.serialize(result)

        logger.opt(lazy=True).debug(f"Query: [{ql}], \nkwargs: [{kwargs}].")
        result = await self.async_api.deepql.query(
            module=self.appmodule,
            query=ql,
            variables=self._prepare_variables(kwargs)
        )
        result = result.get("json")
        self._maybe_handle_error(result)
        return result

    async def query_df(self, ql: str, **kwargs) -> pd.DataFrame:
        """执行ql查询语句

        获取DataFrame格式的二维表
        如有变量，以kwargs的方式提供

        Args:
            ql: 执行的ql


        .. admonition:: 示例

            .. code-block:: python

                dm = DeepModel()

                # 以变量name 查询User对象，得到DataFrame
                dm.query_df('select User{name, is_active} filter .name=<std::str>$name', name='Alice')
        
        See Also:
        
            :func:`query`, 执行ql查询语句，得到序列化后的结果
            :func:`query_object`, 执行ql查询语句，得到原始结果返回
        
        """
        data = await self.query(ql, **kwargs)
        return pd.DataFrame(data=data)

    query.__doc__ = query.__doc__ + DOC_ARGS_KWARGS
    query_object.__doc__ = query_object.__doc__ + DOC_ARGS_KWARGS
    query_df.__doc__ = query_df.__doc__ + DOC_ARGS_KWARGS

    @txn_support
    async def execute(self, qls: Union[str, List[str], List[QueryWithArgs]], **kwargs):
        """以事务执行多句ql

        Args:
            qls: 要执行的若干ql语句
                 可通过提供QueryWithArgs对象ql的方式定制每句ql的参数信息
                 亦可直接以kwargs的形式提供参数信息
                 会自动用作所有string形式ql的参数

        """
        if isinstance(qls, str):
            qls_with_args = [QueryWithArgs(commands=qls, kwargs=kwargs)]
        else:
            qls_with_args = []
            seen_kwargs_key = set()
            for ql in qls:
                if isinstance(ql, QueryWithArgs):
                    if not ONLINE_MODE and ql.kwargs and seen_kwargs_key.intersection(ql.kwargs.keys()):
                        raise NotImplementedError('线下模式不支持重名variables')

                    qls_with_args.append(ql)
                    if ql.kwargs:
                        seen_kwargs_key = seen_kwargs_key.union(ql.kwargs.keys())

                elif isinstance(ql, str):
                    qls_with_args.append(QueryWithArgs(commands=ql, kwargs=kwargs))
                else:
                    raise TypeError(f'qls参数中出现类型非法成员：{type(ql)}')

        await self._maybe_exec_qls(qls_with_args)

    execute.__doc__ = execute.__doc__ + DOC_ARGS_KWARGS

    async def _execute(self, qls_with_args: List[QueryWithArgs]):
        self.alias.reset(BATCH_INSERT_KW)
        if not ONLINE_MODE:
            kwargs = {}
            seen_kwargs_key = set()

            for ql in qls_with_args:
                if ql.kwargs and seen_kwargs_key.intersection(ql.kwargs.keys()):
                    raise NotImplementedError('线下模式不支持重名variables')
                if ql.kwargs:
                    kwargs.update(ql.kwargs)
                    seen_kwargs_key = seen_kwargs_key.union(ql.kwargs.keys())

            commands = ';'.join([ql.commands for ql in qls_with_args])

            logger.opt(lazy=True).debug(
                f"Execute QL: [{commands}], \nkwargs: [{kwargs}]."
            )
            res = await self.async_api.deepql.execute(
                    module=self.appmodule,
                    query=commands,
                    variables=self._prepare_variables(kwargs)
                )
            self._maybe_handle_error(res.get('json'))
            return

        async for tx in self.client.transaction():
            async with tx:
                for ql in qls_with_args:
                    logger.opt(lazy=True).debug(
                        f"Execute QL: [{ql.commands}], \nkwargs: [{ql.kwargs}]."
                    )
                    await tx.execute(ql.commands, **ql.kwargs)

    @staticmethod
    def _maybe_handle_error(res):
        if not isinstance(res, dict):
            return

        if error := res.get('errors'):  # pragma: no cover
            ex_msg = error['message'].strip()
            ex_code = error['code']
            raise edgedb.EdgeDBError._from_code(ex_code, ex_msg)    # noqa

    async def _maybe_exec_qls(self, qls_with_args: List[QueryWithArgs]):
        txn_conf = self._safe_get_txn_conf()

        if txn_conf.in_txn and self._txn_support_:
            txn_conf.qls.extend(qls_with_args)
            return

        await self._execute(qls_with_args)

    @txn_support
    async def insert_df(
        self,
        object_name: str,
        data: pd.DataFrame,
        relation: Dict[str, pd.DataFrame] = None,
        chunksize: int = 500,
    ):
        """以事务执行基于DataFrame字段信息的批量插入数据

        Args:
            object_name: 被插入数据的对象名，需属于当前应用
            data: 要插入的数据，若有single link property，则以列名为link_name@link_property_name的形式提供
            relation: 如有multi link，提供该字典用于补充link target信息，键为link字段名，值为映射关系的DataFrame
                    DataFrame中的source列需为插入对象的业务主键，target列需为link target的业务主键，
                    若有link property，则以property名为列名，提供在除source和target的列中
            chunksize: 单次最大行数

        Notes:

            由于批量insert实现方式为组织 for-union clause 的 insert 语句，而在其中查询self link只能查到已有数据，
            无法查到 for-union clause 之前循环插入的结果，self link字段的数据将被单独抽出，
            在 insert 后再用 for-union clause 的 update 语句更新


        .. admonition:: 示例(不涉及multi link)

            .. code-block:: python

                import pandas as pd
                from datetime import datetime

                dm = DeepModel()

                data = pd.DataFrame(
                    {
                        'p_bool': [True, False],
                        'p_str': ['Hello', 'World'],
                        'p_local_datetime': [datetime(2021, 1, 1, 0, 0, 0), datetime(2021, 2, 1, 0, 0, 0), ],
                    }
                )
                # 将data插入Demo对象
                dm.insert_df('Demo', data)

        .. admonition:: 示例(涉及multi link)

            .. code-block:: python

                import pandas as pd

                dm = DeepModel()
                # 对象主数据
                data = pd.DataFrame(
                    {
                        'name': ['Alice', 'Bob', 'Carol']
                    }
                )
                # 主数据的multi link字段target信息
                relation = {
                    'deck': pd.DataFrame(
                        {
                            # 一对多可用多行source与target的关联表示
                            'source': ['Alice', 'Alice', 'Bob', 'Carol'],
                            'target': [
                                'Dragon',
                                'Golem',
                                'Golem',
                                'Imp'
                            ]
                        }
                    ),
                    'awards': pd.DataFrame(
                        {
                            'source': ['Alice', 'Bob', 'Carol'],
                            'target': ['1st', '2nd', '3rd'],
                        }
                    )
                }
                dm.insert_df('User', data, relation=relation)

        """
        if data.empty:
            logger.info("data为空，无DML执行")
            return

        if not isinstance(chunksize, int):
            raise ValueError("chunksize应为数字")

        if chunksize <= 0:
            raise ValueError("chunksize必须大于0")

        if object_name in self.user_objects:
            obj = self.user_objects[object_name]
        elif object_name in self.system_objects:
            obj = self.system_objects[object_name]
        else:
            raise ObjectNotExist(f'DeepModel对象[{object_name}]在当前应用不存在，无法插入数据')
        if obj.external:
            raise ExternalObjectReadOnly('外部对象只可读')

        relation = relation or {}
        formatted_obj = format_obj(obj)
        structure = ObjectStructure(name=formatted_obj.name, structure=formatted_obj.fields.values())

        required_fields = set(field.name for field in structure.fields.values() if field.required)
        if not required_fields.issubset(data.columns):
            raise RequiredFieldUnfilled(f'缺少必填字段: {required_fields.difference(data.columns)}')

        # 如可在object结构的annotations中取业务主键，则优先取，否则走接口
        if formatted_obj.info and BUSINESS_KEY in formatted_obj.info:
            business_key = formatted_obj.info[BUSINESS_KEY]
        else:
            business_key = self.model_objects[object_name].businessKey

        # 将relation与data关联
        for field_name, relation_df in relation.items():
            if field_name not in structure.fields:
                continue

            if not structure.fields[field_name].is_multi_link:
                if field_name in data.columns:
                    continue

                raise SingleLinkInRelation(
                    f'对象[{object_name}]的Link:[{field_name}]非multi link, '
                    f'请直接作为入参data的{field_name}列提供, '
                    f'值为对象{structure.fields[field_name].type}的业务主键'
                )

            data = self._merge_relation(data, relation_df, structure, business_key, field_name)

        # 记录self link的更新信息
        data, self_link_dfs = self._get_self_link_info(data, relation, structure, business_key)

        field_type = []
        tgt_main_field = {}
        # 准备bulk insert所需field信息
        for field in structure.fields.values():
            if field.name not in data.columns:
                continue

            field_type.append(field)

            if not field.is_link:
                continue
            # 链接至其他对象，记录目标对象信息
            if field.is_multi_link:
                # multi link字段出现在data而非relation中
                if field.name not in relation:
                    raise RelationRequired(f'multi link字段[{field.name}]缺少relation信息')
                link_props = set(relation[field.name].columns).intersection(field.props)
            else:
                link_props = set(
                    c[len(f'{field.name}@')::]
                    for c in data.columns if c.startswith(f'{field.name}@')
                ).intersection(field.props)
            # 如可在object结构的annotations中取业务主键，则优先取，否则走接口
            if field.target.info and BUSINESS_KEY in field.target.info:
                tgt_business_key = field.target.info[BUSINESS_KEY]
            else:
                if (tgt_obj := field.type.rpartition('::')[-1]) in self.model_objects:
                    tgt_business_key = self.model_objects[tgt_obj].businessKey
                else:
                    # Link 至非本应用对象，需单独查询
                    tgt = ObjectElement.construct_from(self.model_objects[object_name]).links[field.name]
                    tgt_model_info = await self.async_api.object.info(
                        app=tgt.targetApp, object_code=tgt.targetObjectCode
                    )
                    tgt_business_key = tgt_model_info.businessKey
            tgt_main_field[field.name] = MainField(tgt_business_key, field.is_multi_link, link_props)

        qls = []

        bulk_insert_ql = bulk_insert_by_fields(object_name, field_type, tgt_main_field)
        data = structure.fit(data)

        for i in range(0, len(data), chunksize):
            part = data.iloc[i: i + chunksize]
            kw_name = self.alias.get(BATCH_INSERT_KW)
            qls.append(
                QueryWithArgs(commands=bulk_insert_ql.replace(f'${BATCH_INSERT_KW}', f'${kw_name}'),
                              kwargs={kw_name: part.to_json(orient='records')})
            )

        if self_link_dfs:
            for update_field, (update_df, main_field) in self_link_dfs.items():
                field = structure.fields[update_field]
                update_df = structure.fit(update_df)
                bulk_update_ql = bulk_update_by_fields(
                    object_name, business_key, [field], {update_field: main_field}, [update_field]
                )
                for i in range(0, len(update_df), chunksize):
                    part = update_df.iloc[i: i + chunksize]
                    kw_name = self.alias.get(BATCH_INSERT_KW)
                    qls.append(
                        QueryWithArgs(commands=bulk_update_ql.replace(f'${BATCH_INSERT_KW}', f'${kw_name}'),
                                      kwargs={kw_name: part.to_json(orient='records')})
                    )

        await self.execute(qls)

    @staticmethod
    def _get_self_link_info(data, relation, structure, business_key):
        self_link_dfs = {}
        for field_name in structure.self_link_fields:
            field = structure.fields[field_name]
            if (relation_df := relation.get(field_name)) is not None:
                link_props = set(relation_df.columns).intersection(field.props)
                self_link_dfs[field_name] = (
                    data[[business_key, field_name]],
                    MainField(business_key, field.is_multi_link, link_props)
                )
                data = data.drop(columns=[field_name])

            elif field_name in data.columns:
                link_prop_cols = []
                link_props = []

                for col in data.columns:
                    if (
                        col.startswith(f'{field_name}@')
                        and ((prop_name := col[len(f'{field_name}@')::]) in field.props)
                    ):
                        link_prop_cols.append(col)
                        link_props.append(prop_name)

                self_link_dfs[field_name] = (
                    data[[business_key, field_name, *link_prop_cols]],
                    MainField(business_key, field.is_multi_link, link_props)
                )
                data = data.drop(columns=[field_name, *link_prop_cols])
        return data, self_link_dfs

    @staticmethod
    def _merge_relation(data, relation_df, structure, business_key, field_name):
        field = structure.fields[field_name]
        assert {'source', 'target'}.issubset(relation_df.columns), "关联表必须包含source和target列"
        valid_cols = {'source', 'target', *field.props}.intersection(relation_df.columns)
        relation_df = relation_df[valid_cols]
        # for fit only
        temp_structure = ObjectStructure(
            field.type,
            [
                FieldInfo(name='source', target=TargetField(name='std::str')),
                FieldInfo(name='target', target=TargetField(name='std::str')),
                *[FieldInfo(**prop.dict()) for prop in field.properties]
            ]
        )
        relation_df = temp_structure.fit(relation_df)
        link = relation_df.groupby('source').apply(_format_link, link_name=field_name)
        # 保证link列不会在join过程中重名
        data = data.drop(columns=[field_name], errors='ignore')
        data = data.join(link.to_frame(field_name), on=business_key)
        return data

    @asynccontextmanager
    async def start_transaction(self):
        """开启事务

        上下文管理器，使用with语法开启上下文，上下文中的ql将作为事务执行
        退出with语句块后，事务将立即执行，执行过程中如果报错会直接抛出

        .. admonition:: 示例

            .. code-block:: python

                import pandas as pd

                dm = DeepModel()

                data = pd.DataFrame(
                    {
                        'name': ['Alice', 'Bob', 'Carol'],
                        'deck': [
                            "Dragon",
                            "Golem",
                            "Imp"
                        ],
                        'awards': [
                            "1st",
                            "2nd",
                            "3rd"
                        ],
                    }
                )

                async with dm.start_transaction():
                    await dm.execute("delete User")
                    await dm.insert_df("User", data)


        Important:

            仅 :func:`insert_df` :func:`execute` 方法支持在事务中执行

        """
        self._safe_get_txn_conf().in_txn = True

        try:
            yield
            if qls := self._txn_.get().qls:
                await self._execute(qls)
        finally:
            self._txn_.set(_TxnConfig())


class DeepModel(AsyncDeepModel, metaclass=SyncMeta):
    synchronize = ('query_object', 'query', 'query_df', 'execute', 'insert_df')

    if TYPE_CHECKING:  # pragma: no cover
        def query_object(self, ql: str, **kwargs) -> List[Any]:
            ...

        def query(self, ql: str, **kwargs) -> List[Any]:
            ...

        def query_df(self, ql: str, **kwargs) -> pd.DataFrame:
            ...

        def execute(self, qls: Union[str, List[str], List[QueryWithArgs]], **kwargs):
            ...

        def insert_df(
            self,
            object_name: str,
            data: pd.DataFrame,
            relation: Dict[str, pd.DataFrame] = None,
            chunksize: int = 500,
        ):
            ...

    @contextmanager
    def start_transaction(self):
        """开启事务

        上下文管理器，使用with语法开启上下文，上下文中的ql将作为事务执行
        退出with语句块后，事务将立即执行，执行过程中如果报错会直接抛出

        .. admonition:: 示例

            .. code-block:: python

                import pandas as pd

                dm = DeepModel()

                data = pd.DataFrame(
                    {
                        'name': ['Alice', 'Bob', 'Carol'],
                        'deck': [
                            "Dragon",
                            "Golem",
                            "Imp"
                        ],
                        'awards': [
                            "1st",
                            "2nd",
                            "3rd"
                        ],
                    }
                )

                with dm.start_transaction():
                    dm.execute("delete User")
                    dm.insert_df("User", data)


        Important:

            仅 :func:`insert_df` :func:`execute` 方法支持在事务中执行

        """
        self._safe_get_txn_conf().in_txn = True

        try:
            yield
            if qls := self._txn_.get().qls:
                evloop.run(self._execute(qls))
        finally:
            self._txn_.set(_TxnConfig())
