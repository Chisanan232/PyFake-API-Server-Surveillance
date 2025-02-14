import os
from typing import Type

import pytest

try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod

from unittest.mock import Mock, patch

from fake_api_server.model import deserialize_api_doc_config

from ci.surveillance.model import EnvironmentVariableKey
from ci.surveillance.runner import run

# isort: off
from test._values.dummy_objects import (
    DummySwaggerAPIDocConfigResponse,
    DummyOpenAPIDocConfigResponse,
    DummyHTTPResponse,
)


# isort: on


@pytest.mark.parametrize("api_doc_config_resp", [DummySwaggerAPIDocConfigResponse, DummyOpenAPIDocConfigResponse])
@patch("urllib3.request")
@patch("ci.surveillance.runner.commit_change_config")
@patch("ci.surveillance.runner.load_config")
@patch("ci.surveillance.runner.Path.exists")
def test_run_with_exist_fake_api_server_config(
    mock_path_exits: Mock, mock_load_config: Mock, mock_commit_process: Mock, mock_request: Mock, api_doc_config_resp: Type[DummyHTTPResponse]
):
    data = {
        # API documentation info
        EnvironmentVariableKey.API_DOC_URL.value: "http://10.20.0.13:8080",
        EnvironmentVariableKey.SERVER_TYPE.value: "rest-server",
        # git info
        EnvironmentVariableKey.GIT_REPOSITORY.value: "test/sample-project",
        EnvironmentVariableKey.GIT_AUTHOR_NAME.value: "test",
        EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value: "test@gmail.com",
        EnvironmentVariableKey.GIT_COMMIT_MSG.value: "✏️ Update the API interface settings.",
        # for subcommand line *pull* options
        EnvironmentVariableKey.CONFIG_PATH.value: "./api.yaml",
        EnvironmentVariableKey.INCLUDE_TEMPLATE_CONFIG.value: "True",
        EnvironmentVariableKey.BASE_FILE_PATH.value: "./",
        EnvironmentVariableKey.BASE_URL.value: "/test/v1",
        EnvironmentVariableKey.DIVIDE_API.value: "true",
        EnvironmentVariableKey.DIVIDE_HTTP.value: "false",
        EnvironmentVariableKey.DIVIDE_HTTP_REQUEST.value: "false",
        EnvironmentVariableKey.DIVIDE_HTTP_RESPONSE.value: "false",
        EnvironmentVariableKey.DRY_RUN.value: "true",
        # GitHub action environment
        "GITHUB_HEAD_REF": "git-branch",
    }
    mock_path_exits.return_value = True
    mock_request.return_value = api_doc_config_resp(
        request_url=data[EnvironmentVariableKey.API_DOC_URL.value],
        status=200,
        version=11,
        version_string="HTTP/1.1",
        reason="",
        decode_content=True,
    )
    mock_commit_process.return_value = True
    mock_load_config.return_value = deserialize_api_doc_config(api_doc_config_resp.mock_data()).to_api_config()
    with patch.dict(os.environ, data, clear=True):
        run()

    mock_request.assert_called_with(method=HTTPMethod.GET, url=data[EnvironmentVariableKey.API_DOC_URL.value])
    mock_commit_process.assert_called_once()
