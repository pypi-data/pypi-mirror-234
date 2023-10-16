from typing import List, Optional, Dict

from .base import BaseModel

__all__ = [
    "ObjectBasicDTO",
    "ObjectInfo",
    "ObjectLinkParam",
    "ObjectPropertyParamRes",
    "ObjectParam",
    "ObjectOperationParam"
]


class ObjectBasicDTO(BaseModel):
    #: 对象所属应用
    app: Optional[str]
    #: 对象所属应用名称
    appName: Optional[str]
    #: 对象编码
    code: Optional[str]
    #: 对象名称
    name: Optional[Dict[str, Optional[str]]]
    #: 对象范围 1：应用级对象 2：空间级对象
    objectScope: Optional[int]


class ObjectInfo(BaseModel):
    #: 链接目标对象所在应用id,如果传过来的是_system代表链接的是空间级对象
    app: Optional[str]
    #: 链接目标对象所在应用名称
    appName: Optional[str]
    #: 链接对象的编码
    code: Optional[str]
    #: 引用对象当前语种名称
    objectName: Optional[str]
    #: 是否为引用对象的链接
    whetherQuotedRelation: Optional[bool]
    #: 是否是为对象指向的链接
    whetherSelfRelation: Optional[bool]


class ObjectLinkParam(BaseModel):
    app: Optional[str]
    code: Optional[str]
    currentObjectUnique: Optional[bool]
    deleteCategory: Optional[str]
    inferBase: Optional[str]
    inferType: Optional[str]
    linkId: Optional[str]
    linkObjectOption: Optional[int]
    linkObjectRequired: Optional[bool]
    linkType: Optional[int]
    name: Optional[Dict[str, Optional[str]]]
    sourceObjectCode: Optional[str]
    state: Optional[int]
    targetApp: Optional[str]
    targetObject: Optional['ObjectParam']
    targetObjectCode: Optional[str]
    targetObjectInfo: Optional[ObjectInfo]
    whetherSystem: Optional[bool]


class ObjectPropertyParamRes(BaseModel):
    #: 应用id
    app: Optional[str]
    #: 是否自动赋值
    autoValue: Optional[bool]
    #: 属性编码
    code: str
    #: 约束
    constraint: Optional[str]
    #: 默认值 默认值类型（0 无,1 定值，2 当前时间 3 枚举）
    defaultValue: Optional[str]
    #: 默认值类型 默认值类型（0 无,1 定值）
    defaultValueType: Optional[int]
    #: 推断基数: AT_LEAST_ONE, AT_MOST_ONE, MANY, ONE
    inferBase: Optional[str]
    #: 最大长度
    maxLength: Optional[int]
    #: 最大数量
    maxNum: Optional[int]
    #: 最大值
    maxValue: Optional[str]
    #: 最大值条件，枚举值 LESS_OR_EQUALS 小于等于；LESS 小于
    maxValueCondition: Optional[str]
    #: 最小值
    minValue: Optional[str]
    #: 最小值条件 GREATER_OR_EQUALS 大于等于；GREATER大于
    minValueCondition: Optional[str]
    #: 属性名称
    name: Dict[str, Optional[str]]
    #: 对象编码
    objectCode: Optional[str]
    #: 是否是业务主键
    whetherBusinessKey: bool
    #: 是否是计算属性
    whetherCalculation: bool
    #: 是否唯一
    whetherOnly: bool
    #: 是否只读
    whetherReadOnly: bool
    #: 是否必填
    whetherRequired: bool
    #: 是否系统属性
    whetherSystemProperties: bool


class ObjectParam(BaseModel):
    app: Optional[str]
    appName: Optional[str]
    code: Optional[str]
    linkCodes: Optional[List[str]]
    linkParamList: Optional[List[ObjectLinkParam]]
    name: Optional[Dict[str, Optional[str]]]
    objectId: Optional[str]
    objectScope: Optional[int]
    objectTypeList: Optional[List[str]]
    propertyCodes: Optional[List[str]]
    propertyParamList: Optional[List[ObjectPropertyParamRes]]
    selfLinkOrder: Optional[int]
    state: Optional[int]
    #: 对象类型: BUILTIN, STANDARD, VIEW
    type: Optional[str]
    whetherSelfReference: Optional[bool]
    businessKey: Optional[str]


class ObjectOperationParam(BaseModel):
    objectList: List[ObjectParam]


ObjectParam.update_forward_refs()
ObjectLinkParam.update_forward_refs()
