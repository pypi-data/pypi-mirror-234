# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing

import click
import pytermor as pt

from ._base import (
    CoreMonitor,
    CoreMonitorConfig,
    GenericDemoComposer,
    CoreMonitorSettings,
    MonitorCliCommand,
)
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command
from es7s.commons import SocketMessage
from es7s.shared import Styles
from es7s.shared import CpuInfo

OUTPUT_WIDTH = 6


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="current CPU load",
    output_examples=[],
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    a
    """
    CpuLoadMonitor(ctx, demo, **kwargs)


class CpuLoadMonitor(CoreMonitor[CpuInfo, CoreMonitorConfig]):
    def __init__(self, ctx: click.Context, demo: bool, **kwargs):
        super().__init__(ctx, demo, **kwargs)

    def _init_settings(self, debug_mode: bool, force_cache: bool) -> CoreMonitorSettings:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="cpu",
            ratio_styles_map=CoreMonitorSettings.alerting_ratio_stmap,
            config=CoreMonitorConfig("monitor.cpu-load", debug_mode, force_cache),
            demo_composer=CpuLoadDemoComposer,
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[CpuInfo]) -> pt.RT | list[pt.FrozenText]:
        na_fmtd = pt.FrozenText("N/A", width=OUTPUT_WIDTH, align="center")
        load_perc = msg.data.load_perc
        if load_perc is None:
            self._state.ratio = 0
            return [na_fmtd]
        self._state.ratio = load_perc / 100
        load_fmtd = pt.FrozenText(f"{round(load_perc):^3d}", Styles.VALUE_PRIM_1)
        unit_fmtd = pt.FrozenText("%", Styles.VALUE_UNIT_4)
        return self._renderer.wrap_progress_bar(load_fmtd, unit_fmtd)


class CpuLoadDemoComposer(GenericDemoComposer):
    def render(self):
        columns = 5
        total_width = columns * (OUTPUT_WIDTH) + (columns - 1)
        self._print_triple_header([("CPU load (all cores)", total_width)])

        load_base = -1
        while load_base < 100:
            row = []
            for _ in range(columns):
                c = 1
                if load_base >= 4:
                    c = 2
                if load_base >= 10:
                    c = 3
                if load_base >= 39:
                    c = 4
                if load_base >= 40:
                    c = 5
                load_base += c
                row.append(self._render_msg(SocketMessage(CpuInfo(load_perc=load_base))))
            self._print_row(*row)

        def _format_special(label: str, output: str) -> tuple[pt.RT, ...]:
            return self._format_row_label(label, total_width - OUTPUT_WIDTH - 1), output

        def _make_specials() -> typing.Iterable[tuple[pt.RT, ...]]:
            yield _format_special("Disabled", self._monitor._renderer.update_disabled())
            yield _format_special("Config reloading", self._monitor._renderer.update_busy())
            yield _format_special("Empty daemon data bus", self._monitor._renderer.update_no_data())
            yield _format_special("Critical failure", self._monitor._renderer.update_on_error())
            yield _format_special("Post-failure timeout", self._monitor._renderer.update_idle())
            yield _format_special("Initialzing", self._monitor._renderer.update_init())

        self._print_triple_header([("Specials", total_width)])
        self._print_rows(*_make_specials())
        self._print_footer(total_width)
