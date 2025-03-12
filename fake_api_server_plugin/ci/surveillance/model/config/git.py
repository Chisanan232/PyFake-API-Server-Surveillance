from dataclasses import dataclass
from typing import Mapping

from git import Actor

from .. import ConfigurationKey
from .._base import _BaseModel


@dataclass
class GitAuthor(_BaseModel):
    name: str
    email: str

    @staticmethod
    def deserialize(data: Mapping) -> "GitAuthor":
        return GitAuthor(
            name=data.get(ConfigurationKey.GIT_AUTHOR_NAME.value, "Fake-API-Server [bot]"),
            email=data.get(ConfigurationKey.GIT_AUTHOR_EMAIL.value, ""),
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
            author=GitAuthor.deserialize(data.get(ConfigurationKey.GIT_AUTHOR.value, {})),
            message=data.get(ConfigurationKey.GIT_COMMIT_MSG.value, "✏️ Update the API interface settings."),
        )


@dataclass
class GitInfo(_BaseModel):
    repository: str
    commit: GitCommit

    @staticmethod
    def deserialize(data: Mapping) -> "GitInfo":
        return GitInfo(
            repository=data[ConfigurationKey.GIT_REPOSITORY.value],
            commit=GitCommit.deserialize(data.get(ConfigurationKey.GIT_COMMIT.value, {})),
        )
