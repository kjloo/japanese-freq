class AnkiConfig:

    deck: int = -1
    kanji: str = ""
    definition: str = ""

    def __init__(self, deck: str, kanji: str, definition: str):
        self.deck = deck
        self.kanji = kanji
        self.definition = definition

    def __init__(self, json_data: dict[str]):
        self.deck = json_data.get("deck", -1)
        self.kanji = json_data.get("kanji", "")
        self.definition = json_data.get("definition", "")
        self._validate()

    def to_dict(self) -> dict[str]:
        return {
            "_id": self.deck,
            "kanji": self.kanji,
            "definition": self.definition
        }

    def _validate(self):
        if self.deck == -1:
            raise ValueError("Deck ID is required.")
        if not self.kanji:
            raise ValueError("Kanji field is required.")
        if not self.definition:
            raise ValueError("Definition field is required.")

    def __repr__(self):
        return (f"AnkiConfig(deck={self.deck}, "
                f"kanji={self.kanji}, "
                f"definition={self.definition})")
