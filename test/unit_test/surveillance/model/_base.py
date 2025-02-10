import os
from abc import ABCMeta, abstractmethod
from typing import Type, Mapping
from unittest.mock import patch

import pytest

from ci.surveillance.model._base import _BaseModel


class _BaseModelTestSuite(metaclass=ABCMeta):

    @abstractmethod
    @pytest.fixture(scope="function")
    def model(self) -> Type[_BaseModel]:
        pass

    @pytest.mark.parametrize("data", [])
    def test_deserialize(self, model: Type[_BaseModel], data: Mapping):
        if not data:
            assert False, "Please implement the parameter values for testing."

        with patch.dict(os.environ, data, clear=True):
            model = model.deserialize(data)
            self._verify_model_props(model, data)

    @abstractmethod
    def _verify_model_props(self, model: _BaseModel, original_data: Mapping) -> None:
        pass
