import os
from model.content.video_content import VideoContent
from model.content.text_content import TextContent
from model.content.source_content import SourceContent
from model.freq_enum import FileType


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
                if sub is None and name.lower().endswith(FileType.SRT):
                    sub = name
                elif name.lower().endswith(FileType.VTT):
                    sub = name
                elif name.lower().endswith(FileType.MP4) or name.lower().endswith(FileType.MKV) or name.lower().endswith(FileType.MP3):
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

    def get_video_by_name(self, name: str) -> VideoContent:
        try:
            return next(sc for sc in self.source_content if sc.get_name() == name)
        except StopIteration:
            raise ValueError(f"Video with name '{name}' not found.")
