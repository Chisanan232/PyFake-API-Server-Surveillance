from typing import Type, Mapping

import pytest

from ci.surveillance.model import EnvironmentVariableKey
from ci.surveillance.model.subcmd_pull import PullApiDocConfigArgs
from ._base import _BaseModelTestSuite


class TestActionInput(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[PullApiDocConfigArgs]:
        return PullApiDocConfigArgs

    @pytest.mark.parametrize(
        "data",
        [
            {
                EnvironmentVariableKey.CONFIG_PATH.value: "./api.yaml",
                EnvironmentVariableKey.INCLUDE_TEMPLATE_CONFIG.value: "true",
                EnvironmentVariableKey.BASE_FILE_PATH.value: "./",
                EnvironmentVariableKey.BASE_URL.value: "/test/v1",
                EnvironmentVariableKey.DIVIDE_API.value: "True",
                EnvironmentVariableKey.DIVIDE_HTTP.value: "False",
                EnvironmentVariableKey.DIVIDE_HTTP_REQUEST.value: "false",
                EnvironmentVariableKey.DIVIDE_HTTP_RESPONSE.value: "False",
                EnvironmentVariableKey.DRY_RUN.value: "True",
            },
        ],
    )
    def test_deserialize(self, model: Type[PullApiDocConfigArgs], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: PullApiDocConfigArgs, original_data: Mapping) -> None:
        assert model.config_path == original_data[EnvironmentVariableKey.CONFIG_PATH.value]
        assert model.include_template_config == bool(original_data[EnvironmentVariableKey.INCLUDE_TEMPLATE_CONFIG.value])
        assert model.base_file_path == original_data[EnvironmentVariableKey.BASE_FILE_PATH.value]
        assert model.base_url == original_data[EnvironmentVariableKey.BASE_URL.value]
        assert model.divide_api == bool(original_data[EnvironmentVariableKey.DIVIDE_API.value])
        assert model.divide_http == bool(original_data[EnvironmentVariableKey.DIVIDE_HTTP.value])
        assert model.divide_http_request == bool(original_data[EnvironmentVariableKey.DIVIDE_HTTP_REQUEST.value])
        assert model.divide_http_response == bool(original_data[EnvironmentVariableKey.DIVIDE_HTTP_RESPONSE.value])
        assert model.dry_run == bool(original_data[EnvironmentVariableKey.DRY_RUN.value])
