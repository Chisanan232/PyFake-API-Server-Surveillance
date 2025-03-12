import ast
from typing import Mapping, Type

import pytest
from fake_api_server.command.subcommand import SubCommandLine

from fake_api_server_plugin.ci.surveillance.model import ConfigurationKey
from fake_api_server_plugin.ci.surveillance.model.config import SurveillanceConfig
from fake_api_server_plugin.ci.surveillance.model.config.api_config import SubCmdConfig

# isort: off
from .._base import _BaseModelTestSuite
from test._values._test_data import fake_data

# isort: on


class TestSurveillanceConfig(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[SurveillanceConfig]:
        return SurveillanceConfig

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.surveillance_config(file_path="./api.yaml", base_test_dir="../"),
        ],
    )
    def test_deserialize(self, model: Type[SurveillanceConfig], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: SurveillanceConfig, original_data: Mapping) -> None:
        # API documentation info
        assert model.api_doc_url == original_data[ConfigurationKey.API_DOC_URL.value]

        # fake-api-server setting
        original_fake_api_server_config = original_data[ConfigurationKey.FAKE_API_SERVER.value]
        assert model.fake_api_server.server_type == original_fake_api_server_config[ConfigurationKey.SERVER_TYPE.value]
        # for subcommand line *pull* options
        original_subcmd_pull = original_fake_api_server_config[ConfigurationKey.SUBCMD.value][
            SubCommandLine.Pull.value
        ][ConfigurationKey.ARGS.value]
        subcmd_pull_args: SubCmdConfig = model.fake_api_server.subcmd[SubCommandLine.Pull].args
        assert subcmd_pull_args == original_subcmd_pull

        # git info
        original_git_info_data = original_data[ConfigurationKey.GIT_INFO.value]
        assert model.git_info.repository == original_git_info_data[ConfigurationKey.GIT_REPOSITORY.value]
        original_git_commit_data = original_git_info_data[ConfigurationKey.GIT_COMMIT.value]
        original_git_author_data = original_git_commit_data[ConfigurationKey.GIT_AUTHOR.value]
        assert model.git_info.commit.author.name == original_git_author_data[ConfigurationKey.GIT_AUTHOR_NAME.value]
        assert model.git_info.commit.author.email == original_git_author_data[ConfigurationKey.GIT_AUTHOR_EMAIL.value]
        assert model.git_info.commit.message == original_git_commit_data[ConfigurationKey.GIT_COMMIT_MSG.value]

        # github info
        original_github_pr_info_data = original_data[ConfigurationKey.GITHUB_INFO.value][
            ConfigurationKey.GITHUB_PULL_REQUEST.value
        ]
        assert model.github_info.pull_request.title == original_github_pr_info_data[ConfigurationKey.PR_TITLE.value]
        assert model.github_info.pull_request.body == original_github_pr_info_data[ConfigurationKey.PR_BODY.value]
        assert model.github_info.pull_request.draft == original_github_pr_info_data[ConfigurationKey.PR_IS_DRAFT.value]
        assert model.github_info.pull_request.labels == original_github_pr_info_data[ConfigurationKey.PR_LABELS.value]

        # operation of action in CI
        assert model.accept_config_not_exist == ast.literal_eval(
            str(original_data[ConfigurationKey.ACCEPT_CONFIG_NOT_EXIST.value]).capitalize()
        )
