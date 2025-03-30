from app.routes.server import app_routes
from flask import jsonify
import threading
from flask import render_template, jsonify
from service import japanese_freq_service


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
