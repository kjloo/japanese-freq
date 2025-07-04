from inspect import signature


class AnkiValues:
    """
    Class to hold Anki values for card creation.
    """
    audio: str
    conjugation: str
    definition: str
    hiragana: str
    kanji: str
    part_of_speech: str
    pitch_accent: str
    romaji: str
    sentence: str
    translation: str

    def __init__(
        self,
        audio: str,
        conjugation: str,
        definition: str,
        hiragana: str,
        kanji: str,
        part_of_speech: str,
        pitch_accent: str,
        romaji: str,
        sentence: str,
        translation: str,
    ):
        self.audio = audio
        self.conjugation = conjugation
        self.definition = definition
        self.hiragana = hiragana
        self.kanji = kanji
        self.part_of_speech = part_of_speech
        self.pitch_accent = pitch_accent
        self.romaji = romaji
        self.sentence = sentence
        self.translation = translation

    def to_dict(self) -> dict[str, str]:
        """
        Convert the Anki values to a dictionary using the class attributes.
        """
        return {attr: getattr(self, attr) for attr in self.attributes()}

    @staticmethod
    def attributes() -> list[str]:
        """
        Return the list of attribute names based on the __init__ signature.
        """
        # Exclude 'self' from parameters
        return [param for param in signature(AnkiValues.__init__).parameters if param != "self"]
