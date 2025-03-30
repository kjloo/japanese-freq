from flask import Flask, Blueprint
from flask_socketio import SocketIO

# Blueprint for routes
app_routes = Blueprint('routes', __name__)

# Initialize Flask app
app = Flask(__name__, static_folder="/app/static/assets",
            template_folder="/app/static")

app.debug = True

# Register Blueprint
app.register_blueprint(app_routes)

# Initialize SocketIO with the same app instance
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSockets
