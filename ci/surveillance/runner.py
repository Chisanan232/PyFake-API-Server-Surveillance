import os
try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod

import urllib3

from .model.action import ActionInput


def run() -> None:
    # get the API doc config from end point (request API doc config and get response)
    # check the diff between local config and the new config (check the diff by git?)
    # if no diff = nothing, else it would update the config (commit the change and request PR by git and gh?)
    print("monitor the github repro ...")
    action_inputs = ActionInput.deserialize(os.environ)
    response = urllib3.request(method=HTTPMethod.GET, url=action_inputs.api_doc_url)
    response_data = response.json()
    print(f"Get response: {response_data}")
    # result = Surveillance.monitor()
    print("got difference~")
    # GitHelper.commit_change()
    # TODO: this is backlog task
    print("notify developers")
    # Notificatier.notidy()
