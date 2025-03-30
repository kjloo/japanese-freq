from flask import Blueprint, render_template, jsonify
import threading

from module.app_module import app
from service import japanese_freq_service

# Blueprint for routes
app_routes = Blueprint('routes', __name__)


@app_routes.route("/api/process", methods=["POST"])
def start_process():
    thread = threading.Thread(target=japanese_freq_service.process_inputs)
    thread.start()
    return jsonify({"status": "started"}), 200


@app_routes.route("/health", methods=["GET"])
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


@app_routes.route("/")
# Main route to serve the app
def home():
    return render_template("index.html")
