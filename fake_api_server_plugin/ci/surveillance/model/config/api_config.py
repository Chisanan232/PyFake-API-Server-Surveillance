"""
This module provides data models and utilities for managing API documentation
configuration settings for section `fake-api-server`, handling subcommand-line
arguments, and deserializing data into structured configurations used in a fake
API server.
"""

import ast
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Type

from fake_api_server.model import ParserArguments
from fake_api_server.model.command.rest_server.cmd_args import SubcmdPullArguments
from fake_api_server.model.subcmd_common import SubCommandLine, SysArg

from .. import ConfigurationKey
from .._base import _BaseModel


@dataclass
class BaseArgsAdapter(metaclass=ABCMeta):
    """
    BaseArgsAdapter serves as an abstract base class for adapting arguments in
    a consistent manner with a specific subcommand model.

    This class is designed to enforce the implementation of the `to_subcmd_model`
    method in all derived classes, ensuring that they convert arguments to a
    `ParserArguments` instance. It is intended to be subclassed and used in
    contexts where argument transformation and adherence to a particular
    subcommand model are required.

    :ivar __abstractmethods__: Defines abstract methods that must be implemented
        by any subclass deriving from BaseArgsAdapter.
    :type __abstractmethods__: frozenset
    """

    @abstractmethod
    def to_subcmd_model(self) -> ParserArguments:
        pass


@dataclass
class PullApiDocConfigArgs(_BaseModel, BaseArgsAdapter):
    """
    Configuration arguments for pulling API documentation.

    This dataclass is designed to encapsulate the configuration details required
    to pull API documentation. It includes settings for config paths, base URLs,
    division of API elements, and other related parameters. This class also
    provides methods to deserialize data into an instance of the class and to
    convert it into a subcommand-compatible model format.

    :ivar config_path: The file path to the API configuration YAML file.
    :type config_path: str
    :ivar include_template_config: Boolean flag indicating whether to include the
        template configuration in the process.
    :type include_template_config: bool
    :ivar base_file_path: The path to the base directory for generated files.
    :type base_file_path: str
    :ivar base_url: The base URL for the API.
    :type base_url: str
    :ivar dry_run: Boolean flag indicating whether the operation should be a
        simulation without actual execution.
    :type dry_run: bool
    :ivar divide_api: Boolean flag indicating whether to divide the API components
        during the process.
    :type divide_api: bool
    :ivar divide_http: Boolean flag indicating whether to divide HTTP components
        in the API process.
    :type divide_http: bool
    :ivar divide_http_request: Boolean flag indicating whether to divide the HTTP
        request parts of the API.
    :type divide_http_request: bool
    :ivar divide_http_response: Boolean flag indicating whether to divide the HTTP
        response parts of the API.
    :type divide_http_response: bool
    """

    config_path: str = "./api.yaml"
    include_template_config: bool = False
    base_file_path: str = "./"
    base_url: str = ""
    dry_run: bool = False
    divide_api: bool = False
    divide_http: bool = False
    divide_http_request: bool = False
    divide_http_response: bool = False

    @staticmethod
    def deserialize(data: Mapping) -> "PullApiDocConfigArgs":
        return PullApiDocConfigArgs(
            config_path=data[ConfigurationKey.CONFIG_PATH.value],
            include_template_config=ast.literal_eval(
                str(data[ConfigurationKey.INCLUDE_TEMPLATE_CONFIG.value]).capitalize()
            ),
            base_file_path=data[ConfigurationKey.BASE_FILE_PATH.value],
            base_url=data[ConfigurationKey.BASE_URL.value],
            divide_api=ast.literal_eval(str(data[ConfigurationKey.DIVIDE_API.value]).capitalize()),
            divide_http=ast.literal_eval(str(data[ConfigurationKey.DIVIDE_HTTP.value]).capitalize()),
            divide_http_request=ast.literal_eval(str(data[ConfigurationKey.DIVIDE_HTTP_REQUEST.value]).capitalize()),
            divide_http_response=ast.literal_eval(str(data[ConfigurationKey.DIVIDE_HTTP_RESPONSE.value]).capitalize()),
            dry_run=ast.literal_eval(str(data[ConfigurationKey.DRY_RUN.value]).capitalize()),
        )

    def to_subcmd_model(self) -> SubcmdPullArguments:
        """
        Transforms and maps the internal configuration objects and attributes into
        a `SubcmdPullArguments` model. This method provides the necessary arguments
        and configuration for constructing a pull command subparser model and
        ensures appropriate data is passed for command execution.

        :rtype: SubcmdPullArguments
        :return: A `SubcmdPullArguments` object that encapsulates the required
            and optional data for executing the Pull sub-command.
        """
        return SubcmdPullArguments(
            # Unnecessary in Fake-API-Server-Surveillance
            subparser_structure=SysArg(subcmd=SubCommandLine.Pull),
            source="",
            source_file="",
            request_with_https=False,
            # Necessary in Fake-API-Server-Surveillance
            config_path=self.config_path,
            base_file_path=self.base_file_path,
            base_url=self.base_url,
            include_template_config=self.include_template_config,
            divide_api=self.divide_api,
            divide_http=self.divide_http,
            divide_http_request=self.divide_http_request,
            divide_http_response=self.divide_http_response,
            dry_run=self.dry_run,
        )


@dataclass
class SubCmdConfig(_BaseModel):
    """
    Represents the configuration for a sub-command in the application.

    The SubCmdConfig class is used for handling sub-command configuration and its
    conversion to a specific model. It provides functionality to deserialize raw
    data into a SubCmdConfig instance and to transform the arguments into a
    sub-command argument model format.

    :ivar args: List of command-line arguments.
    :type args: List[str]
    """

    args: List[str]

    @staticmethod
    def deserialize(data: Mapping) -> "SubCmdConfig":
        return SubCmdConfig(
            args=data.get(ConfigurationKey.ARGS.value, []),
        )

    def to_subcmd_args(self, subcmd_arg_model: Type[BaseArgsAdapter]) -> BaseArgsAdapter:
        """
        Converts a list of command-line arguments into a model instance by mapping
        argument keys and values into the appropriate format. This method parses
        arguments, verifies their validity, and applies them to create and populate
        an instance of the given model class.

        :param subcmd_arg_model: The model class (`BaseArgsAdapter`) to which the
            parsed arguments will be applied. Must subclass `BaseArgsAdapter`.

        :return: An instance of the provided `subcmd_arg_model` populated with
            values derived from the list of command-line arguments.

        :rtype: `BaseArgsAdapter`
        """
        param_with_key: Dict[str, str] = {}
        for arg in self.args:
            arg_eles = arg.split("=")
            assert len(arg_eles) <= 2, f"Invalid subcmd arg: {arg}"
            arg_with_value = arg_eles if len(arg_eles) == 2 else [arg_eles[0], True]  # type: ignore[list-item]
            assert len(arg_with_value) == 2
            arg_key, arg_value = arg_with_value
            arg_key = arg_key.replace("--", "").replace("-", "_")
            param_with_key[arg_key] = arg_value
        return subcmd_arg_model(**param_with_key)


@dataclass
class FakeAPIConfigSetting(_BaseModel):
    """
    Represents the configuration settings for a fake API.

    This class provides the structure and logic for handling and deserializing
    configuration settings related to a fake API system. It includes attributes
    for specifying the type of server and subcommands with their respective
    configuration details. The class supports deserialization from a given
    mapping to produce a fully-initialized configuration setting object.

    :ivar server_type: Specifies the type of the server.
    :type server_type: str
    :ivar subcmd: Maps the subcommand enums to their corresponding configuration
                 details.
    :type subcmd: Dict[SubCommandLine, SubCmdConfig]
    """

    # TODO: Still doesn't support this feature at action
    server_type: str = field(default_factory=str)
    subcmd: Dict[SubCommandLine, SubCmdConfig] = field(default_factory=dict)

    @staticmethod
    def deserialize(data: Mapping) -> "FakeAPIConfigSetting":
        subcmd_configs = {}
        for subcmd_k, subcmd_v in data.get(ConfigurationKey.SUBCMD.value, {}).items():
            subcmd_configs[SubCommandLine.to_enum(subcmd_k)] = SubCmdConfig.deserialize(subcmd_v)
        return FakeAPIConfigSetting(
            server_type=data[ConfigurationKey.SERVER_TYPE.value],
            subcmd=subcmd_configs,
        )
