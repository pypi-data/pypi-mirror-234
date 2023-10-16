# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import itertools
from collections.abc import Iterable
from functools import cached_property

import pytermor as pt

from es7s.commons import SocketMessage
from es7s.shared import (
    NetworkCountryInfo,
    NetworkLatencyInfo,
    NetworkUsageInfo,
    NetworkUsageInfoStats,
)
from es7s.shared import NetworkInfo
from ._base import WAIT_PLACEHOLDER, _BaseIndicator
from ._icon_selector import IIconSelector, IconEnum
from ._state import _BoolState, CheckMenuItemConfig
from es7s.commons import filtere


class NetworkIconEnum(IconEnum):
    DISABLED = "disabled.svg"
    DOWN = "down.svg"
    WAIT = "wait.svg"


class NetworkIconPartEnum(IconEnum):
    NETCOM = "nc"


class NetworkIconPartVpnEnum(IconEnum):
    ENABLED = "vpn"
    WARNING = "vpnw"
    FOREIGN = "vpnf"


class NetworkIconPartArrowEnum(IconEnum):
    VAL_0 = "0"  # @TODO duplicated definitions with NetworkIndicatorIconBuilder
    VAL_1 = "1"
    VAL_2 = "2"
    VAL_3 = "3"
    VAL_4 = "4"
    VAL_5 = "5"
    VAL_6 = "6"
    WARNING = "w"
    ERROR = "e"


class NetworkIconSelector(IIconSelector):
    def __init__(self, exclude_foreign_codes: set[str]):
        super().__init__(NetworkIconEnum.DISABLED, subpath="network")
        self._path_dynamic_tpl = "%s.svg"
        self._exclude_foreign_codes = exclude_foreign_codes

    def select(
        self,
        last_usage: NetworkUsageInfo = None,
        last_country: NetworkCountryInfo = None,
        last_latency: NetworkLatencyInfo = None,
        netcom=False,
    ) -> str | IconEnum:
        if override := super().select():
            return override

        if not last_usage:
            return NetworkIconEnum.WAIT
        if not last_usage.isup:
            return NetworkIconEnum.DOWN

        frames: list[str | None] = [self._get_vpn_fid_part(last_usage, last_country)]
        for uis in (last_usage.sent, last_usage.recv):
            frames.append(self._get_icon_frame(uis, last_latency))
        frames.append(NetworkIconPartEnum.NETCOM if netcom else None)

        return self._compose_path(frames)

    @cached_property
    def icon_names_set(self) -> set[str | IconEnum]:
        def _iter() -> Iterable[str]:
            yield from NetworkIconEnum.list()
            for pts in itertools.product(
                [None, *NetworkIconPartVpnEnum],
                [*NetworkIconPartArrowEnum],
                [*NetworkIconPartArrowEnum],
                [None, NetworkIconPartEnum.NETCOM],
            ):
                yield self._compose_path(pts)

        return set(_iter())

    def _compose_path(self, frames: list[str | None]) -> str:
        return self._path_dynamic_tpl % "-".join(pt.filtern(frames))

    def _get_icon_frame(
        self,
        uis: NetworkUsageInfoStats | None,
        last_latency: NetworkLatencyInfo,
    ) -> str:
        if not uis:
            return NetworkIconPartArrowEnum.VAL_0

        failed_ratio = last_latency.failed_ratio if last_latency else 0.0
        if uis.errors or failed_ratio > 0.5:
            return NetworkIconPartArrowEnum.ERROR

        if uis.drops or failed_ratio > 0.0:
            return NetworkIconPartArrowEnum.WARNING

        if uis.bps:
            if uis.bps > 4e7:  # 40 Mbps
                return NetworkIconPartArrowEnum.VAL_6
            if uis.bps > 2e7:  # 20 Mbps
                return NetworkIconPartArrowEnum.VAL_5
            if uis.bps > 1e7:  # 10 Mbps
                return NetworkIconPartArrowEnum.VAL_4
            if uis.bps > 1e6:  # 1 Mbps
                return NetworkIconPartArrowEnum.VAL_3
            if uis.bps > 1e5:  # 100 kbps
                return NetworkIconPartArrowEnum.VAL_2
            if uis.bps > 1e4:  # 10 kpbs
                return NetworkIconPartArrowEnum.VAL_1
        # if uis.ratio:
        #     if uis.ratio > 0.4:
        #         return "4"
        #     ...
        #     if uis.ratio > 0.01:
        #         return "1"
        return NetworkIconPartArrowEnum.VAL_0

    def _get_vpn_fid_part(
        self,
        last_usage: NetworkUsageInfo,
        last_country: NetworkCountryInfo,
    ) -> str | None:
        if not last_usage or not last_usage.vpn:
            return None

        if not last_country or not last_country.country:
            return NetworkIconPartVpnEnum.WARNING

        if last_country.country.lower() in self._exclude_foreign_codes:
            return NetworkIconPartVpnEnum.ENABLED

        return NetworkIconPartVpnEnum.FOREIGN


class IndicatorNetwork(_BaseIndicator[NetworkInfo, NetworkIconSelector]):
    RENDER_INTERVAL_SEC = 1.0

    def __init__(self):
        self.config_section = "indicator.network"
        self._interface = None
        self._netcom = False

        self._show_rate = _BoolState(
            config_var=(self.config_section, "label-rate"),
            gconfig=CheckMenuItemConfig("Show rate (bit/s, max)", sep_before=True),
        )
        self._show_latency = _BoolState(
            config_var=(self.config_section, "label-latency"),
            gconfig=CheckMenuItemConfig("Show latency/delivery rate"),
        )
        self._show_country = _BoolState(
            config_var=(self.config_section, "label-country"),
            gconfig=CheckMenuItemConfig("Show country code"),
        )

        super().__init__(
            indicator_name="network",
            socket_topic=["network-usage", "network-latency", "network-country"],
            icon_selector=NetworkIconSelector(
                self.uconfig().get("exclude-foreign-codes", set, str),
            ),
            title="Network",
            states=[self._show_rate, self._show_latency, self._show_country],
        )
        self._formatter = pt.StaticFormatter(
            pt.formatter_bytes_human,
            max_value_len=4,
            auto_color=False,
            allow_negative=False,
            allow_fractional=True,
            discrete_input=False,
            unit="",
            unit_separator="",
            pad=True,
        )

    def _update_interface(self, last_usage: NetworkUsageInfo = None):
        if not last_usage:
            return
        self._interface = last_usage.interface
        self._update_title(self._title_base + "\t" + self._interface)

    def _update_dto(self, msg: SocketMessage[NetworkInfo]):
        pass  # actual update is in render()

    def _render(self, msg: SocketMessage[NetworkInfo]):
        last_usage = self._get_last_usage()
        if (
            last_usage
            and hasattr(msg.data, "interface")
            and self._interface != getattr(msg.data, "interface")
        ):
            self._render_no_data()
            self._last_dto.clear()
            return

        self._netcom = False
        super()._update_dto(msg)

        if hasattr(msg, "network_comm") and msg.network_comm:
            self._netcom = True

        icon = self._icon_selector.select(
            self._get_last_usage(),
            self._get_last_country_info(),
            self._last_dto.get(NetworkLatencyInfo, None),
            self._netcom,
        )

        if not last_usage:
            self._render_no_data()
            return

        if not last_usage.isup:
            self._render_result("N/A", "N/A", icon=icon)
            return

        bpss = []
        for uis in (last_usage.sent, last_usage.recv):
            if not uis:
                bpss.append(None)
                continue
            bpss.append(uis.bps)

        result = self._format_result(*bpss)

        self._update_details(f"{self._format_result(*bpss, details=True)}")
        self._render_result(result, result, icon=icon)

    @property
    def _show_any(self):
        return self._show_rate or self._show_country or self._show_latency

    def _render_no_data(self):
        self._render_result("WAIT", "WAIT", icon=self._icon_selector.select())
        self._update_details(f"..." if self._interface else "(no interfaces)")

    def _get_last_usage(self) -> NetworkUsageInfo | None:
        if last_usage := self._last_dto.get(NetworkUsageInfo, None):
            self._update_interface(last_usage)
        return last_usage

    def _get_last_country_info(self) -> NetworkCountryInfo | None:
        return self._last_dto.get(NetworkCountryInfo, None)

    def _format_result(self, *bps_values: float | None, details=False) -> str:
        result = (" · " if details else " ").join(
            filtere(
                [
                    self._format_usage(*bps_values, details=details),
                    self._format_latency(details=details),
                    self._format_country(details=details),
                ],
            )
        )
        if details:
            return result.strip()
        return result

    def _format_usage(self, *bps_values: float | None, details=False) -> str:
        if not self._show_rate and not details:
            return ""
        if details and len(bps_values) > 1:
            return f"D↓{self._format_usage(bps_values[1], details=True)}  U↑{self._format_usage(bps_values[0], details=True)}"
        if not any(bps_values):
            return " 0.0k"
        val = max(bps_values)
        if val < 1000:
            return "<1.0k"
        return self._formatter.format(val)

    def _format_latency(self, details=False) -> str:
        if not self._show_latency and not details:
            return ""
        if not (last_latency := self._last_dto.get(NetworkLatencyInfo, None)):
            return WAIT_PLACEHOLDER
        if last_latency.failed_ratio:
            return f"{100*(1-last_latency.failed_ratio):3.0f}%"
        val, sep, pfx, unit = pt.formatter_time_ms._format_raw(last_latency.latency_s * 1000)
        return " " * max(0, 4 - len(val + pfx + unit)) + val + pfx + unit

    def _format_country(self, details=False) -> str:
        cc = self._format_country_code(details)
        if cc and details:
            return cc + self._format_vpn(details)
        return cc

    def _format_country_code(self, details=False) -> str:
        if not self._show_country and not details:
            return ""
        if not (last_country := self._last_dto.get(NetworkCountryInfo, None)):
            return WAIT_PLACEHOLDER
        return last_country.country or ""

    def _format_vpn(self, details=False) -> str:
        if not self._show_country and not details:
            return ""
        if last_usage := self._last_dto.get(NetworkUsageInfo, None):
            return "*" if last_usage.vpn else ""
        return ""
