from typing import Mapping, Type

import pytest

from ci.surveillance.model import EnvironmentVariableKey
from ci.surveillance.model.git import GitAuthor, GitCommit, GitInfo

from ._base import _BaseModelTestSuite


class TestGitAuthor(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[GitAuthor]:
        return GitAuthor

    @pytest.mark.parametrize(
        "data",
        [
            {
                EnvironmentVariableKey.GIT_AUTHOR_NAME.value: "test",
                EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value: "test@gmail.com",
            },
        ],
    )
    def test_deserialize(self, model: Type[GitAuthor], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: GitAuthor, original_data: Mapping) -> None:
        assert model.name == original_data[EnvironmentVariableKey.GIT_AUTHOR_NAME.value]
        assert model.email == original_data[EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value]


class TestGitCommit(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[GitCommit]:
        return GitCommit

    @pytest.mark.parametrize(
        "data",
        [
            {
                EnvironmentVariableKey.GIT_AUTHOR_NAME.value: "test",
                EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value: "test@gmail.com",
                EnvironmentVariableKey.GIT_COMMIT_MSG.value: "✏️ Update the API interface settings.",
            },
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
            {
                EnvironmentVariableKey.GIT_REPOSITORY.value: "test/sample-project",
                EnvironmentVariableKey.GIT_AUTHOR_NAME.value: "test",
                EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value: "test@gmail.com",
                EnvironmentVariableKey.GIT_COMMIT_MSG.value: "✏️ Update the API interface settings.",
            },
        ],
    )
    def test_deserialize(self, model: Type[GitInfo], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: GitInfo, original_data: Mapping) -> None:
        assert model.repository == original_data[EnvironmentVariableKey.GIT_REPOSITORY.value]
        assert model.commit.author.name == original_data[EnvironmentVariableKey.GIT_AUTHOR_NAME.value]
        assert model.commit.author.email == original_data[EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value]
        assert model.commit.message == original_data[EnvironmentVariableKey.GIT_COMMIT_MSG.value]
