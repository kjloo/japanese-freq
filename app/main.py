from module.app_module import app
from routes.admin_routes import admin_routes
from routes.frequency_routes import frequency_routes
from routes.io_routes import io_routes
from routes.video_routes import video_routes

app.register_blueprint(admin_routes)
app.register_blueprint(frequency_routes)
app.register_blueprint(io_routes)
app.register_blueprint(video_routes)
