# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os

from es7s._version import __version__, __updated__


VERBOSITY_ENVVAR_MAP = {
    "VERBOSE": 1,
    "DEBUG": 2,
    "TRACE": 3,
}

# --------------------------------------------------------------

APP_NAME = "es7s"
APP_VERSION = __version__
APP_UPDATED = __updated__

APP_DAEMON_DEBUG = bool(os.getenv("ES7S_DAEMON_DEBUG"))

APP_VERBOSITY = 0
if (envvar_value := os.getenv("ES7S_VERBOSITY")) in VERBOSITY_ENVVAR_MAP.keys():
    APP_VERBOSITY = VERBOSITY_ENVVAR_MAP.get(envvar_value)
elif envvar_value:
    try:
        APP_VERBOSITY = int(envvar_value)
    except ValueError:
        pass
