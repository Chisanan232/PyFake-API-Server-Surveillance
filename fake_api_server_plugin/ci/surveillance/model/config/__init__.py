import ast
from dataclasses import dataclass
from typing import Mapping

from .. import ConfigurationKey
from .._base import _BaseModel
from .api_config import FakeAPIConfigSetting, PullApiDocConfigArgs
from .git import GitInfo
from .github import GitHubInfo


@dataclass
class SurveillanceConfig(_BaseModel):
    api_doc_url: str
    fake_api_server: FakeAPIConfigSetting
    git_info: GitInfo
    github_info: GitHubInfo
    accept_config_not_exist: bool

    @staticmethod
    def deserialize(data: Mapping) -> "SurveillanceConfig":
        return SurveillanceConfig(
            api_doc_url=data[ConfigurationKey.API_DOC_URL.value],
            fake_api_server=FakeAPIConfigSetting.deserialize(
                data.get(ConfigurationKey.FAKE_API_SERVER.value, {})
            ),
            git_info=GitInfo.deserialize(data.get(ConfigurationKey.GIT_INFO.value, {})),
            github_info=GitHubInfo.deserialize(data.get(ConfigurationKey.GITHUB_INFO.value, {})),
            accept_config_not_exist=data.get(ConfigurationKey.ACCEPT_CONFIG_NOT_EXIST.value, False),
        )
