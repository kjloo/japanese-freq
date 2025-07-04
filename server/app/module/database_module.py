from flask import Flask
from mongoengine import connect
from app.repository.mongo import MongoDBConnector
from app.module.config.mongo_config import MongoConfig

mongo_config: MongoConfig = None
mongo_connector: MongoDBConnector = None


def _get_mongo_config(app: Flask) -> MongoConfig:
    """
    Get the MongoDB configuration from the app config.
    :return: MongoConfig instance.
    """
    global mongo_config
    if mongo_config is not None:
        return mongo_config
    mongo_config = app.config.get("MONGO_CONFIG")
    if not mongo_config:
        raise ValueError("MongoDB configuration is not set in the app config.")
    return mongo_config


def get_mongo_connector(app: Flask) -> MongoDBConnector:
    """
    Get the MongoDB connector instance.
    :return: MongoDBConnector instance.
    """
    global mongo_connector
    if mongo_connector is not None:
        return mongo_connector
    mongo_config = _get_mongo_config(app)
    mongo_connector = MongoDBConnector(mongo_config.get_server_url(), mongo_config.db)
    return mongo_connector


def initialize_mongo_connection(app: Flask):
    """
    Initialize the MongoDB connection using the provided configuration.
    """
    mongo_config = _get_mongo_config(app)
    if not isinstance(mongo_config, MongoConfig):
        raise TypeError(
            "Expected MongoConfig instance, got: {}".format(type(mongo_config))
        )
    if not mongo_config:
        raise ValueError("MongoDB configuration is not set in the app config.")
    connect(
        db=mongo_config.db,
        host=mongo_config.host,
        port=mongo_config.port,
        username=mongo_config.user,
        password=mongo_config.password,
        authentication_source="admin",
    )
