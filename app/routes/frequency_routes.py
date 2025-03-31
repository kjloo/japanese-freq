from flask import Blueprint, request, jsonify
import threading

from service import frequency_service

# Blueprint for routes
frequency_routes = Blueprint('frequency_routes', __name__)


@frequency_routes.route("/api/frequency/process", methods=["POST"])
def start_process():
    # Extract the list of inputs from the request body
    data = request.get_json()
    # Default to an empty list if "inputs" is not provided
    inputs: list[str] = data.get("inputs", [])

    if not isinstance(inputs, list):
        return jsonify({"error": "Invalid input format. 'inputs' must be a list."}), 400

    # Start the processing in a separate thread
    thread = threading.Thread(
        target=frequency_service.process_inputs, args=(inputs))
    thread.start()

    return jsonify({"status": "started"}), 200
