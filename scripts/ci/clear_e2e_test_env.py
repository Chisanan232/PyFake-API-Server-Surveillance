import re
from typing import Optional, List

from git import Repo


class NotFoundTargetGitBranch(RuntimeError):
    def __init__(self, branch: str, current_all_branches: List[str]):
        self._target_branch = branch
        self._current_all_branches = current_all_branches

    def __str__(self):
        return f"Cannot find the target git branch *{self._target_branch}*. Current all branches: {self._current_all_branches}."


REPO: Optional[Repo] = None


def init_git() -> None:
    global REPO
    REPO = Repo("./")


def get_all_branch() -> List[str]:
    return [ref.name for ref in REPO.refs]


def search_branch(name: str, all_branch: List[str]) -> str:
    for branch in all_branch:
        if re.search(r"", str(branch), re.IGNORECASE):
            return branch
    raise NotFoundTargetGitBranch(name, all_branch)


def delete_remote_branch(name: str) -> None:
    REPO.git.push("origin", "--delete", name)


def run() -> None:
    init_git()
    all_branch = get_all_branch()
    e2e_test_branch = search_branch(name="fake-api-server-monitor-update-config", all_branch=all_branch)
    delete_remote_branch(e2e_test_branch)


if __name__ == '__main__':
    run()
