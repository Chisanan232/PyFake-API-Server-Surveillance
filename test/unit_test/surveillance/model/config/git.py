from typing import Mapping, Type

import pytest
from git import Actor

from fake_api_server_plugin.ci.surveillance.model import EnvironmentVariableKey
from fake_api_server_plugin.ci.surveillance.model.config.git import (
    GitAuthor,
    GitCommit,
    GitInfo,
)

# isort: off
from ._base import _BaseModelTestSuite
from test._values._test_data import fake_data

# isort: on


class TestGitAuthor(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[GitAuthor]:
        return GitAuthor

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.git_operation_info(),
        ],
    )
    def test_deserialize(self, model: Type[GitAuthor], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: GitAuthor, original_data: Mapping) -> None:
        assert model.name == original_data[EnvironmentVariableKey.GIT_AUTHOR_NAME.value]
        assert model.email == original_data[EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value]

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.git_operation_info(),
        ],
    )
    def test_serialize_for_git(self, model: Type[GitAuthor], data: Mapping) -> None:
        git_author = model.deserialize(data).serialize_for_git()
        assert isinstance(git_author, Actor)
        assert git_author.name == data[EnvironmentVariableKey.GIT_AUTHOR_NAME.value]
        assert git_author.email == data[EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value]


class TestGitCommit(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[GitCommit]:
        return GitCommit

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.git_operation_info(),
        ],
    )
    def test_deserialize(self, model: Type[GitCommit], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: GitCommit, original_data: Mapping) -> None:
        assert model.author.name == original_data[EnvironmentVariableKey.GIT_AUTHOR_NAME.value]
        assert model.author.email == original_data[EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value]
        assert model.message == original_data[EnvironmentVariableKey.GIT_COMMIT_MSG.value]


class TestGitInfo(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[GitInfo]:
        return GitInfo

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.git_operation_info(),
        ],
    )
    def test_deserialize(self, model: Type[GitInfo], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: GitInfo, original_data: Mapping) -> None:
        assert model.repository == original_data[EnvironmentVariableKey.GIT_REPOSITORY.value]
        assert model.commit.author.name == original_data[EnvironmentVariableKey.GIT_AUTHOR_NAME.value]
        assert model.commit.author.email == original_data[EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value]
        assert model.commit.message == original_data[EnvironmentVariableKey.GIT_COMMIT_MSG.value]
