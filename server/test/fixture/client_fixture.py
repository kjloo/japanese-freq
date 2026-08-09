import pytest
from unittest import mock
from app.module.app_module import app, register_all_blueprints


@pytest.fixture(scope="module")
def client():
    app.config["TESTING"] = True

    # Mock WordList to avoid MongoDB connection issues
    with mock.patch("app.model.word.word_list.WordList") as mock_word_list:
        mock_word_list.objects.first.return_value = mock.Mock(
            get_words=mock.Mock(return_value=[])
        )
        register_all_blueprints(app)
        with app.test_client() as client:
            yield client
