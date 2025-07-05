from mongoengine import Document, StringField, IntField, DictField, ListField


class WordList(Document):
    words = ListField()

    meta = {"collection": "word_list"}
