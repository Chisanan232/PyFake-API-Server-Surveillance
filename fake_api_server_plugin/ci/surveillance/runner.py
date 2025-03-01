import os
from pathlib import Path
from typing import Mapping

import urllib3
from fake_api_server import FakeAPIConfig

try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod  # type: ignore[no-redef]

from fake_api_server.model import deserialize_api_doc_config, load_config

from .component.git import GitOperation
from .component.pull import SavingConfigComponent
from .model.action import ActionInput


class FakeApiServerSurveillance:
    def monitor(self) -> None:
        # get the API doc config from end point (request API doc config and get response)
        # check the diff between local config and the new config (check the diff by git?)
        # if no diff = nothing, else it would update the config (commit the change and request PR by git and gh?)
        print("monitor the github repro ...")
        action_inputs = self._deserialize_action_inputs(self._get_action_inputs())

        new_api_doc_config = self._get_latest_api_doc_config(action_inputs)
        has_api_change = self._compare_with_current_config(action_inputs, new_api_doc_config)
        if has_api_change:
            self._update_api_doc_config(action_inputs, new_api_doc_config)
            # result = Surveillance.monitor()

            print("commit the different and push to remote repository")
            self._process_versioning(action_inputs)
            # GitHelper.commit_change()

            # TODO: this is backlog task
            # print("notify developers")
            # Notificatier.notidy()

    def _process_versioning(self, action_inputs: ActionInput) -> None:
        GitOperation().version_change(action_inputs)

    def _update_api_doc_config(self, action_inputs: ActionInput, new_api_doc_config: FakeAPIConfig) -> None:
        SavingConfigComponent().serialize_and_save(cmd_args=action_inputs.subcmd_pull_args, api_config=new_api_doc_config)

    def _compare_with_current_config(self, action_inputs: ActionInput, new_api_doc_config: FakeAPIConfig) -> bool:
        has_api_change = False
        fake_api_server_config = action_inputs.subcmd_pull_args.config_path
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
            if not action_inputs.accept_config_not_exist:
                raise FileNotFoundError("Not found Fake-API-Server config file. Please add it in repository.")
            has_api_change = True
            fake_api_server_config_dir = Path(fake_api_server_config).parent
            if not fake_api_server_config_dir.exists():
                fake_api_server_config_dir.mkdir(parents=True, exist_ok=True)
        return has_api_change

    def _get_latest_api_doc_config(self, action_inputs: ActionInput) -> FakeAPIConfig:
        response = urllib3.request(method=HTTPMethod.GET, url=action_inputs.api_doc_url)
        current_api_doc_config = deserialize_api_doc_config(response.json())
        return current_api_doc_config.to_api_config(base_url=action_inputs.subcmd_pull_args.base_url)

    def _get_action_inputs(self) -> Mapping:
        return os.environ

    def _deserialize_action_inputs(self, action_inputs: Mapping) -> ActionInput:
        return ActionInput.deserialize(action_inputs)


def run() -> None:
    FakeApiServerSurveillance().monitor()
