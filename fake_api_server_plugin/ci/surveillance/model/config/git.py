from dataclasses import dataclass
from typing import Mapping

from git import Actor

from .. import EnvironmentVariableKey
from .._base import _BaseModel


@dataclass
class GitAuthor(_BaseModel):
    name: str
    email: str

    @staticmethod
    def deserialize(data: Mapping) -> "GitAuthor":
        return GitAuthor(
            name=data[EnvironmentVariableKey.GIT_AUTHOR_NAME.value],
            email=data[EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value],
        )

    def serialize_for_git(self) -> Actor:
        return Actor(
            name=self.name,
            email=self.email,
        )


@dataclass
class GitCommit(_BaseModel):
    author: GitAuthor
    message: str

    @staticmethod
    def deserialize(data: Mapping) -> "GitCommit":
        return GitCommit(
            author=GitAuthor.deserialize(data.get(EnvironmentVariableKey.GIT_AUTHOR.value, {})),
            message=data[EnvironmentVariableKey.GIT_COMMIT_MSG.value],
        )


@dataclass
class GitInfo(_BaseModel):
    repository: str
    commit: GitCommit

    @staticmethod
    def deserialize(data: Mapping) -> "GitInfo":
        return GitInfo(
            repository=data[EnvironmentVariableKey.GIT_REPOSITORY.value],
            commit=GitCommit.deserialize(data.get(EnvironmentVariableKey.GIT_COMMIT.value, {})),
        )
