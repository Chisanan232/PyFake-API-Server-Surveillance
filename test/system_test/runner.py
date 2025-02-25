import ast
import os
import shutil
from pathlib import Path
from typing import Type
from unittest.mock import Mock, patch

import pytest
from fake_api_server.model import deserialize_api_doc_config
from git import Repo
from git.remote import PushInfoList

from ci.surveillance.model import EnvironmentVariableKey
from ci.surveillance.runner import run

# isort: off
from test._values._test_data import fake_data, fake_git_data
from test._values.dummy_objects import (
    DummyHTTPResponse,
    DummyOpenAPIDocConfigResponse,
    DummySwaggerAPIDocConfigResponse,
)

# isort: on


@pytest.mark.parametrize("dummy_api_doc_config_resp", [DummySwaggerAPIDocConfigResponse, DummyOpenAPIDocConfigResponse])
@patch("urllib3.request")
@patch("ci.surveillance.runner.load_config")
@patch("git.remote.Remote.push")
def test_entire_flow_with_not_exist_config(
    mock_remote_push: Mock,
    mock_load_config: Mock,
    mock_request: Mock,
    dummy_api_doc_config_resp: Type[DummyHTTPResponse],
):
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

    print("[DEBUG] Initial git repository")
    repo = Repo("./")
    now_in_ci_runtime_env = ast.literal_eval(str(os.getenv("GITHUB_ACTIONS")).capitalize())
    print(f"[DEBUG] os.getenv('GITHUB_ACTIONS'): {os.getenv('GITHUB_ACTIONS')}")
    print(f"[DEBUG] now_in_ci_runtime_env: {now_in_ci_runtime_env}")
    original_branch = repo.active_branch.name
    print(f"[DEBUG] os.getenv('GITHUB_ACTIONS'): {os.getenv('GITHUB_ACTIONS')}")
    print(f"[DEBUG] current all git branches: {[b.name for b in repo.branches]}")
    if now_in_ci_runtime_env and original_branch not in [b.name for b in repo.branches]:
        print(f"[DEBUG] create and switch git branch {original_branch}")
        repo.git.checkout("-b", original_branch)

    try:
        print("[DEBUG] Initial git remote")
        # TODO: change the repo to sample project.
        if fake_git_data.default_remote_name() not in repo.remotes:
            repo.create_remote(
                name=fake_git_data.default_remote_name(), url=f"https://github.com/{fake_data.repo()}.git"
            )

        print("[DEBUG] Mock git remote")
        push_info_list = PushInfoList()
        push_info = Mock()
        push_info.flags = 0
        push_info.ERROR = 1024
        push_info_list.append(push_info)

        mock_remote_push.return_value = push_info_list

        # when
        print("[DEBUG] Run target function")
        data = fake_data.action_input(file_path=filepath, base_test_dir=base_test_dir)
        mock_request.return_value = dummy_api_doc_config_resp.generate(
            request_url=data[EnvironmentVariableKey.API_DOC_URL.value],
        )
        mock_load_config.return_value = deserialize_api_doc_config(
            dummy_api_doc_config_resp.mock_data()
        ).to_api_config()
        with patch.dict(os.environ, data, clear=True):
            run()

        # should
        print("[DEBUG] Checkin commit running state")
        assert repo.head.commit.author.name == data[EnvironmentVariableKey.GIT_AUTHOR_NAME.value]
        assert repo.head.commit.author.email == data[EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value]
        assert repo.head.commit.message == data[EnvironmentVariableKey.GIT_COMMIT_MSG.value]
        commit_files = repo.head.commit.stats.files.keys()
        assert len(commit_files) > 0
        assert data[EnvironmentVariableKey.CONFIG_PATH.value] in commit_files

        print("[DEBUG] Checkin git push running state")
        # mock_remote_push.assert_called_once_with(f"{default_remote}:{git_branch_name}")
        mock_remote_push.assert_called_once_with(
            refspec=f"HEAD:refs/heads/{fake_git_data.fake_api_server_monitor_branch_name()}", force=True
        )
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
