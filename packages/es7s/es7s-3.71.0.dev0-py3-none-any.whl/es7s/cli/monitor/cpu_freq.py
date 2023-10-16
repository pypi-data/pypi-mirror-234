# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import math

import click
import pytermor as pt

from es7s.commons import SocketMessage
from es7s.shared import Styles, FrozenStyle
from ._base import (
    CoreMonitor,
    GenericDemoComposer,
    CoreMonitorSettings,
    MonitorCliCommand,
    CoreMonitorConfig,
    GenericRenderer,
)
from .._decorators import catch_and_log_and_exit, catch_and_print, cli_pass_context, cli_command
from es7s.shared import CpuInfo

OUTPUT_WIDTH = 9


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="current CPU frequency",
    output_examples=[
        "│`2.55 GHz`│    current value",
        "│`max 5.1G`│^A^ max value",
        "│`min 800M`│^A^ min value",
    ],
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    CpuFreqMonitor(ctx, demo, **kwargs)

class CpuFreqMonitor(CoreMonitor[CpuInfo, CoreMonitorConfig]):

    def __init__(self, ctx: click.Context, demo: bool, **kwargs):
        self._formatter = pt.StaticFormatter(
            pad=True,
            allow_negative=False,
            unit_separator=" ",
            unit="Hz",
            prefix_refpoint_shift=+2,
        )
        self._alt_formatter = pt.StaticFormatter(
            self._formatter,
            max_value_len=3,
            unit_separator="",
            unit="",
        )
        self._value_min = None
        self._value_max = None
        super().__init__(ctx, demo, **kwargs)

    def _init_settings(self, debug_mode: bool, force_cache: bool) -> CoreMonitorSettings:
        return CoreMonitorSettings(
            socket_topic="cpu",
            socket_receive_interval_sec=2,
            update_interval_sec=2,
            alt_mode=True,
            #ratio_styles_map=CoreMonitorSettings.grayscale_ratio_stmap,
            renderer=GenericRenderer,
            config=CoreMonitorConfig("monitor.cpu-freq", debug_mode, force_cache),
            demo_composer=CpuFreqDemoComposer,
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[CpuInfo]) -> pt.RT | list[pt.RT]:
        value = msg.data.freq_mhz
        # _, value, _ = freq_mhz.min, freq_mhz.current, freq_mhz.max
        self._value_min = min(self._value_min or value, value)
        self._value_max = max(self._value_max or value, value)

        self._state.ratio = 0
        if self._value_min != self._value_max and self._value_min != value:
            self._state.ratio = (value - self._value_min) / (self._value_max - self._value_min)

        pref_st = Styles.VALUE_UNIT_4
        int_st = Styles.VALUE_PRIM_2
        frac_st = Styles.VALUE_FRAC_3

        if self._state.is_alt_mode:
            if self.current_frame == 0:
                v = self._value_min
                label = "⤓"
            else:
                v = self._value_max
                label = "⤒"
            pref_st = FrozenStyle(pref_st, italic=True)
            int_st = FrozenStyle(int_st, italic=True)
            frac_st = FrozenStyle(frac_st, italic=True)
        else:
            v = value
            label = " "

        val, prefix_unit = self._formatter.format(v).rsplit(" ", 1)
        prefix_unit = prefix_unit.rjust(4)

        result_parts = [
            pt.Fragment(label, Styles.VALUE_PRIM_2),
            *self._renderer.render_frac(val, int_st, frac_st),
            pt.Fragment(prefix_unit, pref_st),
        ]
        return pt.Text(*result_parts)


class CpuFreqDemoComposer(GenericDemoComposer):
    def render(self):
        values_mhz = [
            0.5,
            0.74,
            4,
            25,
            33,
            50,
            60,
            75,
            200,
            300,
            450,
            999,
            1.4e3,
            2.23e3,
            2.6e3,
            3.3e3,
            3.6e3,
            3.8e3,
            4.0e3,
            4.4e3,
            5.1e3,
            5.3e3,
            5.8e3,
            6.0e3,
        ]

        def update(value_mhz: float) -> str:
            return self._render_msg(SocketMessage(CpuInfo(freq_mhz=value_mhz)))

        values_mhz = sorted(values_mhz)
        value_min = values_mhz[0]
        value_max = values_mhz[-1]
        update(value_min)
        update(value_max)  # set up min and max values

        row_len = math.floor(math.sqrt(len(values_mhz)))
        table_len = (OUTPUT_WIDTH + 1) * row_len - 1
        self._print_triple_header([("CPU current frequency", table_len)])
        while len(values_mhz) > 0:
            cells = []
            while len(cells) < row_len:
                if len(values_mhz) == 0:
                    cells.append(" " * OUTPUT_WIDTH)
                    continue
                cells.append(update(values_mhz.pop(0)))
            self._print_row(*cells)

        self._print_triple_header([("Measured freq. range (since boot)", table_len)])
        self._switch_alt_mode(True)

        def print_alt_desc_row(desc: str) -> pt.RT:
            alt_desc_len = (OUTPUT_WIDTH + 1) * (row_len - 1) - 1
            return self._print_row(self._format_row_label(desc, alt_desc_len), update(value_min))

        self._set_alt_frame(0)
        print_alt_desc_row("Alt mode: min value")
        self._set_alt_frame(1)
        print_alt_desc_row("Alt mode: max value")

        self._print_footer(table_len)
