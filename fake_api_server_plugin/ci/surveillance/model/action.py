import ast
from dataclasses import dataclass
from typing import Mapping

from . import EnvironmentVariableKey
from ._base import _BaseModel
from .git import GitInfo
from .github import GitHubInfo
from .subcmd_pull import PullApiDocConfigArgs


@dataclass
class SurveillanceConfig(_BaseModel):
    api_doc_url: str
    server_type: str
    git_info: GitInfo
    github_info: GitHubInfo
    subcmd_pull_args: PullApiDocConfigArgs
    accept_config_not_exist: bool

    @staticmethod
    def deserialize(data: Mapping) -> "SurveillanceConfig":
        return SurveillanceConfig(
            api_doc_url=data[EnvironmentVariableKey.API_DOC_URL.value],
            # TODO: Still doesn't support this feature at action
            server_type=data.get(EnvironmentVariableKey.SERVER_TYPE.value, None),
            git_info=GitInfo.deserialize(data),
            github_info=GitHubInfo.deserialize(data),
            subcmd_pull_args=PullApiDocConfigArgs.deserialize(data),
            accept_config_not_exist=ast.literal_eval(
                str(data[EnvironmentVariableKey.ACCEPT_CONFIG_NOT_EXIST.value]).capitalize()
            ),
        )
