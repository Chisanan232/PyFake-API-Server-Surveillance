import ast
from dataclasses import dataclass
from typing import Mapping

from .. import EnvironmentVariableKey
from .._base import _BaseModel


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
            include_template_config=ast.literal_eval(
                str(data[EnvironmentVariableKey.INCLUDE_TEMPLATE_CONFIG.value]).capitalize()
            ),
            base_file_path=data[EnvironmentVariableKey.BASE_FILE_PATH.value],
            base_url=data[EnvironmentVariableKey.BASE_URL.value],
            divide_api=ast.literal_eval(str(data[EnvironmentVariableKey.DIVIDE_API.value]).capitalize()),
            divide_http=ast.literal_eval(str(data[EnvironmentVariableKey.DIVIDE_HTTP.value]).capitalize()),
            divide_http_request=ast.literal_eval(
                str(data[EnvironmentVariableKey.DIVIDE_HTTP_REQUEST.value]).capitalize()
            ),
            divide_http_response=ast.literal_eval(
                str(data[EnvironmentVariableKey.DIVIDE_HTTP_RESPONSE.value]).capitalize()
            ),
            dry_run=ast.literal_eval(str(data[EnvironmentVariableKey.DRY_RUN.value]).capitalize()),
        )
