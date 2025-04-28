from app.repository.base_repository import BaseRepository
from app.model.anki.anki_settings import AnkiSettings


class AnkiRepository(BaseRepository):
    def __init__(self):
        super().__init__("anki")

    def add_config(self, config: AnkiSettings):
        self.collection.update_one(
            config.get_key(),
            {"$set": config.to_dict()},
            upsert=True
        )


anki_repository = AnkiRepository()
