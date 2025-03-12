from enum import Enum


class ConfigurationKey(Enum):
    SURVEILLANCE_CONFIG_PATH = "CONFIG_PATH"

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
