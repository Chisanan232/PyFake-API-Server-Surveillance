from dataclasses import dataclass, field
from typing import Mapping

from . import EnvironmentVariableKey
from ._base import _BaseModel


@dataclass
class PullRequestInfo(_BaseModel):
    title: str = field(default_factory=str)
    body: str = field(default_factory=str)
    draft: bool = False

    @staticmethod
    def deserialize(data: Mapping) -> "PullRequestInfo":
        return PullRequestInfo(
            title=data[EnvironmentVariableKey.PR_TITLE.value],
            body=data[EnvironmentVariableKey.PR_BODY.value],
            draft=data[EnvironmentVariableKey.PR_IS_DRAFT.value],
        )


@dataclass
class GitHubInfo(_BaseModel):
    pull_request: PullRequestInfo

    @staticmethod
    def deserialize(data: Mapping) -> "GitHubInfo":
        return GitHubInfo(
            pull_request=PullRequestInfo.deserialize(data),
        )
