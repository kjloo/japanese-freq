from flask import Blueprint, render_template, jsonify, Response

# Blueprint for routes
admin_routes = Blueprint('admin_routes', __name__)


@admin_routes.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint to verify if the server is running.
    Returns a JSON response indicating the server status.
    """
    try:
        # You can add more checks here if needed
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@admin_routes.route("/video/stream/<source>", methods=["GET"])
def serve_video(source):
    """
    Serve a video file from the static directory.
    """
    def generate():
        with open(f'videos/{source}', 'rb') as f:
            while chunk := f.read(1024 * 1024):  # Read in 1MB chunks
                yield chunk
    return Response(generate(), content_type='video/mp4')


@admin_routes.route("/")
# Main route to serve the app
def home():
    return render_template("index.html")
