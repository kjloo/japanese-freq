import logging

# Set up Flask logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.INFO)
