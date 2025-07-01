from app.module.app_module import app
from app.repository.mongo import MongoDBConnector
from app.module.config.mongo_config import MongoConfig

mongo_config: MongoConfig = app.config.get("MONGO_CONFIG")

mongo_connector = MongoDBConnector(mongo_config.get_server_url(), mongo_config.db)
