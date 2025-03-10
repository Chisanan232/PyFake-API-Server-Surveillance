from pathlib import Path
from typing import Dict, Union
from unittest.mock import Mock

from fake_api_server_plugin.ci.surveillance.model import EnvironmentVariableKey
from fake_api_server_plugin.ci.surveillance.model.config import SurveillanceConfig
from fake_api_server_plugin.ci.surveillance.model.config.git import (
    GitAuthor,
    GitCommit,
    GitInfo,
)
from fake_api_server_plugin.ci.surveillance.model.config.github import (
    GitHubInfo,
    PullRequestInfo,
)
from fake_api_server_plugin.ci.surveillance.model.config.subcmd_pull import (
    PullApiDocConfigArgs,
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
        cls, file_path: Union[str, Path], base_test_dir: Union[str, Path], accept_config_not_exist: str = "false"
    ) -> Dict[str, str]:
        surveillance = {}
        surveillance.update(cls.backend_project_info())
        surveillance.update(cls.git_operation_info())
        surveillance.update(cls.github_pr_info())
        surveillance.update(cls.subcmd_pull_args(file_path=file_path, base_test_dir=base_test_dir))
        surveillance.update(cls.action_operation(accept_config_not_exist=accept_config_not_exist))
        surveillance.update(fake_github_action_values.ci_env(cls.repo()))
        return surveillance

    @classmethod
    def surveillance_config_model(cls, file_path: Union[str, Path]) -> SurveillanceConfig:
        return SurveillanceConfig(
            server_type=Mock(),
            api_doc_url=Mock(),
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
            subcmd_pull_args=PullApiDocConfigArgs(
                config_path=str(file_path),
                include_template_config=True,
                base_file_path=str(file_path.parent) if isinstance(file_path, Path) else str(Path(file_path).parent),
                base_url="./",
                divide_api=True,
                divide_http=False,
                divide_http_request=False,
                divide_http_response=False,
                dry_run=True,
            ),
            accept_config_not_exist=False,
        )

    @classmethod
    def backend_project_info(cls) -> Dict[str, str]:
        return {
            # API documentation info
            EnvironmentVariableKey.API_DOC_URL.value: "http://127.0.0.1:8080",
            EnvironmentVariableKey.SERVER_TYPE.value: "rest-server",
        }

    @classmethod
    def git_operation_info(cls) -> Dict[str, str]:
        return {
            # git info
            EnvironmentVariableKey.GIT_REPOSITORY.value: cls.repo(),
            EnvironmentVariableKey.GIT_AUTHOR_NAME.value: "test-user[bot]",
            EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value: "test-bot@localhost.com",
            EnvironmentVariableKey.GIT_COMMIT_MSG.value: " 🧪 test commit message",
        }

    @classmethod
    def github_pr_info(cls) -> Dict[str, str]:
        return {
            # git info
            EnvironmentVariableKey.PR_TITLE.value: "✏️ Update the API configuration because API change.",
            EnvironmentVariableKey.PR_BODY.value: "Monitor the project and found changes. Update the configuration.",
            EnvironmentVariableKey.PR_IS_DRAFT.value: "true",
            EnvironmentVariableKey.PR_LABELS.value: "label1, label2",
        }

    @classmethod
    def subcmd_pull_args(cls, file_path: Union[str, Path], base_test_dir: Union[str, Path]) -> Dict[str, str]:
        return {
            # for subcommand line *pull* options
            EnvironmentVariableKey.CONFIG_PATH.value: str(file_path),
            EnvironmentVariableKey.INCLUDE_TEMPLATE_CONFIG.value: "True",
            EnvironmentVariableKey.BASE_FILE_PATH.value: str(base_test_dir),
            EnvironmentVariableKey.BASE_URL.value: "/test/v1",
            EnvironmentVariableKey.DIVIDE_API.value: "true",
            EnvironmentVariableKey.DIVIDE_HTTP.value: "false",
            EnvironmentVariableKey.DIVIDE_HTTP_REQUEST.value: "false",
            EnvironmentVariableKey.DIVIDE_HTTP_RESPONSE.value: "false",
            EnvironmentVariableKey.DRY_RUN.value: "true",
        }

    @classmethod
    def action_operation(cls, accept_config_not_exist: str = "false") -> Dict[str, str]:
        return {
            # operation with action in CI
            EnvironmentVariableKey.ACCEPT_CONFIG_NOT_EXIST.value: accept_config_not_exist,
        }
