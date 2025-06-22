from typing import override

from app.form.base_form import BaseForm
from app.model.anki.anki_settings import AnkiSettings


class AnkiSettingsForm(BaseForm):

    deck_id: int = -1
    config_name: str = ""
    deck_name: str = ""
    model_name: str = ""
    kanji: str = ""
    definition: str = ""
    sentence: str = ""

    def __init__(self, json_data: dict[str]):
        self.deck_id = json_data.get("deck_id", -1)
        self.config_name = json_data.get("config_name", "")
        self.deck_name = json_data.get("deck_name", "")
        self.model_name = json_data.get("model_name", "")
        self.kanji = json_data.get("kanji", "")
        self.definition = json_data.get("definition", "")
        self.sentence = json_data.get("sentence", "")
        super().__init__()

    def to_model(self) -> AnkiSettings:
        attrs = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        return AnkiSettings(attrs)

    @override
    def _validate(self):
        if self.deck_id == -1:
            raise ValueError("Deck ID is required.")
        if not self.config_name:
            raise ValueError("Configuration name is required.")
        if not self.deck_name:
            raise ValueError("Deck name is required.")
        if not self.model_name:
            raise ValueError("Model name is required.")
        if not self.kanji:
            raise ValueError("Kanji field is required.")
        if not self.definition:
            raise ValueError("Definition field is required.")
        if not self.sentence:
            raise ValueError("Sentence field is required.")

    def __repr__(self):
        return (f"AnkiConfig(deck={self.deck_id}, "
                f"config_name={self.config_name}, "
                f"deck_name={self.deck_name}, "
                f"model_name={self.model_name}, "
                f"kanji={self.kanji}, "
                f"definition={self.definition}), "
                f"sentence={self.sentence})")


def anki_config_form_fields() -> list[str]:
    return ["kanji", "definition", "sentence"]
