import os
from flask import Blueprint, render_template, send_from_directory, jsonify, request
from service import japanese_freq_service

# Blueprint for routes
app_routes = Blueprint('routes', __name__)
image_dir = os.environ.get('IMAGE_DIR')


@app_routes.route('/api/board', methods=['GET'])
def get_board():
    resp = game_state_service.get_game_state()
    return resp.to_player_json()


@app_routes.route("/api/spymaster", methods=["GET"])
def get_spymaster_key():
    """
    API endpoint to return a randomly generated 5x5 spymaster key.
    """
    resp = game_state_service.get_game_state()
    return resp.to_master_json()


@app_routes.route("/api/guess", methods=["POST"])
def guess():
    """
    API endpoint to submit a guess
    """
    data = request.get_json()
    guess: int = data.get("guess")
    resp = game_state_service.submit_guess(guess)
    return resp.to_player_json()


@app_routes.route("/api/reset", methods=["POST"])
def reset_board():
    """
    API endpoint to start a new game.
    """
    game_state_service.reset_game_state()
    return jsonify({"message": "Game state reset successfully"}), 200


@app_routes.route('/images/<path:filename>')
def get_image(filename):
    return send_from_directory(image_dir, filename)


@app_routes.route("/")
# Main route to serve the app
def home():
    return render_template("index.html")


@app_routes.route("/<path:path>")
def serve_client_side_routes(path):
    """
    Catch-all route for client-side routing. This ensures React or other front-end frameworks
    handle routing on their end.
    """
    return render_template("index.html")
