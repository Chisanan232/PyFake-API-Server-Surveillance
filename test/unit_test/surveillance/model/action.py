import glob
from pathlib import Path
from typing import Mapping, Type
from unittest.mock import patch

from yaml import load

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader  # type: ignore

import pytest
from fake_api_server._utils.file.operation import YAML

from fake_api_server_plugin.ci.surveillance.model import ConfigurationKey, EnvironmentVariableKey
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

    @pytest.mark.parametrize("config_path", glob.glob("./test/config/e2e_test/**.yaml"))
    def test_get_config(self, config_path: str):
        fake_api_server_config = Path(config_path)
        assert fake_api_server_config.exists()
        with open(config_path, "r", encoding="utf-8") as file_stream:
            config_data: dict = load(stream=file_stream, Loader=Loader)

        with patch.object(YAML, "read", return_value=config_data):
            model = ActionInput(config_path=config_path).deserialize(config_data)

            surveillance_config = model.get_config()
            assert surveillance_config
            assert surveillance_config.api_doc_url == config_data[ConfigurationKey.API_DOC_URL.value]
            if config_data[ConfigurationKey.FAKE_API_SERVER.value] is not None:
                assert surveillance_config.fake_api_server
            if ConfigurationKey.GIT_INFO.value in config_data.keys() is not None:
                assert surveillance_config.fake_api_server
            if ConfigurationKey.GITHUB_INFO.value in config_data.keys() is not None:
                assert surveillance_config.fake_api_server
            if ConfigurationKey.ACCEPT_CONFIG_NOT_EXIST.value in config_data.keys() is not None:
                assert (
                    surveillance_config.accept_config_not_exist
                    == config_data[ConfigurationKey.ACCEPT_CONFIG_NOT_EXIST.value]
                )
