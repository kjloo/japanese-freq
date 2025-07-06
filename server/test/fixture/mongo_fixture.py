from testcontainers.mongodb import MongoDbContainer
from mongoengine import connect, disconnect
import pytest


@pytest.fixture(scope="session")
def mongo_test():
    with MongoDbContainer("mongo:8.0.8") as mongo:
        disconnect(alias="default")
        connect(host=mongo.get_connection_url(),
                alias="default", uuidRepresentation='standard')
        yield
        disconnect(alias="default")
