"""
This module defines data models and serialization logic for Git-related objects,
including authors, commits, and repository information, allowing interoperation
with Git operations such as deserialization and git actor representation.
"""

import os
from dataclasses import dataclass
from typing import Mapping

from git import Actor

from .. import ConfigurationKey
from .._base import _BaseModel


@dataclass
class GitAuthor(_BaseModel):
    """
    Represents a Git author, including their name and email.

    This class models the essential properties and behaviors of a Git author, allowing
    for serialization and deserialization operations. It is typically used to handle
    information related to authors of Git commits, including their name and email
    address.

    :ivar name: The name of the Git author.
    :type name: str
    :ivar email: The email address of the Git author.
    :type email: str
    """

    name: str
    email: str

    @staticmethod
    def deserialize(data: Mapping) -> "GitAuthor":
        return GitAuthor(
            name=data.get(ConfigurationKey.GIT_AUTHOR_NAME.value, "Fake-API-Server [bot]"),
            email=data.get(ConfigurationKey.GIT_AUTHOR_EMAIL.value, ""),
        )

    def serialize_for_git(self) -> Actor:
        """
        Serializes the current object into a format suitable for Git.

        This method constructs and returns an instance of the `Actor` class
        using the name and email attributes of the current object. The
        serialization ensures that the resulting `Actor` object reflects the
        name and email parameters of the current instance. This can be used
        to represent user or committer details for Git-related operations.

        :return: An `Actor` object containing the serialized name and email
            of the current object.
        :rtype: Actor
        """
        return Actor(
            name=self.name,
            email=self.email,
        )


@dataclass
class GitCommit(_BaseModel):
    """
    Represents a Git commit with details about the author and commit message.

    This class is used to store and handle information related to a specific
    Git commit, including the metadata about the author and the commit message.

    :ivar author: Information about the author of the commit.
    :type author: GitAuthor
    :ivar message: The message associated with the commit.
    :type message: str
    """

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
    """
    Represents information about a Git repository and its latest commit.

    This class encapsulates details about a Git repository, including its
    repository URL or identifier and associated commit metadata. It provides
    support for deserializing data into a `GitInfo` object.

    :ivar repository: The URL or identifier of the Git repository.
    :type repository: str
    :ivar commit: Metadata of the commit associated with the repository.
    :type commit: GitCommit
    """

    repository: str
    commit: GitCommit

    @staticmethod
    def deserialize(data: Mapping) -> "GitInfo":
        return GitInfo(
            repository=data.get(ConfigurationKey.GIT_REPOSITORY.value, os.environ["GITHUB_REPOSITORY"]),
            commit=GitCommit.deserialize(data.get(ConfigurationKey.GIT_COMMIT.value, {})),
        )
