import logging


def get_logger(level: str) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(fmt)

    logger.addHandler(handler)
    return logger
