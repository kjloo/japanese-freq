from app.module.logging_module import logger
from server.app.gateway.anki import anki_gateway
from server.app.gateway.anki.anki_card_request import AnkiCardRequest
from server.app.service.anki import anki_settings_service


def create_card_in_deck(deck_id: int, card: AnkiCardRequest) -> None:
    """
    Create a card in a specific deck in Anki.
    :param deck_id: The ID of the deck.
    :param card: AnkiCardRequest object containing card details.
    :raises ValueError: If the deck ID is invalid or if the card creation fails.
    """
    config = anki_settings_service.get_anki_config(deck_id)
    return _create_card(deck_id, card)


def get_deck_names() -> dict[str, int]:
    """
    Get the names of all decks in Anki.
    :return: A dictionary of deck names and their IDs.
    """
    return _get_deck_names()


def get_model_names() -> dict[str, int]:
    """
    Get the names of all models in Anki.
    :return: A dictionary of model names and their IDs.
    """
    return _get_model_names()


def get_model_fields(model_id: int) -> list[str]:
    """
    Get the fields of a specific model in Anki.
    :param model_id: The ID of the model.
    :return: A list of field names for the specified model.
    """
    logger.debug(f"Fetching fields for model ID: {model_id}")
    model = _find_models_by_ids([model_id])
    model_name = model[0]["name"]

    return _get_model_fields(model_name)


def get_cards_in_deck(deck_id: int, field_name: str) -> list[str]:
    """
    Get all cards in a specific deck and output the value of a specific field.

    :param deck_id: The ID of the deck.
    :param field_name: The name of the field to extract.
    :return: A list of field values for the specified field in the deck.
    """
    logger.debug(f"Fetching cards for deck: {deck_id}")
    if not isinstance(deck_id, int):
        raise ValueError("Deck ID must be an integer")

    decks = _get_deck_names()
    decks = {v: k for k, v in decks.items()}

    logger.debug(f"Decks: {decks}")
    if deck_id not in decks.keys():
        raise ValueError(f"Deck {deck_id} not found")
    deck_name = decks[deck_id]

    card_ids = _find_cards(deck_name)
    notes = _find_notes(card_ids)
    note_data = _get_note_data(notes)

    field_values = []
    for note in note_data:
        if field_name in note["fields"]:
            field_values.append(note["fields"][field_name]["value"])
        else:
            logger.warning(
                f"Field '{field_name}' not found in note: {note['noteId']}")

    return field_values


def _create_card(deck_id: int, card: AnkiCardRequest) -> None:
    """
    Create a card in a specific deck.
    :param deck_id: The ID of the deck.
    :param card: AnkiCardRequest object containing card details.
    """
    config = anki_settings_service.get_anki_config(deck_id)
    if not config:
        raise ValueError(f"No Anki configuration found for deck ID {deck_id}")

    model_name = config.model_name
    fields = {
        "kanji": card.kanji,
        "definition": card.definition,
        "sentence": card.sentence
    }

    note = {
        "deckName": config.deck_name,
        "modelName": model_name,
        "fields": fields,
        "tags": config.tags
    }

    response = anki_gateway.post("addNote", {"note": note})
    if not response:
        raise ValueError("Failed to create card in Anki")


def _get_deck_names() -> dict[str, int]:
    """
    Get the names of all decks in Anki.
    :return: A dictionary of deck names and their IDs.
    """
    response = anki_gateway.post("deckNamesAndIds")
    if not response:
        raise ValueError("No decks found")
    return response


def _find_cards(deck_name: str) -> list[int]:
    """
    Find all cards in a specific deck.
    :param deck_name: The name of the deck.
    :return: A list of card IDs in the specified deck.
    """
    card_ids = anki_gateway.post(
        "findCards", {"query": f"deck:\"{deck_name}\""})
    if not card_ids:
        raise ValueError(f"No cards found in deck '{deck_name}'")
    logger.debug(f"Card IDs: {card_ids}")
    return card_ids


def _find_notes(card_ids: list[int]) -> list[int]:
    """
    Find all notes associated with a list of card IDs.
    :param card_ids: A list of card IDs.
    :return: A list of note IDs associated with the specified card IDs.
    """
    notes = anki_gateway.post("cardsToNotes", {"cards": card_ids})
    if not notes:
        raise ValueError("No notes found for the given cards")
    logger.debug(f"Note IDs: {notes}")
    return notes


def _get_note_data(note_ids: list[int]) -> list[dict]:
    """
    Get the data for a specific note ID.
    :param note_ids: A list of note IDs.
    :return: The data for the specified note IDs.
    """
    note_data = anki_gateway.post("notesInfo", {"notes": note_ids})
    if not note_data:
        raise ValueError("No note data found for the given notes")
    logger.debug(f"Note data: {note_data}")
    return note_data


def _get_model_names() -> dict[str, int]:
    """
    Get the names of all models in Anki.
    :return: A dictionary of model names and their IDs.
    """
    response = anki_gateway.post("modelNamesAndIds")
    if not response:
        raise ValueError("No models found")
    return response


def _get_model_fields(model_name: str) -> list[str]:
    """
    Get the fields of a specific model in Anki.
    :param model_name: The name of the model.
    :return: A list of field names for the specified model.
    """
    response = anki_gateway.post("modelFieldNames", {"modelName": model_name})
    if not response:
        raise ValueError(f"No fields found for model '{model_name}'")
    return response


def _find_models_by_ids(model_ids: list[int]) -> list[dict]:
    """
    Find all models associated with a list of model IDs.
    :param model_ids: A list of model IDs.
    :return: A list of model data associated with the specified model IDs.
    """
    response = anki_gateway.post("findModelsById", {"modelIds": model_ids})
    if not response:
        raise ValueError(f"No models found for IDs: {model_ids}")
    return response
