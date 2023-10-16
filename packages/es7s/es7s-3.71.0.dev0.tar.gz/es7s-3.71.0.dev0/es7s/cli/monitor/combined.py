# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import os
import signal
import threading as th
from abc import abstractmethod
from collections import deque
from functools import reduce
from io import StringIO

import click
import pytermor as pt
from pytermor import RT

from es7s.shared import (
    ShutdownableThread,
    get_stdout,
    get_logger,
    get_merged_uconfig,
    init_config,
    Styles,
)
from es7s.shared import OneLineStringIO
from . import LINE, Separator
from ._base import CoreMonitor, MonitorCliCommand
from .._decorators import catch_and_log_and_exit, catch_and_print, cli_command, cli_argument, \
    cli_pass_context


class Source:
    @abstractmethod
    def read(self) -> str:
        ...


class SourceStatic(Source):
    def __init__(self, src: Separator):
        self._src = get_stdout().render(src.fragment)

    def read(self) -> str:
        return self._src


class SourceInterceptor(Source):
    def __init__(self, io: StringIO, length: int):
        self._io = io
        self._length = length

    def read(self) -> str:
        if not self._io.readable():
            return " " * self._length
        result = self._io.read().replace(os.linesep, "")
        self._io.seek(0)
        return result


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="monitors defined in LAYOUT config var as single line",
    output_examples=[],
)
@cli_argument("layout", type=str, required=False, default="layout1")
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    CombinedMonitor(ctx, demo, **kwargs)


class CombinedMonitor(ShutdownableThread):
    """
    ;.
    """

    _UPDATE_TIMEOUTS = {
        "layout1": 1.0,
        "layout2": 2.0,
    }

    def __init__(self, ctx: click.Context, demo: bool, layout: str, **kwargs):
        import pydoc
        super().__init__(command_name=ctx.command.name, thread_name="ui")

        self._update_ui_event = th.Event()
        self._reset_ui_event = th.Event()
        self._init_ui_event = th.Event()
        self._init_ui_event.set()

        self._sources: deque[Source] = deque[Source]()
        self._monitors: deque[CoreMonitor] = deque[CoreMonitor]()

        config = get_merged_uconfig()
        layout_cfg = filter(None, config.get("monitor.combined", layout).strip().split("\n"))
        self._debug_mode = config.get_monitor_debug_mode()
        self._force_cache = config.getboolean("monitor", "force-cache", fallback=False)
        self._update_timeout = self._UPDATE_TIMEOUTS.get(layout)
        self.start()

        from . import ensure_dynload_allowed
        for el in list(layout_cfg):
            module_name, origin_name = el.rsplit(".", 1)
            if (module := pydoc.safeimport(module_name)) is None:
                continue

            origin: type|Separator = getattr(module, origin_name)
            ensure_dynload_allowed(origin)

            if isinstance(origin, Separator):
                self._sources.append(SourceStatic(origin))
                continue

            interceptor = OneLineStringIO()
            monitor = origin(
                ctx,
                demo=demo,
                interceptor=interceptor,
                ui_update=self._update_ui_event,
                debug_mode=self._debug_mode,
                force_cache=self._force_cache,
                **kwargs,
            )
            self._sources.append(SourceInterceptor(interceptor, monitor.get_output_width()))
            self._monitors.append(monitor)
            self._update_ui_event.set()

        signal.signal(signal.SIGUSR1, self._preview_alt_mode)
        signal.signal(signal.SIGUSR2, self._update_settings_request)

        self.join()

    def _preview_alt_mode(self, *args):
        get_logger().debug("Switching to alt mode")
        for monitor in self._monitors:
            monitor._preview_alt_mode(*args)
            self._update_ui_event.set()

    def _update_settings_request(self, signal_code: int, *args):
        get_logger().info(f"Updating the setup: {signal.Signals(signal_code).name} ({signal_code})")
        init_config()
        for monitor in self._monitors:
            monitor._update_settings_request(signal_code, *args)
        self._reset_ui_event.set()

    def shutdown(self):
        super().shutdown()
        for monitor in self._monitors:
            monitor.shutdown()

    def run(self):
        super().run()

        stdout = get_stdout()
        logger = get_logger()

        import psutil
        process = psutil.Process()

        def stats() -> str:
            result = ""
            for s in _stats():
                result += pt.render(LINE.fragment) + s
            return result

        def _stats() -> RT:
            yield from [
                stdout.render(p, Styles.DEBUG_SEP_INT)
                for p in [
                    f"{render_tick:>5d}/W{100*wasted_ticks/render_tick:>2.0f}%",
                    f"T{process.num_threads():>2d} "
                    + f"{process.cpu_percent():>3.0f}% "
                    + f"{pt.format_bytes_human(process.memory_info().rss):>5s}",
                ]
            ]

        render_tick = 0
        wasted_ticks = 0
        combined_line_prev = ""

        while True:
            if self.is_shutting_down():
                self.destroy()
                break
            if stdout.is_broken:
                logger.info("IoProxy detected broken pipe, terminating")
                self.shutdown()
                break

            if self._init_ui_event.is_set():
                stdout.echo_rendered("[...]", Styles.TEXT_DISABLED)

            if self._reset_ui_event.is_set():
                combined_line_prev = ""
                self._reset_ui_event.clear()

            if self._update_ui_event.wait(self._update_timeout):
                logger.debug("Received update ui event")
            else:
                logger.debug("Update ui timeout")
            self._update_ui_event.clear()

            combined_line = reduce(lambda t, s: t + s.read(), self._sources, "")
            render_tick += 1

            if not combined_line or combined_line == combined_line_prev:
                wasted_ticks += 1
                continue

            self._init_ui_event.clear()
            stdout.echo(combined_line + (stats() if self._debug_mode else ""))
            combined_line_prev = combined_line
