import ast
from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Type

from fake_api_server.model.subcmd_common import SubCommandLine

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


@dataclass
class SubCmdConfig(_BaseModel):
    args: List[str]

    @staticmethod
    def deserialize(data: Mapping) -> "SubCmdConfig":
        return SubCmdConfig(
            args=data.get(EnvironmentVariableKey.ARGS.value, []),
        )

    def to_subcmd_args(self, subcmd_arg_model: Type[_BaseModel]) -> _BaseModel:
        param_with_key: Dict[str, str] = {}
        for arg in self.args:
            arg_eles = arg.split("=")
            assert len(arg_eles) <= 2, f"Invalid subcmd arg: {arg}"
            arg_eles = arg_eles if len(arg_eles) == 2 else [arg_eles[0], True]
            assert len(arg_eles) == 2
            arg_key, arg_value = arg_eles
            arg_key = arg_key.replace("--", "").replace("-", "_")
            param_with_key[arg_key] = arg_value
        return subcmd_arg_model(**param_with_key)


@dataclass
class FakeAPIConfigSetting(_BaseModel):
    # TODO: Still doesn't support this feature at action
    server_type: str = field(default_factory=str)
    subcmd: Dict[SubCommandLine, SubCmdConfig] = field(default_factory=dict)

    @staticmethod
    def deserialize(data: Mapping) -> "FakeAPIConfigSetting":
        subcmd_configs = {}
        for subcmd_k, subcmd_v in data.get(EnvironmentVariableKey.SUBCMD.value, {}).items():
            subcmd_configs[SubCommandLine.to_enum(subcmd_k)] = SubCmdConfig.deserialize(subcmd_v)
        return FakeAPIConfigSetting(
            server_type=data[EnvironmentVariableKey.SERVER_TYPE.value],
            subcmd=subcmd_configs,
        )
