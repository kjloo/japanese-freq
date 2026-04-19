from app.module.app_module import app
from app.routes.admin_routes import admin_routes
from app.routes.anki_routes import anki_routes
from app.routes.debug_routes import debug_routes
from app.routes.frequency_routes import frequency_routes
from app.routes.io_routes import io_routes
from app.routes.llm_routes import llm_routes
from app.routes.word_routes import word_routes
from app.routes.video_routes import video_routes

blueprints = [
    admin_routes,
    anki_routes,
    debug_routes,
    frequency_routes,
    io_routes,
    llm_routes,
    word_routes,
    video_routes,
]

# Register all blueprints
for blueprint in blueprints:
    app.register_blueprint(blueprint)
