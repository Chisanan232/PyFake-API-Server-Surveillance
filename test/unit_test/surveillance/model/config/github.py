from typing import Mapping, Type

import pytest

from fake_api_server_plugin.ci.surveillance.model import ConfigurationKey
from fake_api_server_plugin.ci.surveillance.model.config.github import (
    GitHubInfo,
    PullRequestInfo,
)

# isort: off
from .._base import _BaseModelTestSuite
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
        assert model.title == original_data[ConfigurationKey.PR_TITLE.value]
        assert model.body == original_data[ConfigurationKey.PR_BODY.value]
        assert model.draft == original_data[ConfigurationKey.PR_IS_DRAFT.value]
        assert model.labels == original_data[ConfigurationKey.PR_LABELS.value]


class TestGitHubInfo(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[GitHubInfo]:
        return GitHubInfo

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.github_info(),
        ],
    )
    def test_deserialize(self, model: Type[GitHubInfo], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: GitHubInfo, original_data: Mapping) -> None:
        original_github_info_data = original_data[ConfigurationKey.GITHUB_PULL_REQUEST.value]
        assert model.pull_request.title == original_github_info_data[ConfigurationKey.PR_TITLE.value]
        assert model.pull_request.body == original_github_info_data[ConfigurationKey.PR_BODY.value]
        assert model.pull_request.draft == original_github_info_data[ConfigurationKey.PR_IS_DRAFT.value]
        assert model.pull_request.labels == original_github_info_data[ConfigurationKey.PR_LABELS.value]
