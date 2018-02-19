import os
import gzip
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = '/var/log/vision'
LOG_NAME = 'vision.log'
LOGGER_NAME = 'vision'

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh = RotatingFileHandler(os.path.join(LOG_DIR, LOG_NAME), maxBytes=5*2**20, backupCount=10)
fh.setFormatter(formatter)
logger.addHandler(fh)

sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

def get_logger(subsystem=None):
    if subsystem is None:
        logger_name = LOGGER_NAME
    else:
        logger_name = '{}.{}'.format(LOGGER_NAME, subsystem)

    return logging.getLogger(logger_name)

