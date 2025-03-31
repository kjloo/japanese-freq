from flask import Blueprint, jsonify
import threading

from service import frequency_service

# Blueprint for routes
frequency_routes = Blueprint('frequency_routes', __name__)


@frequency_routes.route("/api/frequency/process", methods=["POST"])
def start_process():
    thread = threading.Thread(target=frequency_service.process_inputs)
    thread.start()
    return jsonify({"status": "started"}), 200
