# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click
import pytermor as pt

from ._base import CoreMonitor, MonitorCliCommand, CoreMonitorSettings, CoreMonitorConfig
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command
from es7s.commons import SocketMessage
from es7s.shared import Styles
from es7s.shared import NetworkLatencyInfo

OUTPUT_WIDTH = 5


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="network latency",
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    NetworkLatencyMonitor(ctx, demo, **kwargs)


class NetworkLatencyMonitor(CoreMonitor[NetworkLatencyInfo, CoreMonitorConfig]):
    def _init_settings(
        self, debug_mode: bool, force_cache: bool
    ) -> CoreMonitorSettings[CoreMonitorConfig]:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="network-latency",
            network_comm_indic=True,
            config=CoreMonitorConfig("monitor.network-latency", debug_mode, force_cache),
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[NetworkLatencyInfo]) -> pt.Text:
        if msg.data.failed_ratio is None:
            return pt.Text("---".center(5), Styles.TEXT_DISABLED)

        if msg.data.failed_ratio > 0:
            st = Styles.WARNING
            if msg.data.failed_ratio > 0.5:
                st = Styles.ERROR
            return pt.Text(f"{100*(1-msg.data.failed_ratio):3.0f}%", st)

        val, sep, pfx, unit = pt.formatter_time_ms._format_raw(msg.data.latency_s * 1000)
        val = f"{val:<2s}"
        val = " " * max(0, 4 - len(val + sep + pfx + unit)) + val
        return pt.Text(
            pt.Fragment(val, Styles.VALUE_PRIM_2),
            pt.Fragment(sep),
            pt.Fragment(pfx + unit, Styles.VALUE_UNIT_4),
        )
