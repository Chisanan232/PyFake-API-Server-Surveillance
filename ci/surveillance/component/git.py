import ast
import os
from pathlib import Path
from typing import List, Set, Optional, Union

from git import Repo, Remote, Commit

from ci.surveillance.model.action import ActionInput


class GitOperation:
    def __init__(self):
        self._git_repo: Optional[Repo] = None
        self._all_staged_files: Set[str] = set()

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
        return ast.literal_eval(str(os.getenv("GITHUB_ACTION", "false")).capitalize())

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
            # NOTE: Only for CI runtime environment
            print("[DEBUG] Occur something wrong when trying to get git branch")
            if "HEAD" in str(e) and "detached" in str(e) and self.is_in_ci_env:
                current_git_branch = ""
            else:
                raise e
        return current_git_branch

    def _reset_all_staged_files(self) -> None:
        self._all_staged_files.clear()

    def version_change(self, action_inputs: ActionInput) -> bool:
        # Initial a git project
        self.repository: Repo = self._init_git(action_inputs)

        # Initial git remote setting
        git_remote = self._init_git_remote(action_inputs, self.default_remote_name)

        # Sync up the code version from git
        git_remote.fetch()
        # Switch to target git branch which only for Fake-API-Server
        self._switch_git_branch(self.fake_api_server_monitor_git_branch)

        # Get all files in the folder
        all_files = self._get_all_fake_api_server_configs(action_inputs)
        print(f"Found files: {all_files}")

        # Check untracked files
        print("Check untracked file ...")
        untracked = set(self.repository.untracked_files)
        self._add_files(all_files=all_files, target_files=untracked)

        # Check modified but unstaged files
        print("Check modified file ...")
        diff_index = self.repository.index.diff(None)
        modified = {item.a_path for item in diff_index}
        self._add_files(all_files=all_files, target_files=modified)

        if len(self._all_staged_files) > 0:
            # Commit the update change
            commit = self._commit_changes(action_inputs)

            # Push the change to git server
            self._push_to_remote(git_remote)
            print(f"Successfully pushed commit {commit.hexsha[:8]} to {self.default_remote_name}/{self.fake_api_server_monitor_git_branch}")
        else:
            print("Don't have any files be added. Won't commit the change.")
        return True

    def _init_git(self, action_inputs: ActionInput) -> Repo:
        assert os.path.exists(
            action_inputs.subcmd_pull_args.config_path
        ), "PyFake-API-Server configuration is required. Please check it."
        return Repo("./")

    def _init_git_remote(self, action_inputs: ActionInput, remote_name: str) -> Remote:
        if remote_name not in self.repository.remotes:
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
            git_remote = self.repository.create_remote(name=remote_name, url=remote_url)
        else:
            git_remote = self.repository.remote(name=remote_name)
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

    def _switch_git_branch(self, git_ref: str) -> None:
        if self._current_git_branch != git_ref:
            if git_ref in [b.name for b in self.repository.branches]:
                self.repository.git.switch(git_ref)
            else:
                self.repository.git.checkout("-b", git_ref)

    def _get_all_fake_api_server_configs(self, action_inputs: ActionInput) -> Set[Path]:
        all_files: Set[Path] = set()
        for file_path in Path(action_inputs.subcmd_pull_args.base_file_path).rglob("*.yaml"):
            if file_path.is_file():
                all_files.add(file_path)
        return all_files

    def _add_files(self, all_files: Set[Path], target_files: Set[str]) -> None:

        def _add_file(_file: Union[Path, str]) -> None:
            if _file in all_files:
                self._all_staged_files.add(str(_file))
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

    def _commit_changes(self, action_inputs: ActionInput) -> Commit:
        commit = self.repository.index.commit(
            author=action_inputs.git_info.commit.author.serialize_for_git(),
            message=action_inputs.git_info.commit.message,
        )
        print("Commit the change.")
        self._reset_all_staged_files()
        return commit

    def _push_to_remote(self, git_remote: Remote) -> None:
        # git_remote.push(f"{remote_name}:{git_ref}").raise_if_error()
        git_remote.push(refspec=f"HEAD:refs/heads/{self.fake_api_server_monitor_git_branch}", force=True).raise_if_error()
