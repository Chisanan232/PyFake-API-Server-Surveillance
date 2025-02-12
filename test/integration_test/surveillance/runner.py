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


@patch("git.IndexFile.commit")
@patch("git.Repo.remote")
def test_commit_change_config(mock_init_remote_fun: Mock, mock_git_commit: Mock):
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
            repository=Mock(),
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
    )

    default_remote = "origin"
    git_branch_name = "test-branch"
    real_repo = Repo("./")

    try:
        repo = Repo.init(base_test_dir)
        # TODO: change the repo to sample project.
        repo.create_remote(name=default_remote, url="https://github.com/Chisanan232/fake-api-server-surveillance.git")

        push_info_list = PushInfoList()
        push_info = Mock()
        push_info.flags = 0
        push_info.ERROR = 1024
        push_info_list.append(push_info)

        mock_remote = Mock()
        mock_remote.push = Mock()
        mock_remote.push.return_value = push_info_list
        mock_init_remote_fun.return_value = mock_remote

        # when
        data = {
            "GITHUB_REPOSITORY": "tester/pyfake-test",
            "GITHUB_HEAD_REF": git_branch_name,
        }
        with patch.dict(os.environ, data, clear=True):
            result = commit_change_config(action_inputs)

        # should
        assert result is True

        repo = Repo(base_test_dir)
        assert len(repo.index.diff(None)) == 0
        mock_git_commit.assert_called_once_with(
            author=action_inputs.git_info.commit.author.serialize_for_git(),
            message=action_inputs.git_info.commit.message,
        )
        mock_init_remote_fun.assert_called_once_with(name=default_remote)
        mock_remote.push.assert_called_once_with(f"{default_remote}:{git_branch_name}")

        committed_files = list(map(lambda i: i.a_path, real_repo.index.diff(real_repo.head.commit)))
        assert str(filepath) in committed_files
    finally:
        committed_files = list(map(lambda i: i.a_path, real_repo.index.diff(real_repo.head.commit)))
        if not os.getenv("GITHUB_ACTIONS") and committed_files:
            # test finally
            real_repo.git.restore("--staged", str(filepath))
