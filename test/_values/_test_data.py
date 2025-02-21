from pathlib import Path
from typing import Dict, Type, Union

from ci.surveillance.model import EnvironmentVariableKey



class fake_github_action_env:
    @classmethod
    def action_run_id(cls) -> str:
        return "123456"


class fake_git_data:
    @classmethod
    def default_branch(cls) -> str:
        return "origin"

    @classmethod
    def fake_api_server_monitor_branch(cls) -> str:
        return f"fake-api-server-monitor-update-config_{fake_github_action_env.action_run_id()}"


class fake_data:
    @classmethod
    def repo(cls) -> str:
        return "Chisanan232/Sample-Python-BackEnd"

    @classmethod
    def action_input(cls, file_path: Union[str, Path], base_test_dir: Union[str, Path]) -> Dict[str, str]:
        return {
            # API documentation info
            EnvironmentVariableKey.API_DOC_URL.value: "http://127.0.0.1:8080",
            EnvironmentVariableKey.SERVER_TYPE.value: "rest-server",
            # git info
            EnvironmentVariableKey.GIT_REPOSITORY.value: cls.repo(),
            EnvironmentVariableKey.GIT_AUTHOR_NAME.value: "test-user[bot]",
            EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value: "test-bot@localhost.com",
            EnvironmentVariableKey.GIT_COMMIT_MSG.value: " 🧪 test commit message",
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
            # operation with action in CI
            EnvironmentVariableKey.ACCEPT_CONFIG_NOT_EXIST.value: "false",
            # GitHub action environment
            "GITHUB_TOKEN": "ghp_1234567890",
            "GITHUB_REPOSITORY": cls.repo(),
            "GITHUB_HEAD_REF": "git-branch",
            "GITHUB_RUN_ID": fake_github_action_env.action_run_id(),
        }
