import os
from pathlib import Path
from typing import Mapping, cast

import urllib3
from fake_api_server import FakeAPIConfig
from fake_api_server.command.subcommand import SubCommandLine

from .model.action import ActionInput

try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod  # type: ignore[no-redef]

from fake_api_server._utils.file.operation import YAML
from fake_api_server.model import deserialize_api_doc_config, load_config

from .component.git import GitOperation
from .component.github_opt import GitHubOperation
from .component.pull import SavingConfigComponent
from .model.config import PullApiDocConfigArgs, SurveillanceConfig
from .model.config.github_action import get_github_action_env


class FakeApiServerSurveillance:
    def __init__(self):
        self.subcmd_pull_component = SavingConfigComponent()
        self.git_operation = GitOperation()
        self.github_operation: GitHubOperation = GitHubOperation()

    def monitor(self) -> None:
        print("monitor the github repro ...")
        action_inputs = self._deserialize_action_inputs(self._get_action_inputs())
        surveillance_config = self._deserialize_surveillance_config(action_inputs)

        print("try to get the latest api doc config ...")
        new_api_doc_config = self._get_latest_api_doc_config(surveillance_config)
        print("compare the latest api doc config with current config ...")
        has_api_change = self._compare_with_current_config(surveillance_config, new_api_doc_config)
        if has_api_change:
            print("has something change and will create a pull request")
            self._process_api_change(surveillance_config, new_api_doc_config)
        else:
            print("nothing change and won't do anything..")
            self._process_no_api_change(surveillance_config)

    def _get_action_inputs(self) -> Mapping:
        return os.environ

    def _deserialize_action_inputs(self, action_inputs: Mapping) -> ActionInput:
        print(f"[DEBUG in _deserialize_action_inputs] deserialize action inputs ... ")
        return ActionInput.deserialize(action_inputs)

    def _deserialize_surveillance_config(self, action_input: ActionInput):
        print(f"[DEBUG in _deserialize_action_inputs] read surveillance config ...")
        surveillance_config = YAML().read(action_input.config_path)
        print(f"[DEBUG in _deserialize_action_inputs] deserialize surveillance config ...")
        return SurveillanceConfig.deserialize(surveillance_config)

    def _get_latest_api_doc_config(self, surveillance_config: SurveillanceConfig) -> FakeAPIConfig:
        print(f"[DEBUG in _get_latest_api_doc_config] action_inputs.api_doc_url: {surveillance_config.api_doc_url}")
        response = urllib3.request(method=HTTPMethod.GET, url=surveillance_config.api_doc_url)
        current_api_doc_config = deserialize_api_doc_config(response.json())
        subcmd_args = cast(
            PullApiDocConfigArgs,
            surveillance_config.fake_api_server.subcmd[SubCommandLine.Pull].to_subcmd_args(PullApiDocConfigArgs),
        )
        return current_api_doc_config.to_api_config(base_url=subcmd_args.base_url)

    def _compare_with_current_config(
        self, surveillance_config: SurveillanceConfig, new_api_doc_config: FakeAPIConfig
    ) -> bool:
        has_api_change = False
        subcmd_args = cast(
            PullApiDocConfigArgs,
            surveillance_config.fake_api_server.subcmd[SubCommandLine.Pull].to_subcmd_args(PullApiDocConfigArgs),
        )
        fake_api_server_config = subcmd_args.config_path
        if Path(fake_api_server_config).exists():
            api_config = load_config(fake_api_server_config)

            all_api_configs = api_config.apis.apis
            all_new_api_configs = new_api_doc_config.apis.apis
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
            if not surveillance_config.accept_config_not_exist:
                raise FileNotFoundError("Not found Fake-API-Server config file. Please add it in repository.")
            has_api_change = True
            fake_api_server_config_dir = Path(fake_api_server_config).parent
            if not fake_api_server_config_dir.exists():
                fake_api_server_config_dir.mkdir(parents=True, exist_ok=True)
        return has_api_change

    def _process_api_change(self, surveillance_config: SurveillanceConfig, new_api_doc_config: FakeAPIConfig) -> None:
        subcmd_args = cast(
            PullApiDocConfigArgs,
            surveillance_config.fake_api_server.subcmd[SubCommandLine.Pull].to_subcmd_args(PullApiDocConfigArgs),
        )
        self._update_api_doc_config(subcmd_args, new_api_doc_config)
        print("commit the different and push to remote repository")
        self._process_versioning(surveillance_config)
        self._notify(surveillance_config)

    def _update_api_doc_config(self, args: PullApiDocConfigArgs, new_api_doc_config: FakeAPIConfig) -> None:
        self.subcmd_pull_component.serialize_and_save(cmd_args=args, api_config=new_api_doc_config)

    def _process_versioning(self, surveillance_config: SurveillanceConfig) -> None:
        has_change = self.git_operation.version_change(surveillance_config)
        print(f"[DEBUG] has_change: {has_change}")
        if has_change:
            print(f"has something change and will create a pull request: {has_change}")
            github_action_env = get_github_action_env()
            with self.github_operation(
                repo_owner=github_action_env.repository_owner_name, repo_name=github_action_env.repository_name
            ):
                pull_request_info = surveillance_config.github_info.pull_request
                print(f"[DEBUG] pull_request_info: {pull_request_info}")
                self.github_operation.create_pull_request(
                    title=pull_request_info.title,
                    body=pull_request_info.body,
                    base_branch=github_action_env.base_branch,
                    head_branch=self.git_operation.fake_api_server_monitor_git_branch,
                    labels=pull_request_info.labels,
                )

    def _notify(self, surveillance_config: SurveillanceConfig) -> None:
        # TODO: this is backlog task
        pass

    def _process_no_api_change(self, surveillance_config: SurveillanceConfig) -> None:
        pass


def run() -> None:
    FakeApiServerSurveillance().monitor()
