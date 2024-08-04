from pathlib import Path
import zipfile
import json


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
        return output_map

    def lookup(self, word: str):
        return self.dictionary.get(word, False)
