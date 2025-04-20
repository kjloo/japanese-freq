import requests

from app.module.gateway_module import anki_server_url
from app.module.logging_module import logger
from app.module.app_module import app

ANKI_VERSION = 6


def post(action: str, params: dict = None) -> dict:
    """
    Send a request to the Anki server.
    :param action: The action to perform (e.g., "addNote").
    :param params: Additional parameters for the action.
    :return: The response from the Anki server.
    """
    payload = _anki_payload(action, params)
    logger.info(f"Sending payload to Anki {anki_server_url}: {payload}")
    response = requests.post(anki_server_url, json=payload)
    if response.status_code != 200:
        raise Exception(
            f"Anki server error: {response.status_code} - {response.text}")
    return response.json().get("result", {})


def _anki_payload(action: str, params: dict = None) -> dict:
    """
    Create a payload for Anki API requests.
    :param action: The action to perform (e.g., "addNote").
    :param params: Additional parameters for the action.
    :return: A dictionary representing the payload.
    """
    payload = {
        "action": action,
        "version": ANKI_VERSION,
    }
    if params:
        payload["params"] = params
    return payload
