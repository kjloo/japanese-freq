from collections import defaultdict

from app.service import io_service
from app.service import word_service
from app.form.frequency.process_settings import ProcessSettings
from app.model.content.source_content import SourceContent
from app.model.japanese_content import JapaneseContent
from app.model.progress import Progress
from app.module.socket_module import socketio
from app.module.file_module import file_manager
from app.module.logging_module import logger
from app.module.dictionary_module import dictionary
from app.service import subtitle_service


def process_words(process_settings: ProcessSettings):
    logger.debug(f"Processing Words: {process_settings}")
    progress: Progress = Progress()

    processed: int = 0

    pending_process: list[SourceContent] = [
        f for f in file_manager.source_content if f.get_name() in process_settings.inputs]

    for sc in pending_process:
        logger.debug(f"Processing file: {sc.get_name()}")
        short_dict = _process_input(sc, process_settings.word_check, process_settings.freq_min,
                                    process_settings.requires_definition, process_settings.min_word_length)
        data = sc.download_media(short_dict)
        io_service.write_to_json(data, sc.get_output_file())
        processed += 1
        progress.update_progress(processed / len(pending_process))
        socketio.emit('progress', progress.to_json())


def process_video(process_settings: ProcessSettings) -> dict:
    logger.debug(f"Processing Video: {process_settings}")
    input = process_settings.inputs[0]
    sc = file_manager.get_video_by_name(input)
    short_dict = _process_input(sc, process_settings.word_check, process_settings.freq_min,
                                process_settings.requires_definition, process_settings.min_word_length)
    return short_dict


def _process_input(
    input: SourceContent,
    word_check: bool,
    freq_min: int,
    requires_definition: bool,
    min_word_length: int
) -> dict:
    ignore_list = word_service.get_ignore_list()
    content = input.parse_file()
    content_dict = _analyze_content(
        content, ignore_list, freq_min, requires_definition, min_word_length)
    short_dict = word_service.ask_user(
        content_dict) if word_check else content_dict
    socketio.emit('word_check_complete', {})
    return short_dict


def _analyze_content(
    content: list[JapaneseContent],
    ignore_list: set[str],
    freq_min: int,
    requires_definition: bool,
    min_word_length: int
) -> dict:
    word_freq = defaultdict(
        lambda: {"frequency": 0, "definition": None, "content": []})
    for c in content:
        for word in subtitle_service.get_base_words(c.sentence):
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
