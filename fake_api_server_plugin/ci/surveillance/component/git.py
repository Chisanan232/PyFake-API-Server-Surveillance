"""
This module provides the GitOperation class, enabling various git operations such as
branch management, file staging, committing, pushing, and remote repository setup.

The module also contains methods to handle specific CI/CD-related functionality,
including automated branch switching and version control integration to sync and manage
fake API server configurations.
"""

import ast
import logging
import os
from pathlib import Path
from typing import Optional, Set, Union, cast

from fake_api_server.command.subcommand import SubCommandLine
from git import Commit, Remote, Repo

from ..model.config import PullApiDocConfigArgs, SurveillanceConfig

logger = logging.getLogger(__name__)


class GitOperation:
    """
    Manages Git operations specifically designed for handling code changes and versioning
    in a configuration-based system. This class provides utility methods for initializing
    Git repositories, managing branches, handling file additions, committing changes,
    and pushing to remote repositories, making it suitable for CI/CD environments with
    automated workflows.

    :ivar _git_repo: Represents the Git repository instance used for various Git operations.
    :type _git_repo: Optional[Repo]
    :ivar _all_staged_files: A set of file paths that have been staged and added to the Git index.
    :type _all_staged_files: Set[str]
    """

    def __init__(self):
        self._git_repo: Optional[Repo] = None
        self._all_staged_files: Set[str] = set()

    @property
    def repository(self) -> Repo:
        """
        Provides access to the repository instance that is internally stored. Ensures
        that the repository instance is not accessed until it has been properly
        initialized.

        :raises AssertionError: If the repository instance (_git_repo) is not set.
        :return: The repository instance.
        :rtype: Repo
        """
        assert self._git_repo is not None, "Should set the repository instance before using it."
        return self._git_repo

    @repository.setter
    def repository(self, repo: Repo) -> None:
        assert repo is not None, "Should not set the repository as empty."
        self._git_repo = repo

    @property
    def is_in_ci_env(self) -> bool:
        """
        Determine if the code is running in a Continuous Integration (CI) environment.

        This method evaluates environment variables to determine if the script is
        running in a CI environment such as GitHub Actions.

        :return: A boolean indicating whether the script is running in a CI environment.
        :rtype: bool
        """
        return ast.literal_eval(str(os.getenv("GITHUB_ACTIONS", "false")).capitalize())

    @property
    def is_ci_test_mode(self) -> bool:
        """
        Checks whether the application is running in CI test mode.

        This property reads an environment variable ``CI_TEST_MODE`` and determines
        if the application is operating in a continuous integration test mode. The
        value is parsed as a string, capitalized, evaluated as a Python literal,
        and defaults to ``False`` if the variable is not set.

        :return: Boolean indicating if the application is in CI test mode.
        :rtype: bool
        """
        return ast.literal_eval(str(os.getenv("CI_TEST_MODE", "false")).capitalize())

    @property
    def fake_api_server_monitor_git_branch(self) -> str:
        """
        Determines the Git branch name to use for the fake API server monitor configuration
        updates based on the environment. In CI test mode, it creates a branch name
        specific to the GitHub Action's event and job ID. In other cases, it uses a
        default branch name.

        :raises KeyError: If ``GITHUB_EVENT_NAME`` or ``GITHUB_JOB`` is missing in
                          the environment variables (only applicable in CI test mode).
        :return: The Git branch name for fake API server monitor configuration updates.
        :rtype: str
        """
        if self.is_ci_test_mode:
            github_action_event_name = os.environ["GITHUB_EVENT_NAME"]
            github_action_job_id = os.environ["GITHUB_JOB"]
            git_ref: str = f"fake-api-server-monitor-update-config_{github_action_event_name}_{github_action_job_id}"
        else:
            git_ref: str = "fake-api-server-monitor-update-config"  # type: ignore[no-redef]
        return git_ref

    @property
    def default_remote_name(self) -> str:
        """
        Provides the default remote name used for remote operations.

        :return: The default remote name string.
        :rtype: str
        """
        return "origin"

    @property
    def _current_git_branch(self) -> str:
        """
        Get the name of the current active Git branch.

        This method attempts to retrieve the name of the current active branch
        from the Git repository associated with the object. If the repository
        is in a detached HEAD state and running in a CI environment, it falls
        back to an environment variable to determine the branch name.

        :raises TypeError: If an exception is raised and the issue cannot be handled
            (other than the detached HEAD state in CI environments).

        :return: Name of the current active Git branch, or an environment variable
            value if in CI with detached HEAD state.
        :rtype: str
        """
        try:
            current_git_branch = self.repository.active_branch.name
        except TypeError as e:
            # NOTE: Only for CI runtime environment
            logger.error("Occur something wrong when trying to get git branch.")
            if "HEAD" in str(e) and "detached" in str(e) and self.is_in_ci_env:
                current_git_branch = os.getenv("GITHUB_REF", "")
            else:
                raise e
        return current_git_branch

    def _reset_all_staged_files(self) -> None:
        """
        Resets all staged files by clearing the internal list that holds file references.

        This method ensures that all previously staged files for operation are removed
        and the internal state is reset.

        :return: None
        """
        self._all_staged_files.clear()

    def version_change(self, surveillance_config: SurveillanceConfig) -> bool:
        """
        Update and synchronize the code version from a Git repository based on the provided
        surveillance configuration. This function initializes a Git repository, sets up the
        remote configuration, switches to the target branch, identifies files to add, stages
        them, and optionally commits and pushes changes.

        :param surveillance_config: The configuration object of type SurveillanceConfig that
            specifies the settings and parameters required to manage the code repository.
        :type surveillance_config: SurveillanceConfig
        :return: Boolean indicating if any changes were committed and pushed. Returns True if
            changes were committed and pushed successfully, else False.
        :rtype: bool
        """
        # Initial a git project
        self.repository: Repo = self._init_git(surveillance_config)

        # Initial git remote setting
        git_remote = self._init_git_remote(surveillance_config, self.default_remote_name)

        # Sync up the code version from git
        logger.info("Fetch to update the git ...")
        git_remote.fetch()
        # Switch to target git branch which only for Fake-API-Server
        logger.info("Switch to target branch ...")
        self._switch_git_branch(self.fake_api_server_monitor_git_branch)

        # Get all files in the folder
        all_files = self._get_all_fake_api_server_configs(surveillance_config)
        logger.info(f"Found files: {all_files}")

        # Check untracked files
        logger.info("Check untracked file ...")
        untracked = set(self.repository.untracked_files)
        self._add_files(all_files=all_files, target_files=untracked)

        # Check modified but unstaged files
        logger.info("Check modified file ...")
        diff_index = self.repository.index.diff(None)
        modified = {item.a_path for item in diff_index}
        self._add_files(all_files=all_files, target_files=modified)

        if len(self._all_staged_files) > 0:
            # Commit the update change
            commit = self._commit_changes(surveillance_config)

            # Push the change to git server
            self._push_to_remote(git_remote)
            logger.info(
                f"Successfully pushed commit {commit.hexsha[:8]} to {self.default_remote_name}/{self.fake_api_server_monitor_git_branch}"
            )
            return True
        else:
            logger.info("Don't have any files be added. Won't commit the change.")
            return False

    def _init_git(self, surveillance_config: SurveillanceConfig) -> Repo:
        """
        Initializes a Git repository based on the provided surveillance configuration.

        This function verifies the existence of the required configuration file for the
        PyFake-API-Server. It ensures that the provided configuration is valid and then
        returns a reference to the repository initialized at the provided location.

        :param surveillance_config: The surveillance configuration object containing
            details necessary to manage the fake API server and its subcommands.
        :type surveillance_config: SurveillanceConfig
        :return: A `Repo` object representing the initialized Git repository.
        :rtype: Repo
        :raises AssertionError: If the configuration file specified in the subcommand
            arguments does not exist.
        """
        subcmd_args: PullApiDocConfigArgs = cast(
            PullApiDocConfigArgs,
            surveillance_config.fake_api_server.subcmd[SubCommandLine.Pull].to_subcmd_args(PullApiDocConfigArgs),
        )
        assert os.path.exists(subcmd_args.config_path), "PyFake-API-Server configuration is required. Please check it."
        return Repo("./")

    def _init_git_remote(self, surveillance_config: SurveillanceConfig, remote_name: str) -> Remote:
        """
        Initializes a Git remote for the provided repository configuration and ensures the
        appropriate URL matches the expected format. Creates a new remote if it does not exist,
        or updates the existing remote URL if it is not as expected.

        :param surveillance_config: The configuration object containing Git repository
            information required to set or update the remote.
        :type surveillance_config: SurveillanceConfig
        :param remote_name: The name of the Git remote to create or update.
        :type remote_name: str
        :return: The created or updated Git remote instance.
        :rtype: Remote
        """
        if remote_name not in self.repository.remotes:
            logger.info("Target git remote setting doesn't exist, create one.")
            github_access_token = os.environ["GITHUB_TOKEN"]
            assert github_access_token, "Miss GitHub token"
            remote_url = (
                f"https://x-access-token:{github_access_token}@github.com/{surveillance_config.git_info.repository}"
            )
            git_remote = self.repository.create_remote(name=remote_name, url=remote_url)
        else:
            git_remote = self.repository.remote(name=remote_name)
            if surveillance_config.git_info.repository not in git_remote.url:
                logger.info("Target git remote URL is not as expect, modify the URL.")
                github_access_token = os.environ["GITHUB_TOKEN"]
                assert github_access_token, "Miss GitHub token"
                remote_url = (
                    f"https://x-access-token:{github_access_token}@github.com/{surveillance_config.git_info.repository}"
                )
                git_remote.set_url(new_url=remote_url)
        return git_remote

    def _switch_git_branch(self, git_ref: str) -> None:
        """
        Switches the current git branch to the specified branch reference. If the branch
        exists, it switches to it. Otherwise, it creates a new branch with the given
        reference and switches to it.

        If the current branch is already the specified branch, no action is performed.

        :param git_ref: The name of the branch to switch to. If the branch does not
            exist, a new branch will be created with this name.
        :return: None
        """
        if self._current_git_branch != git_ref:
            if git_ref in [b.name for b in self.repository.branches]:
                self.repository.git.switch(git_ref)
            else:
                self.repository.git.checkout("-b", git_ref)

    def _get_all_fake_api_server_configs(self, surveillance_config: SurveillanceConfig) -> Set[Path]:
        """
        Retrieve all fake API server configurations based on the provided surveillance configuration.

        This function processes a given surveillance configuration to locate fake API
        server configuration files matching a specific pattern. It identifies and returns
        a set of file paths pointing to those fake API server configuration files.

        :param surveillance_config: The configuration object containing information
            about the surveillance setup and associated fake API server data.
        :type surveillance_config: SurveillanceConfig
        :return: A set of file paths to the identified fake API server configuration
            files. Only files matching the criteria will be included in the returned set.
        :rtype: Set[Path]
        """
        subcmd_args: PullApiDocConfigArgs = cast(
            PullApiDocConfigArgs,
            surveillance_config.fake_api_server.subcmd[SubCommandLine.Pull].to_subcmd_args(PullApiDocConfigArgs),
        )
        all_files: Set[Path] = set()
        for file_path in Path(subcmd_args.base_file_path).rglob("*.yaml"):
            if file_path.is_file():
                all_files.add(file_path)
        return all_files

    def _add_files(self, all_files: Set[Path], target_files: Set[str]) -> None:
        """
        Adds multiple files to the repository's index if they match the target criteria
        and logs the file addition operations. The method ensures that staged files
        are tracked and processes specific target files by adding them to the index.

        :param all_files: A set containing the paths of all files which are staged in the
            repository. This is used to check if a file is already staged before adding.
        :type all_files: Set[Path]
        :param target_files: A set containing names or paths of target files to be added
            to the repository's index. Each file in this set is checked and processed
            accordingly (either as a single file or recursively for YAML files).
        :type target_files: Set[str]
        :return: None
        """

        def _add_file(_file: Union[Path, str]) -> None:
            if _file in all_files:
                self._all_staged_files.add(str(_file))
                self.repository.index.add(str(_file))
                logger.info(f"Add file: {_file}")

        for file in target_files:
            logger.info(f"Found some file: {file}")
            file_path_obj = Path(file)
            if file_path_obj.is_file():
                _add_file(file_path_obj)
            else:
                for one_file in Path(file).rglob("*.yaml"):
                    _add_file(one_file)

    def _commit_changes(self, surveillance_config: SurveillanceConfig) -> Commit:
        """
        Commits changes to the repository using the provided surveillance configuration
        and resets all staged files upon completion. This method ensures the change is
        recorded with the appropriate commit metadata.

        :param surveillance_config: The surveillance configuration containing git information
            required for creating the commit.
        :type surveillance_config: SurveillanceConfig
        :return: A reference to the created commit in the repository.
        :rtype: Commit
        """
        commit = self.repository.index.commit(
            author=surveillance_config.git_info.commit.author.serialize_for_git(),
            message=surveillance_config.git_info.commit.message,
        )
        logger.info("Commit the change.")
        self._reset_all_staged_files()
        return commit

    def _push_to_remote(self, git_remote: Remote) -> None:
        """
        Pushes the current branch to the specified remote server.

        This method pushes the local branch to the remote Git repository specified.
        The `refspec` is constructed dynamically based on the branch name stored in
        `self.fake_api_server_monitor_git_branch`. The operation is configured with
        the force option enabled. Any errors encountered during the push operation
        are automatically raised.

        :param git_remote: The remote Git repository where the local branch will
            be pushed.
        :type git_remote: Remote

        :return: None
        """
        git_remote.push(
            refspec=f"HEAD:refs/heads/{self.fake_api_server_monitor_git_branch}", force=True
        ).raise_if_error()
