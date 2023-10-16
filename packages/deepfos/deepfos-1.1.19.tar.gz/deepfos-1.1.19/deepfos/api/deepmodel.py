from typing import Union, Awaitable, List, Any, Dict

from deepfos.lib.decorator import cached_property
from .base import DynamicRootAPI, ChildAPI, get, post
from .models.deepmodel import *


class ObjectAPI(ChildAPI):
    endpoint = '/object'

    @get('all/get')
    def get_all(self, ) -> Union[ObjectOperationParam, Awaitable[ObjectOperationParam]]:
        return {}

    @get('list')
    def list(self, ) -> Union[List[ObjectBasicDTO], Awaitable[List[ObjectBasicDTO]]]:
        return {}

    @get('info')
    def info(self, app: str = None, object_code: str = None) -> Union[ObjectParam, Awaitable[ObjectParam]]:
        return {'param': {'app': app, 'objectCode': object_code}}


class DeepQLAPI(ChildAPI):
    endpoint = '/public/deepql/actions'

    @post('query')
    def query(self, module: str = None, query: str = None, variables: Dict = None) -> Union[Any, Awaitable[Any]]:
        return {'body': {'module': module, 'query': query, 'variables': variables}}

    @post('execute')
    def execute(self, module: str = None, query: str = None, variables: Dict = None) -> Union[Any, Awaitable[Any]]:
        return {'body': {'module': module, 'query': query, 'variables': variables}}


class DeepModelAPI(DynamicRootAPI, builtin=True):
    module_type = 'DM'
    default_version = (1, 0)
    multi_version = False
    cls_name = 'DeepModelAPI'
    module_name = 'deepfos.api.deepmodel'
    api_version = (1, 0)

    @cached_property
    def object(self) -> ObjectAPI:
        return ObjectAPI(self)

    @cached_property
    def deepql(self) -> DeepQLAPI:
        return DeepQLAPI(self)
