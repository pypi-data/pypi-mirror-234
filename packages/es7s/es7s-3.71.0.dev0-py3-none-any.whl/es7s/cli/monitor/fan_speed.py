# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import click
import pytermor as pt

from es7s.commons import SocketMessage
from es7s.shared import Styles, FrozenStyle
from es7s.shared import FanInfo
from ._base import CoreMonitorConfig, CoreMonitor, MonitorCliCommand, CoreMonitorSettings, \
    GenericRenderer
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command

OUTPUT_WIDTH = 9


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="current fan sensors data",
    output_examples=[],
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    FanSpeedMonitor(ctx, demo, **kwargs)


class FanSpeedMonitor(CoreMonitor[FanInfo, CoreMonitorConfig]):
    def __init__(self, ctx: click.Context, demo: bool, **kwargs):
        self._value_min = None
        self._value_max = None
        self._formatter = lambda v: (f"{v:4.0f}", "")
        super().__init__(ctx, demo, **kwargs)

    def _init_settings(
        self, debug_mode: bool, force_cache: bool
    ) -> CoreMonitorSettings[CoreMonitorConfig]:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="fan",
            socket_receive_interval_sec=2,
            update_interval_sec=2,
            alt_mode=True,
            # ratio_styles_map=CoreMonitorSettings.grayscale_ratio_stmap,
            renderer=GenericRenderer,
            config=CoreMonitorConfig("monitor.fan-speed", debug_mode, force_cache),
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[FanInfo]) -> pt.RT | list[pt.RT]:
        valf = msg.data.max()
        self._value_min = min(self._value_min or valf, valf)
        self._value_max = max(self._value_max or valf, valf)

        self._state.ratio = 0
        if self._value_min != self._value_max and self._value_min != valf:
            self._state.ratio = (valf - self._value_min) / (self._value_max - self._value_min)

        pref_st = Styles.VALUE_UNIT_4
        int_st = Styles.VALUE_PRIM_2
        frac_st = Styles.VALUE_FRAC_3

        if self._state.is_alt_mode:
            if self.current_frame == 0:
                label = "⤓"
                valf = self._value_min
            else:
                label = "⤒"
                valf = self._value_max
            pref_st = FrozenStyle(pref_st, italic=True)
            int_st = FrozenStyle(int_st, italic=True)
            frac_st = FrozenStyle(frac_st, italic=True)
        else:
            label = " "

        valstr, prefix_unit = self._formatter(valf)
        result = [
            pt.Fragment(label, Styles.VALUE_PRIM_2),
            *self._renderer.render_frac(valstr, int_st, frac_st),
            pt.Fragment(" " + prefix_unit + "RPM", pref_st),
        ]
        return pt.Text(*result)
