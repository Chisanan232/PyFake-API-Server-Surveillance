"""
This module provides classes and methods for managing and deserializing
GitHub-related data structures, including pull requests and their associated information.
"""

import os.path
import pathlib
from dataclasses import dataclass, field
from typing import List, Mapping

try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod  # type: ignore[no-redef]

from .. import ConfigurationKey
from .._base import _BaseModel
from ..compare import ChangeDetail


@dataclass
class PullRequestInfo(_BaseModel):
    """
    Represents information related to a pull request, including metadata such as title, body, labels,
    and draft status, as well as details of the changes it encompasses.

    This class encapsulates details of a pull request, such as its title, body description, whether
    it be marked as a draft or not, and associated labels. It can be used for creating or processing
    pull requests programmatically. The `deserialize` method allows reconstructing an instance of this
    class from a dictionary-like mapping, supporting specific use cases related to mappings and
    configuration items.

    :ivar title: The title of the pull request.
    :type title: str
    :ivar body: The body content of the pull request.
    :type body: str
    :ivar draft: Indicates if the pull request is marked as a draft.
    :type draft: bool
    :ivar labels: List of labels associated with the pull request.
    :type labels: List[str]
    :ivar change_detail: An object containing statistical and summary details of API changes. This property is new in version 0.2.0.
    :type change_detail: ChangeDetail
    """

    title: str = field(default_factory=str)
    body: str = field(default_factory=str)
    draft: bool = False
    labels: List[str] = field(default_factory=list)
    change_detail: ChangeDetail = field(default_factory=ChangeDetail)

    _NO_API_CHANGE_CONTENT: str = "No changes."

    @classmethod
    def default_pr_body(cls) -> str:
        """
        Generates and returns a default pull request body from a file.

        This method reads the content of a Markdown file named `pr-body.md` located within
        a `_static` directory inside the `surveillance` directory of the project's
        file system structure. The `_find_surveillance_lib_path` helper function navigates
        through the file path hierarchy to locate the `surveillance` directory. If the
        `pr-body.md` file is not found in the expected path, an assertion is raised.

        The returned content of the file can be used as a template for pull request bodies.

        !!! tip ""

            This function is new in version 0.2.0.

        :raises AssertionError: If the default pull request body file (`pr-body.md`) is
                                not found at the expected path.

        :return: The content of the `pr-body.md` file as a string representing
                 the default pull request body.
        :rtype: str
        """

        def _find_surveillance_lib_path(_path: pathlib.Path) -> pathlib.Path:
            if _path.name == "surveillance":
                return _path
            return _find_surveillance_lib_path(_path.parent)

        surveillance = _find_surveillance_lib_path(pathlib.Path(os.path.abspath(__file__)))
        default_pr_body_md_file = pathlib.Path(surveillance, "_static", "pr-body.md")
        assert os.path.exists(default_pr_body_md_file), "Default PR body file not found."
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

    def set_change_detail(self, change_detail: ChangeDetail) -> None:
        """
        Updates the body of the content based on the provided change details, altering it to
        reflect the statistical changes and API summary. Existing placeholders in the body
        are replaced with the relevant information derived from the `change_detail` object.

        !!! tip ""

            This function is new in version 0.2.0.

        :param change_detail: Contains statistical and summary details of API changes that are
            used to update the body content.
        :type change_detail: ChangeDetail

        :return: None
        """
        new_body = self.body

        # Process the details - statistics
        new_body = new_body.replace("{{ NEW_API_NUMBER }}", str(change_detail.statistical.add))
        new_body = new_body.replace("{{ CHANGE_API_NUMBER }}", str(change_detail.statistical.update))
        new_body = new_body.replace("{{ DELETE_API_NUMBER }}", str(change_detail.statistical.delete))

        # Process the details - summary
        for api_path, api_methods in change_detail.summary.add.items():
            new_body = new_body.replace("{{ ADD_API_SUMMARY }}", self._api_change_list(api_path, api_methods))
        for api_path, api_methods in change_detail.summary.update.items():
            new_body = new_body.replace("{{ CHANGE_API_SUMMARY }}", self._api_change_list(api_path, api_methods))
        for api_path, api_methods in change_detail.summary.delete.items():
            new_body = new_body.replace("{{ DELETE_API_SUMMARY }}", self._api_change_list(api_path, api_methods))

        new_body = new_body.replace("{{ ADD_API_SUMMARY }}", self._NO_API_CHANGE_CONTENT)
        new_body = new_body.replace("{{ CHANGE_API_SUMMARY }}", self._NO_API_CHANGE_CONTENT)
        new_body = new_body.replace("{{ DELETE_API_SUMMARY }}", self._NO_API_CHANGE_CONTENT)

        self.body = new_body

    def _api_change_list(self, path: str, methods: List[HTTPMethod]) -> str:
        api_change_summary = f"* `{path}` \n"
        for method in methods:
            api_change_summary += f"  * `{method.name}` \n"
        return api_change_summary


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
