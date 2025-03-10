from dataclasses import field, dataclass
from typing import Mapping

from fake_api_server._utils.file.operation import YAML

from . import EnvironmentVariableKey
from ._base import _BaseModel
from .config import SurveillanceConfig


@dataclass
class ActionInput(_BaseModel):
    config_path: str = field(default_factory=str)

    @staticmethod
    def deserialize(data: Mapping) -> "ActionInput":
        return ActionInput(
            config_path=data.get(EnvironmentVariableKey.SURVEILLANCE_CONFIG_PATH.value, "./fake-api-server-surveillance.yaml"),
        )

    def get_config(self) -> SurveillanceConfig:
        return SurveillanceConfig.deserialize(YAML().read(self.config_path))
