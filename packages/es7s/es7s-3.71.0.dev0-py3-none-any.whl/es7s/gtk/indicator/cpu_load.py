# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import pytermor as pt
from pytermor import format_auto_float

from es7s.commons import SocketMessage
from es7s.shared import CpuInfo
from ._base import _BaseIndicator
from ._icon_selector import ThresholdIconSelector, ThresholdMap
from ._state import _BoolState, CheckMenuItemConfig, RadioMenuItemConfig


class IndicatorCpuLoad(_BaseIndicator[CpuInfo, ThresholdIconSelector]):
    def __init__(self):
        self.config_section = "indicator.cpu-load"

        self._show_perc = _BoolState(
            config_var=(self.config_section, "label-current"),
            gconfig=CheckMenuItemConfig("Show current (%)", sep_before=True),
        )
        self._show_avg_off = _BoolState(
            config_var=(self.config_section, "label-average"),
            config_var_value="off",
            gconfig=RadioMenuItemConfig("No average", sep_before=True, group=self.config_section),
        )
        self._show_avg = _BoolState(
            config_var=(self.config_section, "label-average"),
            config_var_value="one",
            gconfig=RadioMenuItemConfig("Show average (1min)", group=self.config_section),
        )
        self._show_avg3 = _BoolState(
            config_var=(self.config_section, "label-average"),
            config_var_value="three",
            gconfig=RadioMenuItemConfig("Show average (1/5/15min)", group=self.config_section),
        )

        self._freq_formatter = pt.StaticFormatter(
            pad=True,
            allow_negative=False,
            unit_separator=" ",
            unit="Hz",
            prefix_refpoint_shift=+2,
        )

        super().__init__(
            indicator_name="cpu-load",
            socket_topic="cpu",
            icon_selector=ThresholdIconSelector(
                ThresholdMap(100, 95, 87, 75, 62, 50, 37, 25, 12, 0, caution=87, alert=95),
                subpath="cpuload",
                path_dynamic_tpl="%s.svg",
            ),
            title="CPU",
            states=[self._show_perc, self._show_avg_off, self._show_avg, self._show_avg3],
        )

    def _render(self, msg: SocketMessage[CpuInfo]):
        self._update_title(
            f"{'CPU':8s}\t{msg.data.core_count} cores, {msg.data.thread_count} threads"
        )
        self._update_details(
            "\n".join(
                f"{kv[0]:8s}\t{kv[1]!s}"
                for kv in [
                    (
                        self._freq_formatter.format(msg.data.freq_mhz),
                        self._format_result(msg.data.load_perc, *msg.data.load_avg, details=True),
                    ),
                ]
            )
        )
        self._render_result(
            self._format_result(msg.data.load_perc, *msg.data.load_avg),
            self._format_result(100, *[16.16] * len(msg.data.load_avg)),
            icon=self._icon_selector.select(msg.data.load_perc),
        )

    def _format_result(self, perc: float, *avg: float, details=False) -> str:
        parts = []
        if self._show_perc.active or details:
            parts += [f"{perc:3.0f}% "]
        if self._show_avg3.active or details:
            parts += (format_auto_float(a, 4) for a in avg)
        elif self._show_avg.active:
            parts += (format_auto_float(avg[0], 4),)
        return " ".join(parts).rstrip()
