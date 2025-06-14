import logging
from rich.logging import RichHandler


logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X %D]",
    handlers=[RichHandler()]
)


def get_logger(scope: str):
    return logging.getLogger(scope)
