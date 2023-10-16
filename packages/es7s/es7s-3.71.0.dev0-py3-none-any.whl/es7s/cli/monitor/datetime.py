# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import datetime

import click
import pytermor as pt

from ._base import (
    CoreMonitor,
    MonitorCliCommand,
    CoreMonitorSettings,
    CoreMonitorConfig,
    GenericDemoComposer,
)
from . import SPACE_2
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command
from es7s.commons import SocketMessage
from es7s.shared import Styles, get_merged_uconfig


class _DatetimeMonitorConfig(CoreMonitorConfig):
    display_year: bool = False
    display_seconds: bool = False

    def update_from_config(self):
        config = get_merged_uconfig()
        self.display_year = config.getboolean(self._config_section, "display-year")
        self.display_seconds = config.getboolean(self._config_section, "display-seconds")


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="current date and time",
    output_examples=[
        "│`We 14 Dec  21:27`│",
        "│`Th 02 Mar  02:05:11`│",
        "│`Su 27 Nov 2022  04:07:32`│",
    ],
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    Output is a fixed string consisting of two parts separated by two spaces.

    First one is either 10 chars wide: │`DOW·DD·MMM`│, where DOW is current day
    of the week abbreviation, DD is current day, and MMM is current month, or
    15 chars wide: │`DOW·DD·MMM·YYYY`│ (same, but also includes year -- YYYY).

    Second one is either 5 chars wide: │`HH·MM`│, where HH is hours and MM is
    minutes -- current system time, or 8 chars wide: │`HH·MM·SS`│ (same, but
    also includes seconds).

    Total output length varies from 16 to 24 characters.

    Modes depend on config variables <monitor.datetime.display-year> [default: no]
    and <monitor.datetime.display-seconds> [default: no].
    """
    DatetimeMonitor(ctx, demo, **kwargs)


class DatetimeMonitor(CoreMonitor[None, _DatetimeMonitorConfig]):
    def _init_settings(
        self, debug_mode: bool, force_cache: bool
    ) -> CoreMonitorSettings[_DatetimeMonitorConfig]:
        return CoreMonitorSettings(
            socket_topic="datetime",
            config=_DatetimeMonitorConfig("monitor.datetime", debug_mode, force_cache),
            demo_composer=SystemDateDemoComposer,
        )

    def get_output_width(self) -> int:
        year_len = 5 if self._setup.config.display_year else 0
        seconds_len = 3 if self._setup.config.display_seconds else 0
        return 16 + year_len + seconds_len

    def _format_data_impl(self, msg: SocketMessage[None]) -> pt.Text:
        now = datetime.datetime.fromtimestamp(msg.timestamp)

        day_st = Styles.VALUE_PRIM_2
        mon_st = Styles.VALUE_FRAC_3
        dow_st = year_st = Styles.VALUE_LBL_5
        hours_st = Styles.VALUE_PRIM_2
        minutes_st = Styles.VALUE_FRAC_3
        seconds_st = sep_st = Styles.VALUE_LBL_5

        now_str = now.strftime("%a %0e %b %Y %H %M %S").split(" ")
        dow = pt.Fragment(now_str.pop(0)[:2], dow_st)
        day = pt.Fragment(now_str.pop(0), day_st)
        mon = pt.Fragment(now_str.pop(0), mon_st)
        year = pt.Fragment(now_str.pop(0), year_st)
        hours = pt.Fragment(now_str.pop(0), hours_st)
        minutes = pt.Fragment(now_str.pop(0), minutes_st)
        seconds = pt.Fragment(now_str.pop(0), seconds_st)
        sep1 = pt.Fragment(" ")
        sep2 = pt.Fragment(self._get_colon_sep(round(now.timestamp())), sep_st)

        result = [dow, sep1, day, sep1, mon]
        if self._setup.config.display_year:
            result += [sep1, year]
        result += [SPACE_2.fragment, hours, sep2, minutes]
        if self._setup.config.display_seconds:
            result += [sep2, seconds]
        return pt.Text(*result)

    def _get_colon_sep(self, now: int) -> str:
        return ":" if now % 7 > 0 else " "


class SystemDateDemoComposer(GenericDemoComposer):
    pass
