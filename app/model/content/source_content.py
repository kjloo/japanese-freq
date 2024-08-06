from abc import abstractmethod
import os
from model.japanese_content import JapaneseContent


class SourceContent:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    def get_name(self) -> str:
        return os.path.basename(self.input_dir)

    def get_output_file(self) -> str:
        output_file = os.path.join(
            self.output_dir, self.get_name() + '_sub.json')
        return output_file

    @abstractmethod
    def parse_file(self) -> list[JapaneseContent]:
        pass

    @abstractmethod
    def download_media(self, content_dict: dict) -> dict:
        pass
