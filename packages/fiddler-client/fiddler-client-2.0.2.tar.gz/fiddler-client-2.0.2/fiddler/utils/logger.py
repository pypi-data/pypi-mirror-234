import logging
from logging import Logger


def get_logger(name: str) -> Logger:
    logger: Logger = logging.getLogger(name)
    logger.addHandler(logging.NullHandler())
    return logger
