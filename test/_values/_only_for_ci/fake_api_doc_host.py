from test._values.dummy_objects import DummyOpenAPIDocConfigResponse
from typing import Any, Mapping

from flask import Flask

app: Flask = Flask(__name__)


@app.route("/api-doc", methods=["GET"])
def foo_home() -> Mapping[str, Any]:
    print(f"[DEBUG] run API ...")
    return DummyOpenAPIDocConfigResponse.mock_data()
