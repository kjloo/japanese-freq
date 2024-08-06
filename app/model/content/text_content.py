import os
import re
from model.content.source_content import SourceContent
from model.japanese_content import JapaneseContent
from collections import defaultdict


class TextContent(SourceContent):
    def __init__(self, input_dir: str, output_dir: str, text: str):
        super().__init__(input_dir, output_dir)
        self.text = text

    def parse_file(self) -> list[JapaneseContent]:
        input_file = self._get_text()
        data = []
        with open(input_file) as f:
            data = f.read().strip()
        lines = re.findall(r'[^。？！」]+.?', data)
        content: list[JapaneseContent] = []
        for line in lines:
            jc = JapaneseContent(line, None, None)
            content.append(jc)
        return content

    def download_media(self, content_dict: dict) -> dict:
        rc = defaultdict(
            lambda: {"frequency": 0, "definition": None, "sentences": []})

        for word in content_dict:
            rc[word]["frequency"] = content_dict[word]["frequency"]
            rc[word]["definition"] = content_dict[word]["definition"]
            rc[word]["sentences"] = [jc.to_dict()
                                     for jc in content_dict[word]["content"]]

        return rc

    def _get_text(self) -> str:
        return os.path.join(self.input_dir, self.text)
