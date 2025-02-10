import os
from unittest.mock import patch, Mock

from ci.surveillance.model import EnvironmentVariableKey
from ci.surveillance.model.action import ActionInput
from ci.surveillance.runner import run


@patch.object(ActionInput, "deserialize")
def test_run(mock_action_input_model_deserialize: Mock):
    data = {
        EnvironmentVariableKey.API_DOC_URL.value: "http://10.20.0.13:8080",
        EnvironmentVariableKey.SERVER_TYPE.value: "rest-server",
        EnvironmentVariableKey.GIT_REPOSITORY.value: "test/sample-project",
        EnvironmentVariableKey.GIT_AUTHOR_NAME.value: "test",
        EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value: "test@gmail.com",
        EnvironmentVariableKey.GIT_COMMIT_MSG.value: "✏️ Update the API interface settings.",
    }
    with patch.dict(os.environ, data, clear=True):
        run()

    mock_action_input_model_deserialize.assert_called_once()
