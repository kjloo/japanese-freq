from mongoengine import Document, ListField


class WordList(Document):
    words = ListField()

    meta = {"collection": "word_list"}
