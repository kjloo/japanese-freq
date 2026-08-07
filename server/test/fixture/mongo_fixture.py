import pytest
from mongoengine import connect, disconnect
from testcontainers.core.wait_strategies import LogMessageWaitStrategy
from testcontainers.community.mongodb import MongoDbContainer


@pytest.fixture(scope="session")
def mongo_test():
    container = MongoDbContainer("mongo:8.0.8")
    container.waiting_for(LogMessageWaitStrategy("Waiting for connections"))

    with container as mongo:
        disconnect(alias="default")
        connect(
            host=mongo.get_connection_url(),
            alias="default",
            uuidRepresentation="standard",
        )
        yield
        disconnect(alias="default")
