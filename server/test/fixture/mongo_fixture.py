from testcontainers.mongodb import MongoDbContainer
from mongoengine import connect, disconnect
import pytest


@pytest.fixture
def mongo_test():
    with MongoDbContainer("mongo:8.0.8") as mongo:
        connect(host=mongo.get_connection_url())
        yield
        disconnect()
