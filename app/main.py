from module.app_module import app
from routes.routes import app_routes

app.register_blueprint(app_routes)
