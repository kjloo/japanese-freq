from flask import Blueprint, Response, jsonify
from module.logging_module import logger

# Blueprint for routes
debug_routes = Blueprint('debug_routes', __name__)


class Foo:
    def __init__(self):
        self.a: int = 4
        self.b: str = "hello"
        self.c: dict[int, str] = {1: "one", 2: "two"}

    def to_dict(self):
        logger.debug("Converting Foo to JSON")
        return {
            "a": self.a,
            "b": self.b,
            "c": self.c
        }


@debug_routes.route("/api/debug/serde", methods=["GET"])
def get_inputs() -> Response:
    logger.debug("Received request for /api/debug/serde")
    foo = Foo()
    return jsonify(foo)
