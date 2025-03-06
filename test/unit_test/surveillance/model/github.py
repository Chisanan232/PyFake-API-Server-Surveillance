from typing import Mapping, Type

import pytest

from fake_api_server_plugin.ci.surveillance.model.github import PullRequestInfo, GitHubInfo
from fake_api_server_plugin.ci.surveillance.model import EnvironmentVariableKey

# isort: off
from ._base import _BaseModelTestSuite
from test._values._test_data import fake_data

# isort: on


class TestPullRequestInfo(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[PullRequestInfo]:
        return PullRequestInfo

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.github_pr_info(),
        ],
    )
    def test_deserialize(self, model: Type[PullRequestInfo], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: PullRequestInfo, original_data: Mapping) -> None:
        assert model.title == original_data[EnvironmentVariableKey.PR_TITLE.value]
        assert model.body == original_data[EnvironmentVariableKey.PR_BODY.value]
        assert model.draft == original_data[EnvironmentVariableKey.PR_IS_DRAFT.value]


class TestGitHubInfo(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[GitHubInfo]:
        return GitHubInfo

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.github_pr_info(),
        ],
    )
    def test_deserialize(self, model: Type[GitHubInfo], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: GitHubInfo, original_data: Mapping) -> None:
        assert model.pull_request.title == original_data[EnvironmentVariableKey.PR_TITLE.value]
        assert model.pull_request.body == original_data[EnvironmentVariableKey.PR_BODY.value]
        assert model.pull_request.draft == original_data[EnvironmentVariableKey.PR_IS_DRAFT.value]
