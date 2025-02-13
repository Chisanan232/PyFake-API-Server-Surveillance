import json

from urllib3 import BaseHTTPResponse


class DummySwaggerAPIDocConfigResponse(BaseHTTPResponse):

    @property
    def data(self) -> bytes:
        _data = {
            "swagger": "2.0",
            "tags": [],
            "paths": {},
            "definitions": {},
        }
        return json.dumps(_data).encode("utf-8")


class DummyOpenAPIDocConfigResponse(BaseHTTPResponse):

    @property
    def data(self) -> bytes:
        _data = {
            "openapi": "3.0.1",
            "paths": {},
            "components": {
                "schemas": {},
            },
        }
        return json.dumps(_data).encode("utf-8")
