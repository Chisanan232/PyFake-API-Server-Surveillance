from enum import Enum


class EnvironmentVariableKey(Enum):
    GIT_REPOSITORY: str = "GIT_REPOSITORY"
    API_DOC_URL: str = "API_DOC_URL"
    SERVER_TYPE: str = "SERVER_TYPE"
    GIT_AUTHOR_NAME: str = "GIT_AUTHOR_NAME"
    GIT_AUTHOR_EMAIL: str = "GIT_AUTHOR_EMAIL"
    GIT_COMMIT_MSG: str = "GIT_COMMIT_MSG"
