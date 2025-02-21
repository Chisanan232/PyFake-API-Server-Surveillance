import ast
import os
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from git import Repo
from git.remote import PushInfoList

from ci.surveillance.model.action import ActionInput
from ci.surveillance.model.git import GitAuthor, GitCommit, GitInfo
from ci.surveillance.model.subcmd_pull import PullApiDocConfigArgs
from ci.surveillance.runner import commit_change_config


@patch("ci.surveillance.runner.uuid.uuid1")
@patch("git.IndexFile.commit")
@patch("git.Repo.remote")
def test_commit_change_config(mock_init_remote_fun: Mock, mock_git_commit: Mock, mock_uuid: Mock):
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

    action_inputs = ActionInput(
        server_type=Mock(),
        api_doc_url=Mock(),
        git_info=GitInfo(
            repository="Chisanan232/Sample-Python-BackEnd",
            commit=GitCommit(
                author=GitAuthor(
                    name="test-user[bot]",
                    email="test-bot@localhost.com",
                ),
                message=" 🧪 test commit message",
            ),
        ),
        subcmd_pull_args=PullApiDocConfigArgs(
            config_path=f"{base_test_dir}/api.yaml",
            include_template_config=True,
            base_file_path=str(base_test_dir),
            base_url="./",
            divide_api=True,
            divide_http=False,
            divide_http_request=False,
            divide_http_response=False,
            dry_run=True,
        ),
        accept_config_not_exist=False,
    )

    default_remote = "origin"
    github_action_run_id = "123456"
    action_uuid = "123-456-789"
    git_branch_name = f"fake-api-server-monitor-update-config_{github_action_run_id}_{action_uuid}"
    real_repo = Repo("./")
    now_in_ci_runtime_env = ast.literal_eval(str(os.getenv("GITHUB_ACTIONS")).capitalize())
    print(f"[DEBUG] os.getenv('GITHUB_ACTIONS'): {os.getenv('GITHUB_ACTIONS')}")
    print(f"[DEBUG] now_in_ci_runtime_env: {now_in_ci_runtime_env}")
    try:
        original_branch = real_repo.active_branch.name
    except TypeError as e:
        print("[DEBUG] Occur something wrong when trying to get git branch")
        # NOTE: Only for CI runtime environment
        if "HEAD" in str(e) and "detached" in str(e) and now_in_ci_runtime_env:
            # original_branch = os.environ["GITHUB_HEAD_REF"]
            original_branch = "github-action-ci-only"
        else:
            raise e
    if now_in_ci_runtime_env and original_branch not in [b.name for b in real_repo.branches]:
        print(f"[DEBUG] create and switch git branch {original_branch}")
        real_repo.git.checkout("-b", original_branch)

    try:
        mock_uuid.return_value = action_uuid

        print("[DEBUG] Initial git repository")
        repo = Repo.init(base_test_dir)
        # TODO: change the repo to sample project.
        print("[DEBUG] Initial git remote")
        if default_remote not in repo.remotes:
            repo.create_remote(
                name=default_remote, url="https://github.com/Chisanan232/fake-api-server-surveillance.git"
            )

        push_info_list = PushInfoList()
        push_info = Mock()
        push_info.flags = 0
        push_info.ERROR = 1024
        push_info_list.append(push_info)

        print("[DEBUG] Mock git remote")
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
        print("[DEBUG] Run target function")
        data = {
            "GITHUB_TOKEN": "ghp_1234567890",
            "GITHUB_REPOSITORY": "tester/pyfake-test",
            "GITHUB_HEAD_REF": git_branch_name,
            "GITHUB_JOB": github_action_run_id,
            "CI_TEST_MODE": "true",
        }
        with patch.dict(os.environ, data, clear=True):
            result = commit_change_config(action_inputs)

        # should
        print("[DEBUG] Start checking running state")
        assert result is True

        print("[DEBUG] Checking remote callable state")
        mock_init_remote_fun.assert_called_once_with(name=default_remote)
        if mock_remote.exists() is True:
            mock_remote.create.assert_not_called()
        else:
            mock_remote.create.assert_called_once()

        print("[DEBUG] Checkin sync state and branch operation state")
        mock_remote.fetch.assert_called_once()

        print("[DEBUG] Checkin commit running state")
        assert len(repo.index.diff(None)) == 0
        mock_git_commit.assert_called_once_with(
            author=action_inputs.git_info.commit.author.serialize_for_git(),
            message=action_inputs.git_info.commit.message,
        )

        committed_files = list(map(lambda i: i.a_path, real_repo.index.diff(real_repo.head.commit)))
        assert str(filepath) in committed_files

        print("[DEBUG] Checkin git push running state")
        # mock_remote.push.assert_called_once_with(f"{default_remote}:{git_branch_name}")
        mock_remote.push.assert_called_once_with(refspec=f"HEAD:refs/heads/{git_branch_name}", force=True)
    finally:
        committed_files = list(map(lambda i: i.a_path, real_repo.index.diff(real_repo.head.commit)))
        if not now_in_ci_runtime_env and str(filepath) in committed_files:
            # test finally
            real_repo.git.restore("--staged", str(filepath))
        if real_repo.active_branch != original_branch:
            real_repo.git.switch(original_branch)
        if git_branch_name in [b.name for b in real_repo.branches]:
            real_repo.git.branch("-D", git_branch_name)
