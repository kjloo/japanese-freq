import os

# TODO: Turn this into a more yaml based config file
ANKI_SERVER_URL = os.getenv("ANKI_SERVER_URL", "http://localhost")
ANKI_SERVER_PORT = os.getenv("ANKI_SERVER_PORT", "8765")
