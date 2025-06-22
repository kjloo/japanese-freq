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

    def get_config(self, deck_id: int) -> AnkiSettings:
        config_data = self.collection.find_one({"_id": deck_id})
        if config_data:
            return AnkiSettings(
                deck_id=config_data["_id"],
                kanji=config_data.get("kanji", ""),
                definition=config_data.get("definition", ""),
                sentence=config_data.get("sentence", "")
            )
        return None


anki_repository = AnkiRepository()
