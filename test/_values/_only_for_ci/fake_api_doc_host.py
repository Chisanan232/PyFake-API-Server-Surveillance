from test._values.dummy_objects import DummyOpenAPIDocConfigResponse
from typing import Any, Mapping

from flask import Flask

app: Flask = Flask(__name__)


@app.route("/api-doc", methods=["GET"])
def api_doc() -> Mapping[str, Any]:
    return DummyOpenAPIDocConfigResponse.mock_data()
