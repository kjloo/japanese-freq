class ProcessSettings:
    def __init__(
        self,
        inputs: list[str],
        word_check: bool,
        freq_min: int,
        requires_definition: bool,
        min_word_length: int
    ):
        self.inputs = inputs
        self.word_check = word_check
        self.freq_min = freq_min
        self.requires_definition = requires_definition
        self.min_word_length = min_word_length

    def __init__(self, json_data: dict[str]):
        self.inputs = json_data.get("inputs", [])
        self.word_check = json_data.get("word_check", True)
        self.freq_min = json_data.get("freq_min", 2)
        self.requires_definition = json_data.get("requires_definition", False)
        self.min_word_length = json_data.get("min_word_length", 1)
        self._validate()

    def with_word_check(self, word_check: bool):
        self.word_check = word_check
        return self

    def _validate(self):
        if not self.inputs:
            raise ValueError("Inputs list is required.")
        if not isinstance(self.word_check, bool):
            raise ValueError("Word check must be a boolean.")
        if not isinstance(self.freq_min, int) or self.freq_min < 0:
            raise ValueError(
                "Frequency minimum must be a non-negative integer.")
        if not isinstance(self.min_word_length, int) or self.min_word_length < 1:
            raise ValueError("Minimum word length must be a positive integer.")

    def __repr__(self):
        return (f"ProcessSettings(inputs={self.inputs}, "
                f"word_check={self.word_check}, "
                f"freq_min={self.freq_min}, "
                f"requires_definition={self.requires_definition}, "
                f"min_word_length={self.min_word_length})")
