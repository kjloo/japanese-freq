from flask import Flask

from app.serde.encoder import CustomJSONProvider
from app.module.socket_module import socketio


# Initialize Flask app
app: Flask = Flask(__name__, static_folder="/app/static/assets",
                   template_folder="/app/static")
app.json = CustomJSONProvider(app)

# Initialize SocketIO with async mode
socketio.init_app(app, cors_allowed_origins="*", async_mode="eventlet")
