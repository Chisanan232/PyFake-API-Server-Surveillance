from dataclasses import dataclass
from typing import Mapping

from . import EnvironmentVariableKey
from ._base import _BaseModel


@dataclass
class PullApiDocConfigArgs(_BaseModel):
    config_path: str
    include_template_config: bool
    base_file_path: str
    base_url: str
    dry_run: bool
    divide_api: bool
    divide_http: bool
    divide_http_request: bool
    divide_http_response: bool

    @staticmethod
    def deserialize(data: Mapping) -> "PullApiDocConfigArgs":
        return PullApiDocConfigArgs(
            config_path=data[EnvironmentVariableKey.CONFIG_PATH.value],
            include_template_config=bool(data[EnvironmentVariableKey.INCLUDE_TEMPLATE_CONFIG.value]),
            base_file_path=data[EnvironmentVariableKey.BASE_FILE_PATH.value],
            base_url=data[EnvironmentVariableKey.BASE_URL.value],
            divide_api=bool(data[EnvironmentVariableKey.DIVIDE_API.value]),
            divide_http=bool(data[EnvironmentVariableKey.DIVIDE_HTTP.value]),
            divide_http_request=bool(data[EnvironmentVariableKey.DIVIDE_HTTP_REQUEST.value]),
            divide_http_response=bool(data[EnvironmentVariableKey.DIVIDE_HTTP_RESPONSE.value]),
            dry_run=bool(data[EnvironmentVariableKey.DRY_RUN.value]),
        )
