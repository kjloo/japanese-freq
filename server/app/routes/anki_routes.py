from flask import Blueprint, jsonify, Response, request
from app.module.app_module import app
from app.module.logging_module import logger
from app.service.anki import anki_service, anki_settings_service
from app.form.anki.anki_settings_form import AnkiSettingsForm
from app.form.anki.anki_card_form import AnkiCardForm
import app.mapper.mongo_json_mapper as mongo_json_mapper

anki_routes = Blueprint("anki_routes", __name__)


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
    payload = AnkiCardForm(deck_id, data)
    resp = anki_service.create_card_in_deck(payload.to_req())
    return jsonify({"note": resp}), 200


@anki_routes.route("/api/anki/configs/fields", methods=["GET"])
def get_anki_config_fields() -> Response:
    fields = anki_settings_service.get_anki_config_fields()
    return jsonify({"fields": fields}), 200


@anki_routes.route("/api/anki/configs", methods=["GET"])
def get_anki_configs() -> Response:
    configs = anki_settings_service.get_anki_configs()
    return (
        jsonify({"configs": [mongo_json_mapper.serialize_config(c) for c in configs]}),
        200,
    )


@anki_routes.route("/api/anki/configs/<string:config_id>", methods=["GET"])
def get_anki_config(config_id: str) -> Response:
    config = anki_settings_service.get_anki_config(config_id)
    if not config:
        return jsonify({"error": "Configuration not found"}), 404
    return jsonify({"config": mongo_json_mapper.serialize_config(config)}), 200


@anki_routes.route("/api/anki/configs", methods=["POST"])
def save_anki_config() -> Response:
    data = request.get_json()
    payload = AnkiSettingsForm(data)
    anki_settings_service.save_anki_config(payload.to_model())
    return jsonify({"message": "Anki configuration saved successfully."}), 200
