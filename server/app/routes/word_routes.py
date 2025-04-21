from flask import Blueprint, jsonify, Response, request

from app.service import word_service

# Blueprint for routes
word_routes = Blueprint('word_routes', __name__)


@word_routes.route("/api/word/ignore-list/sync", methods=["POST"])
def sync_ignore_list() -> Response:
    data = request.get_json()
    deck_id = data.get("deck_id")
    field_name = data.get("field_name")
    word_service.update_from_anki(deck_id, field_name)
    response = word_service.update_from_file()
    return jsonify({"ignore_list": response}), 200
