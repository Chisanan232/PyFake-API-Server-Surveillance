import ast
import os
from dataclasses import dataclass, field
from typing import Mapping

from ci.surveillance.model._base import _BaseModel


@dataclass
class GitHubActionEnvironmentVariable(_BaseModel):
    # the environment variable in github action
    github_actions: str = field(default_factory=str)
    base_branch: str = field(default_factory=str)
    head_branch: str = field(default_factory=str)

    # the environment variable in github action for authentication
    github_token: str = field(default_factory=str)

    @staticmethod
    def deserialize(data: Mapping) -> "GitHubActionEnvironmentVariable":
        return GitHubActionEnvironmentVariable(
            github_actions=ast.literal_eval(str(data.get("GITHUB_ACTIONS", "false")).capitalize()),
            base_branch=data.get("GITHUB_BASE_REF", "master"),
            head_branch=data["GITHUB_HEAD_REF"],
            github_token=data["GITHUB_TOKEN"],
        )


_Global_Environment_Var: GitHubActionEnvironmentVariable = GitHubActionEnvironmentVariable.deserialize(os.environ)


def get_github_action_env() -> GitHubActionEnvironmentVariable:
    return _Global_Environment_Var
