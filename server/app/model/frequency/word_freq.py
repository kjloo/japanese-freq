class WordFreq:
    def __init__(self, freq: int = 0, definition: str = "", content: list[str] = []):
        self.freq: int = freq
        self.defition: str = definition
        self.content: list[str] = content

    def __repr__(self):
        return f"WordFreq(freq={self.freq}, content={self.content})"


class WordFreqDict:
    def __init__(self):
        self.word_freq_dict: dict[str, WordFreq] = {}

    def add_word(self, word: str, freq: int, content: list[str] = []):
        if word in self.word_freq_dict:
            self.word_freq_dict[word].freq += freq
        else:
            self.word_freq_dict[word] = WordFreq(freq=freq)

    def __repr__(self):
        return f"WordFreqDict(word_freq_dict={self.word_freq_dict})"
