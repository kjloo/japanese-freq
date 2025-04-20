from flask import Blueprint, Response, abort, request, jsonify

from app.service import video_service
from app.model.process_settings import ProcessSettings

# Blueprint for routes
video_routes = Blueprint('video_routes', __name__)


@video_routes.route("/api/video/stream/<source>", methods=["GET"])
def serve_video(source) -> Response:
    """
    Serve a video file using the generate method from video_service.
    """
    try:
        # Use the generate method from video_service
        return video_service.generate(source)
    except FileNotFoundError:
        # Handle the case where the video file does not exist
        abort(404, description="Video file not found")


@video_routes.route("/api/video/subtitles/<source>", methods=["POST"])
def get_subtitles(source) -> Response:
    """
    Serve subtitles for a video file using the generate method from video_service.
    Handle errors gracefully.
    """
    # Extract the list of inputs from the request body
    data = request.get_json()
    if not data:
        abort(400, description="Invalid request: JSON body is required")

    payload = ProcessSettings(data).with_word_check(False)

    # Generate subtitles using the video_service
    subtitles = video_service.generate_subtitles(source, payload)
    return jsonify(subtitles), 200
