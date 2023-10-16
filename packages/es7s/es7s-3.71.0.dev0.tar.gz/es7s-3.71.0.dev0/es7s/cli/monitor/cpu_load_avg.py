# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import math
from math import isclose, nextafter

import click
import pytermor as pt

from ._base import (
    CoreMonitor,
    MonitorCliCommand,
    CoreMonitorSettings,
    CoreMonitorConfig,
    GenericDemoComposer,
)
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command
from es7s.commons import SocketMessage
from es7s.shared import CpuInfo, Styles

OUTPUT_WIDTH = 14


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="recent average system load",
    output_examples=[
        "│`0.43 0.24 0.16`│  # low system load",
        "│`3.11 2.67 2.41`│  # (relatively) high system load",
    ],
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    Display amount of processes in the system run queue averaged
    over the last 1, 5 and 15 minutes.

    Output is a fixed string 14 chars wide: │`FF01 FF05 FF15`│, where FFnn
    is an average amount of running processes over the last 1, 5 and 15 minutes,
    respectively.
    """
    CpuLoadAvgMonitor(ctx, demo, **kwargs)

class CpuLoadAvgMonitor(CoreMonitor[CpuInfo, CoreMonitorConfig]):
    STYLES = [Styles.VALUE_PRIM_1, Styles.VALUE_PRIM_2, Styles.VALUE_UNIT_4]

    def _init_settings(self, debug_mode: bool, force_cache: bool) -> CoreMonitorSettings:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="cpu",
            socket_receive_interval_sec=2,
            update_interval_sec=2,
            alt_mode=True,
            config=CoreMonitorConfig("monitor.cpu-load-avg", debug_mode, force_cache),
            demo_composer=CpuLoadAvgDemoComposer,
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[CpuInfo]) -> pt.Text:
        def format_value(val: float) -> str:
            if isclose(val, 0.0, abs_tol=1e-3):
                val = nextafter(1e-3, 0)
            return pt.format_auto_float(float(val), 4, allow_exp_form=False) + " "

        def format_alter(count: int, label: str) -> list[pt.Fragment]:
            count_fmtd = pt.Fragment(f"{count:^3d}", Styles.VALUE_PRIM_2)
            label_fmtd = pt.Fragment(f"{label:^3.3s}", Styles.TEXT_LABEL)
            return [count_fmtd, label_fmtd]

        if self._state.is_alt_mode:
            return pt.Text(
                *format_alter(msg.data.thread_count, "THR"),
                pt.Fragment(" "),
                *format_alter(msg.data.core_count, "CPU"),
                pt.Fragment(" "),
            )

        result = pt.Text()
        load_avg_strs = [*map(format_value, msg.data.load_avg)]
        load_avg_strs[-1] = load_avg_strs[-1].rstrip(" ")
        for (tx, st) in zip(load_avg_strs, self.STYLES):
            result += pt.Fragment(tx, st)
        return result

    def _get_output_on_init(self) -> str | pt.IRenderable:
        return pt.distribute_padded(self.get_output_width(), " ...", " ...", " ...")


class CpuLoadAvgDemoComposer(GenericDemoComposer):
    def render(self):
        input_val_width = 7
        input_width = input_val_width * 3 + 2

        columns = [("CPU load average over", input_width), ("Results", OUTPUT_WIDTH)]
        total_width = sum(c[1] for c in columns) + 1
        self._print_triple_header(columns)

        def make_header_val_cells(cw):
            return ((v, cw) for v in ["1min", "5min", "15min"])

        self._print_header([*make_header_val_cells(7), *make_header_val_cells(4)], tline=False)

        vals = [(v, v / 5, v / 15) for v in [math.pow(math.e, e) for e in range(-8, 6, 1)]]
        for val in vals:
            inp = self._format_row_label(
                " ".join(f"{v:{input_val_width}.{'1e' if v < 1e-3 else '3f'}}" for v in val),
                input_width,
            )
            self._print_row(inp, self._render_msg(SocketMessage(CpuInfo(load_avg=val))))

        self._print_triple_header([("Alternative mode", total_width)])
        self._switch_alt_mode(True)
        label = self._format_row_label("Logical/physical CPUs", input_width)
        self._print_row(label, self._render_msg(SocketMessage(CpuInfo(core_count=4, thread_count=8))))
        self._print_footer(total_width)
