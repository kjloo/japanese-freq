from typing import Generator
from fugashi import TaggedToken
from module.dictionary_module import wakati, IGNORE_POS
from service import word_service


def style_subtitles(line: str) -> str:
    ignore_list: set[str] = word_service.get_ignore_list()
    for word_content in get_subtitle_words(line):
        if word_content.feature.orthBase in ignore_list:
            continue
        if word_content.feature.pos1 in IGNORE_POS:
            continue
        line = line.replace(
            word_content.content, f"<span class='new-word'>{word_content.content}</span>")


def get_subtitle_words(sentence: str) -> Generator[TaggedToken, None, None]:
    for word_content in wakati(sentence):
        yield word_content


def get_base_words(sentence: str) -> Generator[str, None, None]:
    for word_content in get_subtitle_words(sentence):
        if word_content.feature.pos1 in IGNORE_POS:
            continue
        yield word_content.feature.orthBase
