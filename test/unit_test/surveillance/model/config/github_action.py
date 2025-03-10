import ast
import os
from test._values._test_data import fake_github_action_values
from typing import Mapping, Type
from unittest.mock import patch

import pytest

from fake_api_server_plugin.ci.surveillance.model.config.github_action import (
    GitHubActionEnvironmentVariable,
    get_github_action_env,
)

# isort: off
from ._base import _BaseModelTestSuite

# isort: on


def test_get_github_action_env():
    with patch.dict(os.environ, fake_github_action_values.ci_env("Chisanan232/Sample-Python-BackEnd"), clear=True):
        model = get_github_action_env()
        assert model is not None
        TestGitHubActionEnvironmentVariable()._verify_model_props(model, os.environ)


class TestGitHubActionEnvironmentVariable(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[GitHubActionEnvironmentVariable]:
        return GitHubActionEnvironmentVariable

    @pytest.mark.parametrize("data", [fake_github_action_values.ci_env("Chisanan232/Sample-Python-BackEnd")])
    def test_deserialize(self, model: Type[GitHubActionEnvironmentVariable], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: GitHubActionEnvironmentVariable, original_data: Mapping) -> None:
        assert model.github_actions is ast.literal_eval(str(original_data["GITHUB_ACTIONS"]).capitalize())
        assert model.repository == original_data["GITHUB_REPOSITORY"]
        assert model.repository_owner_name
        assert model.repository_name
        assert f"{model.repository_owner_name}/{model.repository_name}" == original_data["GITHUB_REPOSITORY"]
        assert model.base_branch == original_data["GITHUB_BASE_REF"]
        assert model.head_branch == original_data["GITHUB_HEAD_REF"]
        assert model.github_token == original_data["GITHUB_TOKEN"]
