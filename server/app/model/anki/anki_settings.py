from app.model.base_model import BaseModel
from typing import override


class AnkiSettings(BaseModel):

    deck_id: int = -1
    deck_name: str = ""
    kanji: str = ""
    definition: str = ""
    sentence: str = ""

    def __init__(self, deck_id: int, deck_name: str, kanji: str, definition: str, sentence: str):
        self.deck_id = deck_id
        self.deck_name = deck_name
        self.kanji = kanji
        self.definition = definition
        self.sentence = sentence

    @override
    def to_dict(self) -> dict[str]:
        return {
            "deck_name": self.deck_name,
            "kanji": self.kanji,
            "definition": self.definition,
            "sentence": self.sentence,
        }

    @override
    def get_key(self) -> dict[str]:
        return {"_id": self.deck_id}
