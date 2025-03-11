from dataclasses import dataclass, field
from typing import List, Mapping

from .. import EnvironmentVariableKey
from .._base import _BaseModel


@dataclass
class PullRequestInfo(_BaseModel):
    title: str = field(default_factory=str)
    body: str = field(default_factory=str)
    draft: bool = False
    labels: List[str] = field(default_factory=list)

    @staticmethod
    def deserialize(data: Mapping) -> "PullRequestInfo":
        return PullRequestInfo(
            title=data[EnvironmentVariableKey.PR_TITLE.value],
            body=data[EnvironmentVariableKey.PR_BODY.value],
            draft=data[EnvironmentVariableKey.PR_IS_DRAFT.value],
            labels=data[EnvironmentVariableKey.PR_LABELS.value],
        )


@dataclass
class GitHubInfo(_BaseModel):
    pull_request: PullRequestInfo

    @staticmethod
    def deserialize(data: Mapping) -> "GitHubInfo":
        return GitHubInfo(
            pull_request=PullRequestInfo.deserialize(data.get(EnvironmentVariableKey.GITHUB_PULL_REQUEST.value, {})),
        )
