from typing import Union, Awaitable

from deepfos import OPTION
from deepfos.element.base import T_ElementInfoWithServer
from deepfos.lib.decorator import cached_property
from deepfos.lib.utils import concat_url
from .base import ChildAPI, get, RootAPI
from .models.deepconnector import *


class DataSourceAPI(ChildAPI):
    endpoint = '/apis/v3/ds'

    @get('spaces', data_wrapped=False)
    def connection_info(self, space_id: str, app_id: str, element_info: T_ElementInfoWithServer) -> Union[ConnectionInfoVo, Awaitable[ConnectionInfoVo]]:
        return {
            'path': concat_url(space_id, 'apps', app_id, 'connection-info'),
            'param': {
                'elementName': element_info.elementName,
                'folderId': element_info.folderId
            }
        }


class DeepConnectorAPI(RootAPI):
    prefix = lambda: 'http://deep-connector-server'
    module_type = 'CONN'

    @cached_property
    def datasource(self) -> DataSourceAPI:
        return DataSourceAPI(self)
