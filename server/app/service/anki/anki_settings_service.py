from app.form.anki import anki_settings_form
from app.model.anki.anki_settings import AnkiSettings
from app.repository.anki.anki_repository import anki_repository


def get_anki_config_fields() -> list[str]:
    """
    Get the fields of the Anki configuration.
    :return: A list of field names for the Anki configuration.
    """
    return anki_settings_form.anki_config_form_fields()


def save_anki_config(data: AnkiSettings) -> AnkiSettings:
    """
    Save the Anki configuration.
    :param data: The Anki configuration data.
    :return: The saved Anki configuration.
    """
    anki_repository.add_config(data)
    return data
