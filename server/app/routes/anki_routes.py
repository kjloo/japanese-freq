from flask import Blueprint
from app.module.app_module import app
from app.service import anki_service

anki_routes = Blueprint('anki_routes', __name__)


@anki_routes.route("/api/anki/decks", methods=["GET"])
def get_decks():
    resp = anki_service.get_deck_names()
    return resp


@anki_routes.route("/api/anki/models", methods=["GET"])
def get_models():
    resp = anki_service.get_model_names()
    return resp


@anki_routes.route("/api/anki/models/<int:model_id>/fields", methods=["GET"])
def get_model_fields(model_id: int):
    resp = anki_service.get_model_fields(model_id)
    return resp
