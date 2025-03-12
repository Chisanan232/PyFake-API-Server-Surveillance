from pathlib import Path
from typing import Any, Dict, Union
from unittest.mock import Mock

from ci.surveillance.model.action import ActionInput
from ci.surveillance.model.config import FakeAPIConfigSetting
from fake_api_server.command.subcommand import SubCommandLine

from fake_api_server_plugin.ci.surveillance.model import ConfigurationKey, EnvironmentVariableKey
from fake_api_server_plugin.ci.surveillance.model.config import SurveillanceConfig
from fake_api_server_plugin.ci.surveillance.model.config.api_config import (
    SubCmdConfig,
)
from fake_api_server_plugin.ci.surveillance.model.config.git import (
    GitAuthor,
    GitCommit,
    GitInfo,
)
from fake_api_server_plugin.ci.surveillance.model.config.github import (
    GitHubInfo,
    PullRequestInfo,
)


class fake_github_action_values:
    @classmethod
    def action_job_id(cls) -> str:
        return "123456"

    @classmethod
    def event_name(cls) -> str:
        return "pull_request"

    @classmethod
    def ci_env(cls, repo: str) -> Dict[str, str]:
        return {
            # GitHub action environment
            "GITHUB_TOKEN": "ghp_1234567890",
            "GITHUB_ACTIONS": "false",
            "GITHUB_REPOSITORY": repo,
            "GITHUB_BASE_REF": "master",
            "GITHUB_HEAD_REF": "git-branch",
            "GITHUB_JOB": fake_github_action_values.action_job_id(),
            "GITHUB_EVENT_NAME": cls.event_name(),
            "CI_TEST_MODE": "true",
        }


class fake_git_data:
    @classmethod
    def default_remote_name(cls) -> str:
        return "origin"

    @classmethod
    def fake_api_server_monitor_branch_name(cls) -> str:
        return f"fake-api-server-monitor-update-config_{fake_github_action_values.event_name()}_{fake_github_action_values.action_job_id()}"


class fake_data:
    @classmethod
    def repo(cls) -> str:
        return "Chisanan232/Sample-Python-BackEnd"

    @classmethod
    def surveillance_config(
        cls, file_path: Union[str, Path], base_test_dir: Union[str, Path], accept_config_not_exist: bool = False
    ) -> Dict[str, Any]:
        return {
            ConfigurationKey.API_DOC_URL.value: "http://127.0.0.1:8080",
            ConfigurationKey.FAKE_API_SERVER.value: cls.fake_api_server_config(file_path, base_test_dir),
            ConfigurationKey.GIT_INFO.value: cls.git_operation_info(),
            ConfigurationKey.GITHUB_INFO.value: cls.github_info(),
            ConfigurationKey.ACCEPT_CONFIG_NOT_EXIST.value: accept_config_not_exist,
        }

    @classmethod
    def surveillance_config_model(cls, file_path: Union[str, Path]) -> SurveillanceConfig:
        return SurveillanceConfig(
            # server_type=Mock(),
            api_doc_url=Mock(),
            fake_api_server=FakeAPIConfigSetting(
                server_type=Mock(),
                subcmd={
                    SubCommandLine.Pull: SubCmdConfig(
                        args=[
                            f"--config-path={file_path}",
                            "--include-template-config",
                            f"--base-file-path={str(file_path.parent) if isinstance(file_path, Path) else str(Path(file_path).parent)}",
                            "--base-url=/test/v1",
                            "--dry-run",
                            "--divide-api",
                            "--divide-http",
                            "--divide-http-request",
                            "--divide-http-response",
                        ],
                    ),
                },
            ),
            git_info=GitInfo(
                repository="Chisanan232/Sample-Python-BackEnd",
                commit=GitCommit(
                    author=GitAuthor(
                        name="test-user[bot]",
                        email="test-bot@localhost.com",
                    ),
                    message=" 🧪 test commit message",
                ),
            ),
            github_info=GitHubInfo(
                pull_request=PullRequestInfo(
                    title="✏️ Update the API configuration because API change.",
                    body="Monitor the project and found changes. Update the configuration.",
                    draft=True,
                    labels=["label1", "label2"],
                ),
            ),
            accept_config_not_exist=True,
        )

    @classmethod
    def action_input_model(cls) -> ActionInput:
        return ActionInput(
            config_path="./pytest-surveillance.yaml",
        )

    @classmethod
    def action_input(cls) -> Dict[str, str]:
        return {
            EnvironmentVariableKey.SURVEILLANCE_CONFIG_PATH.value: "./pytest-surveillance.yaml",
        }

    @classmethod
    def backend_project_info(cls) -> Dict[str, str]:
        return {
            # API documentation info
            ConfigurationKey.API_DOC_URL.value: "http://127.0.0.1:8080",
            # EnvironmentVariableKey.SERVER_TYPE.value: "rest-server",
        }

    @classmethod
    def git_operation_info(cls) -> Dict[str, Any]:
        return {
            # git info
            ConfigurationKey.GIT_REPOSITORY.value: cls.repo(),
            ConfigurationKey.GIT_COMMIT.value: cls.git_commit_info(),
        }

    @classmethod
    def git_commit_info(cls) -> Dict[str, Any]:
        return {
            ConfigurationKey.GIT_AUTHOR.value: cls.git_commit_author_info(),
            ConfigurationKey.GIT_COMMIT_MSG.value: " 🧪 test commit message",
        }

    @classmethod
    def git_commit_author_info(cls) -> Dict[str, str]:
        return {
            ConfigurationKey.GIT_AUTHOR_NAME.value: "test-user[bot]",
            ConfigurationKey.GIT_AUTHOR_EMAIL.value: "test-bot@localhost.com",
        }

    @classmethod
    def github_info(cls) -> Dict[str, Any]:
        return {
            # github info
            ConfigurationKey.GITHUB_PULL_REQUEST.value: cls.github_pr_info(),
        }

    @classmethod
    def github_pr_info(cls) -> Dict[str, Any]:
        return {
            ConfigurationKey.PR_TITLE.value: "✏️ Update the API configuration because API change.",
            ConfigurationKey.PR_BODY.value: "Monitor the project and found changes. Update the configuration.",
            ConfigurationKey.PR_IS_DRAFT.value: True,
            ConfigurationKey.PR_LABELS.value: ["label1", "label2"],
        }

    @classmethod
    def fake_api_server_config(cls, file_path: Union[str, Path], base_test_dir: Union[str, Path]) -> Dict[str, Any]:
        return {
            ConfigurationKey.SERVER_TYPE.value: "rest-server",
            ConfigurationKey.SUBCMD.value: {
                SubCommandLine.Pull.value: {
                    ConfigurationKey.ARGS.value: [
                        f"--config-path={file_path}",
                        "--include-template-config",
                        f"--base-file-path={base_test_dir}",
                        "--base-url=/test/v1",
                        "--dry-run",
                        "--divide-api",
                        "--divide-http",
                        "--divide-http-request",
                        "--divide-http-response",
                    ],
                },
            },
        }

    @classmethod
    def fake_api_server_subcmd_pull_args(cls) -> Dict[str, Any]:
        return {
            ConfigurationKey.ARGS.value: [
                "--config-path=./pytest-api.yaml",
                "--include-template-config",
                "--base-file-path=./",
                "--base-url=/test/v1",
                "--dry-run",
                "--divide-api",
                "--divide-http",
                "--divide-http-request",
                "--divide-http-response",
            ],
        }

    @classmethod
    def subcmd_pull_args(cls, file_path: Union[str, Path], base_test_dir: Union[str, Path]) -> Dict[str, str]:
        return {
            # for subcommand line *pull* options
            ConfigurationKey.CONFIG_PATH.value: str(file_path),
            ConfigurationKey.INCLUDE_TEMPLATE_CONFIG.value: "True",
            ConfigurationKey.BASE_FILE_PATH.value: str(base_test_dir),
            ConfigurationKey.BASE_URL.value: "/test/v1",
            ConfigurationKey.DIVIDE_API.value: "true",
            ConfigurationKey.DIVIDE_HTTP.value: "false",
            ConfigurationKey.DIVIDE_HTTP_REQUEST.value: "false",
            ConfigurationKey.DIVIDE_HTTP_RESPONSE.value: "false",
            ConfigurationKey.DRY_RUN.value: "true",
        }

    @classmethod
    def action_operation(cls, accept_config_not_exist: str = "false") -> Dict[str, str]:
        return {
            # operation with action in CI
            ConfigurationKey.ACCEPT_CONFIG_NOT_EXIST.value: accept_config_not_exist,
        }
