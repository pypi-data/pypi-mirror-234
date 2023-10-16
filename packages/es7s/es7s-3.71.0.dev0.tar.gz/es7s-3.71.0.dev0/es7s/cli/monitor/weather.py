# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import re
import typing as t

import click
import pytermor as pt

from ._base import (
    CoreMonitor,
    MonitorCliCommand,
    CoreMonitorSettings,
    CoreMonitorConfig,
    GenericDemoComposer,
    CoreMonitorState, GenericRenderer,
)
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command
from es7s.commons import SocketMessage
from es7s.shared import (
    WeatherInfo,
    get_merged_uconfig,
    Styles,
    get_logger,
    FrozenStyle,
)
from es7s.commons import WeatherIconSet, get_wicon, justify_wicon

OUTPUT_WIDTH = 9


class _WeatherMonitorConfig(CoreMonitorConfig):
    weather_icon_max_width: int = 2
    weather_icon_set_id: int = 0
    wind_warn_threshold: float = 10.0

    def update_from_config(self):
        cfg = get_merged_uconfig()
        self.weather_icon_max_width = cfg.getint(self._config_section, "weather-icon-max-width")
        self.weather_icon_set_id = cfg.getint(self._config_section, "weather-icon-set-id")
        self.wind_warn_threshold = cfg.getfloat(self._config_section, "wind-speed-warn-threshold")


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="current weather",
    output_examples=[
        "│` 流 -4 °C`│",
        "│`!↑ 6.1m/s`│^A^",
    ],
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    Indicator of current weather. Queries 'wttr.in' web-service.

    Output is a fixed string 10 chars wide: │`!Ic TTT°C `│, where Ic is the weather
    icon, and TTT is current centigrade temperature. Alternative output format
    is: │`!D WWWm/s `│ (width is the same), where D is the wind direction icon and
    WWW is the speed of the wind in meters per second. Exclamation mark in either
    of formats indicates dangerously high wind speed, which is greater than
    <monitor.weather.wind-speed-warn-threshold> [default: 10] in m/s. Additionally,
    the monitor will periodically switch between primary mode with the temperature
    and alt mode with the wind, but only when necessary.

    Weather icon can be customized with config var <monitor.weather.weather-icon-set-id>,
    which is an integer such as 0 <= set-id <= 4, where 0 is the original emoji
    icon set [this is a default] and 1-4 are icon sets requiring NerdFont-compatible
    font to be available. Set 4 additionally provides differing icons for nighttime
    and daytime. Use '--demo' option to compare the sets.
    """
    WeatherMonitor(ctx, demo, **kwargs)


class WeatherMonitor(CoreMonitor[WeatherInfo, _WeatherMonitorConfig]):
    def _init_settings(self, debug_mode: bool, force_cache: bool) -> CoreMonitorSettings:
        return CoreMonitorSettings[_WeatherMonitorConfig](
            socket_topic="weather",
            socket_receive_interval_sec=0.1,
            update_interval_sec=0.1,  # both for network activity indicator
            message_ttl=3600,  # 1 hour
            alt_mode=True,
            network_comm_indic=True,
            inner_length_control=True,
            config=_WeatherMonitorConfig("monitor.weather", debug_mode, force_cache),
            renderer=WeatherRenderer,
            demo_composer=WeatherDemoComposer,
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[WeatherInfo]) -> pt.Text:
        logger = get_logger()
        fields = msg.data.fields
        logger.debug("Message data\n"+str(fields))
        if len(fields) != 3:
            raise ValueError(f"Malformed response: {fields!s}")

        wicon_max_width = self._setup.config.weather_icon_max_width
        wicon_origin = fields[0].strip().removesuffix("\ufe0f")  # U+FE0F VARIATION SELECTOR-16
        wicon, w_term, wicon_st = get_wicon(wicon_origin, self._setup.config.weather_icon_set_id)
        temp_origin = fields[1]
        temp_origin = temp_origin.removesuffix("°C").strip()
        temp_val = int(temp_origin)
        temp_str = f"{abs(temp_val):<2d}"
        if temp_val > 0:
            temp_str = "+" + temp_str
        elif temp_val < 0:
            temp_str = "-" + temp_str
        temp_unit = "°C"

        wind_origin = fields[2]
        wind_icon, wind_speed_origin, _ = re.split(r"([\d.]+)", wind_origin)
        wind_speed_f = float(wind_speed_origin)
        wind_speed_str = pt.format_auto_float(wind_speed_f, 3, False)
        wind_warning = wind_speed_f > self._setup.config.wind_warn_threshold
        warning_tx = pt.Text(" ")
        wind_unit = "m/s"

        if wind_warning:
            warning_tx = pt.Text("!", FrozenStyle(Styles.WARNING_ACCENT, blink=True, bold=True))

        logger.debug(f"Using weather icon set #{self._setup.config.weather_icon_set_id}")
        logger.debug(f"Weather icon: {wicon_origin} -> {justify_wicon(wicon, wicon_max_width)}")
        logger.debug(f"Temp. value: {temp_origin} -> {temp_val} -> {temp_str}")
        logger.debug(f"Wind speed: {wind_speed_origin} -> {wind_speed_f} -> {wind_speed_str}")

        if self._state.is_alt_mode:
            wind_icon_st = FrozenStyle(Styles.VALUE_PRIM_2)
            wind_val_st = FrozenStyle(Styles.VALUE_PRIM_2, italic=True)
            wind_unit_st = FrozenStyle(Styles.VALUE_UNIT_4, italic=True)
            if wind_warning:
                wind_icon_st = FrozenStyle(Styles.WARNING)
                wind_val_st = FrozenStyle(Styles.WARNING, bold=True, italic=True)
                wind_unit_st = FrozenStyle(Styles.WARNING, dim=True, italic=True)
            return (
                warning_tx
                + pt.Fragment(wind_icon, wind_icon_st)
                + pt.Fragment((" " + wind_speed_str.strip()).center(4), wind_val_st)
                + pt.Fragment(wind_unit.ljust(3), wind_unit_st)
            )

        return (
            warning_tx
            + pt.Fragment(justify_wicon(wicon, wicon_max_width)[0] + w_term, wicon_st)
            + pt.Fragment(temp_str.rjust(4), Styles.VALUE_PRIM_2)
            + pt.Fragment(temp_unit.ljust(2), Styles.VALUE_UNIT_4)
        )


class WeatherRenderer(GenericRenderer):
    def __init__(
        self,
        output_width: int,
        monitor_setup: CoreMonitorSettings,
        monitor_state: CoreMonitorState,
    ):
        weather_icon_len_shift = monitor_setup.config.weather_icon_max_width - 1
        output_width += weather_icon_len_shift
        super().__init__(output_width, monitor_setup, monitor_state)


class WeatherDemoComposer(GenericDemoComposer):
    def render(self):
        self._col_width = OUTPUT_WIDTH + 1
        self._total_width = (self._col_width + 1) * (WeatherIconSet.MAX_SET_ID + 2) - 1

        self._render_header()
        self._render_table()
        self._render_footer()

    def _render_header(self):
        self._print_triple_header([("Current temperature (different icon sets) and wind", self._total_width)])
        header = []
        for set_id in range(WeatherIconSet.MAX_SET_ID + 1):
            header.append((f"Set #{set_id}", self._col_width))  # netmon
        header.append(("Alt mode", self._col_width))
        self._print_header(header, tline=False)

    def _render_table(self):
        netcom_counter = 0
        def update(f: list[str]):
            nonlocal netcom_counter
            netcom_counter += 1
            nc = netcom_counter % 5 == 0
            msg = SocketMessage[WeatherInfo](WeatherInfo("MSK", f), network_comm=nc)
            self._monitor._state.last_valid_msg = msg
            return self._render_msg(msg)

        wmconfig = t.cast(_WeatherMonitorConfig, self._monitor._setup.config)
        fields_set = [
            (["❄", "-30", "↙2.3"], False),
            (["🌨", "-14", "←4.3"], False),
            (["🌫", "0", "↖0.0"], False),
            (["⛅", "6", "↑3.5"], False),
            (["🌦", "10", "↗0.9"], False),
            (["🌧", "14", "→6.5"], False),
            (["☁", "21", "↘13.9"], False),
            (["☀", "24", "↓3.3"], False),
            (["🌩", "29", "↗19.2"], True),
            (["🌩", "31", "↙16.2"], False),
            (["⛈", "40", "↓1.4"], False),
        ]
        for (fields, alt) in fields_set:
            cells = []
            for set_id in range(WeatherIconSet.MAX_SET_ID + 1):
                wmconfig.weather_icon_set_id = set_id
                self._switch_alt_mode(alt)
                cells.append(update(fields))

            self._switch_alt_mode(True)
            cells.append(update(fields))
            self._switch_alt_mode(False)

            self._print_row(*cells)

    def _render_footer(self):
        self._print_footer(self._total_width)
