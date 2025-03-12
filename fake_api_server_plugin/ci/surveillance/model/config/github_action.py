import ast
import os
from dataclasses import dataclass, field
from typing import Mapping, Optional

from .._base import _BaseModel


@dataclass
class GitHubActionEnvironmentVariable(_BaseModel):
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
        print(f"[DEBUG] head_ref: {head_ref}")
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
    global _Global_Environment_Var
    if _Global_Environment_Var is None:
        _Global_Environment_Var = GitHubActionEnvironmentVariable.deserialize(os.environ)
    return _Global_Environment_Var
