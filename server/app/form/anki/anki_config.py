from app.form.base_form import BaseForm
from typing import override


class AnkiConfig(BaseForm):

    deck_id: int = -1
    kanji: str = ""
    definition: str = ""

    def __init__(self, deck_id: int, kanji: str, definition: str):
        self.deck_id = deck_id
        self.kanji = kanji
        self.definition = definition

    def __init__(self, json_data: dict[str]):
        self.deck_id = json_data.get("deck_id", -1)
        self.kanji = json_data.get("kanji", "")
        self.definition = json_data.get("definition", "")
        self._validate()

    @override
    def to_dict(self) -> dict[str]:
        return {
            "kanji": self.kanji,
            "definition": self.definition
        }

    @override
    def get_key(self) -> dict[str]:
        return {"_id": self.deck_id}

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
