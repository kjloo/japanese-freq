from mongoengine import Document, StringField, IntField, DictField


class AnkiSettings(Document):
    name = StringField(required=True, unique=True)
    deck_id = IntField(required=True)
    deck_name = StringField(required=True)
    model_name = StringField(required=True)
    settings = DictField()

    meta = {
        'collection': 'anki_settings'
    }
