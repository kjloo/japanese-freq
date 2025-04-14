from collections import namedtuple, defaultdict
import ffmpeg
import re
import os

from app.model.content.source_content import SourceContent
from app.model.frequency.freq_enum import FileType
from app.model.japanese_content import JapaneseContent, Timestamp
from app.util.envlookup import DOWNLOAD_MEDIA
from app.module.logging_module import logger


VideoData = namedtuple('VideoData', ['subtitles', 'video', 'offset'])


class VideoContent(SourceContent):
    def __init__(self, input_dir: str, output_dir: str, subtitles: str, video: str, offset: str):
        super().__init__(input_dir, output_dir)
        subtitles = self._convert_subtitles_to_vtt(subtitles)
        self.video_data = VideoData(subtitles, video, offset)
        self.video_downloader = VideoDownloader(
            self.get_video(), self._get_offset())

    def parse_file(self) -> list[JapaneseContent]:
        input_file = self.get_subtitles()
        data = []
        with open(input_file) as f:
            data = f.readlines()

        time_pattern = re.compile(
            r'((\d{2}:)?\d{2}:\d{2}[,.]\d{3}) --> ((\d{2}:)?\d{2}:\d{2}[,.]\d{3})'
        )
        build_sentence: list[str] | None = None
        timestamp: Timestamp = None
        counter = 0
        content: list[JapaneseContent] = []
        for line in data:
            # Look for sections
            if build_sentence is None and time_pattern.match(line):
                # Section start
                build_sentence = []
            elif not build_sentence is None and not line.strip():
                # Found section break. Store and reset
                jc = JapaneseContent(''.join(build_sentence), timestamp, os.path.join(self.output_dir, '%s_%d' % (
                    self.get_name(), counter)))
                counter += 1
                content.append(jc)
                build_sentence = None

            if build_sentence is None:
                continue

            ts = time_pattern.match(line)
            if ts:
                timestamp = Timestamp(ts.group(1), ts.group(3))
                continue
            if not line.strip() or line[0].isdigit():
                continue
            clean_sentence = self._remove_parentheses(line.strip()).strip()
            if not clean_sentence:
                continue

            build_sentence.append(clean_sentence)

        return content

    def download_media(self, content_dict: dict) -> dict:
        rc = defaultdict(
            lambda: {"frequency": 0, "definition": None, "sentences": []})

        for word in content_dict:
            for jc in content_dict[word]["content"]:
                if DOWNLOAD_MEDIA:
                    self._extract(
                        jc.timestamp.start_time, jc.timestamp.end_time, jc.audio)

            rc[word]["frequency"] = content_dict[word]["frequency"]
            rc[word]["definition"] = content_dict[word]["definition"]
            rc[word]["sentences"] = [jc for jc in content_dict[word]["content"]]

        return rc

    def get_subtitles(self) -> str:
        return os.path.join(self.input_dir, self.video_data.subtitles)

    def get_video(self) -> str:
        return os.path.join(self.input_dir, self.video_data.video)

    def _get_offset(self) -> str:
        return os.path.join(self.input_dir, self.video_data.offset)

    def _remove_parentheses(self, text) -> str:
        stack = []
        result = []

        for char in text:
            if char == '(' or char == '（':
                stack.append(len(result))
            elif char == ')' or char == '）' and stack:
                start = stack.pop()
                result = result[:start]
            elif not stack:
                result.append(char)

        return ''.join(result)

    def _extract(self, start_time: str, end_time: str, audio: str):
        self.video_downloader.extract(start_time, end_time, audio)

    def _convert_subtitles_to_vtt(self, subtitles: str):
        """
        Convert the subtitles file from .srt to .vtt using ffmpeg.
        If the subtitles file is already .vtt, no conversion is performed.
        """
        subtitles_path = os.path.join(self.input_dir, subtitles)
        # Check if the file is already a .vtt file
        if subtitles_path.endswith(FileType.VTT):
            logger.debug(
                f"Subtitles are already in .vtt format: {subtitles_path}")
            return subtitles

        # Ensure the file is an .srt file
        if not subtitles_path.endswith(FileType.SRT):
            raise ValueError(f"Unsupported subtitle format: {subtitles_path}")

        # Define the output .vtt file path
        vtt_path = subtitles_path.replace(FileType.SRT, FileType.VTT)

        # Use ffmpeg to convert .srt to .vtt
        try:
            logger.debug(f"Converting {subtitles_path} to {vtt_path}...")
            ffmpeg.input(subtitles_path).output(
                vtt_path, format="webvtt").run(overwrite_output=True)
            logger.debug(f"Conversion successful: {vtt_path}")
            # os.remove(subtitles_path)
            # Update the subtitles attribute to point to the new .vtt file
            return os.path.basename(vtt_path)
        except ffmpeg.Error as e:
            logger.debug(
                f"Error occurred during subtitle conversion: {e.stderr}")
            raise RuntimeError(f"Failed to convert {subtitles_path} to .vtt")


class VideoDownloader:
    def __init__(self, video_file: str, offset_file: str):
        offset = '00:00:00.000'
        with open(offset_file) as f:
            offset = f.read().strip()
        self.video_file = video_file
        self.in_file = ffmpeg.input(self.video_file, ss=offset).audio

    def extract(self, start_time: str, end_time: str, output_file: str) -> str:
        try:
            final_output_file = output_file + '.mp3'
            print(f"Create {final_output_file} Start: {
                  start_time} End: {end_time}")
            if os.path.exists(final_output_file):
                return final_output_file
            (
                self.in_file
                .filter('atrim', start=start_time, end=end_time)
                .filter('asetpts', 'PTS-STARTPTS')
                .output(final_output_file, format='mp3', acodec='libmp3lame')
                .run(overwrite_output=True)
            )
            print(f"Extracted video segment saved as {final_output_file}")
            return final_output_file
        except ffmpeg.Error as e:
            print(f"Error occurred: {e.stderr}")
            return None
