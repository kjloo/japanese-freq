import MeCab
import json
from collections import defaultdict

wakati = MeCab.Tagger("-Owakati")


def remove_parentheses(text):
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


def parse_file(input_file: str, output_file: str):
    data = []
    with open(input_file) as f:
        data = f.readlines()

    japanese_sentences = []
    for line in data:
        if not line.strip() or line[0].isdigit():
            continue
        clean_names = remove_parentheses(line.strip()).strip()
        if not clean_names:
            continue

        japanese_sentences.append(clean_names)

    japanese_words = [wakati.parse(sentence).split()
                      for sentence in japanese_sentences]

    word_freq = defaultdict(lambda: {"frequency": 0, "sentences": []})
    for sentence in japanese_words:
        for word in sentence:
            if len(word) > 1:
                word_freq[word]["frequency"] += 1
                word_freq[word]["sentences"].append(''.join(sentence))

    sorted_word_freq = dict(
        sorted(word_freq.items(), key=lambda item: item[1]["frequency"], reverse=True))

    with open(output_file, 'w') as f:
        json.dump(sorted_word_freq, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_file: str = 'input/sub.srt'
    output_file: str = 'output/sub.json'
    parse_file(input_file, output_file)
