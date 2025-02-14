import os
from pathlib import Path

import urllib3

try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod  # type: ignore[no-redef]

from fake_api_server.model import deserialize_api_doc_config, load_config
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
    all_files = set()
    for file_path in Path(action_inputs.subcmd_pull_args.base_file_path).rglob("*.yaml"):
        if file_path.is_file():
            all_files.add(file_path)

    print(f"Found files: {all_files}")

    # Check untracked files
    untracked = set(repo.untracked_files)
    print(f"Check untracked file ...")
    for file in untracked:
        if Path(file).is_file():
            if file in all_files:
                repo.index.add(file)
                print(f"Add file: {file}")
        else:
            for one_file in Path(file).rglob("*.yaml"):
                if one_file in all_files:
                    repo.index.add(one_file)
                    print(f"Add file: {one_file}")

    # Check modified but unstaged files
    diff_index = repo.index.diff(None)
    modified = {item.a_path for item in diff_index}
    print(f"Check modified file ...")
    for file in modified:
        if Path(file).is_file():
            if file in all_files:
                repo.index.add(file)
                print(f"Add file: {file}")
        else:
            for one_file in Path(file).rglob("*.yaml"):
                if one_file in all_files:
                    repo.index.add(one_file)
                    print(f"Add file: {one_file}")

    commit = repo.index.commit(
        author=action_inputs.git_info.commit.author.serialize_for_git(),
        message=action_inputs.git_info.commit.message,
    )
    print(f"Commit the change.")
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
    fake_api_server_config = action_inputs.subcmd_pull_args.config_path
    assert Path(fake_api_server_config).exists(), "The Fake-API-Server config file does not exist."
    api_config = load_config(fake_api_server_config)

    response = urllib3.request(method=HTTPMethod.GET, url=action_inputs.api_doc_url)
    current_api_doc_config = deserialize_api_doc_config(response.json())
    new_api_config = current_api_doc_config.to_api_config(base_url=action_inputs.subcmd_pull_args.base_url)

    has_api_change = False
    all_api_configs = api_config.apis.apis
    all_new_api_configs = new_api_config.apis.apis
    for api_key in all_new_api_configs.keys():
        if api_key in all_api_configs.keys():
            one_api_config = all_api_configs[api_key]
            one_new_api_config = all_new_api_configs[api_key]
            assert one_api_config is not None, "It's strange. Please check it."
            assert one_new_api_config is not None, "It's strange. Please check it."
            has_api_change = one_api_config == one_new_api_config
        else:
            has_api_change = True
            break

    if has_api_change:
        _saving_config_component = SavingConfigComponent()
        _saving_config_component.serialize_and_save(cmd_args=action_inputs.subcmd_pull_args, api_config=new_api_config)
        # result = Surveillance.monitor()

        print("commit the different and push to remote repository")
        commit_change_config(action_inputs)
        # GitHelper.commit_change()

        # TODO: this is backlog task
        # print("notify developers")
        # Notificatier.notidy()
