from flask import Blueprint
from app.module.app_module import app
from app.service import anki_service

anki_routes = Blueprint('anki_routes', __name__)


@anki_routes.route("/api/anki/decks", methods=["GET"])
def get_decks():
    resp = anki_service.get_deck_names()
    return resp
