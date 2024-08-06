import os
from enum import Enum
from collections import namedtuple

SourceContent = namedtuple('SourceContent', ['subtitles', 'video', 'offset'])


class FileType(str, Enum):
    SRT = '.srt'
    MP4 = '.mp4'
    TXT = '.txt'
    OFFSET = 'offset'


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
            offset = None
            text = None
            for name in os.listdir(full_path):
                if name.lower().endswith(FileType.SRT):
                    sub = name
                elif name.lower().endswith(FileType.MP4):
                    video = name
                elif name.lower().endswith(FileType.OFFSET):
                    offset = name
                elif name.lower().endswith(FileType.TXT):
                    text = name
            if not (not text is None or (not sub is None and not video is None)):
                continue
            self.source_content.append(
                ContentManager(full_path, os.path.join(
                    output_dir, f), SourceContent(sub, video, offset)))


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

    def get_offset(self) -> str:
        return os.path.join(self.input_dir, self.source_content.offset)
