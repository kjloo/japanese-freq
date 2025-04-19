from flask import jsonify, Response

from app.gateway import anki_gateway


def get_deck_names() -> Response:
    """
    Get the names of all decks in Anki.
    :return: A list of deck names.
    """
    response = anki_gateway.post("deckNames")
    return jsonify({"decks": response}), 200
