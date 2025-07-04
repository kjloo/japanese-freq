import fugashi
import os
import json

from app.model.dictionary import Dictionary
from app.repository.word.word_repository import word_repository

wakati = fugashi.Tagger()
dictionary = Dictionary("dictionaries/jmdict_english.zip")

# Ignore these parts of speech [Auxillary Verbs, Punctuation, Particle]
IGNORE_POS = ["助動詞", "補助記号", "助詞"]

ignore_list_file: str = ".ignorelist.json"


def _load_ignore_list() -> set[str]:
    """
    Load the ignore list from a database or file.
    """
    ignore_list = word_repository.get_words()
    if ignore_list:
        return set(ignore_list)

    if os.path.exists(ignore_list_file):
        with open(ignore_list_file, "r") as f:
            ignore_list = set(json.load(f))
    return ignore_list


ignore_list: set[str] = _load_ignore_list()
