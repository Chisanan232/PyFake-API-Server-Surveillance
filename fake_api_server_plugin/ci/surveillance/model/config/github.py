"""
This module provides classes and methods for managing and deserializing
GitHub-related data structures, including pull requests and their associated information.
"""

import os.path
import pathlib
from dataclasses import dataclass, field
from typing import List, Mapping

from .. import ConfigurationKey
from .._base import _BaseModel


@dataclass
class PullRequestInfo(_BaseModel):
    """
    Represents information about a pull request.

    This class encapsulates details of a pull request, such as its title, body description, whether
    it is a draft or not, and associated labels. It can be used for creating or processing pull
    requests programmatically. The `deserialize` method allows reconstructing an instance of this
    class from a dictionary-like mapping, supporting specific use cases related to mappings and
    configuration items.

    :ivar title: The title of the pull request.
    :type title: str
    :ivar body: The body description of the pull request, providing further context.
    :type body: str
    :ivar draft: Indicates if the pull request is a draft.
    :type draft: bool
    :ivar labels: A list of labels associated with the pull request.
    :type labels: List[str]
    """

    title: str = field(default_factory=str)
    body: str = field(default_factory=str)
    draft: bool = False
    labels: List[str] = field(default_factory=list)

    @classmethod
    def default_pr_body(cls) -> str:

        def _find_surveillance_lib_path(_path: pathlib.Path) -> pathlib.Path:
            if _path.name == "surveillance":
                return _path
            return _find_surveillance_lib_path(_path.parent)

        surveillance = _find_surveillance_lib_path(pathlib.Path(os.path.abspath(__file__)))
        default_pr_body_md_file = pathlib.Path(surveillance, "_static", "pr-body-default.md")
        assert default_pr_body_md_file.exists(), "Default PR body file not found."
        with open(str(default_pr_body_md_file), "r") as file_stream:
            return file_stream.read()

    @classmethod
    def deserialize(cls, data: Mapping) -> "PullRequestInfo":
        return PullRequestInfo(
            title=data.get(
                ConfigurationKey.PR_TITLE.value,
                "🤖✏️ Update Fake-API-Server configuration because of API changes.",
            ),
            body=data.get(ConfigurationKey.PR_BODY.value, cls.default_pr_body()),
            draft=data.get(ConfigurationKey.PR_IS_DRAFT.value, False),
            labels=data.get(ConfigurationKey.PR_LABELS.value, []),
        )


@dataclass
class GitHubInfo(_BaseModel):
    """
    Represents GitHub-related information within a system model.

    This class encapsulates the GitHub-related information, including details
    about pull requests. It provides a method to deserialize data from a
    mapping structure into an instance of the class for further use.

    :ivar pull_request: Encapsulates the details of a GitHub pull request.
    :type pull_request: PullRequestInfo
    """

    pull_request: PullRequestInfo

    @staticmethod
    def deserialize(data: Mapping) -> "GitHubInfo":
        return GitHubInfo(
            pull_request=PullRequestInfo.deserialize(data.get(ConfigurationKey.GITHUB_PULL_REQUEST.value, {})),
        )
