from flask import Flask
from module.socket_module import socketio

# Initialize Flask app
app: Flask = Flask(__name__, static_folder="/app/static/assets",
                   template_folder="/app/static")

# Initialize SocketIO with async mode
socketio.init_app(app, cors_allowed_origins="*", async_mode="eventlet")
