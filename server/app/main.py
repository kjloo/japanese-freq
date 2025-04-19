from app.module.app_module import app
from app.routes.admin_routes import admin_routes
from app.routes.frequency_routes import frequency_routes
from app.routes.io_routes import io_routes
from app.routes.video_routes import video_routes
from app.routes.debug_routes import debug_routes
from app.routes.anki_routes import anki_routes

app.register_blueprint(admin_routes)
app.register_blueprint(frequency_routes)
app.register_blueprint(io_routes)
app.register_blueprint(video_routes)
app.register_blueprint(debug_routes)
app.register_blueprint(anki_routes)
