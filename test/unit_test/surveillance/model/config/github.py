from typing import Mapping, Type

import pytest

try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod  # type: ignore[no-redef]

from ci.surveillance.model.compare import ChangeStatistical, ChangeSummary

from fake_api_server_plugin.ci.surveillance.model import ConfigurationKey
from fake_api_server_plugin.ci.surveillance.model.compare import ChangeDetail
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

    def test_default_pr_body(self, model: Type[GitHubInfo]):
        github_info_model = model.deserialize({})
        with open("./fake_api_server_plugin/ci/surveillance/_static/pr-body.md", "r") as file_stream:
            expect_pr_body = file_stream.read()

        body = github_info_model.pull_request.body
        assert isinstance(body, str)
        assert body == expect_pr_body

    @pytest.mark.parametrize(
        "change_detail",
        [
            ChangeDetail(
                change_statistical=ChangeStatistical(
                    add=1,
                    update=2,
                    delete=1,
                ),
                apis=ChangeSummary(
                    add={"/add-foo": [HTTPMethod.GET]},
                    update={"/update-foo": [HTTPMethod.GET, HTTPMethod.POST]},
                    delete={"/delete-foo": [HTTPMethod.GET]},
                ),
            ),
            ChangeDetail(
                change_statistical=ChangeStatistical(
                    add=0,
                    update=2,
                    delete=1,
                ),
                apis=ChangeSummary(
                    update={"/update-foo": [HTTPMethod.GET, HTTPMethod.POST]},
                    delete={"/delete-foo": [HTTPMethod.GET]},
                ),
            ),
            ChangeDetail(
                change_statistical=ChangeStatistical(
                    add=1,
                    update=0,
                    delete=0,
                ),
                apis=ChangeSummary(
                    add={"/add-foo": [HTTPMethod.GET]},
                ),
            ),
        ],
    )
    def test_pr_body_after_process(self, model: Type[GitHubInfo], change_detail: ChangeDetail):
        github_info_model = model.deserialize({})
        github_info_model.pull_request.set_change_detail(change_detail)

        body = github_info_model.pull_request.body
        assert isinstance(body, str)
        assert "{{ GITHUB_REPOSITORY }}" not in body
        assert "{{ NEW_API_NUMBER }}" not in body
        assert "{{ CHANGE_API_NUMBER }}" not in body
        assert "{{ DELETE_API_NUMBER }}" not in body
        assert "{{ ADD_API_SUMMARY }}" not in body
        assert "{{ CHANGE_API_SUMMARY }}" not in body
        assert "{{ DELETE_API_SUMMARY }}" not in body
