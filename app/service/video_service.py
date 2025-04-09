import os

from model.file_manager import FileManager
from model.content.video_content import VideoContent
from service import io_service


def generate(source: str):
    """
    Generate video file chunks for streaming.
    """
    file_manager: FileManager = io_service.get_file_manager()
    video_content: VideoContent = file_manager.get_video_by_name(source)
    video_path = video_content.get_video()
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file {source} not found")

    with open(video_path, 'rb') as f:
        while chunk := f.read(1024 * 1024):  # Read in 1MB chunks
            yield chunk


def generate_subtitles(source: str):
    """
    Serve subtitles for a video file.
    """
    file_manager: FileManager = io_service.get_file_manager()
    video_content: VideoContent = file_manager.get_video_by_name(source)
    subtitles_path = video_content.get_subtitles()

    if not os.path.exists(subtitles_path):
        raise FileNotFoundError(f"Subtitles file {source} not found")

    with open(subtitles_path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line
