import ffmpeg
import re
import os
from model.content.source_content import SourceContent
from collections import namedtuple
from model.japanese_content import JapaneseContent, Timestamp
from collections import defaultdict
from util.envlookup import DOWNLOAD_MEDIA


VideoData = namedtuple('VideoData', ['subtitles', 'video', 'offset'])


class VideoContent(SourceContent):
    def __init__(self, input_dir: str, output_dir: str, subtitles: str, video: str, offset: str):
        super().__init__(input_dir, output_dir)
        self.video_data = VideoData(subtitles, video, offset)
        self.video_downloader = VideoDownloader(
            self._get_video(), self._get_offset())

    def parse_file(self) -> list[JapaneseContent]:
        input_file = self._get_subtitles()
        data = []
        with open(input_file) as f:
            data = f.readlines()

        start_pattern = re.compile(r'^\d+$')
        time_pattern = re.compile(
            r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')

        build_sentence: list[str] | None = None
        timestamp: Timestamp = None
        counter = 0
        content: list[JapaneseContent] = []
        for line in data:
            # Look for sections
            if build_sentence is None and start_pattern.match(line):
                # Section start
                build_sentence = []
            elif not build_sentence is None and not line.strip():
                # Found section break. Store and reset
                jc = JapaneseContent(''.join(build_sentence), timestamp, os.path.join(self.output_dir, '%s%d' % (
                    self.get_name(), counter)))
                counter += 1
                content.append(jc)
                build_sentence = None

            if build_sentence is None:
                continue

            ts = time_pattern.match(line)
            if ts:
                timestamp = Timestamp(ts.group(1), ts.group(2))
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
            rc[word]["sentences"] = [jc.to_dict()
                                     for jc in content_dict[word]["content"]]

        return rc

    def _get_subtitles(self) -> str:
        return os.path.join(self.input_dir, self.video_data.subtitles)

    def _get_video(self) -> str:
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
