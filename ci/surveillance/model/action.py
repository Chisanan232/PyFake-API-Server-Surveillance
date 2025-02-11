from dataclasses import dataclass
from typing import Mapping

from . import EnvironmentVariableKey
from ._base import _BaseModel
from .git import GitInfo
from .subcmd_pull import PullApiDocConfigArgs


@dataclass
class ActionInput(_BaseModel):
    api_doc_url: str
    server_type: str
    git_info: GitInfo
    subcmd_pull_args: PullApiDocConfigArgs

    @staticmethod
    def deserialize(data: Mapping) -> "ActionInput":
        return ActionInput(
            api_doc_url=data[EnvironmentVariableKey.API_DOC_URL.value],
            server_type=data[EnvironmentVariableKey.SERVER_TYPE.value],
            git_info=GitInfo.deserialize(data),
            subcmd_pull_args=PullApiDocConfigArgs.deserialize(data),
        )
