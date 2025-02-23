import os
from unittest.mock import patch

import pytest

from ci.surveillance.component.git import GitOperation
from ci.surveillance.model.action import ActionInput

from test._values._test_data import fake_data, fake_github_action_values


class TestGitOperation:
    @pytest.fixture(scope="module")
    def git_operation(self) -> GitOperation:
        return GitOperation()

    @property
    def _given_action_inputs(self) -> ActionInput:
        return fake_data.action_input_model(file_path="./api.yaml")

    def test_init_git_remote_with_not_exist_remote(self, git_operation: GitOperation):
        # given
        action_inputs = self._given_action_inputs
        test_remote_name = "pytest-origin"

        try:
            with patch("os.path.exists", return_value=True):
                git_operation.repository = git_operation._init_git(self._given_action_inputs)

            # when
            dummy_ci_env = fake_github_action_values.ci_env(fake_data.repo())
            with patch.dict(os.environ, dummy_ci_env, clear=True):
                git_operation._init_git_remote(action_inputs=action_inputs, remote_name=test_remote_name)

            # should
            assert test_remote_name in git_operation.repository.remotes
            remote = git_operation.repository.remote(name=test_remote_name)
            assert remote.name == test_remote_name
            assert remote.url == f"https://x-access-token:{dummy_ci_env['GITHUB_TOKEN']}@github.com/{action_inputs.git_info.repository}"
        except Exception as e:
            raise e
        finally:
            # clean test
            if test_remote_name in git_operation.repository.remotes:
                git_operation.repository.delete_remote(remote=git_operation.repository.remote(name=test_remote_name))

    def test_init_git_remote_with_exist_remote(self, git_operation: GitOperation):
        # given
        action_inputs = self._given_action_inputs
        test_remote_name = "pytest-origin"

        try:
            with patch("os.path.exists", return_value=True):
                git_operation.repository = git_operation._init_git(self._given_action_inputs)
            git_operation.repository.create_remote(name=test_remote_name, url="https://test.com")

            # when
            dummy_ci_env = fake_github_action_values.ci_env(fake_data.repo())
            with patch.dict(os.environ, dummy_ci_env, clear=True):
                git_operation._init_git_remote(action_inputs=action_inputs, remote_name=test_remote_name)

            # should
            assert test_remote_name in git_operation.repository.remotes
            remote = git_operation.repository.remote(name=test_remote_name)
            assert remote.name == test_remote_name
            assert remote.url == f"https://x-access-token:{dummy_ci_env['GITHUB_TOKEN']}@github.com/{action_inputs.git_info.repository}"
        finally:
            # clean test
            if test_remote_name in git_operation.repository.remotes:
                git_operation.repository.delete_remote(remote=git_operation.repository.remote(name=test_remote_name))
