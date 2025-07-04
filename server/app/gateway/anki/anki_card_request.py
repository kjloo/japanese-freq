class AnkiCardRequest(object):
    deck_id: int
    deck_name: str
    model_name: str
    settings: dict[str, str]
    values: dict[str, str]

    def __init__(
        self, deck_id: int, deck_name: str, model_name: str, settings: dict[str, str]
    ):
        self.deck_id = deck_id
        self.deck_name = deck_name
        self.model_name = model_name
        self.settings = settings
        self.values = {}

    def set_values(self, values: dict[str, str]):
        self.values = values
