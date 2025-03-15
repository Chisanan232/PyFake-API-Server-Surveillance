"""
This module provides functionality to manage and retrieve GitHub Actions environment variables.
It includes a dataclass `GitHubActionEnvironmentVariable` for deserialization and accessing relevant
environment variables that control repository configuration and authentication in GitHub Actions workflows.
"""

import ast
import os
from dataclasses import dataclass, field
from typing import Mapping, Optional

from .._base import _BaseModel


@dataclass
class GitHubActionEnvironmentVariable(_BaseModel):
    """
    Represents environment variables specific to a GitHub Action execution context.

    This class is used to define and process the environment variables related to GitHub Actions. It includes attributes
    to store details about the repository, branches, and authentication token. The purpose of this class is to manage
    and deserialize the environment data provided by GitHub Actions into a usable data object.

    :ivar github_actions: Indicates if the environment corresponds to a GitHub Action execution.
    :type github_actions: bool
    :ivar repository: The full repository name in the format 'owner/repo'.
    :type repository: str
    :ivar repository_owner_name: The owner name of the repository.
    :type repository_owner_name: str
    :ivar repository_name: The name of the repository.
    :type repository_name: str
    :ivar base_branch: The name of the base branch of the repository.
    :type base_branch: str
    :ivar head_branch: The name of the head branch of the repository.
    :type head_branch: str
    :ivar github_token: The authentication token provided for GitHub Actions.
    :type github_token: str
    """

    # the environment variable in github action
    github_actions: bool = False
    repository: str = field(default_factory=str)
    repository_owner_name: str = field(default_factory=str)
    repository_name: str = field(default_factory=str)
    base_branch: str = field(default_factory=str)
    head_branch: str = field(default_factory=str)

    # the environment variable in github action for authentication
    github_token: str = field(default_factory=str)

    @staticmethod
    def deserialize(data: Mapping) -> "GitHubActionEnvironmentVariable":
        github_repo = str(data["GITHUB_REPOSITORY"])
        github_repo_eles = github_repo.split("/")
        head_ref = data["GITHUB_HEAD_REF"] if data["GITHUB_EVENT_NAME"] == "pull_request" else data["GITHUB_REF"]
        return GitHubActionEnvironmentVariable(
            github_actions=ast.literal_eval(str(data.get("GITHUB_ACTIONS", "false")).capitalize()),
            repository=github_repo,
            repository_owner_name=github_repo_eles[0],
            repository_name=github_repo_eles[1],
            base_branch=data["GITHUB_BASE_REF"] or "master",
            head_branch=head_ref,
            github_token=data["GITHUB_TOKEN"],
        )


_Global_Environment_Var: Optional[GitHubActionEnvironmentVariable] = None


def get_github_action_env() -> GitHubActionEnvironmentVariable:
    """
    Gets the global GitHub action environment variable. This method ensures a
    singleton pattern for the GitHub action environment variable by reusing the
    previously deserialized value or deserializing the current operating system
    environment variables if it hasn't been initialized yet.

    :raises GitHubActionEnvironmentVariableError: If deserialization encounters an
        issue while processing the operating system's environment variables.
    :return: The GitHub action environment variable.
    :rtype: GitHubActionEnvironmentVariable
    """
    global _Global_Environment_Var
    if _Global_Environment_Var is None:
        _Global_Environment_Var = GitHubActionEnvironmentVariable.deserialize(os.environ)
    return _Global_Environment_Var
