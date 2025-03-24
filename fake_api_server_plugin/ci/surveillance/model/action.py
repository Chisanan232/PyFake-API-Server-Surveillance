"""
This module defines the ActionInput class, which represents the input data model
for the surveillance action workflow. It handles deserialization of input data
and provides methods to retrieve the surveillance configuration.

Classes:

- ActionInput: Manages input deserialization and configuration handling.

Dependencies:

- Reads YAML configuration from a file and deserializes it into a SurveillanceConfig.
"""

from dataclasses import dataclass, field
from typing import Mapping

from fake_api_server._utils.file.operation import YAML

from . import EnvironmentVariableKey
from ._base import _BaseModel
from .config import SurveillanceConfig


@dataclass
class ActionInput(_BaseModel):
    """
    Represents the input data structure for an action.

    This class is designed to hold and manage the input configuration path
    for an action. It provides functionality to deserialize input data into
    an `ActionInput` instance and to retrieve the configuration object based
    on the stored configuration path.

    :ivar config_path: The path to the configuration file for the action input.
    :type config_path: str
    """

    config_path: str = field(default_factory=str)

    @staticmethod
    def deserialize(data: Mapping) -> "ActionInput":
        return ActionInput(
            config_path=data.get(
                EnvironmentVariableKey.SURVEILLANCE_CONFIG_PATH.value, "./fake-api-server-surveillance.yaml"
            ),
        )

    def get_config(self) -> SurveillanceConfig:
        """
        Retrieve and deserialize configuration data from a specified YAML file.

        This method reads a YAML file located at the path defined by the
        `config_path` attribute. The file is expected to contain serialized
        data for configuring a `SurveillanceConfig` object. Upon successful
        reading and deserialization, a new `SurveillanceConfig` instance is returned.

        :raises FileNotFoundError: If the YAML file at `config_path` does not exist.
        :raises ValueError: If the file at `config_path` contains invalid YAML data
            or is improperly formatted for `SurveillanceConfig`.

        :return: A `SurveillanceConfig` object created from the YAML file's content.
        :rtype: SurveillanceConfig
        """
        return SurveillanceConfig.deserialize(YAML().read(self.config_path))
