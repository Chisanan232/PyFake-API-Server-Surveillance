"""
This module provides functionality to interact with GitHub repositories using the PyGithub library.
It facilitates operations such as connecting to a repository, retrieving labels, and creating pull requests,
while also utilizing Python context management for ease of use.
"""

import logging
import os
import traceback
from collections import namedtuple
from typing import List, Optional

from github import Github, GithubException, Repository
from github.Label import Label
from github.PullRequest import PullRequest

logger = logging.getLogger(__name__)

"""Define the data structure for storing repository initialization parameters."""
RepoInitParam = namedtuple("RepoInitParam", ("owner", "name"))


class GitHubOperation:
    """
    Handles operations related to GitHub repositories including connecting to a
    repository, managing labels, and creating pull requests.

    This class is designed to interact with GitHub repositories using the official
    `PyGithub` library. It provides utility methods to facilitate repository
    connectivity and certain operations like fetching labels and creating pull
    requests. It also implements context manager protocol for clean resource
    handling and initialization of repositories.

    :ivar _github: An instance of the `Github` class initialized with the
        authentication token from environment variables.
    :type _github: Github
    :ivar _github_repo: An optional reference to the connected GitHub repository.
    :type _github_repo: Optional[Repository]
    :ivar _repo_init_params: Stores repository initialization parameters during
        the repository connection process.
    :type _repo_init_params: Optional[RepoInitParam]
    :ivar _repo_all_labels: A list of all labels available in the connected
        repository.
    :type _repo_all_labels: List[Label]
    """

    def __init__(self):
        self._github = Github(os.environ.get("GITHUB_TOKEN"))
        self._github_repo: Optional[Repository] = None

        self._repo_init_params: Optional[RepoInitParam] = None
        self._repo_all_labels: List[Label] = []

    def __call__(self, **kwargs):
        self._repo_init_params = RepoInitParam(
            owner=kwargs["repo_owner"],
            name=kwargs["repo_name"],
        )
        return self

    def __enter__(self) -> Repository:
        assert self._repo_init_params
        self.connect_repo(self._repo_init_params.owner, self._repo_init_params.name)
        assert self._github_repo
        return self._github_repo

    def __exit__(self, *args):
        self._github.close()

    def connect_repo(self, repo_owner: str, repo_name: str) -> None:
        """
        Connects to a GitHub repository and initializes its labels.

        This function takes the owner and name of a GitHub repository, connects to
        the repository using the GitHub API client, and retrieves all existing
        labels for later processing.

        :param repo_owner: The username or organization name of the repository
            owner.
        :type repo_owner: str
        :param repo_name: The name of the repository to connect to.
        :type repo_name: str
        :return: None
        :rtype: None
        """
        self._github_repo = self._github.get_repo(f"{repo_owner}/{repo_name}")
        self._repo_all_labels = self._get_all_labels()

    def _get_all_labels(self) -> List[Label]:
        """
        Retrieves all labels associated with the connected GitHub repository.

        This method fetches all the labels available in the currently connected
        GitHub repository. If the repository connection is not established prior
        to calling this method, it raises a runtime error.

        :raises RuntimeError: If the GitHub repository is not connected.

        :return: A list of all labels from the GitHub repository.
        :rtype: List[Label]
        """
        if not self._github_repo:
            raise RuntimeError("Please connect to target GitHub repository first before get all labels.")
        return self._github_repo.get_labels()

    def create_pull_request(
        self, title: str, body: str, base_branch: str, head_branch: str, draft: bool = False, labels: List[str] = []
    ) -> Optional[PullRequest]:
        """
        Creates a pull request in the connected GitHub repository. This method initializes and creates a new pull
        request with the specified details, including title, description, base and head branches, draft status,
        and labels. If successful, the new pull request is returned; otherwise, logs the failure and returns None.

        :param title: The title of the pull request.
        :type title: str
        :param body: The description or body of the pull request.
        :type body: str
        :param base_branch: The name of the branch to merge into (base branch).
        :type base_branch: str
        :param head_branch: The name of the branch to merge from (head branch).
        :type head_branch: str
        :param draft: Indicates whether the pull request is to be created as a draft. Default is False.
        :type draft: bool, optional
        :param labels: A list of label names to attach to the pull request. Default is an empty list.
        :type labels: List[str], optional
        :return: The created pull request object if successful, otherwise None.
        :rtype: Optional[PullRequest]
        :raises RuntimeError: If a connection to the target GitHub repository has not been established.
        """
        if not self._github_repo:
            raise RuntimeError("Please connect to target GitHub repository first before create pull request.")
        try:
            pr = self._github_repo.create_pull(
                title=title,
                body=body,
                base=base_branch,
                head=head_branch,
                draft=draft,
            )
            for l in labels:
                label = tuple(filter(lambda _l: _l.name == l, self._repo_all_labels))
                if label:
                    pr.add_to_labels(*label)

            logger.info(f"Pull request created: {pr.html_url}")
            return pr
        except GithubException:
            logger.error("Fail to do something in GitHub. Please check it. Error message:")
            traceback.print_exc()
            return None
