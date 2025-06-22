from app.model.base_model import BaseModel
from typing import override


class AnkiSettings(BaseModel):

    deck_id: int = -1
    deck_name: str = ""
    model_name: str = ""
    kanji: str = ""
    definition: str = ""
    sentence: str = ""

    @override
    def to_dict(self) -> dict[str]:
        return {
            "deck_name": self.deck_name,
            "model_name": self.model_name,
            "kanji": self.kanji,
            "definition": self.definition,
            "sentence": self.sentence,
        }

    @override
    def from_dict(self, data: dict[str]):
        self.deck_id = data.get("deck_id", -1)
        self.deck_name = data.get("deck_name", "")
        self.model_name = data.get("model_name", "")
        self.kanji = data.get("kanji", "")
        self.definition = data.get("definition", "")
        self.sentence = data.get("sentence", "")

    @override
    def get_key(self) -> dict[str]:
        return {"_id": self.deck_id}
