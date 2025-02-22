import ast
import os
from pathlib import Path
from typing import List, Set, Optional, Union

from git import Repo, Remote, Commit

from ci.surveillance.model.action import ActionInput


class GitOperation:
    def __init__(self):
        self._action_inputs: Optional[ActionInput] = None
        self._git_repo: Optional[Repo] = None

    @property
    def repository(self) -> Repo:
        assert self._git_repo is not None, "Should set the repository instance before using it."
        return self._git_repo

    @repository.setter
    def repository(self, repo: Repo) -> None:
        assert repo is not None, "Should not set the repository as empty."
        self._git_repo = repo

    @property
    def is_in_ci_env(self) -> bool:
        return ast.literal_eval(str(os.getenv("CI_TEST_MODE", "false")).capitalize())

    @property
    def fake_api_server_monitor_git_branch(self) -> str:
        if self.is_in_ci_env:
            github_action_event_name = os.environ["GITHUB_EVENT_NAME"]
            print(f"[DEBUG] GitHub event name: {github_action_event_name}")
            github_action_job_id = os.environ["GITHUB_JOB"]
            print(f"[DEBUG] GitHub run ID: {github_action_job_id}")
            git_ref: str = f"fake-api-server-monitor-update-config_{github_action_event_name}_{github_action_job_id}"
        else:
            git_ref: str = "fake-api-server-monitor-update-config"  # type: ignore[no-redef]
        return git_ref

    @property
    def default_remote_name(self) -> str:
        return "origin"

    @property
    def _current_git_branch(self) -> str:
        try:
            current_git_branch = self.repository.active_branch.name
        except TypeError as e:
            print("[DEBUG] Occur something wrong when trying to get git branch")
            # NOTE: Only for CI runtime environment
            if "HEAD" in str(e) and "detached" in str(e) and self.is_in_ci_env:
                # original_branch = os.environ["GITHUB_HEAD_REF"]
                current_git_branch = ""
            else:
                raise e
        return current_git_branch

    def version_change(self, action_inputs: ActionInput) -> bool:
        # Initial a git project
        self._action_inputs: ActionInput = action_inputs
        print(f"[DEBUG] action_inputs: {self._action_inputs}")
        self.repository: Repo = self._init_git(action_inputs)

        # remote_name: str = "origin"
        # git_ref = self._fake_api_server_git_branch

        # Initial git remote setting
        git_remote = self._init_git_remote(self._action_inputs, self.default_remote_name)

        # Sync up the code version from git
        git_remote.fetch()
        # Switch to target git branch which only for Fake-API-Server
        self._switch_git_branch()

        # Get all files in the folder
        all_files = self._get_all_fake_api_server_configs(self._action_inputs)
        print(f"Found files: {all_files}")

        all_ready_commit_files = set()

        # Check untracked files
        untracked = set(self.repository.untracked_files)
        print("Check untracked file ...")
        self._add_files(all_files=all_files, all_ready_commit_files=all_ready_commit_files, target_files=untracked)

        # Check modified but unstaged files
        diff_index = self.repository.index.diff(None)
        modified = {item.a_path for item in diff_index}
        print("Check modified file ...")
        self._add_files(all_files=all_files, all_ready_commit_files=all_ready_commit_files, target_files=modified)

        # Commit the update change
        if len(all_ready_commit_files) > 0:
            commit = self._commit_changes(self._action_inputs)

            # Push the change to git server
            self._push_to_remote(git_remote)
            print(f"Successfully pushed commit {commit.hexsha[:8]} to {self.default_remote_name}/{self.fake_api_server_monitor_git_branch}")
        else:
            print("Don't have any files be added. Won't commit the change.")
        return True

    def _push_to_remote(self, git_remote: Remote) -> None:
        # git_remote.push(f"{remote_name}:{git_ref}").raise_if_error()
        git_remote.push(refspec=f"HEAD:refs/heads/{self.fake_api_server_monitor_git_branch}", force=True).raise_if_error()

    def _commit_changes(self, action_inputs: ActionInput) -> Commit:
        commit = self.repository.index.commit(
            author=action_inputs.git_info.commit.author.serialize_for_git(),
            message=action_inputs.git_info.commit.message,
        )
        print("Commit the change.")
        return commit

    def _switch_git_branch(self) -> None:
        git_ref = self.fake_api_server_monitor_git_branch
        if self._current_git_branch != git_ref:
            if git_ref in [b.name for b in self.repository.branches]:
                self.repository.git.switch(git_ref)
            else:
                self.repository.git.checkout("-b", git_ref)

    def _init_git_remote(self, action_inputs: ActionInput, remote_name: str) -> Remote:
        git_remote = self.repository.remote(name=remote_name)
        if not git_remote.exists():
            print("[DEBUG] Target git remote setting doesn't exist, create one.")
            # github_access_token = os.environ["FAKE_API_SERVER_BOT_GITHUB_TOKEN"]
            github_access_token = os.environ["GITHUB_TOKEN"]
            assert github_access_token, "Miss GitHub token"
            # github_account = action_inputs.git_info.commit.author.name
            # git_ssh_access = f"{github_account}:{github_access_token}@"
            # git_remote.create(
            #     repo=repo, name=remote_name, url=f"https://{git_ssh_access}github.com/{action_inputs.git_info.repository}"
            # )
            remote_url = f"https://x-access-token:{github_access_token}@github.com/{action_inputs.git_info.repository}"
            git_remote.create(repo=self.repository, name=remote_name, url=remote_url)
        else:
            print(f"[DEBUG] git_remote.url: {git_remote.url}")
            if action_inputs.git_info.repository not in git_remote.url:
                print("[DEBUG] Target git remote URL is not as expect, modify the URL.")
                # github_access_token = os.environ["FAKE_API_SERVER_BOT_GITHUB_TOKEN"]
                github_access_token = os.environ["GITHUB_TOKEN"]
                assert github_access_token, "Miss GitHub token"
                # github_account = action_inputs.git_info.commit.author.name
                # git_ssh_access = f"{github_account}:{github_access_token}@"
                # git_remote.set_url(new_url=f"https://{git_ssh_access}github.com/{action_inputs.git_info.repository}")
                # "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/$GITHUB_REPOSITORY"
                remote_url = f"https://x-access-token:{github_access_token}@github.com/{action_inputs.git_info.repository}"
                git_remote.set_url(new_url=remote_url)
            else:
                print("[DEBUG] Remote info all is correct.")
        return git_remote

    def _init_git(self, action_inputs: ActionInput) -> Repo:
        api_config_path = action_inputs.subcmd_pull_args.config_path
        print(f"[DEBUG] api_config_path: {api_config_path}")
        api_config_exists = os.path.exists(api_config_path)
        print(f"[DEBUG] api_config_exists: {api_config_exists}")
        if api_config_exists:
            print("[DEBUG] PyFake config exists, initial git directly.")
            repo = Repo("./")
        else:
            print("[DEBUG] PyFake config doesn't exist, clone the project from GitHub repository.")
            repo = Repo.clone_from(
                url=f"https://github.com/{action_inputs.git_info.repository}",
                to_path="./",
            )
            assert os.path.exists(
                action_inputs.subcmd_pull_args.config_path
            ), "PyFake-API-Server configuration is required. Please check it."
        return repo

    def _get_all_fake_api_server_configs(self, action_inputs: ActionInput) -> Set[Path]:
        all_files: Set[Path] = set()
        for file_path in Path(action_inputs.subcmd_pull_args.base_file_path).rglob("*.yaml"):
            if file_path.is_file():
                all_files.add(file_path)
        return all_files

    def _add_files(self, all_files: Set[Path], all_ready_commit_files: Set[str], target_files: Set[str]) -> None:

        def _add_file(_file: Union[Path, str]) -> None:
            if _file in all_files:
                all_ready_commit_files.add(str(_file))
                self.repository.index.add(str(_file))
                print(f"Add file: {_file}")

        for file in target_files:
            print(f"Found some file: {file}")
            file_path_obj = Path(file)
            if file_path_obj.is_file():
                _add_file(file_path_obj)
            else:
                for one_file in Path(file).rglob("*.yaml"):
                    _add_file(one_file)
