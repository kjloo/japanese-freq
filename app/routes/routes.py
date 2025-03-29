from flask import Blueprint, render_template
from service import japanese_freq_service

# Blueprint for routes
app_routes = Blueprint('routes', __name__)


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
