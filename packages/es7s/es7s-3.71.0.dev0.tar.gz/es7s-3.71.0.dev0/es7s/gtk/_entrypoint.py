# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import pydoc
import signal
import sys
from collections.abc import Iterable
from functools import cached_property

from es7s.shared import (
    IoParams,
    LoggerParams,
    get_stderr,
    get_stdout,
    init_config,
    init_io,
    init_logger,
    uconfig, get_logger,
)
from es7s.shared import UserConfigParams, get_merged_uconfig
from es7s.shared import exit_gracefully
from . import Gtk
from .indicator import ensure_dynload_allowed, IIndicator, IndicatorManager, IndicatorSystemCtl
from .. import APP_VERBOSITY


def invoke():
    os.environ.update({"ES7S_DOMAIN": "GTK"})
    _init()
    try:
        ic = IndicatorController()
        ic.run()
    except SystemExit:
        if stdout := get_stdout(False):
            stdout.echo()
        raise


def _init():
    logger_params = LoggerParams(verbosity=APP_VERBOSITY)
    io_params = IoParams()

    logger = init_logger(params=logger_params)
    _, _ = init_io(io_params)
    init_config(UserConfigParams())

    logger.log_init_params(
        ("Log configuration:", logger_params),
        ("Logger setup:", {"handlers": logger.handlers}),
        ("IO configuration:", io_params),
        ("Stdout proxy setup:", get_stdout().as_dict()),
        ("Stderr proxy setup:", get_stderr().as_dict()),
    )


class IndicatorController:
    def __init__(self):
        # signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGINT, self._exit)
        signal.signal(signal.SIGTERM, self._exit)
        signal.signal(signal.SIGUSR2, self._exit)

        self._indicators: list[IIndicator] = []
        self._indicator_mgr: IndicatorManager | None = None

    def run(self):
        self._init_threads()
        Gtk.main()  # noqa
        for indicator in self._indicators:
            indicator.join()

    def _init_threads(self):
        self._indicators = [*IndicatorFactory().make_all()]

        self._indicator_mgr = IndicatorManager(indicators=self._indicators)
        self._indicators.insert(0, self._indicator_mgr)

    def _exit(self, signal_code: int, *args):
        exit_gracefully(signal_code, callback=None)
        Gtk.main_quit()  # noqa
        sys.exit(signal_code)


class IndicatorFactory:
    @cached_property
    def single_mode(self):
        single_indicator = uconfig.get_merged().indicator_single_mode
        if not single_indicator:
            return None
        from importlib import util
        for import_path in [single_indicator, f"es7s.gtk.indicator.{single_indicator}"]:
            try:
                if util.find_spec(import_path):
                    get_logger().debug(f"Found single indicator class: {import_path}")
                    return import_path
            except ModuleNotFoundError:
                continue
        get_logger().warning(f"Single indicator property is invalid: {single_indicator}")
        return None

    def make_all(self) -> Iterable[IIndicator]:
        def _make_iter():
            yield from self._make_static()
            yield from self._make_dynamic()

        for indic_type in _make_iter():
            if self._instantiation_allowed(indic_type):
                yield indic_type()

    def _instantiation_allowed(self, indic: type[IIndicator]) -> bool:
        if not self.single_mode:
            return True
        return indic.__module__ == self.single_mode

    def _make_static(self) -> Iterable[type[IIndicator]]:
        yield IndicatorSystemCtl

    def _make_dynamic(self) -> Iterable[type[IIndicator]]:
        config = get_merged_uconfig()
        layout_cfg = filter(None, config.get("indicator", "layout").strip().split("\n"))

        for el in reversed([*layout_cfg]):
            module_name, origin_name = el.rsplit(".", 1)
            if (module := pydoc.safeimport(module_name)) is None:
                continue

            origin: type = getattr(module, origin_name)
            ensure_dynload_allowed(origin)

            yield origin
