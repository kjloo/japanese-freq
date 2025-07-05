from app.model.anki.anki_settings import AnkiSettings
from bson import ObjectId


class AnkiRepository:
    def upsert_config(self, config: AnkiSettings):
        """
        Inserts a new AnkiSettings document or updates an existing one based on the presence of _id.
        If _id is present, it updates the existing document; otherwise, it creates a new one.
        """
        config.save()

    def get_config(self, config_id: str) -> AnkiSettings | None:
        try:
            return AnkiSettings.objects(id=ObjectId(config_id)).first()
        except Exception:
            return None

    def get_all_configs(self) -> list[AnkiSettings]:
        return list(AnkiSettings.objects.all())


anki_repository = AnkiRepository()
