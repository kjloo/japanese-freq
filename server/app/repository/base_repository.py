from pymongo.database import Collection
from abc import ABC

from app.module.database_module import mongo_connector


class BaseRepository(ABC):
    def __init__(self, collection_name: str):
        self.collection_name: str = collection_name
        self.collection: Collection = mongo_connector.get_collection(
            collection_name)
