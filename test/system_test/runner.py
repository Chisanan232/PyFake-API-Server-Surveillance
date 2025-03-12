import ast
import os
import shutil
from pathlib import Path
from typing import Type
from unittest.mock import MagicMock, Mock, call, patch

import pytest
from fake_api_server._utils.file.operation import YAML
from fake_api_server.model import deserialize_api_doc_config
from git import Repo
from git.remote import PushInfoList
from github import Label

from fake_api_server_plugin.ci.surveillance.model import ConfigurationKey
from fake_api_server_plugin.ci.surveillance.runner import FakeApiServerSurveillance

# isort: off
from test._values._test_data import fake_data, fake_git_data, fake_github_action_values
from test._values.dummy_objects import (
    DummyHTTPResponse,
    DummyOpenAPIDocConfigResponse,
    DummySwaggerAPIDocConfigResponse,
)

# isort: on


@pytest.mark.parametrize("dummy_api_doc_config_resp", [DummySwaggerAPIDocConfigResponse, DummyOpenAPIDocConfigResponse])
@patch("urllib3.request")
@patch("fake_api_server_plugin.ci.surveillance.runner.load_config")
@patch("git.remote.Remote.push")
def test_entire_flow_with_not_exist_config(
    mock_remote_push: Mock,
    mock_load_config: Mock,
    mock_request: Mock,
    dummy_api_doc_config_resp: Type[DummyHTTPResponse],
):
    # given
    surveillance = FakeApiServerSurveillance()

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

    repo = Repo("./")
    now_in_ci_runtime_env = ast.literal_eval(str(os.getenv("GITHUB_ACTIONS")).capitalize())
    original_branch = repo.active_branch.name
    if now_in_ci_runtime_env and original_branch not in [b.name for b in repo.branches]:
        repo.git.checkout("-b", original_branch)

    try:
        # TODO: change the repo to sample project.
        if fake_git_data.default_remote_name() not in repo.remotes:
            repo.create_remote(
                name=fake_git_data.default_remote_name(), url=f"https://github.com/{fake_data.repo()}.git"
            )

        push_info_list = PushInfoList()
        push_info = Mock()
        push_info.flags = 0
        push_info.ERROR = 1024
        push_info_list.append(push_info)

        mock_remote_push.return_value = push_info_list

        # Setup GitHub operation mocks
        mock_github = Mock()
        mock_repo = Mock()
        mock_pr = Mock()
        mock_pr.html_url = "https://github.com/owner/repo/pull/1"
        mock_pr.add_to_labels = Mock()
        surveillance.github_operation._github = mock_github
        mock_github.get_repo.return_value = mock_repo

        mock_label = MagicMock(spec=Label)  # Use spec to limit attributes available in mock object
        mock_label.name = "label1"
        mock_label.color = "blue"
        mock_label.id = 123

        mock_labels = [mock_label]
        mock_repo.get_labels.return_value = mock_labels
        mock_repo.create_pull.return_value = mock_pr

        # when
        data = fake_data.surveillance_config(file_path=filepath, base_test_dir=base_test_dir)
        mock_request.return_value = dummy_api_doc_config_resp.generate(
            request_url=data[ConfigurationKey.API_DOC_URL.value],
        )
        mock_load_config.return_value = deserialize_api_doc_config(
            dummy_api_doc_config_resp.mock_data()
        ).to_api_config()
        with patch.dict(os.environ, fake_github_action_values.ci_env(fake_data.repo()), clear=True):
            with patch.object(YAML, "read", return_value=data):
                surveillance.monitor()
                expect_head_branch = surveillance.git_operation.fake_api_server_monitor_git_branch

        # should
        git_info = fake_data.git_operation_info()
        assert (
            repo.head.commit.author.name
            == git_info[ConfigurationKey.GIT_COMMIT.value][ConfigurationKey.GIT_AUTHOR.value][
                ConfigurationKey.GIT_AUTHOR_NAME.value
            ]
        )
        assert (
            repo.head.commit.author.email
            == git_info[ConfigurationKey.GIT_COMMIT.value][ConfigurationKey.GIT_AUTHOR.value][
                ConfigurationKey.GIT_AUTHOR_EMAIL.value
            ]
        )
        assert (
            repo.head.commit.message
            == git_info[ConfigurationKey.GIT_COMMIT.value][ConfigurationKey.GIT_COMMIT_MSG.value]
        )
        commit_files = repo.head.commit.stats.files.keys()
        assert len(commit_files) > 0
        assert str(filepath) in commit_files

        mock_remote_push.assert_called_once_with(
            refspec=f"HEAD:refs/heads/{fake_git_data.fake_api_server_monitor_branch_name()}", force=True
        )

        github_pr_info = fake_data.github_pr_info()
        ci_env = fake_github_action_values.ci_env(git_info[ConfigurationKey.GIT_REPOSITORY.value])
        mock_repo.create_pull.assert_called_with(
            title=github_pr_info[ConfigurationKey.PR_TITLE.value],
            body=github_pr_info[ConfigurationKey.PR_BODY.value],
            base=ci_env["GITHUB_BASE_REF"],
            head=expect_head_branch,
            draft=False,
        )
        mock_pr.add_to_labels.assert_has_calls(calls=[call(*(mock_label,))])
    finally:
        committed_files = list(map(lambda i: i.a_path, repo.index.diff(repo.head.commit)))
        if not now_in_ci_runtime_env and str(filepath) in committed_files:
            # test finally
            repo.git.restore("--staged", str(filepath))
        if fake_git_data.default_remote_name() in repo.remotes:
            repo.delete_remote(repo.remote(fake_git_data.default_remote_name()))
        if Path(filepath).exists():
            shutil.rmtree(base_test_dir)
        if repo.active_branch != original_branch:
            repo.git.switch(original_branch)
        if fake_git_data.fake_api_server_monitor_branch_name() in [b.name for b in repo.branches]:
            repo.git.branch("-D", fake_git_data.fake_api_server_monitor_branch_name())
