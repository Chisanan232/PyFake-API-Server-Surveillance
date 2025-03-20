import os
from typing import Mapping, Type
from unittest.mock import patch

import pytest
from git import Actor

from fake_api_server_plugin.ci.surveillance.model import ConfigurationKey
from fake_api_server_plugin.ci.surveillance.model.config.git import (
    GitAuthor,
    GitCommit,
    GitInfo,
)

# isort: off
from .._base import _BaseModelTestSuite
from test._values._test_data import fake_data

# isort: on


class TestGitAuthor(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[GitAuthor]:
        return GitAuthor

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.git_commit_author_info(),
        ],
    )
    def test_deserialize(self, model: Type[GitAuthor], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: GitAuthor, original_data: Mapping) -> None:
        assert model.name == original_data[ConfigurationKey.GIT_AUTHOR_NAME.value]
        assert model.email == original_data[ConfigurationKey.GIT_AUTHOR_EMAIL.value]

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.git_commit_author_info(),
        ],
    )
    def test_serialize_for_git(self, model: Type[GitAuthor], data: Mapping) -> None:
        git_author = model.deserialize(data).serialize_for_git()
        assert isinstance(git_author, Actor)
        assert git_author.name == data[ConfigurationKey.GIT_AUTHOR_NAME.value]
        assert git_author.email == data[ConfigurationKey.GIT_AUTHOR_EMAIL.value]


class TestGitCommit(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[GitCommit]:
        return GitCommit

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.git_commit_info(),
        ],
    )
    def test_deserialize(self, model: Type[GitCommit], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: GitCommit, original_data: Mapping) -> None:
        original_git_commit_author_data = original_data[ConfigurationKey.GIT_AUTHOR.value]
        assert model.author.name == original_git_commit_author_data[ConfigurationKey.GIT_AUTHOR_NAME.value]
        assert model.author.email == original_git_commit_author_data[ConfigurationKey.GIT_AUTHOR_EMAIL.value]
        assert model.message == original_data[ConfigurationKey.GIT_COMMIT_MSG.value]


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
        mock_project = "foo/sample-project"
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": mock_project}, clear=True):
            super().test_deserialize(model, data)

    def _verify_model_props(self, model: GitInfo, original_data: Mapping) -> None:
        assert model.repository == original_data[ConfigurationKey.GIT_REPOSITORY.value]
        original_git_commit_data = original_data[ConfigurationKey.GIT_COMMIT.value]
        original_git_commit_author_data = original_git_commit_data[ConfigurationKey.GIT_AUTHOR.value]
        assert model.commit.author.name == original_git_commit_author_data[ConfigurationKey.GIT_AUTHOR_NAME.value]
        assert model.commit.author.email == original_git_commit_author_data[ConfigurationKey.GIT_AUTHOR_EMAIL.value]
        assert model.commit.message == original_git_commit_data[ConfigurationKey.GIT_COMMIT_MSG.value]

    def test_deserialize_with_empty_data(self, model: Type[GitInfo]):
        mock_project = "foo/sample-project"
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": mock_project}, clear=True):
            model = model.deserialize({})
            assert model.repository == mock_project
