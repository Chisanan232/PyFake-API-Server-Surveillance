"""
This module provides functionality for initializing and configuring logging settings.
It allows customization of logging formats, date/time formats, and logging levels.
The module also ensures compatibility for Python versions below 3.9 by handling the
absence of the `encoding` parameter in the `logging.basicConfig` function.
"""

import logging
import sys

DEBUG_LEVEL_LOG_FORMAT: str = "%(asctime)s [%(levelname)8s] (%(name)s - %(funcName)s at %(lineno)d): %(message)s"
DEBUG_LEVEL_LOG_DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S UTC%z"


def init_logger_config(
    formatter: str = "",
    datefmt: str = "",
    level: int = logging.INFO,
    encoding: str = "utf-8",
) -> None:
    """
    Configures the logger with the specified settings and initializes the logging system.
    Allows setting the format, date format, logging level, and encoding for the logs.
    If the logging level is DEBUG, it overrides the `formatter` and `datefmt` with predefined
    debug-level configurations. Compatibility for Python versions below 3.9 is handled
    by omitting the encoding parameter in those cases.

    :param formatter: Specifies the log message format. Defaults to an empty string.
    :param datefmt: Specifies the date/time format for log messages. Defaults to an empty string.
    :param level: Sets the logging level (e.g., DEBUG, INFO, WARNING). Defaults to logging.INFO.
    :param encoding: Encoding used for log messages. Defaults to "utf-8". This parameter is applied
        only for Python versions 3.9 and above.
    :return: This function does not return a value.
    """
    if level == logging.DEBUG:
        formatter = DEBUG_LEVEL_LOG_FORMAT
        datefmt = DEBUG_LEVEL_LOG_DATETIME_FORMAT

    if sys.version_info >= (3, 9):
        logging.basicConfig(
            format=formatter,
            datefmt=datefmt,
            level=level,
            encoding=encoding,
        )
    else:
        logging.basicConfig(
            format=formatter,
            datefmt=datefmt,
            level=level,
        )
