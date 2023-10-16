# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import getpass
import logging
import os
import signal
import tempfile
from time import sleep

from .. import APP_DAEMON_DEBUG

RUNTIME_DIRS = [
    "/var/run/es7s",
    "/tmp/es7s",
]
_runtime_dir: str | None = None


def get_socket_path(topic: str, write: bool = False):
    filename = f"{topic}.socket"
    path = os.path.join(_get_runtime_dir(write), filename)
    if APP_DAEMON_DEBUG:
        path += ".debug"
    return path


def get_daemon_lockfile_path():
    return os.path.join(_get_runtime_dir(write=True), "es7s-daemon.lock")


def _get_runtime_dir(write: bool = False) -> str:
    max_attempt = 5
    for a in range(max_attempt):
        try:
            interval_sec = a**2
            if interval_sec > 0:
                logging.getLogger(__package__).warning(
                    f"Attempt #{a+1}/{max_attempt} to find runtime dir in {interval_sec} sec..."
                )
                sleep(interval_sec)  # retry after 1,4,9,16 sec -> 30 sec max total

            result = _get_runtime_dir_attempt(write)
            logging.getLogger(__package__).debug(f"Succesfully found runtime dir in {a+1} attempts: {result!r}")
            return result

        except Exception:
            pass
    raise RuntimeError("Applicable runtime dir not found")


def _get_runtime_dir_attempt(write: bool = False) -> str:
    global _runtime_dir
    if _runtime_dir:
        return _runtime_dir

    def try_read():
        open(os.path.join(runtime_dir, "es7s-daemon.lock"), mode="rt").close()

    def try_write():
        os.makedirs(runtime_dir, exist_ok=True)
        tempfile.TemporaryFile(dir=runtime_dir).close()

    for runtime_dir in RUNTIME_DIRS:
        try:
            if not write:
                try_read()
            else:
                try_write()
        except Exception:
            logging.getLogger(__package__).warning(
                f'Runtime dir is not {"writeable" if write else "readable"}: "{runtime_dir}"'
            )
            continue
        _runtime_dir = runtime_dir
        return runtime_dir
    raise RuntimeError("Could not find suitable runtime directory")


def get_cur_user() -> str:
    try:
        return os.getlogin()
    except OSError:
        return getpass.getuser()


def get_signal_desc(code: int) -> str:
    return f"{signal.Signals(code).name} ({code}): {signal.strsignal(code)}"
