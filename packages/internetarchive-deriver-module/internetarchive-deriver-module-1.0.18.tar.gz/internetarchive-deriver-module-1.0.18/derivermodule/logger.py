import logging
import logging.config

def set_level_debug():
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)

def set_level_info():
    logger.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)

def set_level_warning():
    logger.setLevel(logging.WARNING)
    ch.setLevel(logging.WARNING)

def set_level_error():
    logger.setLevel(logging.ERROR)
    ch.setLevel(logging.ERROR)

def set_level_critical():
    logger.setLevel(logging.CRITICAL)
    ch.setLevel(logging.CRITICAL)

def get_logger(logger_name):
    """
    Returns an instance of ``logging.Logger`` with a specific log format and
    logging level.
    """
    DEFAULT_LOGGING_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'

    logger = logging.getLogger(logger_name)
    logger.setLevel(DEFAULT_LOGGING_LEVEL)
    ch = logging.StreamHandler()
    ch.setLevel(DEFAULT_LOGGING_LEVEL)
    formatter = logging.Formatter(LOG_FORMAT)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

#: Default logger with name ``'derivermodule'``
logger = get_logger('derivermodule')
