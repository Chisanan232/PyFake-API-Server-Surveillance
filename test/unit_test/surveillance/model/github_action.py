import os
from typing import Mapping, Type

import pytest

from fake_api_server_plugin.ci.surveillance.model.github_action import get_github_action_env, GitHubActionEnvironmentVariable

# isort: off
from ._base import _BaseModelTestSuite

# isort: on


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS", "false") == "true",
    reason="It should test the really environment to guarantee that it could correctly initial this data model.",
)
def test_get_github_action_env():
    model = get_github_action_env()
    assert model is not None
    TestGitHubActionEnvironmentVariable()._verify_model_props(model, os.environ)


class TestGitHubActionEnvironmentVariable(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[GitHubActionEnvironmentVariable]:
        return GitHubActionEnvironmentVariable

    @pytest.mark.skipif(
        os.getenv("GITHUB_ACTIONS", "false") == "true",
        reason="It should test the really environment to guarantee that it could correctly initial this data model.",
    )
    @pytest.mark.parametrize("data", [os.environ])
    def test_deserialize(self, model: Type[GitHubActionEnvironmentVariable], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(cls, model: GitHubActionEnvironmentVariable, original_data: Mapping) -> None:
        assert model.github_actions is True
        assert model.repository == original_data["GITHUB_REPOSITORY"]
        assert model.repository_owner_name
        assert model.repository_name
        assert f"{model.repository_owner_name}/{model.repository_name}" == original_data["GITHUB_REPOSITORY"]
        assert model.base_branch == original_data["GITHUB_BASE_REF"]
        assert model.head_branch == original_data["GITHUB_HEAD_REF"]
        assert model.github_token == original_data["GITHUB_TOKEN"]
