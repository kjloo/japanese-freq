from collections import defaultdict
from threading import Event
import fugashi
import json

from model.japanese_content import JapaneseContent
from model.file_manager import FileManager
from model.dictionary import Dictionary
from util.envlookup import FREQ_MIN, MIN_WORD_LENGTH, REQUIRES_DEFINITION
from model.progress import Progress
from module.socket_module import socketio

# wakati = fugashi.Tagger("-Owakati")
wakati = fugashi.Tagger()
dictionary = Dictionary('dictionaries/jmdict_english.zip')

# Ignore these parts of speech [Auxillary Verbs, Punctuation, Particle]
IGNORE_POS = ["助動詞", "補助記号", "助詞"]

# Settings
input_dir: str = 'input'
output_dir: str = 'output'
ignore_list_file: str = '.ignorelist'
ignore_list: set[str] = []
with open(ignore_list_file, 'r') as f:
    ignore_list = set(json.load(f))


def process_inputs():
    progress: Progress = Progress()

    file_manager = FileManager(input_dir, output_dir)
    processed: int = 0
    for sc in file_manager.source_content:
        content = sc.parse_file()
        content_dict = _analyze_content(content, ignore_list)
        short_dict = _ask_user(content_dict)
        data = sc.download_media(short_dict)
        _write_to_json(data, sc.get_output_file())
        processed += 1
        progress.update_progress(processed / len(file_manager.source_content))
        socketio.emit('progress', progress.to_json())


def _analyze_content(content: list[JapaneseContent], ignore_list: set[str]) -> dict:
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

    filtered_word_freq = {w: word_freq[w] for w in word_freq if word_freq[w]["frequency"] >= FREQ_MIN and (
        not REQUIRES_DEFINITION or bool(word_freq[w]["definition"]))}
    sorted_word_freq = dict(
        sorted(filtered_word_freq.items(), key=lambda item: item[1]["frequency"], reverse=True))
    return sorted_word_freq


def _ask_user(content: dict, ignore_list_file: str) -> dict:
    """
    Asks user if they already know the word and waits for their response.
    Removes words with a True response from the data dictionary and adds them to the ignore list file.
    """
    response_event = Event()  # Event to wait for user response

    def handle_response(response: dict):
        """
        Callback to handle user response from the client.
        """
        word = response.get('word')
        answer = response.get('answer')  # True or False

        if answer:  # If the user knows the word (True)
            # Remove the word from the data dictionary
            content.pop(word, None)

            ignore_list.add(word)
            # Add the word to the ignore list file
            with open(ignore_list_file, 'w') as f:
                json.dump(ignore_list, f, indent=4)

        response_event.set()  # Signal that the response has been received

    # Register a temporary SocketIO event listener for 'response'
    socketio.on_event('response', handle_response)

    for word in list(content.keys()):
        socketio.emit('word_check', {
            'word': word,
            'definition': content[word]["definition"]
        })
        response_event.clear()  # Reset the event
        response_event.wait()  # Wait for the user to respond

    # Unregister the event listener after processing
    socketio.off_event('response', handle_response)

    return content


def _write_to_json(data: dict, output_file: str):
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
