# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import pytermor as pt
from pytermor import format_auto_float

from es7s.commons import SocketMessage
from es7s.shared import MemoryInfo
from es7s.shared import get_merged_uconfig
from ._base import (
    _BaseIndicator,
)
from ._icon_selector import ThresholdIconSelector, ThresholdMap
from ._state import _BoolState, CheckMenuItemConfig, RadioMenuItemConfig


class IndicatorMemory(_BaseIndicator[MemoryInfo, ThresholdIconSelector]):
    def __init__(self):
        self.config_section = "indicator.memory"

        self._show_phys_perc = _BoolState(
            config_var=(self.config_section, "label-physical-percents"),
            gconfig=CheckMenuItemConfig("Show physical (%)", sep_before=True),
        )

        self._show_phys_bytes_none = _BoolState(
            config_var=(self.config_section, "label-physical-bytes"),
            config_var_value="off",
            gconfig=RadioMenuItemConfig(
                "No physical abs. value", sep_before=True, group=self.config_section
            ),
        )
        self._show_phys_bytes_dynamic = _BoolState(
            config_var=(self.config_section, "label-physical-bytes"),
            config_var_value="dynamic",
            gconfig=RadioMenuItemConfig("Show physical (kB/MB/GB)", group=self.config_section),
        )
        self._show_phys_bytes_short = _BoolState(
            config_var=(self.config_section, "label-physical-bytes"),
            config_var_value="short",
            gconfig=RadioMenuItemConfig("Show physical (GB)", group=self.config_section),
        )

        self._show_swap_perc = _BoolState(
            config_var=(self.config_section, "label-swap-percents"),
            gconfig=CheckMenuItemConfig("Show swap (%)", sep_before=True),
        )
        self._show_swap_bytes = _BoolState(
            config_var=(self.config_section, "label-swap-bytes"),
            gconfig=CheckMenuItemConfig("Show swap (kB/MB/GB)"),
        )

        self._phys_warn_threshold: float = get_merged_uconfig().getfloat(
            self.config_section, "physical-warn-threshold"
        )
        self._swap_warn_threshold: float = get_merged_uconfig().getfloat(
            self.config_section, "swap-warn-threshold"
        )

        super().__init__(
            indicator_name="memory",
            socket_topic="memory",
            icon_selector=ThresholdIconSelector(
                ThresholdMap(100, 95, *range(90, -10, -10)),
                subpath="memory",
                path_dynamic_tpl="%s.svg",
            ),
            title="RAM",
            states=[
                self._show_phys_perc,
                self._show_phys_bytes_none,
                self._show_phys_bytes_dynamic,
                self._show_phys_bytes_short,
                self._show_swap_perc,
                self._show_swap_bytes,
            ],
        )

    def _render(self, msg: SocketMessage[MemoryInfo]):
        phys_ratio = msg.data.phys_used / msg.data.phys_total

        warning_phys = phys_ratio > self._phys_warn_threshold
        warning_swap = msg.data.swap_used / msg.data.swap_total > self._swap_warn_threshold

        if warning_phys:
            self._enqueue_notification(f"High memory usage ({phys_ratio*100:.0f}%)")

        self._update_details(
            self._format_result(
                msg.data.phys_used,
                msg.data.phys_total,
                msg.data.swap_used,
                msg.data.swap_total,
                ignore_setup=True,
            ),
        )

        self._render_result(
            self._format_result(
                msg.data.phys_used,
                msg.data.phys_total,
                msg.data.swap_used,
                msg.data.swap_total,
            ),
            self._format_result(1e10, 1e10, 1e10, 1e10),
            False,  # warning_phys or warning_swap,
            self._icon_selector.select(100 * phys_ratio),
        )

    def _format_result(
        self,
        phys_used: float,
        phys_total: float,
        swap_used: float,
        swap_total: float,
        ignore_setup=False,
    ) -> str:
        parts = []
        if ignore_setup:
            parts += ["Phys."]
        if self._show_phys_perc or ignore_setup:
            parts += [self._format_used_perc(phys_used, phys_total)]
        if (self._show_phys_bytes_dynamic or self._show_phys_bytes_short) or ignore_setup:
            parts += [
                "".join(
                    self._format_used_bytes(
                        round(phys_used), short=self._show_phys_bytes_short.value
                    )
                )
            ]
        if ignore_setup:
            parts[-1] += " / " + "".join(self._format_used_bytes(round(phys_total)))
            parts.append("\nSwap")
        if self._show_swap_perc or ignore_setup:
            parts += [self._format_used_perc(swap_used, swap_total)]
        if self._show_swap_bytes or ignore_setup:
            parts += ["".join(self._format_used_bytes(round(swap_used)))]
        if ignore_setup:
            parts[-1] += " / " + "".join(self._format_used_bytes(round(swap_total)))
            return "\t".join(parts)
        return " ".join(parts).rstrip()

    def _format_used_perc(self, used: float, total: float) -> str:
        return f"{100 * used / total:3.0f}% "

    def _format_used_bytes(self, used: int, short: bool = False) -> tuple[str, str]:
        used_kb = used / 1024
        used_mb = used / 1024**2
        used_gb = used / 1024**3
        if short:
            return pt.format_auto_float(used_gb, 3), "G"

        if used_kb < 1:
            return "< 1k", ""
        if used_kb < 1000:
            return format_auto_float(used_kb, 4, False), "k"
        if used_mb < 10000:
            return format_auto_float(used_mb, 4, False), "M"
        return format_auto_float(used_gb, 4, False), "G"
