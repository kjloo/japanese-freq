from flask import Response, request, jsonify
import os
import re

from app.module.file_module import file_manager
from app.model.content.video_content import VideoContent
from server.app.form.frequency.process_settings import ProcessSettings
from app.service import subtitle_service
from app.service import frequency_service

# Map of file extensions to Content-Type
CONTENT_TYPE_MAP = {
    "mp4": "video/mp4",
    "mkv": "video/x-matroska",
}


def generate(source: str) -> Response:
    """
    Generate video file chunks for streaming with support for seeking.
    """
    video_content: VideoContent = file_manager.get_video_by_name(source)
    video_path = video_content.get_video()
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file {source} not found")

    # Determine the file extension and content type
    file_extension = os.path.splitext(video_path)[1][1:].lower()
    content_type = CONTENT_TYPE_MAP.get(
        file_extension, "application/octet-stream")

    # Handle HTTP Range Requests
    range_header = request.headers.get("Range", None)
    if range_header:
        range_match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if not range_match:
            return Response("Invalid Range header", status=400)

        start = int(range_match.group(1))
        end = range_match.group(2)
        file_size = os.path.getsize(video_path)

        end = int(end) if end else file_size - 1

        if start >= file_size or end >= file_size:
            return Response("Requested Range Not Satisfiable", status=416)

        chunk_size = end - start + 1
        with open(video_path, "rb") as f:
            f.seek(start)
            chunk = f.read(chunk_size)

        response = Response(chunk, status=206, content_type=content_type)
        response.headers.add(
            "Content-Range", f"bytes {start}-{end}/{file_size}")
        response.headers.add("Accept-Ranges", "bytes")
        response.headers.add("Content-Length", str(chunk_size))
        return response

    # If no Range header, serve the entire file
    def read_video_chunks(video_path):
        with open(video_path, "rb") as f:
            while chunk := f.read(1024 * 1024):  # Read in 1MB chunks
                yield chunk

    response = Response(read_video_chunks(video_path),
                        content_type=content_type)
    response.headers.add("Accept-Ranges", "bytes")
    response.headers.add("Content-Length", str(os.path.getsize(video_path)))
    return response


def generate_subtitles(source: str, process_settings: ProcessSettings) -> dict[str]:
    """
    Serve subtitles for a video file along with the list of ignored words.
    """
    video_content: VideoContent = file_manager.get_video_by_name(source)
    subtitles_path = video_content.get_subtitles()

    if not os.path.exists(subtitles_path):
        raise FileNotFoundError(f"Subtitles file {source} not found")

    # Read the subtitle file content
    def read_subtitle_file(subtitles_path) -> list[str]:
        with open(subtitles_path, 'r', encoding='utf-8') as f:
            return f.readlines()

    subtitle_content: list[str] = read_subtitle_file(subtitles_path)

    styled_content = subtitle_service.style_subtitles(subtitle_content)

    content_dict = frequency_service.process_video(process_settings)

    # Construct the JSON response
    response_payload = {
        "content": content_dict,
        "subtitles": styled_content,
    }

    return response_payload
