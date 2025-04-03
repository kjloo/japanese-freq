from flask import Blueprint, request, jsonify
import threading

from service import frequency_service
from module.logging import logger

# Blueprint for routes
frequency_routes = Blueprint('frequency_routes', __name__)


@frequency_routes.route("/api/frequency/process", methods=["POST"])
def start_process():
    # Extract the list of inputs from the request body
    data = request.get_json()
    # Default to an empty list if "inputs" is not provided
    inputs: list[str] = data.get("inputs", [])
    word_check: bool = bool(data.get("word_check", True))
    freq_min: int = int(data.get("freq_min", 0))
    requires_definition: bool = bool(data.get("requires_definition", True))
    min_word_length: int = int(data.get("min_word_length", 1))

    logger.debug("Starting frequency process with inputs: %s, word_check, %s, freq_min: %d, requires_definition: %s, min_word_length: %d",
                 inputs, word_check, freq_min, requires_definition, min_word_length)

    if not isinstance(inputs, list):
        return jsonify({"error": "Invalid input format. 'inputs' must be a list."}), 400

    # Start the processing in a separate thread
    thread = threading.Thread(
        target=frequency_service.process_inputs, args=(inputs, word_check, freq_min, requires_definition, min_word_length))
    thread.start()

    return jsonify({"status": "started"}), 200
