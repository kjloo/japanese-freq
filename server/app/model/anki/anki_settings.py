from bson import ObjectId
from app.model.base_model import BaseModel
from typing import override, Any


class AnkiSettings(BaseModel):
    _id: ObjectId = None  # Use None as default, let MongoDB generate if not set
    name: str = ""
    deck_id: int = -1
    deck_name: str = ""
    model_name: str = ""
    settings: dict[str, str] = {}

    @override
    def to_dict(self) -> dict:
        doc = {
            "name": self.name,
            "deck_id": self.deck_id,
            "deck_name": self.deck_name,
            "model_name": self.model_name,
            "settings": self.settings,
        }
        # Only include _id if it is not None
        if self._id is not None:
            doc["_id"] = str(self._id)
        return doc

    @override
    def from_dict(self, data: dict):
        self._id = data.get("_id")
        self.name = data.get("name", "")
        self.deck_id = data.get("deck_id", -1)
        self.deck_name = data.get("deck_name", "")
        self.model_name = data.get("model_name", "")
        self.settings = data.get("settings", {})

    @override
    def get_key(self) -> dict:
        # Only return _id if it is not None
        if self._id is not None:
            return {"_id": self._id}
