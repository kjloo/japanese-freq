import zipfile
import fugashi
import os
import json

from app.model.dictionary import Dictionary
from app.module.logging_module import logger
from app.repository.word.word_repository import word_repository


def _check_and_create_directory() -> str:
    """
    Check if the directory exists, and create it if it does not.
    """
    base_dir = os.path.join("dictionaries")
    dict_dir = os.path.join(base_dir, "unidic")
    zip_path = os.path.join(base_dir, "unidic-3.10.zip")
    if not os.path.exists(dict_dir):
        logger.info(f"Dictionary not found at {dict_dir}, extracting...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(base_dir)
        logger.info("Extraction complete.")
    else:
        logger.info(f"Dictionary already exists at {dict_dir}")
    return dict_dir


def _get_tagger():
    dict_path = _check_and_create_directory()
    return fugashi.Tagger(f"-r /dev/null -d {dict_path}")


wakati = _get_tagger()

dictionary = Dictionary("dictionaries/jmdict_english.zip")

# Ignore these parts of speech [Auxillary Verbs, Punctuation, Particle]
IGNORE_POS = ["助動詞", "補助記号", "助詞"]

ignore_list_file: str = ".ignorelist.json"


def _load_ignore_list() -> set[str]:
    """
    Load the ignore list from a database or file.
    """
    ignore_list: set[str] = set(word_repository.get_words())
    if ignore_list:
        return ignore_list

    if os.path.exists(ignore_list_file):
        with open(ignore_list_file, "r") as f:
            ignore_list = set(json.load(f))
    return ignore_list


ignore_list: set[str] = _load_ignore_list()
