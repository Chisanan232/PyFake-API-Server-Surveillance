import ast
from typing import Mapping, Type

import pytest
from fake_api_server.command.subcommand import SubCommandLine

from fake_api_server_plugin.ci.surveillance.model import EnvironmentVariableKey
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
        assert model.config_path == original_data[EnvironmentVariableKey.CONFIG_PATH.value]
        assert model.include_template_config == ast.literal_eval(
            str(original_data[EnvironmentVariableKey.INCLUDE_TEMPLATE_CONFIG.value]).capitalize()
        )
        assert model.base_file_path == original_data[EnvironmentVariableKey.BASE_FILE_PATH.value]
        assert model.base_url == original_data[EnvironmentVariableKey.BASE_URL.value]
        assert model.divide_api == ast.literal_eval(
            str(original_data[EnvironmentVariableKey.DIVIDE_API.value]).capitalize()
        )
        assert model.divide_http == ast.literal_eval(
            str(original_data[EnvironmentVariableKey.DIVIDE_HTTP.value]).capitalize()
        )
        assert model.divide_http_request == ast.literal_eval(
            str(original_data[EnvironmentVariableKey.DIVIDE_HTTP_REQUEST.value]).capitalize()
        )
        assert model.divide_http_response == ast.literal_eval(
            str(original_data[EnvironmentVariableKey.DIVIDE_HTTP_RESPONSE.value]).capitalize()
        )
        assert model.dry_run == ast.literal_eval(str(original_data[EnvironmentVariableKey.DRY_RUN.value]).capitalize())


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
        # assert subcmd_config.to_subcmd_args(PullApiDocConfigArgs) == fake_api_server_subcmd_pull_args["args"]


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
