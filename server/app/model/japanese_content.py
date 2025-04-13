from collections import namedtuple

Timestamp = namedtuple('Timestamp', ['start_time', 'end_time'])


class JapaneseContent:
    def __init__(self, sentence: str, timestamp: Timestamp = None, audio: str = None):
        self.sentence = sentence
        self.timestamp = Timestamp(timestamp.start_time.replace(
            ',', '.'), timestamp.end_time.replace(',', '.')) if timestamp else None
        self.audio = audio

    def to_dict(self):
        return {
            'sentence': self.sentence,
            'start_time': self.timestamp.start_time if self.timestamp else None,
            'end_time': self.timestamp.end_time if self.timestamp else None,
            'audio': self.audio
        }
