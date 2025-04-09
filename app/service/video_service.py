from flask import Response
import os

from model.file_manager import FileManager
from model.content.video_content import VideoContent
from service import io_service

# Map of file extensions to Content-Type
CONTENT_TYPE_MAP = {
    "mp4": "video/mp4",
    "mkv": "video/x-matroska",
}


def generate(source: str) -> Response:
    """
    Generate video file chunks for streaming.
    """
    file_manager: FileManager = io_service.get_file_manager()
    video_content: VideoContent = file_manager.get_video_by_name(source)
    video_path = video_content.get_video()
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file {source} not found")

    # Determine the file extension and content type
    # Extract file extension without the dot
    file_extension = os.path.splitext(video_path)[1][1:].lower()
    content_type = CONTENT_TYPE_MAP.get(
        file_extension, "application/octet-stream")  # Default to binary stream

    def read_video_chunks(video_path):
        with open(video_path, 'rb') as f:
            while chunk := f.read(1024 * 1024):  # Read in 1MB chunks
                yield chunk

    return Response(read_video_chunks(video_path), content_type=content_type)


def generate_subtitles(source: str) -> Response:
    """
    Serve subtitles for a video file.
    """
    file_manager: FileManager = io_service.get_file_manager()
    video_content: VideoContent = file_manager.get_video_by_name(source)
    subtitles_path = video_content.get_subtitles()

    if not os.path.exists(subtitles_path):
        raise FileNotFoundError(f"Subtitles file {source} not found")

    def read_subtitle_file(subtitles_path):
        with open(subtitles_path, 'r', encoding='utf-8') as f:
            for line in f:
                yield line

    return Response(read_subtitle_file(subtitles_path), content_type="text/vtt")
