from pathlib import Path
import zipfile
import json
import cutlet

katsu = cutlet.Cutlet()


class ShortDef:
    def __init__(self, definition: str, kanji: str, hiragana: str, romaji: str):
        self.defintion = definition
        self.kanji = kanji
        self.hiragana = hiragana
        self.romaji = romaji

    def to_dict(self):
        return {
            "definition": self.defintion,
            "kanji": self.kanji,
            "hiragana": self.hiragana,
            "romaji": self.romaji
        }


class Dictionary:

    def __init__(self, input_file: str):
        self.dictionary = self._load_dictionary(input_file)

    def _load_dictionary(self, input_file: str) -> dict:
        output_map = {}
        archive = zipfile.ZipFile(input_file, 'r')

        result = list()
        for file in archive.namelist():
            if file.startswith('term'):
                with archive.open(file) as f:
                    data = f.read()
                    d = json.loads(data.decode("utf-8"))
                    result.extend(d)

        for entry in result:
            if (entry[0] in output_map):
                output_map[entry[0]].append(entry)
            else:
                # Using headword as key for finding the dictionary entry
                output_map[entry[0]] = [entry]
            if (entry[1] in output_map):
                output_map[entry[1]].append(entry)
            else:
                # Add hiragana keys
                output_map[entry[1]] = [entry]

        return output_map

    def lookup(self, word: str) -> list:
        return self.dictionary.get(word, [])

    def short_lookup(self, word: str) -> ShortDef:
        definitions = self.dictionary.get(word, [])
        if len(definitions) == 0:
            return None
        definition = definitions[0]
        meaning = '\n'.join(
            [f"({i + 1}): {'; '.join(d[5])}" for i, d in enumerate(definitions)])

        hiragana = definition[1] if definition[1] else definition[0]

        kanji = '\n'.join(
            [f"({i + 1}): {d[0] if d[1] else None}" for i, d in enumerate(definitions)])
        romaji = katsu.romaji(hiragana).lower()
        return ShortDef(meaning, kanji, hiragana, romaji)
