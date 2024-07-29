import MeCab
import json
import os
import re
from collections import defaultdict
from model.japanese_content import JapaneseContent, Timestamp
from model.file_manager import FileManager, ContentManager
from model.video_downloader import VideoDownloader

wakati = MeCab.Tagger("-Owakati")


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
    video_downloader = VideoDownloader(content_manager.get_video())
    data = []
    with open(input_file) as f:
        data = f.readlines()

    pattern = re.compile(
        r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')

    timestamp: Timestamp = None
    content: list[JapaneseContent] = []
    counter = 0
    for line in data:
        ts = pattern.match(line)
        if ts:
            timestamp = Timestamp(ts.group(1), ts.group(2))
            continue
        if not line.strip() or line[0].isdigit():
            continue
        clean_sentence = remove_parentheses(line.strip()).strip()
        if not clean_sentence:
            continue

        jc = JapaneseContent(clean_sentence, timestamp)
        jc.audio = video_downloader.extract(
            jc.timestamp.start_time, jc.timestamp.end_time, os.path.join(content_manager.output_dir, '%s%d' % (content_manager.get_name(), counter)))
        counter += 1
        content.append(jc)
    return content


def analyze_content(content: list[JapaneseContent], output_file: str):
    word_freq = defaultdict(lambda: {"frequency": 0, "sentences": []})
    for c in content:
        for word in wakati.parse(c.sentence).split():
            if len(word) > 1:
                word_freq[word]["frequency"] += 1
                word_freq[word]["sentences"].append(c.to_dict())

    sorted_word_freq = dict(
        sorted(word_freq.items(), key=lambda item: item[1]["frequency"], reverse=True))

    with open(output_file, 'w') as f:
        json.dump(sorted_word_freq, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_dir: str = 'input'
    output_dir: str = 'output'

    file_manager = FileManager(input_dir, output_dir)
    for sc in file_manager.source_content:
        content = parse_file(sc)
        analyze_content(content, sc.output_dir + 'sub.json')
