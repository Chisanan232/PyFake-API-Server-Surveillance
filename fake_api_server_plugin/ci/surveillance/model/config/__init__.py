"""
All the models about PyFake-API-Server-Surveillance configuration.
"""

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
    """
    Represents the configuration for the surveillance system.

    This class encapsulates various configuration settings required for the
    surveillance system, including API documentation URL, fake API server details,
    Git repository information, and GitHub integration details. An optional
    configuration flag is also provided to accept the absence of the configuration
    settings.

    :ivar api_doc_url: The URL to the API documentation.
    :type api_doc_url: str
    :ivar fake_api_server: Configuration settings for the fake API server.
    :type fake_api_server: FakeAPIConfigSetting
    :ivar git_info: Information about the Git repository configuration.
    :type git_info: GitInfo
    :ivar github_info: Details about GitHub integration configuration.
    :type github_info: GitHubInfo
    :ivar accept_config_not_exist: Determines whether to proceed even if the
        configuration does not exist.
    :type accept_config_not_exist: bool
    """

    api_doc_url: str
    fake_api_server: FakeAPIConfigSetting
    git_info: GitInfo
    github_info: GitHubInfo
    accept_config_not_exist: bool

    @staticmethod
    def deserialize(data: Mapping) -> "SurveillanceConfig":
        return SurveillanceConfig(
            api_doc_url=data[ConfigurationKey.API_DOC_URL.value],
            fake_api_server=FakeAPIConfigSetting.deserialize(data.get(ConfigurationKey.FAKE_API_SERVER.value, {})),
            git_info=GitInfo.deserialize(data.get(ConfigurationKey.GIT_INFO.value, {})),
            github_info=GitHubInfo.deserialize(data.get(ConfigurationKey.GITHUB_INFO.value, {})),
            accept_config_not_exist=data.get(ConfigurationKey.ACCEPT_CONFIG_NOT_EXIST.value, False),
        )
