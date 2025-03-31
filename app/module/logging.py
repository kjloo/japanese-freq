import logging

# Set up Flask logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.DEBUG)
