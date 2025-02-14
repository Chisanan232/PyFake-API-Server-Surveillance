from typing import Mapping, Any

from flask import Flask

from test._values.dummy_objects import DummyOpenAPIDocConfigResponse

app: Flask = Flask(__name__)


@app.route("/api-doc", methods=["GET"])
def api_doc() -> Mapping[str, Any]:
    return DummyOpenAPIDocConfigResponse.mock_data()
