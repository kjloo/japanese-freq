import pytest

from app.model.word.word_list import WordList

from test.fixture.mongo_fixture import mongo_test


@pytest.fixture(autouse=True)
def clear_word_list():
    """
    Automatically clear the WordList collection before each test.
    """
    WordList.objects.delete()


@pytest.mark.usefixtures("mongo_test")
def test_add_words():
    from app.repository.word.word_repository import word_repository

    words = ["apple", "banana", "cherry"]
    word_list = word_repository.add_words(words)
    assert set(word_list.words) == set(words)

    more_words = ["banana", "date", "fig"]
    updated_word_list = word_repository.add_words(more_words)
    assert set(updated_word_list.words) == set(
        ["apple", "banana", "cherry", "date", "fig"]
    )


@pytest.mark.usefixtures("mongo_test")
def test_get_words():
    from app.repository.word.word_repository import word_repository

    words = ["apple", "banana", "cherry"]
    word_list = word_repository.add_words(words)
    assert set(word_list.words) == set(words)
    current_words = word_repository.get_words()
    assert set(current_words) == set(words)


@pytest.mark.usefixtures("mongo_test")
def test_get_words_empty():
    from app.repository.word.word_repository import word_repository

    current_words = word_repository.get_words()
    assert current_words == []


@pytest.mark.usefixtures("mongo_test")
def test_remove_word():
    from app.repository.word.word_repository import word_repository

    words = ["apple", "banana", "cherry"]
    word_repository.add_words(words)

    current_words = word_repository.remove_word("banana")
    assert set(current_words.words) == set(["apple", "cherry"])

    # Removing a non-existent word should not raise an error
    current_words = word_repository.remove_word("date")
    assert set(current_words.words) == set(["apple", "cherry"])
