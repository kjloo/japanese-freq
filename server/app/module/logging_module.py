from flask import current_app
import logging

# Set up Flask logging
logging.basicConfig()
logger = logging.getLogger('werkzeug')
logger.setLevel(current_app.config.get('LOG_LEVEL').upper())
