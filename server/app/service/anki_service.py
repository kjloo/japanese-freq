from flask import jsonify, Response

from app.module.logging_module import logger
from app.gateway import anki_gateway


def get_deck_names() -> Response:
    """
    Get the names of all decks in Anki.
    :return: A list of deck names.
    """
    response = anki_gateway.post("deckNamesAndIds")
    return jsonify({"decks": response}), 200


def get_model_names() -> Response:
    """
    Get the names of all models in Anki.
    :return: A list of model names.
    """
    response = anki_gateway.post("modelNamesAndIds")
    return jsonify({"models": response}), 200


def get_model_fields(model_id: int) -> Response:
    """
    Get the fields of a specific model in Anki.
    :param model_id: The id of the model.
    :return: A list of field names for the specified model.
    """
    logger.debug(f"Fetching fields for model ID: {model_id}")
    model = anki_gateway.post(
        "findModelsById", {"modelIds": [model_id]})
    logger.debug(f"Model data: {model}")
    if not model:
        return jsonify({"error": f"Model {model_id} not found"}), 404
    model_name = model[0]["name"]
    response = anki_gateway.post("modelFieldNames", {"modelName": model_name})
    return jsonify({"fields": response}), 200
