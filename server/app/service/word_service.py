from threading import Event
import json

from app.module.socket_module import socketio
from app.module.logging_module import logger
from app.module.dictionary_module import ignore_list, ignore_list_file
from app.service import anki_service
from app.repository.word_repository import word_repository


def get_ignore_list() -> set[str]:
    return ignore_list


def update_from_anki(deck_id: int, field_name: str) -> list[str]:
    """
    Update the ignore list with words from Anki.
    :param deck_id: The ID of the Anki deck.
    :param field_name: The name of the field to extract from Anki.
    :return: A list of words from the Anki deck.
    """
    anki_words = anki_service.get_cards_in_deck(deck_id, field_name)
    logger.debug(f"Words from Anki: {anki_words}")

    _update_ignore_list(anki_words)
    return list(ignore_list)


def update_from_file() -> list[str]:
    """
    Update the ignore list from a file.
    :return: A list of words from the ignore list file.
    """
    word_repository.add_words(list(ignore_list))
    return word_repository.get_words()


def ask_user(content: dict) -> dict:
    """
    Asks user if they already know the word and waits for their response.
    Removes words with a True response from the data dictionary and adds them to the ignore list file.
    """
    response_event = Event()  # Event to wait for user response

    def handle_response(response: dict):
        """
        Callback to handle user response from the client.
        """
        word = response.get('word')
        answer = response.get('answer')

        if answer:  # If the user knows the word (True)
            # Remove the word from the data dictionary
            content.pop(word, None)
            _update_ignore_list([word])

        response_event.set()  # Signal that the response has been received

    # Register a temporary SocketIO event listener for 'response'
    socketio.on_event('word_response', handle_response)

    for word in list(content.keys()):
        logger.debug(f"Requesting user input for word: {word}")
        socketio.emit('word_check', {
            'word': word,
            'frequency': content[word]["frequency"],
            'definition': content[word]["definition"]
        })
        response_event.clear()  # Reset the event
        response_event.wait()  # Wait for the user to respond

    return content


def _update_ignore_list(word_list: list[str]) -> None:
    """
    Update the ignore list by adding a word to it.
    :param word_list: The list of words to be added to the ignore list.
    """
    ignore_list.update(word_list)
    with open(ignore_list_file, 'w', encoding='utf-8') as f:
        json.dump(list(ignore_list), f, ensure_ascii=False, indent=4)
