from flask import Flask
from module.socket_module import socketio
import json


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # Check if the object has a `to_dict` method
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        # Let the base class default method raise the TypeError
        return super().default(obj)


# Initialize Flask app
app: Flask = Flask(__name__, static_folder="/app/static/assets",
                   template_folder="/app/static")
app.json_encoder = CustomJSONEncoder

# Initialize SocketIO with async mode
socketio.init_app(app, cors_allowed_origins="*", async_mode="eventlet")
