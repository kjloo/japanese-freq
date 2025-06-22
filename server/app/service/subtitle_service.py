from typing import Generator
from fugashi.fugashi import UnidicNode

from app.module.dictionary_module import wakati, IGNORE_POS
from app.service import word_service
from app.module.logging_module import logger


def style_subtitles(subtitles: list[str]) -> list[str]:
    styled_subtitles = []
    block = []

    for line in subtitles:
        if not line.strip() or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            styled_subtitles.append(line)
            continue

        if "-->" in line:
            # New timestamp found, flush previous block
            styled_subtitles.append(''.join(block))
            block = []
            styled_subtitles.append(line)
        else:
            block.append(_style_subtitle(line))

    # Flush the last block if present
    styled_subtitles.append(''.join(block))

    return [line for line in styled_subtitles if line.strip()]


def _style_subtitle(line: str) -> str:
    for word_content in _get_subtitle_words(line):
        if _filter_word(word_content) or word_content is None:
            continue
        if word_content.feature.orth is None:
            logger.warning(f"Word content has no orth: {word_content}")
            continue
        line = line.replace(
            word_content.feature.orth, f"<span class='new-word'>{word_content.feature.orth}</span>")
    return line


def get_base_words(sentence: str) -> Generator[str, None, None]:
    for word_content in _get_subtitle_words(sentence):
        if _filter_word(word_content):
            continue
        yield word_content.feature.orthBase


def _get_subtitle_words(sentence: str) -> Generator[UnidicNode, None, None]:
    for word_content in wakati(sentence):
        yield word_content


def _filter_word(word_content: UnidicNode) -> bool:
    ignore_list: set[str] = word_service.get_ignore_list()
    if word_content.feature.orthBase in ignore_list:
        return True
    if word_content.feature.pos1 in IGNORE_POS:
        return True
    return False
