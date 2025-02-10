import json
import os
from http import HTTPMethod, HTTPStatus
from unittest.mock import Mock, patch

from urllib3 import BaseHTTPResponse

from ci.surveillance.model import EnvironmentVariableKey
from ci.surveillance.runner import run


class DummyResponse(BaseHTTPResponse):

    @property
    def data(self) -> bytes:
        _data = {"key": "value"}
        return json.dumps(_data).encode("utf-8")


@patch("urllib3.request")
def test_run(mock_request: Mock):
    data = {
        EnvironmentVariableKey.API_DOC_URL.value: "http://10.20.0.13:8080",
        EnvironmentVariableKey.SERVER_TYPE.value: "rest-server",
        EnvironmentVariableKey.GIT_REPOSITORY.value: "test/sample-project",
        EnvironmentVariableKey.GIT_AUTHOR_NAME.value: "test",
        EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value: "test@gmail.com",
        EnvironmentVariableKey.GIT_COMMIT_MSG.value: "✏️ Update the API interface settings.",
    }
    mock_request.return_value = DummyResponse(
        request_url=data[EnvironmentVariableKey.API_DOC_URL.value],
        status=HTTPStatus.OK,
        version=11,
        version_string="HTTP/1.1",
        reason="",
        decode_content=True,
    )
    with patch.dict(os.environ, data, clear=True):
        run()

    mock_request.assert_called_with(method=HTTPMethod.GET, url=data[EnvironmentVariableKey.API_DOC_URL.value])
