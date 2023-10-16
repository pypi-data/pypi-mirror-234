# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import logging

import click
import pytermor as pt

from es7s.commons import SocketMessage
from es7s.shared import Styles, get_logger, FrozenStyle
from es7s.shared import TemperatureInfo
from ._base import (
    MonitorCliCommand,
    CoreMonitor,
    CoreMonitorSettings,
    CoreMonitorConfig,
    GenericDemoComposer,
    GenericRenderer,
)
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command

OUTPUT_WIDTH = 11


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="current temperature sensors data",
    output_examples=[],
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    TemperatureMonitor(ctx, demo, **kwargs)


class TemperatureMonitor(CoreMonitor[TemperatureInfo, CoreMonitorConfig]):
    def __init__(self, ctx: click.Context, demo: bool, **kwargs):
        self._value_min = None
        self._value_max = None
        super().__init__(ctx, demo, **kwargs)

    def _init_settings(self, debug_mode: bool, force_cache: bool) -> CoreMonitorSettings:
        return CoreMonitorSettings(
            socket_topic="temperature",
            alt_mode=True,
            config=CoreMonitorConfig("monitor.temperature", debug_mode, force_cache),
            renderer=GenericRenderer,
            demo_composer=TemperatureDemoComposer,
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[TemperatureInfo]) -> pt.RT | list[pt.RT]:
        orig_values = msg.data.values_c
        sorted_values = sorted(orig_values, key=lambda v: v[1], reverse=True)

        if len(sorted_values) > 0:
            local_min = sorted_values[-1][1]
            local_max = sorted_values[0][1]
            self._value_min = min(self._value_min or local_min, local_min)
            self._value_max = max(self._value_max or local_max, local_max)

        if self._state.is_alt_mode:
            if self.current_frame == 0:
                val, mm, label = self._value_min, "min", "⤓"
            else:
                val, mm, label = self._value_max, "max", "⤒"

            result = [
                pt.Fragment(mm, FrozenStyle(Styles.VALUE_LBL_5, italic=True)),
                pt.Fragment(" " + label, Styles.VALUE_PRIM_2),
                pt.Fragment(
                    str(round(val)).center(4),
                    FrozenStyle(self._check_value_thresholds(None, val), italic=True),
                ),
                pt.Fragment("°C", FrozenStyle(Styles.VALUE_UNIT_4, italic=True)),
            ]
            return pt.Text(*result)

        values_limit = 3
        top_values_origin_indexes = []
        for (k, v) in sorted_values[:values_limit]:
            top_values_origin_indexes.append(orig_values.index((k, v)))

        values = []
        total_len = 0
        allowed_len = 6
        for oindex in sorted(top_values_origin_indexes):
            k, v = orig_values[oindex]
            st = self._check_value_thresholds(k, v)
            val_str = str(round(v))
            if len(val_str) == 1:
                val_str = " " + val_str
            if (total_len := total_len + len(val_str)) > allowed_len:
                break
            values.append(pt.Fragment(val_str, st))

        no_value_frag = pt.Fragment("--", Styles.TEXT_LABEL)
        if len(values) == 0:
            values += [no_value_frag] * 3
        if len(values) == 1:
            values += [no_value_frag]
        if len(values) == 2:
            values += [pt.Fragment()]

        result = pt.distribute_padded(OUTPUT_WIDTH - 3, *values)
        result += pt.Fragment(" °C", Styles.VALUE_UNIT_4)

        return result

    def _check_value_thresholds(self, key: str | None, val: float) -> pt.Style:
        if val < 30:  # @TODO to config
            return FrozenStyle(fg=pt.cv.CYAN)
        if val < 80:  # @TODO to config
            return Styles.VALUE_PRIM_2
        if val < 90:  # @TODO to config
            return Styles.WARNING
        if val < 100:  # @TODO to config
            if key and not self._demo:
                get_logger().warning(f"Sensor {key} detected high temperature: {val:.0f} C")  # @TODO to provider
            return Styles.ERROR
        if key and not self._demo:
            get_logger().error(f"Sensor {key} detected critical temperature: {val:.0f} C")   # @TODO to provider
        return Styles.CRITICAL_ACCENT


class TemperatureDemoComposer(GenericDemoComposer):
    def render(self):
        def update(values: list[tuple[str, float]]) -> str:
            return self._render_msg(SocketMessage(TemperatureInfo(values)))

        ROW_LEN = 3

        table_len = (OUTPUT_WIDTH + 1) * ROW_LEN - 1
        self._print_triple_header([("Temperature sensors data", table_len)])

        cells = [
            update([]),
        ]
        for bv in [-11, *range(0, 112, 6)]:
            cells.append(update([("", v) for v in [bv + 8.1, bv - 0.25, bv - 7.1]]))

        row = []
        while len(cells) > 0:
            row.append(cells.pop(0))
            if len(row) >= ROW_LEN or len(cells) == 0:
                self._print_row(*row)
                row.clear()

        def print_alt_desc_row(desc: str) -> pt.RT:
            alt_desc_len = (OUTPUT_WIDTH + 1) * (ROW_LEN - 1) - 1
            return self._print_row(self._format_row_label(desc, alt_desc_len), update([("", 0)]))

        self._print_triple_header([("Measured temp. range (since boot)", table_len)])
        self._switch_alt_mode(True)

        self._switch_alt_mode(True)
        self._set_alt_frame(0)
        print_alt_desc_row("Alt mode: min value")
        self._set_alt_frame(1)
        print_alt_desc_row("Alt mode: max value")

        self._print_footer(table_len)
