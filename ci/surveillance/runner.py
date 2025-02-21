import ast
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
    # Initial a git project
    print(f"[DEBUG] action_inputs: {action_inputs}")
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

    remote_name: str = "origin"
    in_ci_runtime_env = ast.literal_eval(str(os.getenv("CI_TEST_MODE", "false")).capitalize())
    if in_ci_runtime_env:
        github_action_job_id = os.environ["GITHUB_JOB"]
        print(f"[DEBUG] GitHub run ID: {github_action_job_id}")
        git_ref: str = f"fake-api-server-monitor-update-config_{github_action_job_id}"
    else:
        git_ref: str = "fake-api-server-monitor-update-config"  # type: ignore[no-redef]

    # Initial git remote setting
    git_remote = repo.remote(name=remote_name)
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
        git_remote.create(repo=repo, name=remote_name, url=remote_url)
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

    # Sync up the code version from git
    git_remote.fetch()
    now_in_ci_runtime_env = ast.literal_eval(str(os.getenv("GITHUB_ACTIONS")).capitalize())
    try:
        current_git_branch = repo.active_branch.name
    except TypeError as e:
        print("[DEBUG] Occur something wrong when trying to get git branch")
        # NOTE: Only for CI runtime environment
        if "HEAD" in str(e) and "detached" in str(e) and now_in_ci_runtime_env:
            # original_branch = os.environ["GITHUB_HEAD_REF"]
            current_git_branch = ""
        else:
            raise e
    # Switch to target git branch which only for Fake-API-Server
    if current_git_branch != git_ref:
        if git_ref in [b.name for b in repo.branches]:
            repo.git.switch(git_ref)
        else:
            repo.git.checkout("-b", git_ref)

    # Get all files in the folder
    all_files = set()
    for file_path in Path(action_inputs.subcmd_pull_args.base_file_path).rglob("*.yaml"):
        if file_path.is_file():
            all_files.add(file_path)

    print(f"Found files: {all_files}")

    all_ready_commit_files = set()

    # Check untracked files
    untracked = set(repo.untracked_files)
    print("Check untracked file ...")
    for file in untracked:
        print(f"Found untracked files: {file}")
        file_path_obj = Path(file)
        if file_path_obj.is_file():
            if file_path_obj in all_files:
                all_ready_commit_files.add(str(file_path_obj))
                repo.index.add(str(file_path_obj))
                print(f"Add file: {file_path_obj}")
        else:
            for one_file in Path(file).rglob("*.yaml"):
                if one_file in all_files:
                    all_ready_commit_files.add(str(file_path_obj))
                    repo.index.add(one_file)
                    print(f"Add file: {one_file}")

    # Check modified but unstaged files
    diff_index = repo.index.diff(None)
    modified = {item.a_path for item in diff_index}
    print("Check modified file ...")
    for file in modified:
        print(f"Found modified files: {file}")
        file_path_obj = Path(file)
        if file_path_obj.is_file():
            if file_path_obj in all_files:
                all_ready_commit_files.add(str(file_path_obj))
                repo.index.add(str(file_path_obj))
                print(f"Add file: {file_path_obj}")
        else:
            for one_file in Path(file).rglob("*.yaml"):
                if one_file in all_files:
                    all_ready_commit_files.add(str(file_path_obj))
                    repo.index.add(one_file)
                    print(f"Add file: {one_file}")

    # Commit the update change
    if len(all_ready_commit_files) > 0:
        commit = repo.index.commit(
            author=action_inputs.git_info.commit.author.serialize_for_git(),
            message=action_inputs.git_info.commit.message,
        )
        print("Commit the change.")

        # Push the change to git server
        # git_remote.push(f"{remote_name}:{git_ref}").raise_if_error()
        git_remote.push(refspec=f"HEAD:refs/heads/{git_ref}", force=True).raise_if_error()
        print(f"Successfully pushed commit {commit.hexsha[:8]} to {remote_name}/{git_ref}")
    else:
        print("Don't have any files be added. Won't commit the change.")
    return True


def run() -> None:
    # get the API doc config from end point (request API doc config and get response)
    # check the diff between local config and the new config (check the diff by git?)
    # if no diff = nothing, else it would update the config (commit the change and request PR by git and gh?)
    print("monitor the github repro ...")
    has_api_change = False
    action_inputs = ActionInput.deserialize(os.environ)

    response = urllib3.request(method=HTTPMethod.GET, url=action_inputs.api_doc_url)
    current_api_doc_config = deserialize_api_doc_config(response.json())
    new_api_config = current_api_doc_config.to_api_config(base_url=action_inputs.subcmd_pull_args.base_url)

    fake_api_server_config = action_inputs.subcmd_pull_args.config_path
    if Path(fake_api_server_config).exists():
        api_config = load_config(fake_api_server_config)

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
    else:
        if not action_inputs.accept_config_not_exist:
            raise FileNotFoundError("Not found Fake-API-Server config file. Please add it in repository.")
        has_api_change = True
        fake_api_server_config_dir = Path(fake_api_server_config).parent
        if not fake_api_server_config_dir.exists():
            fake_api_server_config_dir.mkdir(parents=True, exist_ok=True)

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
