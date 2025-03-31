from flask import Blueprint, jsonify

from service import io_service

# Blueprint for routes
io_routes = Blueprint('io_routes', __name__)


@io_routes.route("/api/io/inputs", methods=["GET"])
def get_inputs():
    inputs = io_service.get_inputs()
    return jsonify({"inputs": inputs}), 200
