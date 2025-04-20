from flask import jsonify, Response

from app.module.logging_module import logger
from app.gateway import anki_gateway


def get_deck_names() -> Response:
    """
    Get the names of all decks in Anki.
    :return: A list of deck names.
    """
    response = _get_deck_names()
    if not response:
        return jsonify({"error": "No decks found"}), 404
    return jsonify({"decks": response}), 200


def get_model_names() -> Response:
    """
    Get the names of all models in Anki.
    :return: A list of model names.
    """
    response = _get_model_names()
    if not response:
        return jsonify({"error": "No models found"}), 404
    return jsonify({"models": response}), 200


def get_model_fields(model_id: int) -> Response:
    """
    Get the fields of a specific model in Anki.
    :param model_id: The id of the model.
    :return: A list of field names for the specified model.
    """
    logger.debug(f"Fetching fields for model ID: {model_id}")
    model = _find_models_by_ids([model_id])
    if not model:
        return jsonify({"error": f"Model {model_id} not found"}), 404
    logger.debug(f"Model data: {model}")
    if not model:
        return jsonify({"error": f"Model {model_id} not found"}), 404
    model_name = model[0]["name"]

    response = _get_model_fields(model_name)
    if not response:
        return jsonify({"error": f"No fields found for model '{model_name}'"}), 404
    return jsonify({"fields": response}), 200


def get_cards_in_deck(deck_id: int, field_name: str) -> Response:
    """
    Get all cards in a specific deck and output the value of a specific field.

    :param deck_id: The id of the deck.
    :param field_name: The name of the field to extract.
    :return: A list of field values for the specified field in the deck.
    """
    logger.debug(f"Fetching cards for deck: {deck_id}")
    if not isinstance(deck_id, int):
        return jsonify({"error": "Deck ID must be an integer"}), 400
    decks = _get_deck_names()
    if not decks:
        return jsonify({"error": "No decks found"}), 404
    decks = {v: k for k, v in decks.items()}

    logger.debug(f"Decks: {decks}")
    if deck_id not in decks.keys():
        return jsonify({"error": f"Deck {deck_id} not found"}), 404
    deck_name = decks[deck_id]

    card_ids = _find_cards(deck_name)
    if not card_ids:
        return jsonify({"error": f"No cards found in deck '{deck_name}'"}), 404

    notes = _find_notes(card_ids)
    if not notes:
        return jsonify({"error": f"No notes found for cards in deck '{deck_name}'"}), 404

    note_data = _get_note_data(notes)
    if not note_data:
        return jsonify({"error": f"No note data found for notes in deck '{deck_name}'"}), 404

    field_values = []
    for note in note_data:
        if field_name in note["fields"]:
            field_values.append(note["fields"][field_name]["value"])
        else:
            logger.warning(
                f"Field '{field_name}' not found in note: {note['noteId']}")

    return jsonify({"field_values": field_values}), 200


def _get_deck_names() -> dict[str, int]:
    """
    Get the names of all decks in Anki.
    :return: A list of deck names.
    """
    response = anki_gateway.post("deckNamesAndIds")
    return response


def _find_cards(deck_name: str) -> list[int]:
    """
    Find all cards in a specific deck.
    :param deck_id: The id of the deck.
    :return: A list of card IDs in the specified deck.
    """
    card_ids = anki_gateway.post(
        "findCards", {"query": f"deck:\"{deck_name}\""})
    logger.debug(f"Card IDs: {card_ids}")
    return card_ids


def _find_notes(card_ids: list[int]) -> list[int]:
    """
    Find all notes associated with a list of card IDs.
    :param card_ids: A list of card IDs.
    :return: A list of note IDs associated with the specified card IDs.
    """
    notes = anki_gateway.post("cardsToNotes", {"cards": card_ids})
    logger.debug(f"Note IDs: {notes}")
    return notes


def _get_note_data(note_ids: list[int]) -> list[dict]:
    """
    Get the data for a specific note ID.
    :param note_id: The id of the note.
    :return: The data for the specified note ID.
    """
    # Get note data and extract the specified field
    note_data = anki_gateway.post("notesInfo", {"notes": note_ids})
    logger.debug(f"Note data: {note_data}")
    return note_data


def _get_model_names() -> str:
    """
    Get the name of a specific model in Anki.
    :return: The name of the specified model.
    """
    response = anki_gateway.post("modelNamesAndIds")
    return response


def _get_model_fields(model_name: str) -> dict:
    """
    Get the fields of a specific model in Anki.
    :param model_name: The name of the model.
    :return: A list of field names for the specified model.
    """
    response = anki_gateway.post("modelFieldNames", {"modelName": model_name})
    return response


def _find_models_by_ids(model_ids: list[int]) -> list[dict]:
    """
    Find all models associated with a list of model IDs.
    :param model_ids: A list of model IDs.
    :return: A list of model data associated with the specified model IDs.
    """
    response = anki_gateway.post(
        "findModelsById", {"modelIds": model_ids})
    return response
