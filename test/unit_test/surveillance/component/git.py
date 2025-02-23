import os
from unittest.mock import patch

import pytest

from ci.surveillance.component.git import GitOperation

# isort: off
from test._values._test_data import fake_data, fake_github_action_values
# isort: on


class TestGitOperation:
    @pytest.fixture(scope="module")
    def git_operation(self) -> GitOperation:
        return GitOperation()

    @pytest.mark.parametrize(
        ("ci_test_mode", "expect_git_branch"),
        [
            ("false", "fake-api-server-monitor-update-config"),
            ("true", "fake-api-server-monitor-update-config_<event_name>_<job_id>"),
        ],
    )
    def test_fake_api_server_monitor_git_branch(self, git_operation: GitOperation, ci_test_mode: str, expect_git_branch: str):
        dummy_ci_env = fake_github_action_values.ci_env(fake_data.repo())
        dummy_ci_env["CI_TEST_MODE"] = ci_test_mode
        with patch.dict(os.environ, dummy_ci_env, clear=True):
            fake_api_server_git_branch = git_operation.fake_api_server_monitor_git_branch
        if ci_test_mode:
            expect_git_branch = expect_git_branch.replace("<event_name>", dummy_ci_env["GITHUB_EVENT_NAME"]).replace("<job_id>", dummy_ci_env["GITHUB_JOB"])
        assert fake_api_server_git_branch == expect_git_branch
