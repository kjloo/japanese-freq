from app.repository.base_repository import BaseRepository
from app.model.anki.anki_settings import AnkiSettings
from bson import ObjectId


class AnkiRepository(BaseRepository):
    def __init__(self):
        super().__init__("anki")

    def add_config(self, config: AnkiSettings):
        if config._id is not None:
            self.collection.update_one(
                config.get_key(),
                {"$set": config.to_dict()},
                upsert=True
            )
        else:
            # Remove _id from dict to let MongoDB generate it
            doc = config.to_dict()
            doc.pop("_id", None)
            self.collection.insert_one(doc)

    def get_config(self, config_id: str) -> AnkiSettings:
        # Convert to ObjectId if it's a string
        id = ObjectId(config_id)
        config_data = self.collection.find_one({"_id": id})
        if config_data:
            return AnkiSettings(config_data)
        return None

    def get_all_configs(self) -> list[AnkiSettings]:
        configs = []
        for config_data in self.collection.find():
            configs.append(AnkiSettings(config_data))
        return configs


anki_repository = AnkiRepository()
