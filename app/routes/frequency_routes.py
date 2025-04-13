from flask import Blueprint, request, jsonify
import threading

from service import frequency_service
from module.logging import logger
from model.process_settings import ProcessSettings

# Blueprint for routes
frequency_routes = Blueprint('frequency_routes', __name__)


@frequency_routes.route("/api/frequency/process", methods=["POST"])
def start_process():
    # Extract the list of inputs from the request body
    data = request.get_json()
    payload = ProcessSettings(data)

    logger.debug(f"Starting frequency process with inputs: {payload}")

    # Start the processing in a separate thread
    thread = threading.Thread(
        target=frequency_service.process_words, args=(payload,))
    thread.start()

    return jsonify({"status": "started"}), 200
