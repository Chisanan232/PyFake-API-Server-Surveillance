import os
from collections import namedtuple
from typing import List, Optional

from github import Github, GithubException, Repository
from github.Label import Label
from github.PullRequest import PullRequest

RepoInitParam = namedtuple("RepoInitParam", ("owner", "name"))


class GitHubOperation:

    def __init__(self):
        self._github = Github(os.environ.get("GITHUB_TOKEN"))
        self._github_repo: Optional[Repository] = None

        self._repo_init_params: Optional[RepoInitParam] = None
        self._repo_all_labels: List[Label] = []

    def __call__(self, **kwargs):
        # assert self._check_params(**kwargs)
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
        self._github_repo = self._github.get_repo(f"{repo_owner}/{repo_name}")
        self._repo_all_labels = self._get_all_labels()

    def _get_all_labels(self) -> List[Label]:
        if not self._github_repo:
            raise RuntimeError("Please connect to target GitHub repository first before get all labels.")
        return self._github_repo.get_labels()

    def create_pull_request(
        self, title: str, body: str, base_branch: str, head_branch: str, draft: bool = False, labels: List[str] = []
    ) -> Optional[PullRequest]:
        if not self._github_repo:
            raise RuntimeError("Please connect to target GitHub repository first before create pull request.")
        try:
            print(f"[DEBUG] base_branch: {base_branch}")
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

            print(f"Pull request created: {pr.html_url}")
            return pr
        except GithubException as e:
            print(f"[ERROR] e: {e}")
            return None
