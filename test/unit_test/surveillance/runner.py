import os
from typing import Type

import pytest
from fake_api_server import FakeAPIConfig
from fake_api_server.model.api_config.apis import ResponseStrategy
from github.Label import Label

try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod

from unittest.mock import MagicMock, Mock, call, patch

from fake_api_server._utils.file.operation import YAML
from fake_api_server.model import deserialize_api_doc_config, MockAPIs, MockAPI, HTTP, HTTPRequest, HTTPResponse

from fake_api_server_plugin.ci.surveillance.component.git import GitOperation
from fake_api_server_plugin.ci.surveillance.model import ConfigurationKey
from fake_api_server_plugin.ci.surveillance.runner import FakeApiServerSurveillance

# isort: off
from test._values._test_data import fake_data, fake_github_action_values
from test._values.dummy_objects import (
    DummySwaggerAPIDocConfigResponse,
    DummyOpenAPIDocConfigResponse,
    DummyHTTPResponse,
)

# isort: on


@pytest.mark.parametrize("api_doc_config_resp", [DummySwaggerAPIDocConfigResponse, DummyOpenAPIDocConfigResponse])
@patch("urllib3.request")
@patch.object(GitOperation, "version_change")
@patch("fake_api_server_plugin.ci.surveillance.runner.load_config")
@patch("fake_api_server_plugin.ci.surveillance.runner.Path.exists")
def test_run_with_exist_fake_api_server_config(
    mock_path_exits: Mock,
    mock_load_config: Mock,
    mock_version_change_process: Mock,
    mock_request: Mock,
    api_doc_config_resp: Type[DummyHTTPResponse],
):
    surveillance = FakeApiServerSurveillance()

    data = fake_data.surveillance_config(file_path="./api.yaml", base_test_dir="./", accept_config_not_exist=True)
    mock_path_exits.return_value = True
    mock_request.return_value = api_doc_config_resp.generate(
        request_url=data[ConfigurationKey.API_DOC_URL.value],
    )
    mock_version_change_process.return_value = True
    mock_load_config.return_value = FakeAPIConfig(apis=MockAPIs(apis={"get_sample": MockAPI(url="/sample", http=HTTP(request=HTTPRequest(method="GET"), response=HTTPResponse(strategy=ResponseStrategy.STRING, value="test")))}))

    # Setup mocks
    mock_github = Mock()
    mock_repo = Mock()
    mock_pr = Mock()
    mock_pr.html_url = "https://github.com/owner/repo/pull/1"
    mock_pr.add_to_labels = Mock()
    surveillance.github_operation._github = mock_github
    mock_github.get_repo.return_value = mock_repo

    mock_label = MagicMock(spec=Label)  # Use spec to limit attributes available in mock object
    mock_label.name = "label1"
    mock_label.color = "blue"
    mock_label.id = 123

    mock_labels = [mock_label]
    mock_repo.get_labels.return_value = mock_labels
    mock_repo.create_pull.return_value = mock_pr

    with patch.dict(os.environ, fake_github_action_values.ci_env(fake_data.repo()), clear=True):
        with patch.object(YAML, "read", return_value=data):
            surveillance.monitor()
            expect_head_branch = surveillance.git_operation.fake_api_server_monitor_git_branch

    mock_load_config.assert_called_once()
    mock_request.assert_called_with(method=HTTPMethod.GET, url=data[ConfigurationKey.API_DOC_URL.value])
    mock_version_change_process.assert_called_once()

    git_info = fake_data.git_operation_info()
    github_pr_info = fake_data.github_pr_info()
    ci_env = fake_github_action_values.ci_env(git_info[ConfigurationKey.GIT_REPOSITORY.value])
    mock_repo.create_pull.assert_called_with(
        title=github_pr_info[ConfigurationKey.PR_TITLE.value],
        body=github_pr_info[ConfigurationKey.PR_BODY.value],
        base=ci_env["GITHUB_BASE_REF"],
        head=expect_head_branch,
        draft=False,
    )
    mock_pr.add_to_labels.assert_has_calls(calls=[call(*(mock_label,))])


@pytest.mark.parametrize("api_doc_config_resp", [DummySwaggerAPIDocConfigResponse, DummyOpenAPIDocConfigResponse])
@patch("urllib3.request")
@patch.object(GitOperation, "version_change")
@patch("fake_api_server_plugin.ci.surveillance.runner.load_config")
@patch("fake_api_server_plugin.ci.surveillance.runner.Path.exists")
def test_run_with_not_exist_fake_api_server_config(
    mock_path_exits: Mock,
    mock_load_config: Mock,
    mock_version_change_process: Mock,
    mock_request: Mock,
    api_doc_config_resp: Type[DummyHTTPResponse],
):
    surveillance = FakeApiServerSurveillance()

    data = fake_data.surveillance_config(file_path="./api.yaml", base_test_dir="./", accept_config_not_exist=True)
    mock_path_exits.return_value = False
    mock_request.return_value = api_doc_config_resp.generate(
        request_url=data[ConfigurationKey.API_DOC_URL.value],
    )
    mock_version_change_process.return_value = True
    mock_load_config.return_value = FakeAPIConfig()

    # Setup mocks
    mock_github = Mock()
    mock_repo = Mock()
    mock_pr = Mock()
    mock_pr.html_url = "https://github.com/owner/repo/pull/1"
    mock_pr.add_to_labels = Mock()
    surveillance.github_operation._github = mock_github
    mock_github.get_repo.return_value = mock_repo

    mock_label = MagicMock(spec=Label)  # Use spec to limit attributes available in mock object
    mock_label.name = "label1"
    mock_label.color = "blue"
    mock_label.id = 123

    mock_labels = [mock_label]
    mock_repo.get_labels.return_value = mock_labels
    mock_repo.create_pull.return_value = mock_pr

    with patch.dict(os.environ, fake_github_action_values.ci_env(fake_data.repo()), clear=True):
        with patch.object(YAML, "read", return_value=data):
            surveillance.monitor()
            expect_head_branch = surveillance.git_operation.fake_api_server_monitor_git_branch

    mock_load_config.assert_not_called()
    mock_request.assert_called_with(method=HTTPMethod.GET, url=data[ConfigurationKey.API_DOC_URL.value])
    mock_version_change_process.assert_called_once()

    git_info = fake_data.git_operation_info()
    github_pr_info = fake_data.github_pr_info()
    ci_env = fake_github_action_values.ci_env(git_info[ConfigurationKey.GIT_REPOSITORY.value])
    mock_repo.create_pull.assert_called_with(
        title=github_pr_info[ConfigurationKey.PR_TITLE.value],
        body=github_pr_info[ConfigurationKey.PR_BODY.value],
        base=ci_env["GITHUB_BASE_REF"],
        head=expect_head_branch,
        draft=False,
    )
    mock_pr.add_to_labels.assert_has_calls(calls=[call(*(mock_label,))])


@pytest.mark.parametrize("api_doc_config_resp", [DummySwaggerAPIDocConfigResponse, DummyOpenAPIDocConfigResponse])
@patch("urllib3.request")
@patch.object(GitOperation, "version_change")
@patch("fake_api_server_plugin.ci.surveillance.runner.load_config")
@patch("fake_api_server_plugin.ci.surveillance.runner.Path.exists")
def test_run_with_not_exist_fake_api_server_config_and_not_accept_nonexist_config(
    mock_path_exits: Mock,
    mock_load_config: Mock,
    mock_version_change_process: Mock,
    mock_request: Mock,
    api_doc_config_resp: Type[DummyHTTPResponse],
):
    surveillance = FakeApiServerSurveillance()

    data = fake_data.surveillance_config(file_path="./api.yaml", base_test_dir="./", accept_config_not_exist=False)
    mock_path_exits.return_value = False
    mock_request.return_value = api_doc_config_resp.generate(
        request_url=data[ConfigurationKey.API_DOC_URL.value],
    )
    mock_version_change_process.return_value = True
    mock_load_config.return_value = FakeAPIConfig()

    # Setup mocks
    mock_github = Mock()
    mock_repo = Mock()
    mock_pr = Mock()
    mock_pr.html_url = "https://github.com/owner/repo/pull/1"
    mock_pr.add_to_labels = Mock()
    surveillance.github_operation._github = mock_github
    mock_github.get_repo.return_value = mock_repo

    mock_label = MagicMock(spec=Label)  # Use spec to limit attributes available in mock object
    mock_label.name = "label1"
    mock_label.color = "blue"
    mock_label.id = 123

    mock_labels = [mock_label]
    mock_repo.get_labels.return_value = mock_labels
    mock_repo.create_pull.return_value = mock_pr

    with patch.dict(os.environ, fake_github_action_values.ci_env(fake_data.repo()), clear=True):
        with patch.object(YAML, "read", return_value=data):
            with pytest.raises(FileNotFoundError):
                surveillance.monitor()

    mock_load_config.assert_not_called()
    mock_request.assert_called_once_with(method=HTTPMethod.GET, url=data[ConfigurationKey.API_DOC_URL.value])
    mock_version_change_process.assert_not_called()
    mock_repo.create_pull.assert_not_called()
    mock_pr.add_to_labels.assert_not_called()
