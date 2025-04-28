from app.model.base_model import BaseModel
from typing import override


class AnkiConfig(BaseModel):

    deck_id: int = -1
    kanji: str = ""
    definition: str = ""

    def __init__(self, deck_id: int, kanji: str, definition: str):
        self.deck_id = deck_id
        self.kanji = kanji
        self.definition = definition

    @override
    def to_dict(self) -> dict[str]:
        return {
            "kanji": self.kanji,
            "definition": self.definition
        }

    @override
    def get_key(self) -> dict[str]:
        return {"_id": self.deck_id}
