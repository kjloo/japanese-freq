from flask import Blueprint, jsonify, Response, request
from app.module.app_module import app
from app.module.logging_module import logger
from app.service.anki import anki_service, anki_settings_service
from app.form.anki.anki_settings_form import AnkiSettingsForm

anki_routes = Blueprint('anki_routes', __name__)


@anki_routes.route("/api/anki/decks", methods=["GET"])
def get_decks() -> Response:
    decks = anki_service.get_deck_names()
    return jsonify({"decks": decks}), 200


@anki_routes.route("/api/anki/models", methods=["GET"])
def get_models() -> Response:
    logger.debug("Fetching Anki models")
    models = anki_service.get_model_names()
    logger.debug(f"Retrieved models: {models}")
    return jsonify({"models": models}), 200


@anki_routes.route("/api/anki/models/<int:model_id>/fields", methods=["GET"])
def get_model_fields(model_id: int) -> Response:
    fields = anki_service.get_model_fields(model_id)
    return jsonify({"fields": fields}), 200


@anki_routes.route("/api/anki/decks/<int:deck_id>/cards", methods=["GET"])
def get_cards_in_deck(deck_id: int) -> Response:
    field_name = app.config.get("ANKI_FIELD_NAME", "Kanji")
    cards = anki_service.get_cards_in_deck(deck_id, field_name)
    return jsonify({"cards": cards}), 200


@anki_routes.route("/api/anki/decks/<int:deck_id>/cards", methods=["POST"])
def create_card_in_deck(deck_id: int) -> Response:
    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid data format"}), 400

    field_name = app.config.get("ANKI_FIELD_NAME", "Kanji")
    if field_name not in data:
        return jsonify({"error": f"Missing required field: {field_name}"}), 400

    try:
        anki_service.create_card_in_deck(deck_id, data[field_name])
        return jsonify({"message": "Card created successfully."}), 201
    except Exception as e:
        logger.error(f"Error creating card in deck {deck_id}: {e}")
        return jsonify({"error": str(e)}), 500


@anki_routes.route("/api/anki/config", methods=["GET"])
def get_anki_config_fields() -> Response:
    fields = anki_settings_service.get_anki_config_fields()
    return jsonify({"fields": fields}), 200


@anki_routes.route("/api/anki/config", methods=["POST"])
def save_anki_config() -> Response:
    data = request.get_json()
    payload = AnkiSettingsForm(data)
    anki_settings_service.save_anki_config(payload.to_model())
    return jsonify({"message": "Anki configuration saved successfully."}), 200
