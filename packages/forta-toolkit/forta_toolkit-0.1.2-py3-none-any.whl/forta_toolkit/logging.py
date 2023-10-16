"""Log scanning events."""

import logging
import sys

import forta_toolkit.metadata

# FORMAT ######################################################################

MESSAGE_PATTERN = '[{version}{{levelname}}] {{message}}'

def setup_log_format(pattern: str=MESSAGE_PATTERN, version: str='') -> str:
    """Return the log format string with the common informations filled."""
    __version = version
    # try reading the package metadata
    if not __version:
        __version = forta_toolkit.metadata.get_bot_version()
    # include the bot version in the log message if known
    if __version:
        __version = __version + ' - '
    return pattern.format(version=__version)

# LOGGING #####################################################################

def setup_logger(level: int=logging.INFO, pattern: str=setup_log_format(pattern=MESSAGE_PATTERN, version='')) -> None:
    """Configure the default log objects for a specific bot."""
    __formatter = logging.Formatter(pattern, style='{')

    __handler = logging.StreamHandler(sys.stdout)
    __handler.setLevel(level)
    __handler.setFormatter(__formatter)

    __logger = logging.getLogger()
    __logger.setLevel(level)
    __logger.addHandler(__handler)
