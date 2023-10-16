# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import time

import click
import pytermor as pt

from es7s.commons import SocketMessage
from es7s.shared import Styles, FrozenStyle
from es7s.shared import TimestampInfo
from ._base import CoreMonitor, MonitorCliCommand, CoreMonitorSettings, CoreMonitorConfig
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command

OUTPUT_WIDTH = 8


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="delta of current time and a timestamp from local or remote file",
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    TimestampMonitor(ctx, demo, **kwargs)


class TimestampMonitor(CoreMonitor[TimestampInfo, CoreMonitorConfig]):
    def __init__(self, ctx: click.Context, demo: bool, **kwargs):
        self._formatter = pt.dual_registry.get_by_max_len(6)
        self._formatter._allow_fractional = False  # @TODO @FIXME
        super().__init__(ctx, demo, **kwargs)

    def _init_settings(
        self, debug_mode: bool, force_cache: bool
    ) -> CoreMonitorSettings[CoreMonitorConfig]:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="timestamp",
            socket_receive_interval_sec=0.1,
            update_interval_sec=0.1,  # both for network activity indicator
            network_comm_indic=True,
            config=CoreMonitorConfig("monitor.timestamp", debug_mode, force_cache),
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[TimestampInfo]) -> pt.Text:
        now = time.time()
        if (cur_value := msg.data.ts) is None:
            return pt.Text("--".center(OUTPUT_WIDTH), Styles.TEXT_DISABLED)

        label = "∆"
        label_st = Styles.VALUE_LBL_5
        value_fg = pt.NOOP_COLOR
        value = now - cur_value
        value_prefix = ""

        if 0 < value < 300:
            value_fg = Styles.TEXT_UPDATED.fg
        if value < 0:
            label = "∇"
            label_st = FrozenStyle(fg=pt.cv.CYAN)
        if not msg.data.ok:
            value_prefix = "±"
            label_st = Styles.WARNING_LABEL

        delta_str = self._formatter.format(value).center(6)
        result = [
            pt.Fragment(label + " " + value_prefix, label_st),
            *self._renderer.render_time_delta(delta_str, value_fg),
        ]
        return pt.Text(*result)
