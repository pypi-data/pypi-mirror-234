import logging


def get_logger(name: str = "") -> logging.Logger:
    if name is None or len(name) == 0:
        logger = logging.getLogger("randog")
    else:
        logger = logging.getLogger(f"randog.{name}")

    logger.addHandler(logging.NullHandler())
    return logger
