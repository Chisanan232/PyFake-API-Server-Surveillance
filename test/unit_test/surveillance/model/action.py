import ast
from typing import Mapping, Type

import pytest

from ci.surveillance.model import EnvironmentVariableKey
from ci.surveillance.model.action import ActionInput

from ._base import _BaseModelTestSuite


class TestActionInput(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[ActionInput]:
        return ActionInput

    @pytest.mark.parametrize(
        "data",
        [
            {
                # API documentation info
                EnvironmentVariableKey.API_DOC_URL.value: "http://10.20.0.13:8080",
                EnvironmentVariableKey.SERVER_TYPE.value: "rest-server",
                # git info
                EnvironmentVariableKey.GIT_REPOSITORY.value: "test/sample-project",
                EnvironmentVariableKey.GIT_AUTHOR_NAME.value: "test",
                EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value: "test@gmail.com",
                EnvironmentVariableKey.GIT_COMMIT_MSG.value: "✏️ Update the API interface settings.",
                # for subcommand line *pull* options
                EnvironmentVariableKey.CONFIG_PATH.value: "./api.yaml",
                EnvironmentVariableKey.INCLUDE_TEMPLATE_CONFIG.value: "True",
                EnvironmentVariableKey.BASE_FILE_PATH.value: "./",
                EnvironmentVariableKey.BASE_URL.value: "/test/v1",
                EnvironmentVariableKey.DIVIDE_API.value: "true",
                EnvironmentVariableKey.DIVIDE_HTTP.value: "false",
                EnvironmentVariableKey.DIVIDE_HTTP_REQUEST.value: "false",
                EnvironmentVariableKey.DIVIDE_HTTP_RESPONSE.value: "false",
                EnvironmentVariableKey.DRY_RUN.value: "true",
            },
        ],
    )
    def test_deserialize(self, model: Type[ActionInput], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: ActionInput, original_data: Mapping) -> None:
        # API documentation info
        assert model.api_doc_url == original_data[EnvironmentVariableKey.API_DOC_URL.value]
        assert model.server_type == original_data[EnvironmentVariableKey.SERVER_TYPE.value]

        # git info
        assert model.git_info.repository == original_data[EnvironmentVariableKey.GIT_REPOSITORY.value]
        assert model.git_info.commit.author.name == original_data[EnvironmentVariableKey.GIT_AUTHOR_NAME.value]
        assert model.git_info.commit.author.email == original_data[EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value]
        assert model.git_info.commit.message == original_data[EnvironmentVariableKey.GIT_COMMIT_MSG.value]

        # for subcommand line *pull* options
        assert model.subcmd_pull_args.config_path == original_data[EnvironmentVariableKey.CONFIG_PATH.value]
        assert model.subcmd_pull_args.include_template_config == ast.literal_eval(
            str(original_data[EnvironmentVariableKey.INCLUDE_TEMPLATE_CONFIG.value]).capitalize()
        )
        assert model.subcmd_pull_args.base_file_path == original_data[EnvironmentVariableKey.BASE_FILE_PATH.value]
        assert model.subcmd_pull_args.base_url == original_data[EnvironmentVariableKey.BASE_URL.value]
        assert model.subcmd_pull_args.divide_api == ast.literal_eval(
            str(original_data[EnvironmentVariableKey.DIVIDE_API.value]).capitalize()
        )
        assert model.subcmd_pull_args.divide_http == ast.literal_eval(
            str(original_data[EnvironmentVariableKey.DIVIDE_HTTP.value]).capitalize()
        )
        assert model.subcmd_pull_args.divide_http_request == ast.literal_eval(
            str(original_data[EnvironmentVariableKey.DIVIDE_HTTP_REQUEST.value]).capitalize()
        )
        assert model.subcmd_pull_args.divide_http_response == ast.literal_eval(
            str(original_data[EnvironmentVariableKey.DIVIDE_HTTP_RESPONSE.value]).capitalize()
        )
        assert model.subcmd_pull_args.dry_run == ast.literal_eval(
            str(original_data[EnvironmentVariableKey.DRY_RUN.value]).capitalize()
        )
