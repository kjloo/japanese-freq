import pytest
from unittest.mock import patch, MagicMock
# from fugashi import TaggedToken

from app.service.subtitle_service import style_subtitles, get_subtitle_words, get_base_words


@pytest.fixture
def mock_ignore_list():
    return {"ignored_word"}


@pytest.fixture
def mock_ignore_pos():
    return {"助詞"}


@patch("app.service.subtitle_service.word_service.get_ignore_list")
@patch("app.service.subservice.IGNORE_POS", {"助詞"})
@patch("app.service.subtitle_service.wakati")
def test_style_subtitles(mock_wakati, mock_get_ignore_list, mock_ignore_list):
    mock_get_ignore_list.return_value = mock_ignore_list
    mock_wakati.return_value = [
        MagicMock(content="new_word", feature=MagicMock(
            orthBase="new_word", pos1="名詞")),
        MagicMock(content="ignored_word", feature=MagicMock(
            orthBase="ignored_word", pos1="名詞")),
        MagicMock(content="は", feature=MagicMock(orthBase="は", pos1="助詞")),
    ]

    line = "new_word ignored_word は"
    styled_line = style_subtitles(line)

    assert styled_line == "<span class='new-word'>new_word</span> ignored_word は"


@patch("app.service.subtitle_service.wakati")
def test_get_subtitle_words(mock_wakati):
    mock_wakati.return_value = [
        MagicMock(content="word1"),
        MagicMock(content="word2"),
    ]

    sentence = "word1 word2"
    words = list(get_subtitle_words(sentence))

    assert len(words) == 2
    assert words[0].content == "word1"
    assert words[1].content == "word2"


@patch("app.service.subtitle_service.wakati")
@patch("app.service.subservice.IGNORE_POS", {"助詞"})
def test_get_base_words(mock_wakati):
    mock_wakati.return_value = [
        MagicMock(feature=MagicMock(orthBase="base_word1", pos1="名詞")),
        MagicMock(feature=MagicMock(orthBase="base_word2", pos1="助詞")),
    ]

    sentence = "word1 word2"
    base_words = list(get_base_words(sentence))

    assert len(base_words) == 1
    assert base_words[0] == "base_word1"
