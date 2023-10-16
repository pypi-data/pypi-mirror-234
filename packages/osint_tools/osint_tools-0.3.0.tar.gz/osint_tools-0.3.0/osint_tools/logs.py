import logging
from os import environ

def setup_logger(which_logger):
    logging.basicConfig(
        filename=environ.get('LOG_FILE_PATH'),# taken from loca .env file, not set in settings.py
        format='%(asctime)s - %(process)d-%(levelname)s-%(funcName)s - %(message)s', 
        datefmt='%d-%b-%y %H:%M:%S',
        level=logging.INFO)
    log = logging.getLogger(which_logger)
    return log


WHICH_LOGGER = environ.get('WHICH_LOGGER')
# assert WHICH_LOGGER is not None, 'Set WHICH_LOGGER'
logger = setup_logger(WHICH_LOGGER)



