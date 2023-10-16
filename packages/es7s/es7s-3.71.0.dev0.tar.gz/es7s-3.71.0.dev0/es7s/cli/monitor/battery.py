# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass

import click
import pytermor as pt

from es7s.commons import SocketMessage
from es7s.shared import Styles, BatteryInfo, FrozenStyle
from ._base import (
    CoreMonitor,
    MonitorCliCommand,
    AltItalicRenderer,
    CoreMonitorSettings,
    CoreMonitorConfig,
    GenericDemoComposer,
    CoreMonitorState,
)
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command

OUTPUT_WIDTH = 7


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="battery level and state",
    output_examples=[
        "│`▕▃▏↑45%`│    45%, charging (default)",
        "│`▕▂▏↑24%`│    24%, discharging (yellow)",
        "│`▕!▏  7%`│    7%, critical (red)",
        "│`~25 min`│^A^ 25 min. remaining",
    ],
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    Indicator of current battery charge level. Displays `ERROR` if there is no battery
    installed (or if the monitor failed to detect one).

    Output is a fixed string *7* chars wide: │`▕▃▏↑DD%`│, where DD is battery
    charge level in percents. Alternative output format is: │`~Hh␣MMm`│,
    where H and MM -- hours and minutes that indicate estimated duration of autonomic
    work (i.e., without external power sources).
    """
    BatteryMonitor(ctx, demo, **kwargs)

class BatteryMonitor(CoreMonitor[BatteryInfo, CoreMonitorConfig]):
    def _init_settings(self, debug_mode: bool, force_cache: bool) -> CoreMonitorSettings:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="battery",
            message_ttl=15.0,
            update_interval_sec=5.0,
            alt_mode=True,
            config=CoreMonitorConfig("monitor.battery", debug_mode, force_cache),
            renderer=_BatteryRenderer,
            demo_composer=BatteryDemoComposer,
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[BatteryInfo]) -> pt.Text:
        return self._renderer.format(msg.data, self._state.is_alt_mode)


@dataclass
class _IndicatorFormat:
    level_threshold: int | None
    is_charging: bool | None
    label: str
    label_style: FrozenStyle = Styles.FILL_DEFAULT
    charging_style: FrozenStyle = FrozenStyle(fg=pt.cv.GREEN, bold=True)
    overcolor_level: bool = False
    overcolor_border: bool = False

    def matches(self, binfo: BatteryInfo) -> bool:
        return binfo.level <= self.level_threshold and (
            binfo.is_charging == self.is_charging or self.is_charging is None
        )

    @property
    def level_style(self) -> pt.Style:
        return self.label_style if self.overcolor_level else Styles.TEXT_DEFAULT

    @property
    def border_style(self) -> pt.Style:
        return self.label_style if self.overcolor_border else Styles.BORDER_DEFAULT


class _BatteryRenderer(AltItalicRenderer):
    BORDER_LEFT_CHAR = "▕"
    BORDER_RIGHT_CHAR = "▏"

    # fmt: off
    VALUES_FMT = [
        _IndicatorFormat(6, False, '!', Styles.CRITICAL_ACCENT, Styles.CRITICAL_ACCENT, True, True),
        _IndicatorFormat(6, True, '!', Styles.ERROR, FrozenStyle(fg=pt.cv.HI_RED, bold=True), True, True),
        _IndicatorFormat(12, None, '!', Styles.ERROR, FrozenStyle(fg=pt.cv.HI_RED, bold=True), True, True),
        _IndicatorFormat(24, None, '▁', Styles.WARNING, FrozenStyle(fg=pt.cv.HI_YELLOW, bold=True), True, True),
        _IndicatorFormat(35, None, '▂'),
        _IndicatorFormat(45, None, '▃'),
        _IndicatorFormat(55, None, '▅'),
        _IndicatorFormat(65, None, '▅'),
        _IndicatorFormat(75, None, '▆'),
        _IndicatorFormat(85, None, '▇'),
        _IndicatorFormat(92, None, '█'),
        _IndicatorFormat(99, None, '█'),
        _IndicatorFormat(100, False, '✔', FrozenStyle(fg=Styles.TEXT_DEFAULT.fg, inversed=True), Styles.TEXT_DEFAULT),
        _IndicatorFormat(100, True, '✔', FrozenStyle(fg=pt.cv.GREEN, inversed=True), FrozenStyle(fg=pt.cv.GREEN)),
    ]
    NODATA_FMT = _IndicatorFormat(None, None, '?', label_style=FrozenStyle(Styles.WARNING_ACCENT), overcolor_level=True)
    BUSY_FMT = _IndicatorFormat(None, None, '*', FrozenStyle(Styles.WARNING), FrozenStyle(fg=pt.cv.GRAY), True, False)
    DISABLED_FMT = _IndicatorFormat(None, None, '-', FrozenStyle(Styles.TEXT_DISABLED), FrozenStyle(fg=pt.cv.GRAY), True, True)
    ERROR_FMT = _IndicatorFormat(None, None, 'X', FrozenStyle(Styles.ERROR), FrozenStyle(fg=pt.cv.GRAY), True, False)
    # fmt: on

    def __init__(
        self,
        output_width: int,
        monitor_setup: CoreMonitorSettings,
        monitor_state: CoreMonitorState,
    ):
        super().__init__(output_width, monitor_setup, monitor_state)
        self._output_error = self._apply(self.ERROR_FMT, status="", level="ERRO")
        self._output_disabled = self._apply(self.DISABLED_FMT, status=" ", level="OFF")
        self._output_no_data = self._apply(self.NODATA_FMT, status="", level="EMPT")
        self._output_busy = self._apply(self.BUSY_FMT, status="", level="BUSY")
        self._remaining_formatter = pt.DualFormatter(
            units=[
                pt.DualBaseUnit("sec", 60),
                pt.DualBaseUnit("min", 60),
                pt.DualBaseUnit("hr", 24, collapsible_after=10),
                pt.DualBaseUnit("day", overflow_after=365),
            ],
            allow_negative=False,
            allow_fractional=False,
            unit_separator=" ",
        )

    def format(self, binfo: BatteryInfo, alter_mode_enabled: bool) -> pt.Text:
        fmt = self._get_indicator_fmt(binfo)
        if alter_mode_enabled:
            remaining = self.render_time_delta(self._format_remaining(binfo))
            return pt.Text(*remaining)
        return self._apply(fmt, self._format_status(binfo), self._format_level(binfo))

    def _apply(self, fmt: _IndicatorFormat, status: str, level: str) -> pt.Text:
        """OUTPUT SIZE: 7"""
        return pt.Text(self.BORDER_LEFT_CHAR, fmt.border_style).append(
            pt.Fragment(fmt.label, fmt.label_style),
            pt.Fragment(self.BORDER_RIGHT_CHAR, fmt.border_style),
            pt.Fragment(status, fmt.charging_style),
            pt.Fragment(level, fmt.level_style),
        )

    def _get_indicator_fmt(self, binfo: BatteryInfo) -> _IndicatorFormat:
        if binfo.level is None:
            return self.NODATA_FMT
        for fmt in self.VALUES_FMT:
            if fmt.matches(binfo):
                return fmt
        return self.VALUES_FMT[-1]

    def _format_level(self, binfo: BatteryInfo) -> str:
        """OUTPUT SIZE: 3"""
        if binfo.level is None:
            return " --"
        if binfo.is_max:
            return "ULL"
        if isinstance(binfo.level, int | float):
            level_str = f"{binfo.level:.0f}"
        else:
            level_str = str(binfo.level)
        return "{:>3s}".format(f"{level_str}%")

    def _format_status(self, binfo: BatteryInfo) -> str:
        """OUTPUT SIZE: 1"""
        if binfo.is_max:
            return "F"
        if binfo.is_charging:
            return "↑"
        return " "

    def _format_remaining(self, binfo: BatteryInfo) -> str:
        """OUTPUT SIZE: 7"""
        if not binfo.is_charging:
            if binfo.remaining_sec is not None:
                return ("~" + self._remaining_formatter.format(binfo.remaining_sec)).center(
                    OUTPUT_WIDTH
                )
            return "?".center(OUTPUT_WIDTH)
        return "N/A".center(OUTPUT_WIDTH)


class BatteryDemoComposer(GenericDemoComposer):
    def render(self):
        left_col_width = 7
        total_width = left_col_width + 3 * (OUTPUT_WIDTH + 1)

        self._print_triple_header([("Battery state", total_width)])
        self._print_header(
            [
                ("Power", left_col_width),
                ("Discharging", 1 + 2 * OUTPUT_WIDTH),
                ("A/C", OUTPUT_WIDTH),
            ],
            tline=False,
            bline=False,
        )
        self._print_header(
            [
                ("level", left_col_width),
                ("default", OUTPUT_WIDTH),
                ("alt", OUTPUT_WIDTH),
                ("default", OUTPUT_WIDTH),
            ],
            tline=False,
            bline=True,
        )

        label_alt_ac = ""
        for level in range(0, 101, 5):
            cells = [self._format_row_label(str(level), left_col_width)]
            for charging in (False, True):
                for alt_mode in (False, True):
                    self._switch_alt_mode(alt_mode)
                    remaining_sec = int(10.5 * 3600 * (level + 0.01) / 100)

                    binfo = BatteryInfo(level, charging, remaining_sec)
                    msg = SocketMessage(data=binfo)
                    data_rendered = self._render_msg(msg)

                    if alt_mode and charging:
                        if level == 100:
                            label_alt_ac = data_rendered
                        continue
                    cells.append(data_rendered)
            self._print_row(*cells)

        def _format_special(label: str, output: str):
            return [self._format_row_label(label, left_col_width + 16), output]

        self._switch_alt_mode(False)
        self._print_triple_header([("Specials", total_width)])

        mrenderer = self._monitor._renderer
        self._print_rows(
            *[
                _format_special("Disabled", mrenderer.update_disabled()),
                _format_special("Config reloading", mrenderer.update_busy()),
                _format_special("Empty daemon data bus", mrenderer.update_no_data()),
                _format_special("Critical failure", mrenderer.update_on_error()),
                _format_special("Post-failure timeout", mrenderer.update_idle()),
                _format_special("Alt mode on A/C", label_alt_ac),
                _format_special("Initialzing", mrenderer.update_init()),
            ]
        )
        self._print_footer(total_width)
