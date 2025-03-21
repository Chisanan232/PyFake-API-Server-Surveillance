import ast
import os
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from git import Repo
from git.remote import PushInfoList

from fake_api_server_plugin.ci.surveillance.component.git import GitOperation
from fake_api_server_plugin.ci.surveillance.model.config import SurveillanceConfig

# isort: off
from test._values._test_data import fake_data, fake_github_action_values, fake_git_data

# isort: on


class TestGitOperation:
    @pytest.fixture(scope="module")
    def git_operation(self) -> GitOperation:
        return GitOperation()

    @property
    def _given_action_inputs(self) -> SurveillanceConfig:
        return fake_data.surveillance_config_model(file_path="./api.yaml")

    @pytest.mark.parametrize("branch_already_exist", [False, True])
    def test_switch_git_branch(self, git_operation: GitOperation, branch_already_exist: bool):
        # given
        original_branch = ""
        test_remote_name = "pytest-branch"

        try:
            with patch("os.path.exists", return_value=True):
                git_operation.repository = git_operation._init_git(self._given_action_inputs)
            original_branch = git_operation.repository.active_branch.name
            if branch_already_exist:
                if test_remote_name not in [b.name for b in git_operation.repository.branches]:
                    git_operation.repository.git.checkout("-b", test_remote_name)
                git_operation.repository.git.switch(original_branch)

            # when
            git_operation._switch_git_branch(git_ref=test_remote_name)

            # should
            assert git_operation.repository.active_branch.name == test_remote_name
        finally:
            # clean test
            if git_operation.repository.active_branch.name != original_branch:
                git_operation.repository.git.switch(original_branch)
            if test_remote_name in [b.name for b in git_operation.repository.branches]:
                git_operation.repository.git.branch("-D", test_remote_name)

    @pytest.mark.parametrize("remote_already_exist", [False, True])
    def test_init_git_remote(self, git_operation: GitOperation, remote_already_exist: bool):
        # given
        action_inputs = self._given_action_inputs
        test_remote_name = "pytest-origin"

        try:
            with patch("os.path.exists", return_value=True):
                git_operation.repository = git_operation._init_git(self._given_action_inputs)
            if remote_already_exist:
                git_operation.repository.create_remote(name=test_remote_name, url="https://test.com")

            # when
            dummy_ci_env = fake_github_action_values.ci_env(fake_data.repo())
            with patch.dict(os.environ, dummy_ci_env, clear=True):
                git_operation._init_git_remote(surveillance_config=action_inputs, remote_name=test_remote_name)

            # should
            assert test_remote_name in git_operation.repository.remotes
            remote = git_operation.repository.remote(name=test_remote_name)
            assert remote.name == test_remote_name
            assert (
                remote.url
                == f"https://x-access-token:{dummy_ci_env['GITHUB_TOKEN']}@github.com/{action_inputs.git_info.repository}"
            )
        finally:
            # clean test
            if test_remote_name in git_operation.repository.remotes:
                git_operation.repository.delete_remote(remote=git_operation.repository.remote(name=test_remote_name))

    @patch("git.IndexFile.commit")
    @patch("git.Repo.create_remote")
    @patch.object(GitOperation, "_push_to_remote")
    def test_version_change(self, mock_remote_push: Mock, mock_init_remote_fun: Mock, mock_git_commit: Mock):
        # given
        base_test_dir = Path("./test/_values/verify_git_feature")
        if not base_test_dir.exists():
            base_test_dir.mkdir(parents=True)
        else:
            shutil.rmtree(base_test_dir)
            base_test_dir.mkdir(parents=True)

        filepath = base_test_dir / "api.yaml"
        if not filepath.exists():
            filepath.touch()
        assert filepath.exists(), "File doesn't be created. Please check it."

        action_inputs = fake_data.surveillance_config_model(file_path=filepath)

        real_repo = Repo("./")
        original_branch = real_repo.active_branch.name
        if self._is_in_ci_env and original_branch not in [b.name for b in real_repo.branches]:
            real_repo.git.checkout("-b", original_branch)

        try:
            repo = Repo.init(base_test_dir)
            # TODO: change the repo to sample project.

            push_info_list = PushInfoList()
            push_info = Mock()
            push_info.flags = 0
            push_info.ERROR = 1024
            push_info_list.append(push_info)

            mock_remote = Mock()
            mock_remote.exists = Mock(return_value=True)
            mock_remote.create = Mock()
            mock_remote.fetch = Mock()
            mock_remote.refs = []
            mock_remote.url = f"https://github.com/{action_inputs.git_info.repository}"
            mock_remote.push = Mock()
            mock_remote.push.return_value = push_info_list
            mock_init_remote_fun.return_value = mock_remote

            # when
            dummy_ci_env = fake_github_action_values.ci_env(fake_data.repo())
            with patch.dict(os.environ, dummy_ci_env, clear=True):
                result = GitOperation().version_change(action_inputs)

            # should
            assert result is True

            if mock_remote.exists() is True:
                mock_remote.create.assert_not_called()
            else:
                mock_remote.create.assert_called_once()

            assert len(repo.index.diff(None)) == 0
            mock_git_commit.assert_called_once_with(
                author=action_inputs.git_info.commit.author.serialize_for_git(),
                message=action_inputs.git_info.commit.message,
            )

            committed_files = list(map(lambda i: i.a_path, real_repo.index.diff(real_repo.head.commit)))
            assert str(filepath) in committed_files

            mock_remote_push.assert_called_once()
        finally:
            committed_files = list(map(lambda i: i.a_path, real_repo.index.diff(real_repo.head.commit)))
            if not self._is_in_ci_env and str(filepath) in committed_files:
                # test finally
                real_repo.git.restore("--staged", str(filepath))
            if real_repo.active_branch != original_branch:
                real_repo.git.switch(original_branch)
            if fake_git_data.fake_api_server_monitor_branch_name() in [b.name for b in real_repo.branches]:
                real_repo.git.branch("-D", fake_git_data.fake_api_server_monitor_branch_name())

    @property
    def _is_in_ci_env(self) -> bool:
        return ast.literal_eval(str(os.getenv("GITHUB_ACTIONS")).capitalize())
