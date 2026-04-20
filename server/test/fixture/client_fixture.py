import pytest
from app.module.app_module import app, register_all_blueprints


@pytest.fixture(scope="module")
def client():
    app.config["TESTING"] = True
    register_all_blueprints(app)
    with app.test_client() as client:
        yield client
