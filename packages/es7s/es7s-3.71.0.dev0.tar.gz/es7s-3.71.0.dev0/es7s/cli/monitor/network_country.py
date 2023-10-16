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
from es7s.shared import NetworkCountryInfo

OUTPUT_WIDTH = 2


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="network external ip origin",
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    NetworkCountryMonitor(ctx, demo, **kwargs)


class NetworkCountryMonitor(CoreMonitor[NetworkCountryInfo, CoreMonitorConfig]):
    def __init__(self, ctx: click.Context, demo: bool, **kwargs):
        self._prev_value: str | None = None
        self._render_updated_till: int | None = None
        super().__init__(ctx, demo, **kwargs)

    def _init_settings(
        self, debug_mode: bool, force_cache: bool
    ) -> CoreMonitorSettings[CoreMonitorConfig]:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="network-country",
            network_comm_indic=True,
            alt_mode=True,
            config=CoreMonitorConfig("monitor.network-country", debug_mode, force_cache),
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[NetworkCountryInfo]) -> pt.Text:
        if self._state.is_alt_mode:
            conn_props = pt.Text()
            for label, attr in {"+M": "mobile", "+P": "proxy", "+H": "hosting"}.items():
                if getattr(msg.data, attr):
                    conn_props.append(pt.Fragment(label, Styles.VALUE_PRIM_2))
            if len(conn_props) == 0:
                conn_props += pt.Fragment("--", Styles.TEXT_DISABLED)
            return conn_props

        if cur_value := msg.data.country:
            if self._prev_value != cur_value:
                if self._prev_value:
                    self._render_updated_till = self._state.tick_render_num + 10
                self._prev_value = cur_value

            st = Styles.VALUE_PRIM_2
            if (self._render_updated_till or 0) > self._state.tick_render_num:
                st = Styles.TEXT_UPDATED
            geo_frag = pt.Fragment(f"{cur_value:2.2s}", st)
        else:
            geo_frag = pt.Fragment("--", Styles.TEXT_DISABLED)

        return pt.Text(geo_frag)
