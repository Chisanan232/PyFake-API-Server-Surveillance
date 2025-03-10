import ast
from typing import Mapping, Type

import pytest

from fake_api_server_plugin.ci.surveillance.model import EnvironmentVariableKey
from fake_api_server_plugin.ci.surveillance.model.config import SurveillanceConfig

# isort: off
from ._base import _BaseModelTestSuite
from test._values._test_data import fake_data

# isort: on


class TestSurveillanceConfig(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[SurveillanceConfig]:
        return SurveillanceConfig

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.action_input(file_path="./api.yaml", base_test_dir="../"),
        ],
    )
    def test_deserialize(self, model: Type[SurveillanceConfig], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: SurveillanceConfig, original_data: Mapping) -> None:
        # API documentation info
        assert model.api_doc_url == original_data[EnvironmentVariableKey.API_DOC_URL.value]
        assert model.server_type == original_data[EnvironmentVariableKey.SERVER_TYPE.value]

        # git info
        assert model.git_info.repository == original_data[EnvironmentVariableKey.GIT_REPOSITORY.value]
        assert model.git_info.commit.author.name == original_data[EnvironmentVariableKey.GIT_AUTHOR_NAME.value]
        assert model.git_info.commit.author.email == original_data[EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value]
        assert model.git_info.commit.message == original_data[EnvironmentVariableKey.GIT_COMMIT_MSG.value]

        # github info
        assert model.github_info.pull_request.title == original_data[EnvironmentVariableKey.PR_TITLE.value]
        assert model.github_info.pull_request.body == original_data[EnvironmentVariableKey.PR_BODY.value]
        assert model.github_info.pull_request.draft == original_data[EnvironmentVariableKey.PR_IS_DRAFT.value]

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

        # operation of action in CI
        assert model.accept_config_not_exist == ast.literal_eval(
            str(original_data[EnvironmentVariableKey.ACCEPT_CONFIG_NOT_EXIST.value]).capitalize()
        )
