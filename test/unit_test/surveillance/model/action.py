from typing import Mapping, Type

import pytest

from fake_api_server_plugin.ci.surveillance.model import EnvironmentVariableKey
from fake_api_server_plugin.ci.surveillance.model.action import ActionInput

# isort: off
from test.unit_test.surveillance.model._base import _BaseModelTestSuite
from test._values._test_data import fake_data

# isort: on


class TestActionInput(_BaseModelTestSuite):

    @pytest.fixture(scope="function")
    def model(self) -> Type[ActionInput]:
        return ActionInput

    @pytest.mark.parametrize(
        "data",
        [
            fake_data.action_input(),
        ],
    )
    def test_deserialize(self, model: Type[ActionInput], data: Mapping):
        super().test_deserialize(model, data)

    def _verify_model_props(self, model: ActionInput, original_data: Mapping) -> None:
        assert model.config_path == original_data[EnvironmentVariableKey.SURVEILLANCE_CONFIG_PATH.value]
