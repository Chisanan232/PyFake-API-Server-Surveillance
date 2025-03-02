import ast
from typing import Mapping, Type

import pytest

from fake_api_server_plugin.ci.surveillance.model import EnvironmentVariableKey
from fake_api_server_plugin.ci.surveillance.model.subcmd_pull import (
    PullApiDocConfigArgs,
)

# isort: off
from ._base import _BaseModelTestSuite
from test._values._test_data import fake_data

# isort: on


class TestActionInput(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[PullApiDocConfigArgs]:
        return PullApiDocConfigArgs

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.subcmd_pull_args(file_path="./api.yaml", base_test_dir="./"),
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
