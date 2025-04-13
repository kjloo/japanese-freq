import fugashi
import os

from model.dictionary import Dictionary

wakati = fugashi.Tagger()
dictionary = Dictionary('dictionaries/jmdict_english.zip')

# Ignore these parts of speech [Auxillary Verbs, Punctuation, Particle]
IGNORE_POS = ["助動詞", "補助記号", "助詞"]

ignore_list_file: str = '.ignorelist'
ignore_list: set[str] = []

if os.path.exists(ignore_list_file):
    with open(ignore_list_file, 'r') as f:
        ignore_list = set(json.load(f))
