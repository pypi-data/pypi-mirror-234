# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import itertools
import subprocess
from collections.abc import Iterable
from functools import cached_property
from subprocess import CalledProcessError

import pytermor as pt

from es7s.commons import SocketMessage
from es7s.shared import ShocksInfo, ShocksProxyInfo
from es7s.shared import get_logger, get_merged_uconfig
from ._base import (
    _BaseIndicator,
)
from ._icon_selector import IIconSelector, IconEnum
from ._state import _StaticState, _BoolState, MenuItemConfig, CheckMenuItemConfig


class ShocksIconEnum(IconEnum):
    WAIT = "wait.svg"
    DISABLED = "disabled.svg"
    DOWN = "down.svg"


class ShocksIconPartEnum(IconEnum):
    TPL_FAILURE = "failure-%s.svg"
    TPL_SLOW = "slow-%s.svg"
    TPL_UP = "up-%s.svg"

    def compose(self, suffix: "ShocksIconSuffixEnum") -> str:
        return self.value % suffix.value


class ShocksIconSuffixEnum(str, pt.ExtendedEnum):
    VAL_1 = "1"
    VAL_2 = "2"
    VAL_3 = "3"
    VAL_4 = "4"
    VAL_NC = "nc"


class ShocksIconSelector(IIconSelector):
    def __init__(self, latency_warning_threshold_ms: int):
        super().__init__(ShocksIconEnum.WAIT, subpath="shocks")
        self._latency_warning_threshold_ms = latency_warning_threshold_ms

    def select(
        self,
        data: ShocksProxyInfo = None,
        tunnel_amount: int = None,
        network_comm: bool = None,
    ) -> str:
        if override := super().select():
            return override

        suffix = ShocksIconSuffixEnum.VAL_1
        if network_comm:
            suffix = ShocksIconSuffixEnum.VAL_NC
        elif tunnel_amount:
            suffix = ShocksIconSuffixEnum.resolve_by_value(str(max(1, min(tunnel_amount, 4))))

        if not data or not data.worker_up:
            return ShocksIconEnum.DOWN

        if not data.running:
            return ShocksIconEnum.DISABLED

        if not data.healthy:
            return ShocksIconPartEnum.TPL_FAILURE.compose(suffix)

        if not tunnel_amount:
            return ShocksIconEnum.WAIT

        if (data.latency_s or 0) * 1000 >= self._latency_warning_threshold_ms:
            return ShocksIconPartEnum.TPL_SLOW.compose(suffix)

        return ShocksIconPartEnum.TPL_UP.compose(suffix)

    @cached_property
    def icon_names_set(self) -> set[str]:
        def _iter() -> Iterable[str]:
            yield from ShocksIconEnum
            yield from [
                tpl.compose(suffix)
                for tpl, suffix in itertools.product(
                    ShocksIconPartEnum,
                    ShocksIconSuffixEnum,
                )
            ]

        return set(_iter())


class IndicatorShocks(_BaseIndicator[ShocksInfo, ShocksIconSelector]):
    SYSTEMCTL_CALL_TIMEOUT_SEC = 60

    def __init__(self):
        self.config_section = "indicator.shocks"

        self._restart = _StaticState(
            callback=self._enqueue_restart,
            gconfig=MenuItemConfig("Restart service", sep_before=False),
        )
        self._show_lat = _BoolState(
            config_var=(self.config_section, "label"),
            gconfig=CheckMenuItemConfig("Show latency", sep_before=True),
        )
        self._latency_warning_threshold_ms = get_merged_uconfig().getint(
            self.config_section, "latency-warn-threshold-ms"
        )

        super().__init__(
            indicator_name="shocks",
            socket_topic=["shocks"],
            icon_selector=ShocksIconSelector(self._latency_warning_threshold_ms),
            title="SSH⚡SOCKS proxy",
            states=[self._restart, self._show_lat],
        )

    def _restart_service(self):
        self._state.wait_timeout = self.SYSTEMCTL_CALL_TIMEOUT_SEC

        out, err = None, None
        try:
            try:
                cp = subprocess.run(
                    ["systemctl", "restart", "es7s-shocks.target"],
                    capture_output=True,
                    timeout=self.SYSTEMCTL_CALL_TIMEOUT_SEC,
                    check=True,
                )
            except CalledProcessError as e:
                out, err = e.stdout, e.stderr
                raise
        except Exception as e:
            get_logger().exception(e)
            self._add_timeout(self.RENDER_ERROR_TIMEOUT_SEC)
            self._render_no_data()
            [scc.monitor_data_buf.clear() for scc in self._socket_client_conn.values()]
        else:
            out, err = cp.stdout, cp.stderr

        if out:
            get_logger().info(out)
        if err:
            get_logger().error(err)

    def _enqueue_restart(self, _=None):
        self._enqueue(self._restart_service)

    def _render(self, msg: SocketMessage[ShocksInfo]):
        if self._state.is_waiting:
            if msg.data.proxies and any((p.running and p.healthy) for p in msg.data.proxies):
                self._state.cancel_wait()
            else:
                icon = self._get_icon()
                if self._show_lat:
                    self._render_result("BUSY", icon=icon)
                else:
                    self._render_result("", icon=icon)
                return

        if not msg.data.proxies:
            self._render_no_data()
            return

        details = []
        for proxy in msg.data.proxies:
            details.append(f"[{proxy.name}]" + "\t" + self._format_result(proxy, details=True))
            result = self._format_result(proxy)
            if proxy.name == "default" or len(msg.data.proxies) == 1:
                icon = self._icon_selector.select(proxy, msg.data.tunnel_amount, msg.network_comm)
                self._render_result(result, icon=icon)

        self._update_details("\n".join(sorted(details)))

    def _format_result(self, data: ShocksProxyInfo, details=False) -> str:
        def format_latency(lat_s: float) -> str:
            if lat_s * 1000 >= self._latency_warning_threshold_ms:
                return pt.format_auto_float(lat_s, 3, allow_exp_form=False) + "s"
            else:
                return pt.format_time_ms(lat_s * 1e3)

        if not self._show_lat and not details:
            return ""
        if not data.worker_up:
            return "DWN"
        if not data.running:
            return "OFF"
        if not data.healthy:
            if details and data.proxy_latency_s:
                return "\t".join([format_latency(data.proxy_latency_s), "OUTF"])
            return "ERR"

        if not data.latency_s:
            return "---"

        if not details:
            return format_latency(data.latency_s)
        lats = [data.latency_s]
        if data.proxy_latency_s:
            lats.insert(0, data.proxy_latency_s)
        return "\t".join(format_latency(f) for f in lats)
