from typing import Type, Mapping

import pytest

from ci.surveillance.model import EnvironmentVariableKey
from ci.surveillance.model.action import ActionInput
from ._base import _BaseModelTestSuite


class TestActionInput(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[ActionInput]:
        return ActionInput

    @pytest.mark.parametrize(
        "data",
        [
            {
                EnvironmentVariableKey.API_DOC_URL.value: "http://10.20.0.13:8080",
                EnvironmentVariableKey.SERVER_TYPE.value: "rest-server",
                EnvironmentVariableKey.GIT_REPOSITORY.value: "test/sample-project",
                EnvironmentVariableKey.GIT_AUTHOR_NAME.value: "test",
                EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value: "test@gmail.com",
                EnvironmentVariableKey.GIT_COMMIT_MSG.value: "✏️ Update the API interface settings.",
            },
        ],
    )
    def test_deserialize(self, model: Type[ActionInput], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: ActionInput, original_data: Mapping) -> None:
        assert model.api_doc_url == original_data[EnvironmentVariableKey.API_DOC_URL.value]
        assert model.server_type == original_data[EnvironmentVariableKey.SERVER_TYPE.value]
        assert model.git_info.repository == original_data[EnvironmentVariableKey.GIT_REPOSITORY.value]
        assert model.git_info.commit.author.name == original_data[EnvironmentVariableKey.GIT_AUTHOR_NAME.value]
        assert model.git_info.commit.author.email == original_data[EnvironmentVariableKey.GIT_AUTHOR_EMAIL.value]
        assert model.git_info.commit.message == original_data[EnvironmentVariableKey.GIT_COMMIT_MSG.value]
