# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os.path
import tempfile
from importlib import resources
from pathlib import Path

from .. import APP_NAME

# @TODO let the shell to find a binary in PATH or find it ourselves
SHELL_PATH = '/bin/bash'
LS_PATH = '/bin/ls'
LESS_PATH = '/usr/local/bin/less'
ENV_PATH = '/bin/env'
GIT_PATH = '/usr/bin/git'
WMCTRL_PATH = '/bin/wmctrl'
DOCKER_PATH = "/bin/docker"
TMUX_PATH = "/usr/local/bin/tmux"
GH_LINGUIST_PATH = "/usr/local/bin/github-linguist"
XDOTOOL_PATH = "/usr/bin/xdotool"
DCONF_PATH = "/usr/bin/dconf"

RESOURCE_PACKAGE = f'{APP_NAME}.data'
GIT_LSTAT_DIR = 'lstat-cache'

USER_ES7S_BIN_DIR = Path(os.path.expanduser("~/.es7s/bin"))
USER_ES7S_DATA_DIR = Path(os.path.expanduser("~/.es7s/data"))
USER_XBINDKEYS_RC_FILE = Path(os.path.expanduser("~/.xbindkeysrc"))

SHELL_COMMONS_FILE = "es7s-shell-commons.sh"

ESQDB_DATA_PIPE = os.path.join(tempfile.gettempdir(), 'es7s-esqdb-pipe')


def get_user_config_dir() -> str:
    import click

    return click.get_app_dir(APP_NAME)


def get_user_data_dir() -> Path:
    return USER_ES7S_DATA_DIR


def get_app_config_yaml(name: str) -> dict | list:
    import yaml

    filename = f"{name}.yml"
    user_path = os.path.join(USER_ES7S_DATA_DIR, filename)

    if os.path.isfile(user_path):
        with open(user_path, "rt") as f:
            return yaml.safe_load(f.read())
    else:
        f = resources.open_text(RESOURCE_PACKAGE, filename)
        return yaml.safe_load(f)
