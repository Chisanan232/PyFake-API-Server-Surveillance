import ast
from typing import Mapping, Type, List, Union

import pytest
from fake_api_server.command.subcommand import SubCommandLine

from fake_api_server_plugin.ci.surveillance.model import ConfigurationKey
from fake_api_server_plugin.ci.surveillance.model.config.api_config import (
    FakeAPIConfigSetting,
    PullApiDocConfigArgs,
    SubCmdConfig,
)

# isort: off
from .._base import _BaseModelTestSuite
from test._values._test_data import fake_data

# isort: on


class TestPullApiDocConfigArgs(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[PullApiDocConfigArgs]:
        return PullApiDocConfigArgs

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.subcmd_pull_args(file_path="./api.yaml", base_test_dir="../"),
        ],
    )
    def test_deserialize(self, model: Type[PullApiDocConfigArgs], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: PullApiDocConfigArgs, original_data: Mapping) -> None:
        assert model.config_path == original_data[ConfigurationKey.CONFIG_PATH.value]
        assert model.include_template_config == ast.literal_eval(
            str(original_data[ConfigurationKey.INCLUDE_TEMPLATE_CONFIG.value]).capitalize()
        )
        assert model.base_file_path == original_data[ConfigurationKey.BASE_FILE_PATH.value]
        assert model.base_url == original_data[ConfigurationKey.BASE_URL.value]
        assert model.divide_api == ast.literal_eval(str(original_data[ConfigurationKey.DIVIDE_API.value]).capitalize())
        assert model.divide_http == ast.literal_eval(
            str(original_data[ConfigurationKey.DIVIDE_HTTP.value]).capitalize()
        )
        assert model.divide_http_request == ast.literal_eval(
            str(original_data[ConfigurationKey.DIVIDE_HTTP_REQUEST.value]).capitalize()
        )
        assert model.divide_http_response == ast.literal_eval(
            str(original_data[ConfigurationKey.DIVIDE_HTTP_RESPONSE.value]).capitalize()
        )
        assert model.dry_run == ast.literal_eval(str(original_data[ConfigurationKey.DRY_RUN.value]).capitalize())


class TestSubCmdConfig(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[SubCmdConfig]:
        return SubCmdConfig

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.fake_api_server_subcmd_pull_args(),
        ],
    )
    def test_deserialize(self, model: Type[SubCmdConfig], data: Mapping):
        model = model.deserialize(data)
        self._verify_model_props(model, data)

    def _verify_model_props(self, model: SubCmdConfig, original_data: Mapping) -> None:
        assert model.args == original_data["args"]

    def test_to_subcmd_args(self):
        fake_api_server_subcmd_pull_args = fake_data.fake_api_server_subcmd_pull_args()
        subcmd_config = SubCmdConfig.deserialize(fake_api_server_subcmd_pull_args)

        subcmd_args = subcmd_config.to_subcmd_args(PullApiDocConfigArgs)

        assert isinstance(subcmd_args, PullApiDocConfigArgs)
        original_args_config: List[str] = fake_api_server_subcmd_pull_args[ConfigurationKey.ARGS.value]

        def _find(_k: str) -> Union[str, bool] :

            def _filter_value(_e: str) -> bool:
                return _k in _e

            _filter_result = list(filter(lambda e: _filter_value(e), original_args_config))
            if _filter_result:
                _filter_result = _filter_result[0]
                if "=" in _filter_result:
                    return _filter_result.split("=")[-1]
                else:
                    return True
            else:
                return False

        assert subcmd_args.config_path == _find("config-path")
        assert subcmd_args.base_file_path == _find("base-file-path")
        assert subcmd_args.base_url == _find("base-url")
        assert subcmd_args.include_template_config is _find("include-template-config")
        assert subcmd_args.divide_api is _find("divide-api")
        assert subcmd_args.divide_http is _find("divide-http")
        assert subcmd_args.divide_http_request is _find("divide-http-request")
        assert subcmd_args.divide_http_response is _find("divide-http-response")
        assert subcmd_args.dry_run is _find("dry-run")


class TestFakeAPIConfigSetting(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[FakeAPIConfigSetting]:
        return FakeAPIConfigSetting

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.fake_api_server_config(file_path="./api.yaml", base_test_dir="./"),
        ],
    )
    def test_deserialize(self, model: Type[FakeAPIConfigSetting], data: Mapping):
        model = model.deserialize(data)
        self._verify_model_props(model, data)

    def _verify_model_props(self, model: FakeAPIConfigSetting, original_data: Mapping) -> None:
        assert model.server_type == original_data["server-type"]
        for subcmd_k, subcmd_v in original_data["subcmd"].items():
            assert SubCommandLine.to_enum(subcmd_k) in model.subcmd.keys()
            subcmd_config = model.subcmd[SubCommandLine.to_enum(subcmd_k)]
            assert subcmd_config.args == subcmd_v["args"]
