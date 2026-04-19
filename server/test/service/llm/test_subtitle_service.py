from unittest import mock
import pytest

from app.service import subtitle_service
from test.fixture.mongo_fixture import mongo_test


@pytest.mark.usefixtures("mongo_test")
@mock.patch("app.service.subtitle_service.word_service.get_ignore_list")
def test_style_subtitles(mock_ignore_list):
    subtitles = [
        "WEBVTT",
        "Kind: captions",
        "Language: ja",
        "00:00:00.133 --> 00:00:02.052",
        "赤いリンゴが好きです。",
        "",
        "00:00:02.052 --> 00:00:04.671",
        "青い空が綺麗です。",
        "",
        "00:00:04.671 --> 00:00:07.007",
        "美味しいりんごを食べている。",
        "" "00:00:14.381 --> 00:00:16.066",
        "雨に降られた。",
        "",
    ]
    expected = [
        "WEBVTT",
        "Kind: captions",
        "Language: ja",
        "00:00:00.133 --> 00:00:02.052",
        "<span class='new-word'>赤い</span><span class='new-word'>リンゴ</span>が好きです。",
        "00:00:02.052 --> 00:00:04.671",
        "<span class='new-word'>青い</span><span class='new-word'>空</span>が綺麗です。",
        "00:00:04.671 --> 00:00:07.007",
        "<span class='new-word'>美味しい</span><span class='new-word'>りんご</span>を食べている。",
        "" "00:00:14.381 --> 00:00:16.066",
        "<span class='new-word'>雨</span>に<span class='new-word'>降ら</span>れた。",
    ]
    mock_ignore_list.return_value = {"好き", "飲む", "ルンゴ", "綺麗", "食べる", "いる"}
    styled_subtitles = subtitle_service.style_subtitles(subtitles)
    assert styled_subtitles == expected


@pytest.mark.usefixtures("mongo_test")
@mock.patch("app.service.subtitle_service.word_service.get_ignore_list")
def test_get_base_words(mock_ignore_list):
    mock_ignore_list.return_value = set(["物", "会う"])
    sentence = "彼が「明日、公園で会いましょう！」と言った。"
    base_words = list(subtitle_service.get_base_words(sentence))

    assert len(base_words) == 4
    assert base_words[0] == "彼"
    assert base_words[1] == "明日"
    assert base_words[2] == "公園"
    assert base_words[3] == "言う"
