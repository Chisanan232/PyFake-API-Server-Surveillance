import os
import pytest
from unittest.mock import patch, Mock

from fake_api_server_plugin.ci.surveillance.component.github_opt import GitHubOperation, RepoInitParam
from github import Github, Repository, PullRequest, GithubException


class TestGitHubOperationClass:

    @pytest.fixture(scope="function")
    def github_operation(self):
        operation = GitHubOperation()
        yield operation
        # Reset environment after each test
        operation._github = None
        operation._github_repo = None
        operation._repo_init_params = None

    def test_call_initializes_repo_params(self, github_operation: GitHubOperation):
        github_operation(repo_owner="test_owner", repo_name="test_repo")
        assert github_operation._repo_init_params == RepoInitParam(owner="test_owner", name="test_repo")

    def test_call_method(self, github_operation: GitHubOperation):
        """Test the __call__ method sets repo initialization parameters"""
        # gh_op = GitHubOperation()
        result = github_operation(repo_owner="test_owner", repo_name="test_repo")

        assert result._repo_init_params == RepoInitParam(owner="test_owner", name="test_repo")

    def test_connect_repo_success(self, github_operation: GitHubOperation):
        mock_github = Mock()
        mock_repo = Mock()
        github_operation._github = mock_github
        mock_github.get_repo.return_value = mock_repo

        github_operation.connect_repo("test_owner", "test_repo")
        mock_github.get_repo.assert_called_once_with("test_owner/test_repo")
        assert github_operation._github_repo is mock_repo

    def test_create_pull_request_success(self, github_operation: GitHubOperation):
        mock_github = Mock()
        mock_repo = Mock()
        mock_pr = Mock()
        mock_pr.html_url = "https://github.com/owner/repo/pull/1"
        github_operation._github = mock_github
        mock_github.get_repo.return_value = mock_repo
        mock_repo.create_pull.return_value = mock_pr

        with github_operation(repo_owner="test_owner", repo_name="test_repo"):
            pr = github_operation.create_pull_request(
                title="Test PR", body="Test body", base_branch="main", head_branch="feature"
            )
            assert pr is mock_pr
            mock_repo.create_pull.assert_called_once_with(
                title="Test PR", body="Test body", base="main", head="feature", draft=False
            )

    def test_create_pull_request_failure_no_repo(self, github_operation: GitHubOperation):
        with pytest.raises(RuntimeError):
            github_operation.create_pull_request(
                title="Test PR", body="Test body", base_branch="main", head_branch="feature"
            )

    def test_create_pull_request_github_exception(self, github_operation: GitHubOperation):
        mock_github = Mock()
        mock_repo = Mock()
        github_operation._github = mock_github
        mock_github.get_repo.return_value = mock_repo
        mock_repo.create_pull.side_effect = GithubException(404, "Not Found")

        with github_operation(repo_owner="test_owner", repo_name="test_repo"):
            pr = github_operation.create_pull_request(
                title="Test PR", body="Test body", base_branch="main", head_branch="feature"
            )
            assert pr is None

    def test_context_manager_connects_and_closes_repo(self, github_operation: GitHubOperation):
        mock_github = Mock()
        mock_repo = Mock()
        github_operation._github = mock_github
        mock_github.get_repo.return_value = mock_repo

        with github_operation(repo_owner="test_owner", repo_name="test_repo") as repo:
            assert repo is mock_repo
            mock_github.get_repo.assert_called_once_with("test_owner/test_repo")
        mock_github.close.assert_called_once()

    # Integration-like tests
    # @patch.dict(os.environ, {"GITHUB_TOKEN": "dummy_token"})
    # @patch("fake_api_server_plugin.ci.surveillance.component.github_opt.Github")
    # def test_integration_like_flow(self, mock_instantiate_github: Mock, github_operation: GitHubOperation):
    #     mock_github_instance = Mock()
    #     mock_github_get_repo_fun = Mock
    #     mock_repo_instance = Mock()
    #     mock_github_get_repo_fun.return_value = mock_repo_instance
    #     mock_pr_instance = Mock()
    #
    #     mock_instantiate_github.return_value = mock_github_instance
    #     mock_github_instance.get_repo.return_value = mock_repo_instance
    #     mock_repo_instance.create_pull.return_value = mock_pr_instance
    #     mock_pr_instance.html_url = "https://github.com/test_owner/test_repo/pull/123"
    #
    #     with github_operation(repo_owner="test_owner", repo_name="test_repo") as repo:
    #         pr = github_operation.create_pull_request(
    #             title="Integration Test PR",
    #             body="Integration Test Body",
    #             base_branch="main",
    #             head_branch="feature_branch",
    #         )
    #         assert pr.html_url == "https://github.com/test_owner/test_repo/pull/123"
    #         mock_github_instance.get_repo.assert_called_once_with("test_owner/test_repo")
    #         mock_repo_instance.create_pull.assert_called_once()
    #     mock_github_instance.close.assert_called_once()
