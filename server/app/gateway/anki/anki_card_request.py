

class AnkiCardRequest(object):
    kanji: str = ""
    definition: str = ""
    sentence: str = ""

    def __init__(self, kanji: str, definition: str, sentence: str):
        self.kanji = kanji
        self.definition = definition
        self.sentence = sentence
