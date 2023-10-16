# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import signal

import daemon
import daemon.pidfile

from es7s.shared import (
    IoParams,
    LoggerParams,
    get_logger,
    get_stdout,
    init_config,
    init_io,
    init_logger,
)
from es7s.shared import get_daemon_lockfile_path
from es7s.shared import exit_gracefully
from es7s.shared import UserConfigParams
from .provider._factory import DataProviderFactory
from .. import APP_DAEMON_DEBUG, APP_VERBOSITY


def invoke():
    os.environ.update({"ES7S_DOMAIN": "DAEMON"})
    if APP_DAEMON_DEBUG:
        init_daemon_keep_streams()
    else:
        init_daemon_no_streams()


def init_daemon_no_streams():
    logger_params = LoggerParams(quiet=True)
    try:
        pidfile = daemon.pidfile.TimeoutPIDLockFile(get_daemon_lockfile_path(), 1)
        with daemon.DaemonContext(pidfile=pidfile, detach_process=False):
            d = Daemon(logger_params, None)
            d.run()
    except Exception as e:
        logger_params = LoggerParams(quiet=False)
        logger = init_logger(logger_params)
        logger.exception(e)


def init_daemon_keep_streams():
    logger_params = LoggerParams(verbosity=APP_VERBOSITY, quiet=False)
    try:
        d = Daemon(logger_params, IoParams())
        d.run()
    except Exception as e:
        get_stdout().echo(str(e))
        get_logger().exception(e)


class Daemon:
    def __init__(self, logger_params: LoggerParams, io_params: IoParams = None):
        init_logger(params=logger_params)
        if io_params:
            init_io(io_params)
        init_config(UserConfigParams())

        signal.signal(signal.SIGINT, self._exit)
        signal.signal(signal.SIGTERM, self._exit)
        signal.signal(signal.SIGUSR2, self._exit)

        self._providers = DataProviderFactory.make_providers()

    def run(self):
        for provider in self._providers:
            provider.prestart()
        for provider in self._providers:
            provider.join()

    def _exit(self, signal_code: int, *args):
        exit_gracefully(signal_code)
