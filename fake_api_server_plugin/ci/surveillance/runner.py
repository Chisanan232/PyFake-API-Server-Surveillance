"""
This module implements the monitoring and management of a Fake API Server's
GitHub repository (means the fake server configuration which be built by
PyFake-API-Server). The module provides a class called `FakeApiServerSurveillance`
which handles the surveillance of the API documentation configuration. It
provides methods which could be customized by yourself for monitoring the
repository for changes in the API documentation configuration, comparing
the current configuration with the latest configuration, and creating pull
requests when changes are detected.

The main functionality is provided by the `FakeApiServerSurveillance` class,
which automates the process of tracking changes in API documentation to
keep the fake server repository up-to-date.
"""

import logging
import os
from pathlib import Path
from typing import Mapping, Tuple, cast

import urllib3
from fake_api_server import FakeAPIConfig
from fake_api_server.command._common.component import SavingConfigComponent
from fake_api_server.command.subcommand import SubCommandLine
from fake_api_server.model import (
    MockAPIs,
    SubcmdPullArguments,
    deserialize_api_doc_config,
    load_config,
)

from .log import init_logger_config
from .model.action import ActionInput
from .model.compare import CompareInfo

try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod  # type: ignore[no-redef]

from .component.git import GitOperation
from .component.github_opt import GitHubOperation
from .model.config import PullApiDocConfigArgs, SurveillanceConfig
from .model.config.github_action import get_github_action_env

logger = logging.getLogger(__name__)


class FakeApiServerSurveillance:
    """
    Manages the surveillance of a Fake API Server's GitHub repository, monitoring
    and handling changes in its API documentation.

    This class is designed to monitor the GitHub repository of a Fake API Server
    for changes in the API documentation configuration. It interacts with
    various components like Git operations, GitHub operations, and API
    documentations, ensuring the configurations are up-to-date and initiating
    necessary processes such as creating pull requests when changes are detected.
    It also handles situations where no changes are present or configurations are
    missing. This class encapsulates the workflow required for this monitoring and
    management.

    :ivar subcmd_pull_component: Represents the configuration saving component
        for handling API documentation updates.
    :type subcmd_pull_component: SavingConfigComponent
    :ivar git_operation: Encapsulates git-related operations such as versioning.
    :type git_operation: GitOperation
    :ivar github_operation: Handles interactions with GitHub, such as creating pull
        requests or repository-level actions.
    :type github_operation: GitHubOperation
    """

    def __init__(self):
        self.subcmd_pull_component = SavingConfigComponent()
        self.git_operation = GitOperation()
        self.github_operation: GitHubOperation = GitHubOperation()

    def monitor(self) -> None:
        """
        Monitors a GitHub repository for changes in API documentation configurations.
        This method checks for updates in the API documentation configuration of a
        given repository, compares it with the current configuration, and processes
        the changes if any are detected. If no changes are found, it handles the
        situation accordingly without additional actions.

        :raises ValueError: If the Action Inputs or Surveillance Configuration deserialization
                            fails during processing.
        :raises RuntimeError: If the retrieval or comparison processes encounter unexpected
                              conditions that prevent completion.

        :return: None
        """
        logger.info("Start to monitor the github repro ...")
        action_inputs = self._deserialize_action_inputs(self._get_action_inputs())
        surveillance_config = self._deserialize_surveillance_config(action_inputs)

        logger.info("Try to get the latest API documentation configuration ...")
        new_api_doc_config = self._get_latest_api_doc_config(surveillance_config)
        logger.info("Compare the latest API documentation configuration with current configuration ...")
        has_api_change, change_info = self._compare_with_current_config(surveillance_config, new_api_doc_config)
        surveillance_config.github_info.pull_request.set_change_detail(change_info.change_detail)
        if has_api_change:
            logger.info("Has something change and will create a pull request.")
            self._process_api_change(surveillance_config, new_api_doc_config)
        else:
            logger.info("Nothing change and won't do anything.")
            self._process_no_api_change(surveillance_config)

    def _get_action_inputs(self) -> Mapping:
        """
        Retrieves the action inputs as a mapping from the environment variables.

        This method extracts action-related inputs from the current environment
        by accessing the ``os.environ`` dictionary. It is primarily used to interface
        with a configuration or actions that depend on environment-specific details.

        :raises KeyError: If any expected environment variable is not found.
        :raises TypeError: If the returned object is not a valid Mapping.

        :return: A mapping object containing the action inputs extracted from the
                 environment variables.
        :rtype: Mapping
        """
        return os.environ

    def _deserialize_action_inputs(self, action_inputs: Mapping) -> ActionInput:
        """
        Deserializes the provided action_inputs mapping into an ActionInput object.

        :param action_inputs: The dictionary-like mapping containing the input data
            for an action that needs to be deserialized.
        :type action_inputs: Mapping
        :return: The deserialized ActionInput object constructed based on the provided
            action_inputs mapping.
        :rtype: ActionInput
        """
        return ActionInput.deserialize(action_inputs)

    def _deserialize_surveillance_config(self, action_input: ActionInput) -> SurveillanceConfig:
        """
        Deserializes the surveillance configuration from the given action input.

        This method extracts and converts the surveillance configuration data
        from the provided ``ActionInput`` object. It returns a ``SurveillanceConfig``
        object constructed using the configuration data obtained.

        :param action_input: Input object containing the surveillance configuration
            that needs to be deserialized.
        :type action_input: ActionInput
        :return: The deserialized surveillance configuration.
        :rtype: SurveillanceConfig
        """
        return action_input.get_config()

    def _get_latest_api_doc_config(self, surveillance_config: SurveillanceConfig) -> FakeAPIConfig:
        """
        Fetches the latest API documentation configuration from the specified API endpoint.

        The method makes a GET request to the API documentation URL provided in the
        configuration. Upon successful retrieval, it deserializes the received response
        to construct a configuration object, converts it into a usable API configuration
        instance, and adjusts the base URL using the pulled subcommand arguments from the
        fake API server configuration.

        :param surveillance_config: Configuration for surveillance including API documentation URL
                                    and fake API server details.
        :type surveillance_config: SurveillanceConfig
        :return: Fake API configuration derived from the latest API documentation.
        :rtype: FakeAPIConfig
        """
        response = urllib3.request(method=HTTPMethod.GET, url=surveillance_config.api_doc_url)
        logger.info(f"Get the API documentation configuration with response status code: {response.status}")
        current_api_doc_config = deserialize_api_doc_config(response.json())
        subcmd_args = cast(
            PullApiDocConfigArgs,
            surveillance_config.fake_api_server.subcmd[SubCommandLine.Pull].to_subcmd_args(PullApiDocConfigArgs),
        )
        return current_api_doc_config.to_api_config(base_url=subcmd_args.base_url)

    def _compare_with_current_config(
        self, surveillance_config: SurveillanceConfig, new_api_doc_config: FakeAPIConfig
    ) -> Tuple[bool, CompareInfo]:
        """
        Determines if there are any changes in the new API documentation configuration compared to the current
        surveillance configuration. This function compares the API documentation configurations stored within
        the specified configurations and checks whether API keys exist in both configurations and if their data
        matches.

        :param surveillance_config: SurveillanceConfig object containing the current surveillance configuration,
            which includes Fake-API-Server configurations and settings.
        :param new_api_doc_config: FakeAPIConfig object representing the new set of API documentation configurations
            to be compared with the current surveillance configuration.
        :return: A boolean value indicating whether there is any change in the API documentation configuration.
        """
        subcmd_args = cast(
            PullApiDocConfigArgs,
            surveillance_config.fake_api_server.subcmd[SubCommandLine.Pull].to_subcmd_args(PullApiDocConfigArgs),
        )
        fake_api_server_config = subcmd_args.config_path
        if Path(fake_api_server_config).exists():
            api_config = load_config(fake_api_server_config)
            change_detail_info = CompareInfo(local_model=api_config, remote_model=new_api_doc_config)
            has_api_change = change_detail_info.has_different()
        else:
            if not surveillance_config.accept_config_not_exist:
                raise FileNotFoundError("Not found Fake-API-Server config file. Please add it in repository.")
            has_api_change = True
            change_detail_info = CompareInfo(
                local_model=FakeAPIConfig(apis=MockAPIs(apis={})), remote_model=new_api_doc_config
            )
            assert change_detail_info.has_different()
            fake_api_server_config_dir = Path(fake_api_server_config).parent
            if not fake_api_server_config_dir.exists():
                fake_api_server_config_dir.mkdir(parents=True, exist_ok=True)
        return has_api_change, change_detail_info

    def _process_api_change(self, surveillance_config: SurveillanceConfig, new_api_doc_config: FakeAPIConfig) -> None:
        """
        Processes changes in API configuration for the surveillance system. This method updates the
        new API documentation configuration based on the surveillance configuration, handles versioning,
        and sends out necessary notifications. It is designed to ensure that changes to API are
        integrated seamlessly into the system workflow.

        :param surveillance_config: Current surveillance configuration used for managing API data.
                                    Expected to include details related to API server and subcommands.
        :type surveillance_config: SurveillanceConfig
        :param new_api_doc_config: The new API documentation configuration to be applied.
        :type new_api_doc_config: FakeAPIConfig
        :return: This method does not return any value.
        :rtype: None
        """
        subcmd_args = cast(
            PullApiDocConfigArgs,
            surveillance_config.fake_api_server.subcmd[SubCommandLine.Pull].to_subcmd_args(PullApiDocConfigArgs),
        )
        self._update_api_doc_config(subcmd_args.to_subcmd_model(), new_api_doc_config)
        self._process_versioning(surveillance_config)
        self._notify(surveillance_config)

    def _update_api_doc_config(self, args: SubcmdPullArguments, new_api_doc_config: FakeAPIConfig) -> None:
        """
        Updates the API documentation configuration using the provided arguments and configuration.

        :param args: The arguments required to execute the API documentation configuration update by subcommand line *pull* of Fake-API-Server.
        :type args: SubcmdPullArguments
        :param new_api_doc_config: The new configuration object for the API documentation to
            be applied.
        :type new_api_doc_config: FakeAPIConfig
        :returns: None
        """
        self.subcmd_pull_component.serialize_and_save(cmd_args=args, api_config=new_api_doc_config)

    def _process_versioning(self, surveillance_config: SurveillanceConfig) -> None:
        """
        Processes version change by creating a pull request if changes are detected.

        Identifies changes in repository versioning and initiates the pull request
        creation process. Uses the `GitOperation` class to determine if changes
        occurred and constructs a pull request with the help of `GithubOperation`
        using the repository metadata derived from the `GithubActionEnv`.

        :param surveillance_config: Configuration object containing required versioning
            and pull request information.
        :type surveillance_config: SurveillanceConfig
        :return: None
        """
        has_change = self.git_operation.version_change(surveillance_config)
        if has_change:
            logger.info("Has something change and will create a pull request.")
            github_action_env = get_github_action_env()
            with self.github_operation(
                repo_owner=github_action_env.repository_owner_name, repo_name=github_action_env.repository_name
            ):
                pull_request_info = surveillance_config.github_info.pull_request
                self.github_operation.create_pull_request(
                    title=pull_request_info.title,
                    body=pull_request_info.body,
                    base_branch=github_action_env.base_branch,
                    head_branch=self.git_operation.fake_api_server_monitor_git_branch,
                    labels=pull_request_info.labels,
                )

    def _notify(self, surveillance_config: SurveillanceConfig) -> None:
        """
        Notifies the surveillance system based on the provided configuration.

        This method is intended to handle the notification logic based on the given
        surveillance configuration.

        !!! warning "🚧 This feature is under checking and development."

            Currently, the implementation is pending as this represents a
            backlog task.

        :param surveillance_config: The configuration object containing details
            required for the surveillance notification.
        :type surveillance_config: SurveillanceConfig
        :return: No value is returned as the method is designed to perform an
            internal operation without producing a direct output.
        :rtype: None
        """

    def _process_no_api_change(self, surveillance_config: SurveillanceConfig) -> None:
        """
        Processes the given surveillance configuration where no API change is required.

        This internal method is responsible for handling surveillance configurations
        that do not necessitate modifications to the API. The received configuration is
        processed accordingly to ensure compliance with the required internal protocols.

        :param surveillance_config: The surveillance configuration instance to be
            processed. It contains all the necessary settings and parameters
            relevant for system operations.
        :return: This method does not return any values.
        """


def run() -> None:
    """
    Executes the main operation to monitor the fake API server.

    This function is responsible for initializing the logger configuration and
    triggering the monitoring process using the `FakeApiServerSurveillance` class.

    :returns: None
    """
    init_logger_config()
    FakeApiServerSurveillance().monitor()
