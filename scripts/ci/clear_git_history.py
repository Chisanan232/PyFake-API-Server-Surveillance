import os
import re
from enum import Enum
from typing import Iterator, Optional

from fake_api_server.ci.surveillance.model import EnvironmentVariableKey
from git import Commit, GitCommandError, Repo

_SEARCH_GIT_COMMIT_COUNT: int = os.environ.get("SEARCH_GIT_COMMIT_COUNT", 5)
_GIT_COMMITTER: str = os.environ[EnvironmentVariableKey.GIT_AUTHOR_NAME.value]
_GIT_COMMIT_MSG: str = os.environ[EnvironmentVariableKey.GIT_COMMIT_MSG.value]


repo = Repo("./")


def display_current_commits() -> None:
    commits: Iterator[Commit] = repo.iter_commits(max_count=_SEARCH_GIT_COMMIT_COUNT)
    for commit in commits:
        print(f"[DEBUG] +------------------------------------------+")
        print(f"[DEBUG] commit author.name: {commit.author.name}")
        print(f"[DEBUG] commit author.email: {commit.author.email}")
        print(f"[DEBUG] commit message: {commit.message}")
        print(f"[DEBUG] commit hexsha: {commit.hexsha}")
        print(f"[DEBUG] commit datetime: {commit.committed_datetime}")
    print(f"[DEBUG] +------------------------------------------+")


def find_tes_commit() -> Optional[Commit]:
    commits: Iterator[Commit] = repo.iter_commits(max_count=_SEARCH_GIT_COMMIT_COUNT)
    for commit in commits:
        if re.search(re.escape(_GIT_COMMITTER), str(commit.author.name)) and re.search(
            re.escape(_GIT_COMMIT_MSG), str(commit.message), re.IGNORECASE
        ):
            print("[DEBUG] Found commit.")
            return commit
    print("[WARN] No commit found, pass it.")
    return None


class RemoveCommitMethod(Enum):
    RESET = "reset"
    REVERT = "revert"
    REBASE = "rebase"


def remove_commit(method: RemoveCommitMethod, commit_hash: str) -> None:
    try:
        if method == "reset":
            # Hard reset to the commit before the one we want to remove
            repo.git.reset("--hard", f"{commit_hash}^")
            print(f"Successfully reset to commit before {commit_hash}")

        elif method == "revert":
            # Create a new commit that undoes the specified commit
            repo.git.revert(commit_hash)
            print(f"Successfully reverted commit {commit_hash}")

        elif method == "rebase":
            # Remove the commit while keeping subsequent changes
            try:
                repo.git.rebase("-i", f"{commit_hash}^")
                print(f"Started interactive rebase to remove commit {commit_hash}")
            except GitCommandError:
                print("Interactive rebase requires manual intervention")
                print("Please complete the rebase in your Git interface")

    except GitCommandError as e:
        print(f"Git operation failed: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    print("[DEBUG] Before running remove commit history.")
    display_current_commits()
    commit = find_tes_commit()
    if commit:
        remove_commit(method=RemoveCommitMethod.REVERT, commit_hash=commit.hexsha)
    print("[DEBUG] After running remove commit history.")
    display_current_commits()
