from http.client import HTTPException
from flask import Flask, jsonify
import logging

from app.serde.encoder import CustomJSONProvider
from app.module.socket_module import socketio
from app.module.config_module import config


# Initialize Flask app
app: Flask = Flask(
    __name__, static_folder="/app/static/assets", template_folder="/app/static"
)
app.json = CustomJSONProvider(app)
app.config.from_object(config)
app.logger.setLevel(app.config["LOG_LEVEL"])

# 400 - Bad Request


@app.errorhandler(KeyError)
@app.errorhandler(ValueError)
@app.errorhandler(TypeError)
def handle_bad_request(e):
    return jsonify({"error": str(e)}), 400


# 401 - Unauthorized


@app.errorhandler(PermissionError)
def handle_unauthorized(e):
    return jsonify({"error": "Unauthorized access"}), 401


# 403 - Forbidden


@app.errorhandler(PermissionError)
def handle_forbidden(e):
    return jsonify({"error": "Forbidden"}), 403


# 404 - Not Found


@app.errorhandler(FileNotFoundError)
@app.errorhandler(NotImplementedError)
def handle_not_found(e):
    return jsonify({"error": "Resource not found"}), 404


# 405 - Method Not Allowed (handled by Flask/Werkzeug)


@app.errorhandler(405)
def handle_method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405


# 409 - Conflict


@app.errorhandler(RuntimeError)
def handle_conflict(e):
    return jsonify({"error": "Conflict: " + str(e)}), 409


# 415 - Unsupported Media Type


@app.errorhandler(UnsupportedOperation := OSError)
def handle_unsupported_media_type(e):
    return jsonify({"error": "Unsupported media operation"}), 415


# 422 - Unprocessable Entity


@app.errorhandler(AttributeError)
def handle_unprocessable_entity(e):
    return jsonify({"error": "Unprocessable entity: " + str(e)}), 422


# 500 - Internal Server Error (catch-all)


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return jsonify({"error": e.description}), e.code
    return jsonify({"error": "Internal server error: " + str(e)}), 500


# Initialize SocketIO with async mode
socketio.init_app(app, cors_allowed_origins="*", async_mode="eventlet")
