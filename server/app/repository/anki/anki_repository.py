from app.repository.base_repository import BaseRepository
from server.app.form.anki.anki_config import AnkiConfig


class AnkiRepository(BaseRepository):
    def __init__(self):
        super().__init__("anki")

    def add_config(self, config: AnkiConfig):
        # Add a list of words to the list in MongoDB
        self.collection.insert_one(
            config.to_dict(),
            upsert=True
        )


anki_repository = AnkiRepository()
