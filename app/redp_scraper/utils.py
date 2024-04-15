import logging
from typing import Callable

def exception_handler(logger: logging.Logger, expected_message: str = None):
    """Exception handler decorator that logs the exception and returns None."""
    def decorator(func: Callable):
        def inner(*args, **kwargs):
            """Inner function that wraps the function and handles the exception."""
            try:
                return func(*args, **kwargs)
            except Exception as exception:
                if expected_message:
                    logger.info(f'{expected_message}: {exception}')
                else:
                    logger.error(f'Exception in {func.__name__}: {exception}')
                return None
        return inner
    return decorator

def set_logger_config() -> None:
    """
    Set up the logger configuration for the application.

    This function configures the logger to log messages at the INFO level and
    formats the log messages to include the timestamp, log level, and message.
    The log messages are output to the console using a StreamHandler.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] - %(name)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
