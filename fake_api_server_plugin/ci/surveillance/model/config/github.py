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
            title=data.get(EnvironmentVariableKey.PR_TITLE.value, "🤖✏️ Update Fake-API-Server configuration because of API changes."),
            body=data.get(EnvironmentVariableKey.PR_BODY.value, "Update Fake-API-Server configuration."),
            draft=data.get(EnvironmentVariableKey.PR_IS_DRAFT.value, False),
            labels=data.get(EnvironmentVariableKey.PR_LABELS.value, []),
        )


@dataclass
class GitHubInfo(_BaseModel):
    pull_request: PullRequestInfo

    @staticmethod
    def deserialize(data: Mapping) -> "GitHubInfo":
        return GitHubInfo(
            pull_request=PullRequestInfo.deserialize(data.get(EnvironmentVariableKey.GITHUB_PULL_REQUEST.value, {})),
        )
