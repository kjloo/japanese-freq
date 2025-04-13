from threading import Event
import json
import os

from module.socket_module import socketio
from module.logging import logger

ignore_list_file: str = '.ignorelist'
ignore_list: set[str] = []

if os.path.exists(ignore_list_file):
    with open(ignore_list_file, 'r') as f:
        ignore_list = set(json.load(f))


def get_ignore_list() -> set[str]:
    return ignore_list


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

            ignore_list.add(word)

            # Add the word to the ignore list file
            with open(ignore_list_file, 'w', encoding='utf-8') as f:
                json.dump(list(ignore_list), f, ensure_ascii=False, indent=4)

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
