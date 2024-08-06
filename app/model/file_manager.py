import os
from enum import Enum
from collections import namedtuple
from model.content.video_content import VideoContent
from model.content.text_content import TextContent
from model.content.source_content import SourceContent


class FileType(str, Enum):
    SRT = '.srt'
    MP4 = '.mp4'
    TXT = '.txt'
    OFFSET = 'offset'


class FileManager:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.source_content: list[SourceContent] = []
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
            if text:
                self.source_content.append(TextContent(full_path, os.path.join(
                    output_dir, f), text))
            elif sub and video:
                self.source_content.append(
                    VideoContent(full_path, os.path.join(
                        output_dir, f), sub, video, offset))
