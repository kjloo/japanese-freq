from bson import ObjectId
from mongoengine import Document


def serialize_config(config: Document) -> dict:
    data = config.to_mongo().to_dict()
    if "_id" in data and isinstance(data["_id"], ObjectId):
        data["_id"] = str(data["_id"])
    return data
