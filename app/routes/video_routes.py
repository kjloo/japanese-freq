from flask import Blueprint, Response, abort
from service import video_service

# Blueprint for routes
video_routes = Blueprint('video_routes', __name__)


@video_routes.route("/api/video/stream/<source>", methods=["GET"])
def serve_video(source):
    """
    Serve a video file using the generate method from video_service.
    """
    try:
        # Use the generate method from video_service
        return Response(video_service.generate(source), content_type='video/mp4')
    except FileNotFoundError:
        # Handle the case where the video file does not exist
        abort(404, description="Video file not found")


@video_routes.route("/api/video/subtitles/<source>", methods=["GET"])
def get_subtitles(source):
    """
    Serve subtitles for a video file using the generate method from video_service.
    """
    return Response(video_service.generate_subtitles(source), content_type='text/vtt')
