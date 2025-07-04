from typing import override

from app.form.base_form import BaseForm
from app.gateway.anki.anki_card_request import AnkiCardRequest


class AnkiCardForm(BaseForm):

    deck_id: int = None
    deck_name: str = ""
    model_name: str = ""
    settings: dict[str, str] = {}

    def __init__(self, deck_id: int, json_data: dict[str]):
        self.deck_id = deck_id
        self.deck_name = json_data.get("deck_name", "")
        self.model_name = json_data.get("model_name", "")
        self.settings = json_data.get("settings", "")
        super().__init__()

    def to_req(self) -> AnkiCardRequest:
        return AnkiCardRequest(
            self.deck_id, self.deck_name, self.model_name, self.settings
        )

    @override
    def _validate(self):
        if not self.deck_id:
            raise ValueError("Deck ID cannot be empty")
        if not self.deck_name:
            raise ValueError("Deck name cannot be empty")
        if not self.model_name:
            raise ValueError("Model name cannot be empty")
        if not self.settings:
            raise ValueError("Settings cannot be empty")
