import logging

# Set up Flask logging
logging.basicConfig()
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.INFO)
