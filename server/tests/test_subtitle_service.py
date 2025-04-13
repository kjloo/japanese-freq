from unittest import mock
import pytest

from app.service.subtitle_service import style_subtitles, get_base_words


@pytest.mark.parametrize(
    "line, ignore_list, expected",
    [
        ("赤いリンゴが好きです。", {"好き", "飲む", "りんご"},
         "<span class='new-word'>赤い</span><span class='new-word'>リンゴ</span>が好きです。"),
        ("青い空が綺麗です。", {
         "綺麗"}, "<span class='new-word'>青い</span><span class='new-word'>空</span>が綺麗です。"),
        ("美味しいりんごを食べている。", {
         "食べる", "いる"}, "<span class='new-word'>美味しい</span><span class='new-word'>りんご</span>を食べている。"),
    ],
)
@mock.patch("app.service.subtitle_service.word_service.get_ignore_list")
def test_style_subtitles(mock_ignore_list, line, ignore_list, expected):
    mock_ignore_list.return_value = ignore_list
    styled_line = style_subtitles(line)
    assert styled_line == expected


@mock.patch("app.service.subtitle_service.word_service.get_ignore_list")
def test_get_base_words(mock_ignore_list):
    mock_ignore_list.return_value = set(["物", "会う"])
    sentence = "彼が「明日、公園で会いましょう！」と言った。"
    base_words = list(get_base_words(sentence))

    assert len(base_words) == 4
    assert base_words[0] == "彼"
    assert base_words[1] == "明日"
    assert base_words[2] == "公園"
    assert base_words[3] == "言う"
