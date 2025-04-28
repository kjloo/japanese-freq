from typing import override

from app.form.base_form import BaseForm
from app.model.anki.anki_config import AnkiConfig


class AnkiConfigForm(BaseForm):

    deck_id: int = -1
    kanji: str = ""
    definition: str = ""

    def __init__(self, json_data: dict[str]):
        self.deck_id = json_data.get("deck_id", -1)
        self.kanji = json_data.get("kanji", "")
        self.definition = json_data.get("definition", "")
        super().__init__()

    def to_model(self) -> AnkiConfig:
        return AnkiConfig(self.deck_id, self.kanji, self.definition)

    @override
    def _validate(self):
        if self.deck_id == -1:
            raise ValueError("Deck ID is required.")
        if not self.kanji:
            raise ValueError("Kanji field is required.")
        if not self.definition:
            raise ValueError("Definition field is required.")

    def __repr__(self):
        return (f"AnkiConfig(deck={self.deck_id}, "
                f"kanji={self.kanji}, "
                f"definition={self.definition})")


def anki_config_form_fields() -> list[str]:
    return ["deck_id", "kanji", "definition"]
