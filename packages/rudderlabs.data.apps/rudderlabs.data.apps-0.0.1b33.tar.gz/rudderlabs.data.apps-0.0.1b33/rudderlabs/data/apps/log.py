#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Logging utilities."""

import logging
import os
import sys

from collections.abc import Callable

import click
import termcolor

# get the default root logger of Rudderlabs
_logger = logging.getLogger("rudderlabs")

# by default, warning and error messages should be written to sys.stderr
_warn_err = logging.StreamHandler(sys.stderr)
_warn_err.setLevel(logging.WARNING)
_logger.addHandler(_warn_err)

# debug and info messages are written to sys.stdout


class _InfoFilter:
    def filter(self, record):
        return record.levelno <= logging.INFO


_debug_info = logging.StreamHandler(sys.stdout)
_debug_info.setLevel(logging.DEBUG)
_debug_info.addFilter(_InfoFilter())
_logger.addHandler(_debug_info)


COLORMAP = dict(
    debug=dict(),
    info=dict(attrs=["bold"]),
    warn=dict(color="yellow", attrs=["bold"]),
    warning=dict(color="yellow", attrs=["bold"]),
    error=dict(color="red"),
    exception=dict(color="red", attrs=["bold"]),
    critical=dict(color="red", attrs=["bold"]),
)
"""Default color map for homogenized color display"""


def _supports_color():
    """Returns True if the running system's terminal supports color, and False
    otherwise."""
    plat = sys.platform
    supported_platform = plat != "Pocket PC" and (
        plat != "win32" or "ANSICON" in os.environ
    )
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True


class ColorLog(object):
    """Colorizes logging colors."""

    def __init__(self, logger):
        self._log = logger

    def __getattr__(self, name):
        if name in [
            "debug",
            "info",
            "warn",
            "warning",
            "error",
            "exception",
            "critical",
        ]:
            if _supports_color():
                return lambda s, *args: getattr(self._log, name)(
                    termcolor.colored(s, **COLORMAP[name]), *args
                )
            else:
                return lambda s, *args: getattr(self._log, name)(s, *args)

        return getattr(self._log, name)


def get_logger(name):
    """Returns the default logger as setup by this module."""

    return ColorLog(logging.getLogger(name))


def _echo(text, *args, **kwargs):
    """Provides a colorized version of :py:func:`click.echo` (for terminals)

    The color is stripped off if outputting to a file or piping the results of
    a command using this function.

    Args:
      text (str): The text to be printed
      args (tuple): Tuple of attributes directly passed to
        :py:func:`termcolor.colored`
      kwargs (dict): Dictionary of attributes directly passed to
        :py:func:`termcolor.colored`
    """

    click.echo(termcolor.colored(text, *args, **kwargs))


def echo_normal(text):
    """Color preset for normal text output for :py:func:`click.echo`"""

    click.echo(text)


def echo_info(text):
    """Color preset for normal text output for :py:func:`click.echo`"""

    _echo(text, "green")


def echo_warning(text):
    """Color preset for normal warning output for :py:func:`click.echo`"""

    _echo(text, **COLORMAP["warn"])


# helper functions to instantiate and set-up logging
def setup(
    logger_name: str,
    format: str = "%(levelname)s:%(name)s@%(asctime)s: %(message)s",
) -> logging.Logger:
    """This function returns a logger object that is set up to perform logging
    using Rudderlabs loggers.

    Args:
        logger_name: The name of the module to generate logs for
        format: The format of the logs, see :py:class:`logging.LogRecord` for more
            details. By default, the log contains the logger name, the log time, the
            log level and the massage.

    Returns:
        logging.Logger: The logger configured for logging. The same logger can be retrieved using
            the :py:func:`logging.getLogger` function.
    """
    # generate new logger object
    logger = logging.getLogger(logger_name)

    # add log the handlers if not yet done
    if not logger_name.startswith("rudderlabs") and not logger.handlers:
        logger.addHandler(_warn_err)
        logger.addHandler(_debug_info)

    # this formats the logger to print the desired information
    formatter = logging.Formatter(format)
    # we have to set the formatter to all handlers registered in the current
    # logger
    for handler in logger.handlers:
        handler.setFormatter(formatter)

    # set the same formatter for rudderlabs loggers
    for handler in _logger.handlers:
        handler.setFormatter(formatter)

    return ColorLog(logger)


def setup_file_logger(
    log_file_name: str = "log.log", log_level: int = logging.INFO
) -> logging.Logger:
    """
    Get a logger object.

    :param log_file_name: The name of the log file.
    :param log_level: The log level.
    :return: The logger object.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # create a file handler
    handler = logging.FileHandler(log_file_name)
    handler.setLevel(log_level)

    # create a logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger


def set_verbosity_level(logger: logging.Logger, level: int):
    """Sets the log level for the given logger.

    Args:
        logger: The logger to generate logs for, or the name  of the module to generate logs for.
        level: Possible log levels are: 0: Error; 1: Warning; 2: Info; 3: Debug.

    Raises:
        ValueError:  If the level is not in range(0, 4).
    """
    if level not in range(0, 4):
        raise ValueError(
            "The verbosity level %d does not exist. Please reduce the number of "
            "'--verbose' parameters in your command line" % level
        )
    # set up the verbosity level of the logging system
    log_level = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }[level]

    # set this log level to the logger with the specified name
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    logger.setLevel(log_level)
    # set the same log level for the rudderlabs logger
    _logger.setLevel(log_level)


def verbosity_option(**kwargs) -> Callable:
    """Adds a -v/--verbose option to a click command.

    Args:
        **kwargs: Keyword arguments passed to :py:func:`click.option`

    Returns:
        Callable: A function that can be used as a decorator for a click command.
    """

    global _logger
    import click

    def custom_verbosity_option(f):
        def callback(ctx, param, value):
            ctx.meta["verbosity"] = value
            set_verbosity_level(_logger, value)
            _logger.debug("`rudderlabs' logging level set to %d", value)
            return value

        return click.option(
            "-v",
            "--verbose",
            count=True,
            expose_value=False,
            default=0,
            help="Increase the verbosity level from 0 (only error messages) "
            "to 1 (warnings), 2 (info messages), 3 (debug information) by "
            "adding the --verbose option as often as desired "
            "(e.g. '-vvv' for debug).",
            callback=callback,
            **kwargs,
        )(f)

    return custom_verbosity_option
