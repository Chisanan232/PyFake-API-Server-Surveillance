import pytest
from fake_api_server import FakeAPIConfig
from fake_api_server.model import (
    HTTP,
    APIParameter,
    HTTPRequest,
    HTTPResponse,
    MockAPI,
    MockAPIs,
)
from fake_api_server.model.api_config.apis import ResponseStrategy

try:
    from http import HTTPMethod
except ImportError:
    from fake_api_server.model.http import HTTPMethod  # type: ignore[assignment]

from fake_api_server_plugin.ci.surveillance.model.compare import CompareInfo


class TestCompareInfo:

    @pytest.fixture(scope="module")
    def local_config_model(self) -> FakeAPIConfig:
        return FakeAPIConfig(
            apis=MockAPIs(
                apis={
                    "get_test_v1_sample": MockAPI(
                        url="/test/v1/sample",
                        http=HTTP(
                            request=HTTPRequest(
                                method="GET", parameters=[APIParameter(name="value", value_type="str")]
                            ),
                            response=HTTPResponse(strategy=ResponseStrategy.STRING, value="test"),
                        ),
                    ),
                    "post_test_v1_sample": MockAPI(
                        url="/test/v1/sample",
                        http=HTTP(
                            request=HTTPRequest(method="POST"),
                            response=HTTPResponse(strategy=ResponseStrategy.STRING, value="test"),
                        ),
                    ),
                    "get_test_v1_deprecate": MockAPI(
                        url="/test/v1/deprecate",
                        http=HTTP(
                            request=HTTPRequest(method="GET"),
                            response=HTTPResponse(strategy=ResponseStrategy.STRING, value="test"),
                        ),
                    ),
                },
            ),
        )

    @pytest.fixture(scope="module")
    def remote_config_model(self) -> FakeAPIConfig:
        return FakeAPIConfig(
            apis=MockAPIs(
                apis={
                    "get_test_v1_sample": MockAPI(
                        url="/test/v1/sample",
                        http=HTTP(
                            request=HTTPRequest(
                                method="GET",
                                parameters=[
                                    APIParameter(name="value", value_type="str"),
                                    APIParameter(name="id", value_type="str"),
                                ],
                            ),
                            response=HTTPResponse(strategy=ResponseStrategy.STRING, value="test"),
                        ),
                    ),
                    "post_test_v1_sample": MockAPI(
                        url="/test/v1/sample",
                        http=HTTP(
                            request=HTTPRequest(method="POST"),
                            response=HTTPResponse(strategy=ResponseStrategy.STRING, value="test"),
                        ),
                    ),
                    "get_test_v1_new": MockAPI(
                        url="/test/v1/new",
                        http=HTTP(
                            request=HTTPRequest(method="GET"),
                            response=HTTPResponse(strategy=ResponseStrategy.STRING, value="test"),
                        ),
                    ),
                    "post_test_v1_new": MockAPI(
                        url="/test/v1/new",
                        http=HTTP(
                            request=HTTPRequest(method="POST"),
                            response=HTTPResponse(strategy=ResponseStrategy.STRING, value="test"),
                        ),
                    ),
                    "put_test_v1_new": MockAPI(
                        url="/test/v1/new",
                        http=HTTP(
                            request=HTTPRequest(method="PUT"),
                            response=HTTPResponse(strategy=ResponseStrategy.STRING, value="test"),
                        ),
                    ),
                },
            ),
        )

    @pytest.fixture(scope="function")
    def model(self, local_config_model: FakeAPIConfig, remote_config_model: FakeAPIConfig) -> CompareInfo:
        return CompareInfo(
            local_model=local_config_model,
            remote_model=remote_config_model,
        )

    def test_has_different(self, model: CompareInfo):
        assert model.has_different() is True
        change_detail = model.change_detail

        apis = change_detail.apis
        assert apis.keys() == {"/test/v1/sample", "/test/v1/deprecate", "/test/v1/new"}
        assert apis["/test/v1/sample"] == [HTTPMethod.GET]
        assert apis["/test/v1/deprecate"] == [HTTPMethod.GET]
        assert apis["/test/v1/new"] == [HTTPMethod.GET, HTTPMethod.POST, HTTPMethod.PUT]

        change_statistical = change_detail.change_statistical
        assert change_statistical.add == len(apis["/test/v1/new"])
        assert change_statistical.update == len(apis["/test/v1/sample"])
        assert change_statistical.delete == len(apis["/test/v1/deprecate"])
