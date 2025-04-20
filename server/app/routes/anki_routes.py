from flask import Blueprint, jsonify, Response
from app.module.app_module import app
from app.service import anki_service

anki_routes = Blueprint('anki_routes', __name__)


@anki_routes.route("/api/anki/decks", methods=["GET"])
def get_decks() -> Response:
    try:
        decks = anki_service.get_deck_names()
        return jsonify({"decks": decks}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@anki_routes.route("/api/anki/models", methods=["GET"])
def get_models() -> Response:
    try:
        models = anki_service.get_model_names()
        return jsonify({"models": models}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@anki_routes.route("/api/anki/models/<int:model_id>/fields", methods=["GET"])
def get_model_fields(model_id: int) -> Response:
    try:
        fields = anki_service.get_model_fields(model_id)
        return jsonify({"fields": fields}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@anki_routes.route("/api/anki/decks/<int:deck_id>/cards", methods=["GET"])
def get_cards_in_deck(deck_id: int) -> Response:
    try:
        field_name = app.config.get("ANKI_FIELD_NAME", "Kanji")
        cards = anki_service.get_cards_in_deck(deck_id, field_name)
        return jsonify({"cards": cards}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
