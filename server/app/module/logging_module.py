import logging

# Set format of logging with class and function name
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(filename)s.%(funcName)s: %(message)s'
)
logger = logging.getLogger('app.module.app_module')
