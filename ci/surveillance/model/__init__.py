from enum import Enum


class EnvironmentVariableKey(Enum):
    # API documentation info
    API_DOC_URL = "API_DOC_URL"
    SERVER_TYPE = "SERVER_TYPE"
    # git info
    GIT_REPOSITORY = "GIT_REPOSITORY"
    GIT_AUTHOR_NAME = "GIT_AUTHOR_NAME"
    GIT_AUTHOR_EMAIL = "GIT_AUTHOR_EMAIL"
    GIT_COMMIT_MSG = "GIT_COMMIT_MSG"
