import os
import subprocess
from pathlib import Path

import urllib3

try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod  # type: ignore[no-redef]

from fake_api_server.model import deserialize_api_doc_config
from git import Repo

from .component import SavingConfigComponent
from .model.action import ActionInput


def commit_change_config(action_inputs: ActionInput) -> bool:
    if os.path.exists(action_inputs.subcmd_pull_args.config_path):
        repo = Repo("./")
    else:
        repo = Repo.clone_from(
            url=f"https://github.com/{os.environ['GITHUB_REPOSITORY']}",
            to_path="./",
        )
        assert os.path.exists(
            action_inputs.subcmd_pull_args.config_path
        ), "PyFake-API-Server configuration is required. Please check it."

    remote_name: str = "origin"
    git_ref: str = os.environ["GITHUB_HEAD_REF"]

    # Get all files in the folder
    for file_path in Path(action_inputs.subcmd_pull_args.base_file_path).rglob("*.yaml"):
        if file_path.is_file():
            print(f"[DEBUG] file_path: {file_path}")
            repo.index.add(str(file_path))

    result = subprocess.run("git status", shell=True, capture_output=True)
    print(f"[DEBUG] git status (before add file): {result.stdout}")
    # Check untracked files
    untracked = set(repo.untracked_files)
    for file in untracked:
        print(f"[DEBUG] file: {file}")
        repo.index.add(file)

    result = subprocess.run("git status", shell=True, capture_output=True)
    print(f"[DEBUG] git status (add untracked files): {result.stdout}")

    # Check modified but unstaged files
    diff_index = repo.index.diff(None)
    modified = {item.a_path for item in diff_index}
    for file in modified:
        print(f"[DEBUG] file: {file}")
        repo.index.add(file)

    result = subprocess.run("git status", shell=True, capture_output=True)
    print(f"[DEBUG] git status (add unstaged files): {result.stdout}")

    commit = repo.index.commit(
        author=action_inputs.git_info.commit.author.serialize_for_git(),
        message=action_inputs.git_info.commit.message,
    )
    push_result = repo.remote(name=remote_name).push(f"{remote_name}:{git_ref}")
    # Check push result
    if push_result[0].flags & push_result[0].ERROR:
        print("Push failed. Please check.")
        return False

    print(f"Successfully pushed commit {commit.hexsha[:8]} to {remote_name}/{git_ref}")
    return True


def run() -> None:
    # get the API doc config from end point (request API doc config and get response)
    # check the diff between local config and the new config (check the diff by git?)
    # if no diff = nothing, else it would update the config (commit the change and request PR by git and gh?)
    print("monitor the github repro ...")
    action_inputs = ActionInput.deserialize(os.environ)

    response = urllib3.request(method=HTTPMethod.GET, url=action_inputs.api_doc_url)
    current_api_doc_config = deserialize_api_doc_config(response.json())

    _saving_config_component = SavingConfigComponent()
    api_config = current_api_doc_config.to_api_config(base_url=action_inputs.subcmd_pull_args.base_url)
    _saving_config_component.serialize_and_save(cmd_args=action_inputs.subcmd_pull_args, api_config=api_config)
    # result = Surveillance.monitor()

    print("commit the different and push to remote repository")
    commit_change_config(action_inputs)
    # GitHelper.commit_change()

    # TODO: this is backlog task
    print("notify developers")
    # Notificatier.notidy()
