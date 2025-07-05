from app.model.anki.anki_settings import AnkiSettings
from app.repository.anki.anki_repository import anki_repository
from app.model.anki.anki_values import AnkiValues


def get_anki_config_fields() -> list[str]:
    """
    Get the fields of the Anki configuration.
    :return: A list of field names for the Anki configuration.
    """
    return AnkiValues.attributes()


def save_anki_config(data: AnkiSettings) -> AnkiSettings:
    """
    Save the Anki configuration.
    :param data: The Anki configuration data.
    :return: The saved Anki configuration.
    """
    anki_repository.upsert_config(data)
    return data


def get_anki_config(config_id: int) -> AnkiSettings:
    """
    Get the Anki configuration for a specific deck.
    :param config_id: The ID of the deck.
    :return: The Anki configuration for the specified deck.
    """
    return anki_repository.get_config(config_id)


def get_anki_configs() -> list[AnkiSettings]:
    """
    Get all Anki configurations.
    :return: A list of all Anki configurations.
    """
    return anki_repository.get_all_configs()
