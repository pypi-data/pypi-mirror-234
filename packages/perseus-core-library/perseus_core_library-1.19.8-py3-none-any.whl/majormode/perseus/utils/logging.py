# Copyright (C) 2019 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import logging
import sys

from majormode.perseus.constant.logging import LOGGING_LEVELS
from majormode.perseus.constant.logging import LoggingLevelLiteral
from majormode.perseus.utils import cast


DEFAULT_LOGGING_FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
DEFAULT_LOGGING_LEVEL = LoggingLevelLiteral.info


def cast_string_to_logging_level(logging_level: str) -> LoggingLevelLiteral:
    return cast.string_to_enum(logging_level, LoggingLevelLiteral)


def get_console_handler(logging_formatter: logging.Formatter = DEFAULT_LOGGING_FORMATTER) -> logging.StreamHandler:
    """
    Return a logging handler that sends logging output to the system's
    standard output.


    @param logging_formatter: An object `Formatter` to set for this handler
        to appropriately format logging records.


    @return: An instance of the `StreamHandler` class which write logging
        record, appropriately formatted, to the standard output stream.
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging_formatter)
    return console_handler


def set_up_logger(
        logging_formatter: logging.Formatter = DEFAULT_LOGGING_FORMATTER,
        logging_level: LoggingLevelLiteral = DEFAULT_LOGGING_LEVEL,
        logger_name: str = None) -> logging.Logger:
    """
    Set up a logging handler that sends logging output to the system's
    standard output.


    @param logging_formatter: An object `Formatter` to to appropriately
        format logging records.

    @param logging_level: The logging threshold for this logger.  Logging
        messages which are less severe than this value will be ignored;
        logging messages which have severity level or higher will be
        emitted by whichever handler or handlers service this logger,
        unless a handler’s level has been set to a higher severity level
        than `logging_level`.

    @param logger_name: The name of the logger to add the logging handler
        to.  If `logger_name` is `None`, the function attaches the logging
        handler to the root logger of the hierarchy.


    @return: An object `Logger`.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(LOGGING_LEVELS[logging_level or DEFAULT_LOGGING_LEVEL])
    logger.addHandler(get_console_handler(logging_formatter=logging_formatter))
    logger.propagate = False
    return logger
