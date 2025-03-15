"""
This sub-package focuses on managing configuration keys and environment variables
essential for the Fake API Server Surveillance system.

It provides structured enumerations for various configuration settings related
to API servers, Git operations, GitHub integrations, and CI/CD workflows. These
enumerations ensure consistent use of keys throughout the application and promote
maintainability by avoiding hardcoded values.
"""

from enum import Enum


class EnvironmentVariableKey(Enum):
    """
    Represents an enumeration of environment variable keys.

    This class defines a set of keys used for accessing specific environment
    variables required by the application. Each key represents a constant
    string value that corresponds to a particular environment configuration.

    :ivar SURVEILLANCE_CONFIG_PATH: Key representing the configuration
        path environment variable.
    :type SURVEILLANCE_CONFIG_PATH: str
    """

    SURVEILLANCE_CONFIG_PATH = "CONFIG_PATH"


class ConfigurationKey(Enum):
    """
    Enumeration containing configuration keys used across the system.

    Provides a structured set of constants for easy reference and reuse
    within the application. This enumeration encapsulates keys for API
    documentation, Fake-API-Server settings, Git information, GitHub
    pull request details, and configurations for various subcommands or CI
    operations.

    Usage of this class promotes consistency and reduces hardcoding of
    string literals in the application code, ensuring easier maintenance
    and clarity.

    :ivar API_DOC_URL: URL reference for accessing the API documentation.
    :type API_DOC_URL: str
    :ivar FAKE_API_SERVER: Key representing a fake API server setting.
    :type FAKE_API_SERVER: str
    :ivar SERVER_TYPE: Key representing the type of server.
    :type SERVER_TYPE: str
    :ivar SUBCMD: Subcommand identifier for configurations.
    :type SUBCMD: str
    :ivar PULL: Key identifying pull-related operations or subcommands.
    :type PULL: str
    :ivar ARGS: Key for command-line or configuration arguments.
    :type ARGS: str
    :ivar GIT_INFO: Indicator for Git-related configuration or data.
    :type GIT_INFO: str
    :ivar GIT_REPOSITORY: Key for Git repository information.
    :type GIT_REPOSITORY: str
    :ivar GIT_COMMIT: Key to identify a specific Git commit.
    :type GIT_COMMIT: str
    :ivar GIT_AUTHOR: Key referring to Git author-related details.
    :type GIT_AUTHOR: str
    :ivar GIT_AUTHOR_NAME: Key for the Git author's name.
    :type GIT_AUTHOR_NAME: str
    :ivar GIT_AUTHOR_EMAIL: Key for the Git author's email address.
    :type GIT_AUTHOR_EMAIL: str
    :ivar GIT_COMMIT_MSG: Key referencing the Git commit message.
    :type GIT_COMMIT_MSG: str
    :ivar GITHUB_INFO: Key grouping GitHub-related information.
    :type GITHUB_INFO: str
    :ivar GITHUB_PULL_REQUEST: Key referencing GitHub pull request details.
    :type GITHUB_PULL_REQUEST: str
    :ivar PR_TITLE: Key representing the pull request title.
    :type PR_TITLE: str
    :ivar PR_BODY: Key referencing the body content of a pull request.
    :type PR_BODY: str
    :ivar PR_IS_DRAFT: Boolean key indicating if the pull request is a draft.
    :type PR_IS_DRAFT: str
    :ivar PR_LABELS: Key for labels assigned to a pull request.
    :type PR_LABELS: str
    :ivar CONFIG_PATH: Configuration file path for a specific setup.
    :type CONFIG_PATH: str
    :ivar INCLUDE_TEMPLATE_CONFIG: Key specifying inclusion of template config.
    :type INCLUDE_TEMPLATE_CONFIG: str
    :ivar BASE_FILE_PATH: Key for referring to a base file path.
    :type BASE_FILE_PATH: str
    :ivar BASE_URL: Key representing a base URL in configurations.
    :type BASE_URL: str
    :ivar DIVIDE_API: Key to segregate divided API-related settings.
    :type DIVIDE_API: str
    :ivar DIVIDE_HTTP: Key for separate HTTP-related configurations.
    :type DIVIDE_HTTP: str
    :ivar DIVIDE_HTTP_REQUEST: Key for individual HTTP request settings or data.
    :type DIVIDE_HTTP_REQUEST: str
    :ivar DIVIDE_HTTP_RESPONSE: Key indicating HTTP response details or mapping.
    :type DIVIDE_HTTP_RESPONSE: str
    :ivar DRY_RUN: Key to trigger dry run mode for operations.
    :type DRY_RUN: str
    :ivar ACCEPT_CONFIG_NOT_EXIST: Key allowing acceptance of missing configurations.
    :type ACCEPT_CONFIG_NOT_EXIST: str
    """

    # API documentation info
    API_DOC_URL = "api-doc-url"

    # Fake-API-Server settings
    FAKE_API_SERVER = "fake-api-server"
    SERVER_TYPE = "server-type"
    SUBCMD = "subcmd"
    PULL = "pull"
    ARGS = "args"

    # git info
    GIT_INFO = "git-info"
    GIT_REPOSITORY = "repo"
    GIT_COMMIT = "commit"
    GIT_AUTHOR = "author"
    GIT_AUTHOR_NAME = "name"
    GIT_AUTHOR_EMAIL = "email"
    GIT_COMMIT_MSG = "message"

    # github info
    GITHUB_INFO = "github-info"
    GITHUB_PULL_REQUEST = "pull-request"
    PR_TITLE = "title"
    PR_BODY = "body"
    PR_IS_DRAFT = "draft"
    PR_LABELS = "labels"

    # for subcommand line *pull* options
    CONFIG_PATH = "CONFIG_PATH"
    INCLUDE_TEMPLATE_CONFIG = "INCLUDE_TEMPLATE_CONFIG"
    BASE_FILE_PATH = "BASE_FILE_PATH"
    BASE_URL = "BASE_URL"
    DIVIDE_API = "DIVIDE_API"
    DIVIDE_HTTP = "DIVIDE_HTTP"
    DIVIDE_HTTP_REQUEST = "DIVIDE_HTTP_REQUEST"
    DIVIDE_HTTP_RESPONSE = "DIVIDE_HTTP_RESPONSE"
    DRY_RUN = "DRY_RUN"

    # operation with action in CI
    ACCEPT_CONFIG_NOT_EXIST = "accept_config_not_exist"
