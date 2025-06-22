from typing import override

from app.form.base_form import BaseForm
from app.gateway.anki.anki_card_request import AnkiCardRequest


class AnkiCardForm(BaseForm):

    kanji: str = ""
    definition: str = ""
    sentence: str = ""

    def __init__(self, json_data: dict[str]):
        self.kanji = json_data.get("kanji", "")
        self.definition = json_data.get("definition", "")
        self.sentence = json_data.get("sentence", "")
        super().__init__()

    def to_req(self) -> AnkiCardRequest:
        return AnkiCardRequest(self.kanji, self.definition, self.sentence)

    @override
    def _validate(self):
        if not self.kanji:
            raise ValueError("Kanji field is required.")
        if not self.definition:
            raise ValueError("Definition field is required.")
        if not self.sentence:
            raise ValueError("Sentence field is required.")
