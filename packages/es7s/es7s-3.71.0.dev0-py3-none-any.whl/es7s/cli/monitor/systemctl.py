# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click
import pytermor as pt

from es7s.commons import SocketMessage
from es7s.shared import FrozenStyle, Styles
from es7s.shared import SystemCtlInfo
from ._base import CoreMonitor, CoreMonitorConfig, CoreMonitorSettings, IMonitorRenderer, \
    LetterIndicatorRenderer, MonitorCliCommand
from .._decorators import catch_and_log_and_exit, catch_and_print, cli_command, cli_pass_context

OUTPUT_WIDTH = 1
LABEL = 'F'


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="systemctl status",
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    SystemCtlMonitor(ctx, demo, **kwargs)


class SystemCtlMonitor(CoreMonitor[SystemCtlInfo, CoreMonitorConfig]):
    def _init_settings(
        self, debug_mode: bool, force_cache: bool
    ) -> CoreMonitorSettings[CoreMonitorConfig]:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="systemctl",
            config=CoreMonitorConfig("monitor.systemctl", debug_mode, force_cache),
            renderer=LetterIndicatorRenderer,
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _init_renderer(self) -> IMonitorRenderer:
        return LetterIndicatorRenderer(LABEL, self._setup, self._state)

    def _format_data_impl(self, msg: SocketMessage[SystemCtlInfo]) -> pt.Text:
        if msg.data.ok:
            st = Styles.TEXT_DISABLED
        else:
            st = FrozenStyle(fg=pt.cvr.LUST, bold=True, blink=True)

        return pt.Text(LABEL, st)
