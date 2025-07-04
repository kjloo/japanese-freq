from app.model.anki.anki_settings import AnkiSettings
from bson import ObjectId


class AnkiRepository:
    def add_config(self, config: AnkiSettings):
        # Save or update using mongoengine's API
        config.save()  # This will insert or update based on the presence of _id

    def get_config(self, config_id: str) -> AnkiSettings | None:
        try:
            return AnkiSettings.objects(id=ObjectId(config_id)).first()
        except Exception:
            return None

    def get_all_configs(self) -> list[AnkiSettings]:
        return list(AnkiSettings.objects.all())


anki_repository = AnkiRepository()
