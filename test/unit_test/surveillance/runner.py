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
from test._values._test_data import fake_data
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
    mock_path_exits: Mock,
    mock_load_config: Mock,
    mock_commit_process: Mock,
    mock_request: Mock,
    api_doc_config_resp: Type[DummyHTTPResponse],
):
    data = fake_data.action_input(file_path="./api.yaml", base_test_dir="./", accept_config_not_exist="true")
    mock_path_exits.return_value = True
    mock_request.return_value = api_doc_config_resp.generate(
        request_url=data[EnvironmentVariableKey.API_DOC_URL.value],
    )
    mock_commit_process.return_value = True
    mock_load_config.return_value = deserialize_api_doc_config(api_doc_config_resp.mock_data()).to_api_config()
    with patch.dict(os.environ, data, clear=True):
        run()

    mock_load_config.assert_called_once()
    mock_request.assert_called_with(method=HTTPMethod.GET, url=data[EnvironmentVariableKey.API_DOC_URL.value])
    mock_commit_process.assert_called_once()


@pytest.mark.parametrize("api_doc_config_resp", [DummySwaggerAPIDocConfigResponse, DummyOpenAPIDocConfigResponse])
@patch("urllib3.request")
@patch("ci.surveillance.runner.commit_change_config")
@patch("ci.surveillance.runner.load_config")
@patch("ci.surveillance.runner.Path.exists")
def test_run_with_not_exist_fake_api_server_config(
    mock_path_exits: Mock,
    mock_load_config: Mock,
    mock_commit_process: Mock,
    mock_request: Mock,
    api_doc_config_resp: Type[DummyHTTPResponse],
):
    data = fake_data.action_input(file_path="./api.yaml", base_test_dir="./", accept_config_not_exist="true")
    mock_path_exits.return_value = False
    mock_request.return_value = api_doc_config_resp.generate(
        request_url=data[EnvironmentVariableKey.API_DOC_URL.value],
    )
    mock_commit_process.return_value = True
    mock_load_config.return_value = deserialize_api_doc_config(api_doc_config_resp.mock_data()).to_api_config()
    with patch.dict(os.environ, data, clear=True):
        run()

    mock_load_config.assert_not_called()
    mock_request.assert_called_with(method=HTTPMethod.GET, url=data[EnvironmentVariableKey.API_DOC_URL.value])
    mock_commit_process.assert_called_once()


@pytest.mark.parametrize("api_doc_config_resp", [DummySwaggerAPIDocConfigResponse, DummyOpenAPIDocConfigResponse])
@patch("urllib3.request")
@patch("ci.surveillance.runner.commit_change_config")
@patch("ci.surveillance.runner.load_config")
@patch("ci.surveillance.runner.Path.exists")
def test_run_with_not_exist_fake_api_server_config_and_not_accept_nonexist_config(
    mock_path_exits: Mock,
    mock_load_config: Mock,
    mock_commit_process: Mock,
    mock_request: Mock,
    api_doc_config_resp: Type[DummyHTTPResponse],
):
    data = fake_data.action_input(file_path="./api.yaml", base_test_dir="./")
    mock_path_exits.return_value = False
    mock_request.return_value = api_doc_config_resp.generate(
        request_url=data[EnvironmentVariableKey.API_DOC_URL.value],
    )
    mock_commit_process.return_value = True
    mock_load_config.return_value = deserialize_api_doc_config(api_doc_config_resp.mock_data()).to_api_config()
    with patch.dict(os.environ, data, clear=True):
        with pytest.raises(FileNotFoundError):
            run()

    mock_load_config.assert_not_called()
    mock_request.assert_called_with(method=HTTPMethod.GET, url=data[EnvironmentVariableKey.API_DOC_URL.value])
    mock_commit_process.assert_not_called()
