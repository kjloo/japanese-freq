import fugashi
import json
import os
import re
from collections import defaultdict
from model.japanese_content import JapaneseContent, Timestamp
from model.file_manager import ContentManager, FileManager
from model.video_downloader import VideoDownloader
from model.dictionary import Dictionary
from util.envlookup import DOWNLOAD_MEDIA, FREQ_MIN, MIN_WORD_LENGTH, REQUIRES_DEFINITION
from pprint import pprint

# wakati = fugashi.Tagger("-Owakati")
wakati = fugashi.Tagger()
dictionary = Dictionary('dictionaries/jmdict_english.zip')

# Ignore these parts of speech [Auxillary Verbs, Punctuation, Particle]
IGNORE_POS = ["助動詞", "補助記号", "助詞"]


def remove_parentheses(text) -> str:
    stack = []
    result = []

    for char in text:
        if char == '(' or char == '（':
            stack.append(len(result))
        elif char == ')' or char == '）' and stack:
            start = stack.pop()
            result = result[:start]
        elif not stack:
            result.append(char)

    return ''.join(result)


def parse_file(content_manager: ContentManager) -> list[JapaneseContent]:
    input_file = content_manager.get_subtitles()
    offset = '00:00:00.000'
    data = []
    with open(input_file) as f:
        data = f.readlines()
    with open(content_manager.get_offset()) as f:
        offset = f.read().strip()

    start_pattern = re.compile(r'^\d+$')
    time_pattern = re.compile(
        r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')

    build_sentence: list[str] | None = None
    timestamp: Timestamp = None
    counter = 0
    content: list[JapaneseContent] = []
    for line in data:
        # Look for sections
        if build_sentence is None and start_pattern.match(line):
            # Section start
            build_sentence = []
        elif not build_sentence is None and not line.strip():
            # Found section break. Store and reset
            jc = JapaneseContent(''.join(build_sentence), timestamp, os.path.join(content_manager.output_dir, '%s%d' % (
                content_manager.get_name(), counter)))
            counter += 1
            content.append(jc)
            build_sentence = None

        if build_sentence is None:
            continue

        ts = time_pattern.match(line)
        if ts:
            timestamp = Timestamp(ts.group(1), ts.group(2))
            continue
        if not line.strip() or line[0].isdigit():
            continue
        clean_sentence = remove_parentheses(line.strip()).strip()
        if not clean_sentence:
            continue

        build_sentence.append(clean_sentence)

    return content


def analyze_content(content: list[JapaneseContent], ignore_list: set[str]) -> dict:
    word_freq = defaultdict(
        lambda: {"frequency": 0, "definition": None, "content": []})
    for c in content:
        for word_content in wakati(c.sentence):
            if word_content.feature.pos1 in IGNORE_POS:
                continue
            word = word_content.feature.orthBase
            if word is None:
                continue
            if len(word) >= MIN_WORD_LENGTH and word not in ignore_list:
                word_freq[word]["frequency"] += 1
                if word_freq[word]["definition"] is None:
                    sd = dictionary.short_lookup(word)
                    word_freq[word]["definition"] = sd.to_dict(
                    ) if sd else False

                word_freq[word]["content"].append(c)

    filtered_word_freq = {w: word_freq[w] for w in word_freq if word_freq[w]["frequency"] > FREQ_MIN and (
        not REQUIRES_DEFINITION or bool(word_freq[w]["definition"]))}
    sorted_word_freq = dict(
        sorted(filtered_word_freq.items(), key=lambda item: item[1]["frequency"], reverse=True))
    return sorted_word_freq


def download_media(content_manager: ContentManager, content_dict: dict) -> dict:
    rc = defaultdict(
        lambda: {"frequency": 0, "definition": None, "sentences": []})
    video_downloader = VideoDownloader(
        content_manager.get_video(), content_manager.get_offset())
    for word in content_dict:
        for jc in content_dict[word]["content"]:
            if DOWNLOAD_MEDIA:
                video_downloader.extract(
                    jc.timestamp.start_time, jc.timestamp.end_time, jc.audio)

        rc[word]["frequency"] = content_dict[word]["frequency"]
        rc[word]["definition"] = content_dict[word]["definition"]
        rc[word]["sentences"] = [jc.to_dict()
                                 for jc in content_dict[word]["content"]]

    return rc


def write_to_json(data: dict, output_file: str):
    with open(output_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


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


if __name__ == "__main__":
    input_dir: str = 'input'
    output_dir: str = 'output'
    ignore_list_file: str = '.ignorelist'

    ignore_list: set[str] = []
    with open(ignore_list_file, 'r') as f:
        ignore_list = set(json.load(f))

    file_manager = FileManager(input_dir, output_dir)
    for sc in file_manager.source_content:
        content = parse_file(sc)
        content_dict = analyze_content(content, ignore_list)
        data = download_media(sc, content_dict)
        write_to_json(data, sc.output_dir + '_sub.json')
