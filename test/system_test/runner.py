import ast
import os
import shutil
from pathlib import Path
from test._values.dummy_objects import (
    DummyHTTPResponse,
    DummyOpenAPIDocConfigResponse,
    DummySwaggerAPIDocConfigResponse,
)
from typing import Type
from unittest.mock import Mock, patch

import pytest
from fake_api_server.model import deserialize_api_doc_config
from git import Repo
from git.remote import PushInfoList

from ci.surveillance.model import EnvironmentVariableKey
from ci.surveillance.runner import run


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

    default_remote = "origin"
    github_action_run_id = "123456"
    git_branch_name = f"fake-api-server-monitor-update-config_{github_action_run_id}"

    print("[DEBUG] Initial git repository")
    repo = Repo("./")
    now_in_ci_runtime_env = ast.literal_eval(str(os.getenv("GITHUB_ACTIONS")).capitalize())
    print(f"[DEBUG] os.getenv('GITHUB_ACTIONS'): {os.getenv('GITHUB_ACTIONS')}")
    print(f"[DEBUG] now_in_ci_runtime_env: {now_in_ci_runtime_env}")
    try:
        original_branch = repo.active_branch.name
    except TypeError as e:
        print("[DEBUG] Occur something wrong when trying to get git branch")
        # NOTE: Only for CI runtime environment
        if "HEAD" in str(e) and "detached" in str(e) and now_in_ci_runtime_env:
            # original_branch = os.environ["GITHUB_HEAD_REF"]
            original_branch = "github-action-ci-only"
        else:
            raise e
    print(f"[DEBUG] os.getenv('GITHUB_ACTIONS'): {os.getenv('GITHUB_ACTIONS')}")
    print(f"[DEBUG] current all git branches: {[b.name for b in repo.branches]}")
    all_branches = [str(b.name) for b in repo.branches]
    if now_in_ci_runtime_env and original_branch not in [b.name for b in repo.branches]:
        print(f"[DEBUG] create and switch git branch {original_branch}")
        repo.git.checkout("-b", original_branch)

    try:
        print("[DEBUG] Initial git remote")
        # TODO: change the repo to sample project.
        if default_remote not in repo.remotes:
            repo.create_remote(name=default_remote, url="https://github.com/Chisanan232/Sample-Python-BackEnd.git")

        print("[DEBUG] Mock git remote")
        push_info_list = PushInfoList()
        push_info = Mock()
        push_info.flags = 0
        push_info.ERROR = 1024
        push_info_list.append(push_info)

        mock_remote_push.return_value = push_info_list

        # when
        print("[DEBUG] Run target function")
        data = {
            # API documentation info
            EnvironmentVariableKey.API_DOC_URL.value: "http://127.0.0.1:8080",
            EnvironmentVariableKey.SERVER_TYPE.value: "rest-server",
            # git info
            EnvironmentVariableKey.GIT_REPOSITORY.value: "Chisanan232/Sample-Python-BackEnd",
            EnvironmentVariableKey.GIT_AUTHOR_NAME.value: "test-user[bot]",
            EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value: "test-bot@localhost.com",
            EnvironmentVariableKey.GIT_COMMIT_MSG.value: " 🧪 test commit message",
            # for subcommand line *pull* options
            EnvironmentVariableKey.CONFIG_PATH.value: str(filepath),
            EnvironmentVariableKey.INCLUDE_TEMPLATE_CONFIG.value: "True",
            EnvironmentVariableKey.BASE_FILE_PATH.value: str(base_test_dir),
            EnvironmentVariableKey.BASE_URL.value: "/test/v1",
            EnvironmentVariableKey.DIVIDE_API.value: "true",
            EnvironmentVariableKey.DIVIDE_HTTP.value: "false",
            EnvironmentVariableKey.DIVIDE_HTTP_REQUEST.value: "false",
            EnvironmentVariableKey.DIVIDE_HTTP_RESPONSE.value: "false",
            EnvironmentVariableKey.DRY_RUN.value: "true",
            # operation with action in CI
            EnvironmentVariableKey.ACCEPT_CONFIG_NOT_EXIST.value: "false",
            # GitHub action environment
            "GITHUB_TOKEN": "ghp_1234567890",
            "GITHUB_REPOSITORY": "Chisanan232/Sample-Python-BackEnd",
            "GITHUB_HEAD_REF": "git-branch",
            "GITHUB_JOB": github_action_run_id,
            "CI_TEST_MODE": "true",
        }
        mock_request.return_value = dummy_api_doc_config_resp(
            request_url=data[EnvironmentVariableKey.API_DOC_URL.value],
            status=200,
            version=11,
            version_string="HTTP/1.1",
            reason="",
            decode_content=True,
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
        mock_remote_push.assert_called_once_with(refspec=f"HEAD:refs/heads/{git_branch_name}", force=True)
    finally:
        committed_files = list(map(lambda i: i.a_path, repo.index.diff(repo.head.commit)))
        if not now_in_ci_runtime_env and str(filepath) in committed_files:
            # test finally
            repo.git.restore("--staged", str(filepath))
        if default_remote in repo.remotes:
            repo.delete_remote(repo.remote(default_remote))
        if Path(filepath).exists():
            shutil.rmtree(base_test_dir)
        if repo.active_branch != original_branch:
            repo.git.switch(original_branch)
        if git_branch_name in [b.name for b in repo.branches]:
            repo.git.branch("-D", git_branch_name)
