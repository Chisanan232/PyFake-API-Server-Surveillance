import json
from abc import ABC, abstractmethod
from typing import Mapping

from urllib3 import BaseHTTPResponse


class DummyHTTPResponse(BaseHTTPResponse, ABC):

    @staticmethod
    @abstractmethod
    def mock_data() -> Mapping:
        pass

    @classmethod
    def generate(cls, request_url: str) -> "DummyHTTPResponse":
        return cls(
            request_url=request_url,
            status=200,
            version=11,
            version_string="HTTP/1.1",
            reason="",
            decode_content=True,
        )


class DummySwaggerAPIDocConfigResponse(DummyHTTPResponse):

    @staticmethod
    def mock_data() -> Mapping:
        return {
            "swagger": "2.0",
            "tags": [],
            "paths": {
                "/api/v1/test/foo": {
                    "get": {
                        "tags": [],
                        "summary": "This is Foo API",
                        "description": "  400 - Bad request error\n 401 - Unauthorized error\n 404 - Not found voucher\n 500 - Unexpected error\n",
                        "operationId": "",
                        "produces": ["*/*"],
                        "parameters": [],
                        "responses": {"200": {"description": "OK", "schema": {"$ref": "#/definitions/Unit"}}},
                    },
                },
            },
            "definitions": {
                "Unit": {"type": "object", "title": "Unit"},
            },
        }

    @property
    def data(self) -> bytes:
        return json.dumps(DummySwaggerAPIDocConfigResponse.mock_data()).encode("utf-8")


class DummyOpenAPIDocConfigResponse(DummyHTTPResponse):

    @staticmethod
    def mock_data() -> Mapping:
        return {
            "openapi": "3.0.1",
            "paths": {
                "/api/v1/test/foo": {
                    "get": {
                        "tags": [],
                        "summary": "This is Foo API",
                        "description": "  400 - Bad request error\n 401 - Unauthorized error\n 404 - Not found voucher\n 500 - Unexpected error\n",
                        "operationId": "",
                        "parameters": [],
                        "responses": {
                            "200": {
                                "description": "OK",
                                "content": {"*/*": {"schema": {"$ref": "#/components/schemas/Unit"}}},
                            }
                        },
                    },
                },
            },
            "components": {
                "schemas": {
                    "Unit": {"type": "object", "title": "Unit"},
                },
            },
        }

    @property
    def data(self) -> bytes:
        return json.dumps(DummyOpenAPIDocConfigResponse.mock_data()).encode("utf-8")
