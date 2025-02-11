import os
import urllib3

try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod  # type: ignore[no-redef]

from fake_api_server.model import deserialize_api_doc_config

from .component import SavingConfigComponent
from .model.action import ActionInput


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
    print("got difference~")
    # GitHelper.commit_change()
    # TODO: this is backlog task
    print("notify developers")
    # Notificatier.notidy()
