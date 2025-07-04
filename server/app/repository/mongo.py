from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.database import Database, Collection

from app.module.logging_module import logger


class MongoDBConnector:
    def __init__(self, uri: str, db_name: str):
        self.uri: str = uri
        self.db_name: str = db_name
        self.client: MongoClient = None
        self.db: Database = None
        self._connect()

    def _connect(self):
        try:
            self.client = MongoClient(self.uri)
            # Trigger a connection check
            self.client.admin.command("ping")
            self.db = self.client[self.db_name]
            logger.info(f"Connected to MongoDB: {self.uri}/{self.db_name}")
        except ConnectionFailure as e:
            logger.warning("MongoDB connection failed:", e)

    def get_collection(self, collection_name: str) -> Collection:
        if self.db is None:
            raise Exception("Not connected to the database")
        return self.db[collection_name]

    def close(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
