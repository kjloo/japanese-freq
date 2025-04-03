from collections import defaultdict
import fugashi

from service import io_service
from service import word_service
from model.content.source_content import SourceContent
from model.japanese_content import JapaneseContent
from model.dictionary import Dictionary
from model.progress import Progress
from module.socket_module import socketio
from module.logging import logger

# wakati = fugashi.Tagger("-Owakati")
wakati = fugashi.Tagger()
dictionary = Dictionary('dictionaries/jmdict_english.zip')

# Ignore these parts of speech [Auxillary Verbs, Punctuation, Particle]
IGNORE_POS = ["助動詞", "補助記号", "助詞"]


def process_inputs(inputs: list[str], word_check: bool, freq_min: int, requires_definition: bool, min_word_length: int):
    logger.debug(
        f"Processing inputs: {inputs}, word_check: {word_check}, freq_min: {freq_min}, requires_definition: {requires_definition}, min_word_length: {min_word_length}")
    ignore_list = word_service.get_ignore_list()
    progress: Progress = Progress()

    file_manager = io_service.get_file_manager()
    processed: int = 0

    pending_process: list[SourceContent] = [
        f for f in file_manager.source_content if f.get_name() in inputs]

    for sc in pending_process:
        logger.debug(f"Processing file: {sc.get_name()}")
        content = sc.parse_file()
        content_dict = _analyze_content(
            content, ignore_list, freq_min, requires_definition, min_word_length)
        short_dict = word_service.ask_user(
            content_dict) if word_check else content_dict
        socketio.emit('word_check_complete', {})
        data = sc.download_media(short_dict)
        io_service.write_to_json(data, sc.get_output_file())
        processed += 1
        progress.update_progress(processed / len(pending_process))
        socketio.emit('progress', progress.to_json())


def _analyze_content(content: list[JapaneseContent], ignore_list: set[str], freq_min: int, requires_definition: bool, min_word_length: int) -> dict:
    word_freq = defaultdict(
        lambda: {"frequency": 0, "definition": None, "content": []})
    for c in content:
        for word_content in wakati(c.sentence):
            if word_content.feature.pos1 in IGNORE_POS:
                continue
            word = word_content.feature.orthBase
            if word is None:
                continue
            if len(word) >= min_word_length and word not in ignore_list:
                word_freq[word]["frequency"] += 1
                if word_freq[word]["definition"] is None:
                    sd = dictionary.short_lookup(word)
                    word_freq[word]["definition"] = sd.to_dict(
                    ) if sd else False

                word_freq[word]["content"].append(c)

    filtered_word_freq = {w: word_freq[w] for w in word_freq if word_freq[w]["frequency"] >= freq_min and (
        not requires_definition or bool(word_freq[w]["definition"]))}
    sorted_word_freq = dict(
        sorted(filtered_word_freq.items(), key=lambda item: item[1]["frequency"], reverse=True))
    return sorted_word_freq


def _debug():
    text = "お腹空いたらたくさん食べられる。"
    print(wakati(text))
    for word in wakati(text):
        print("################# %s #####################" % word)
        l = []
        for attr in dir(word.feature):
            if not callable(getattr(word.feature, attr)) and not attr.startswith("_"):
                l.append(f"{attr}: {getattr(word.feature, attr)}")
        print(','.join(l))
