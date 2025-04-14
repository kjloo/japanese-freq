from enum import Enum


class FileType(str, Enum):
    SRT = '.srt'
    VTT = '.vtt'
    MP4 = '.mp4'
    MKV = '.mkv'
    MP3 = '.mp3'
    TXT = '.txt'
    OFFSET = 'offset'
