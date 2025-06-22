from typing import override

from app.form.base_form import BaseForm
from app.model.anki.anki_settings import AnkiSettings


class AnkiSettingsForm(BaseForm):

    deck_id: int = -1
    deck_name: str = ""
    kanji: str = ""
    definition: str = ""
    sentence: str = ""

    def __init__(self, json_data: dict[str]):
        self.deck_id = json_data.get("deck_id", -1)
        self.deck_name = json_data.get("deck_name", "")
        self.kanji = json_data.get("kanji", "")
        self.definition = json_data.get("definition", "")
        self.sentence = json_data.get("sentence", "")
        super().__init__()

    def to_model(self) -> AnkiSettings:
        return AnkiSettings(self.deck_id, self.deck_name, self.kanji, self.definition, self.sentence)

    @override
    def _validate(self):
        if self.deck_id == -1:
            raise ValueError("Deck ID is required.")
        if not self.deck_name:
            raise ValueError("Deck name is required.")
        if not self.kanji:
            raise ValueError("Kanji field is required.")
        if not self.definition:
            raise ValueError("Definition field is required.")
        if not self.sentence:
            raise ValueError("Sentence field is required.")

    def __repr__(self):
        return (f"AnkiConfig(deck={self.deck_id}, "
                f"deck_name={self.deck_name}, "
                f"kanji={self.kanji}, "
                f"definition={self.definition}), "
                f"sentence={self.sentence})")


def anki_config_form_fields() -> list[str]:
    return ["kanji", "definition", "sentence"]
