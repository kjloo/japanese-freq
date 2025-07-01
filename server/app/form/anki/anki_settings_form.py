from typing import override

from app.form.base_form import BaseForm
from app.model.anki.anki_settings import AnkiSettings


class AnkiSettingsForm(BaseForm):

    name: str = ""
    deck_id: int = -1
    deck_name: str = ""
    model_name: str = ""
    settings: dict[str, str] = {}

    def __init__(self, json_data: dict[str]):
        self.name = json_data.get("name", "")
        self.deck_id = json_data.get("deck_id", -1)
        self.deck_name = json_data.get("deck_name", "")
        self.model_name = json_data.get("model_name", "")
        self.settings = json_data.get("settings", {})
        super().__init__()

    def to_model(self) -> AnkiSettings:
        attrs = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return AnkiSettings(attrs)

    @override
    def _validate(self):
        if not self.name:
            raise ValueError("Configuration name is required.")
        if self.deck_id == -1:
            raise ValueError("Deck ID is required.")
        if not self.deck_name:
            raise ValueError("Deck name is required.")
        if not self.model_name:
            raise ValueError("Model name is required.")
        if not self.settings:
            raise ValueError("Settings must not be empty.")

    def __repr__(self):
        return (
            f"AnkiConfig("
            f"name={self.name}, "
            f"deck_id={self.deck_id}, "
            f"deck_name={self.deck_name}, "
            f"model_name={self.model_name}, "
            f"settings={self.settings})"
        )


def anki_config_form_fields() -> list[str]:
    return [
        "audio",
        "conjugation",
        "definition",
        "hiragana",
        "kanji",
        "part_of_speech",
        "pitch_accent",
        "romaji",
        "sentence",
        "translation",
    ]
