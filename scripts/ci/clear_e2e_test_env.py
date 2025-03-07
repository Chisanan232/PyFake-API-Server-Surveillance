import os
import re
from typing import List, Optional

from git import Repo
from github import Github
from github.PullRequest import PullRequest


class NotFoundTargetGitBranch(RuntimeError):
    def __init__(self, branch: str, current_all_branches: List[str]):
        self._target_branch = branch
        self._current_all_branches = current_all_branches

    def __str__(self):
        return f"Cannot find the target git branch *{self._target_branch}*. Current all branches: {self._current_all_branches}."


REPO: Optional[Repo] = None
GITHUB: Optional[Github] = None


def init_git() -> None:
    global REPO
    REPO = Repo("./")


def get_all_branch() -> List[str]:
    return [ref.name for ref in REPO.refs]  # type: ignore[union-attr]


def expect_branch_name() -> str:
    github_action_event_name = os.environ["GITHUB_EVENT_NAME"]
    print(f"[DEBUG] GitHub event name: {github_action_event_name}")
    github_action_job_id = os.environ["GITHUB_JOB"]
    print(f"[DEBUG] GitHub run ID: {github_action_job_id}")
    return f"fake-api-server-monitor-update-config_{github_action_event_name}_{github_action_job_id}"


def search_branch(name: str, all_branch: List[str]) -> str:
    for branch in all_branch:
        if re.search(re.escape(name), str(branch), re.IGNORECASE):
            return branch.replace("origin/", "")
    raise NotFoundTargetGitBranch(name, all_branch)


def delete_remote_branch(name: str) -> None:
    REPO.git.push("origin", "--delete", name)  # type: ignore[union-attr]


def init_github() -> None:
    global GITHUB
    GITHUB = Github(os.environ["GITHUB_TOKEN"])


def search_github_repo_pr(head_branch: str) -> PullRequest:
    prs = GITHUB.get_repo(os.environ["GITHUB_REPOSITORY"]).get_pulls(
        state="open",
        sort="created",
        base=os.environ["GITHUB_BASE_REF"] or "master",
        head=head_branch,
    )
    assert prs.totalCount == 1, "Should only have one PR for the target branch."
    return prs[0]


def delete_github_repo_pr(pr: PullRequest) -> None:
    pr.edit(state="closed")
    print(f"Pull request #{pr.number} closed successfully.")


def run() -> None:
    init_git()
    all_branch = get_all_branch()
    print(f"[DEBUG] All git branch: {all_branch}")
    e2e_test_branch = search_branch(name=expect_branch_name(), all_branch=all_branch)
    print(f"[DEBUG] Target branch: {e2e_test_branch}")

    init_github()
    pr = search_github_repo_pr(e2e_test_branch)
    try:
        delete_github_repo_pr(pr)
    except Exception as e:
        raise e
    finally:
        delete_remote_branch(e2e_test_branch)


if __name__ == "__main__":
    run()
