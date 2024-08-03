import os
from enum import Enum
from collections import namedtuple

SourceContent = namedtuple('SourceContent', ['subtitles', 'video'])


class FileType(str, Enum):
    SRT = '.srt'
    MP4 = '.mp4'


class FileManager:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.source_content: list[ContentManager] = []
        for f in os.listdir(input_dir):
            full_path = os.path.join(input_dir, f)
            if not os.path.isdir(full_path):
                continue
            sub = None
            video = None
            for name in os.listdir(full_path):
                if name.lower().endswith(FileType.SRT):
                    sub = name
                elif name.lower().endswith(FileType.MP4):
                    video = name
            if sub is None or video is None:
                continue
            self.source_content.append(
                ContentManager(full_path, os.path.join(
                    output_dir, f), SourceContent(sub, video)))


class ContentManager:
    def __init__(self, input_dir: str, output_dir: str, source_content: SourceContent):
        self.input_dir = input_dir
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        self.source_content = source_content

    def get_name(self):
        return os.path.basename(self.input_dir)

    def get_subtitles(self) -> str:
        return os.path.join(self.input_dir, self.source_content.subtitles)

    def get_video(self) -> str:
        return os.path.join(self.input_dir, self.source_content.video)
