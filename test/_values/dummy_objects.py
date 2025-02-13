import json
from typing import Mapping
from abc import ABC, abstractmethod

from urllib3 import BaseHTTPResponse


class DummyHTTPResponse(BaseHTTPResponse, ABC):

    @staticmethod
    @abstractmethod
    def mock_data() -> Mapping:
        pass


class DummySwaggerAPIDocConfigResponse(DummyHTTPResponse):

    @staticmethod
    def mock_data() -> Mapping:
        return {
            "swagger": "2.0",
            "tags": [],
            "paths": {},
            "definitions": {},
        }

    @property
    def data(self) -> bytes:
        return json.dumps(DummySwaggerAPIDocConfigResponse.mock_data()).encode("utf-8")


class DummyOpenAPIDocConfigResponse(DummyHTTPResponse):

    @staticmethod
    def mock_data() -> Mapping:
        return {
            "openapi": "3.0.1",
            "paths": {},
            "components": {
                "schemas": {},
            },
        }

    @property
    def data(self) -> bytes:
        return json.dumps(DummyOpenAPIDocConfigResponse.mock_data()).encode("utf-8")
