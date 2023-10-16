# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import math
from collections import namedtuple

from es7s.commons import SocketMessage
from es7s.shared import FanInfo
from ._base import _BaseIndicator
from ._icon_selector import ThresholdIconSelector, ThresholdMap
from ._state import _BoolState, CheckMenuItemConfig


ValueRange = namedtuple("ValueRange", ["min", "max"])


class IndicatorFanSpeed(_BaseIndicator[FanInfo, ThresholdIconSelector]):
    def __init__(self):
        self.config_section = "indicator.fan"

        self._show_rpm = _BoolState(
            config_var=(self.config_section, "label-rpm"),
            gconfig=CheckMenuItemConfig("Show value (RPM)", sep_before=True),
        )

        self._val_range = ValueRange(
            self.uconfig().get("value-min", int, fallback=0),
            self.uconfig().get("value-max", int, fallback=5000),
        )

        super().__init__(
            indicator_name="fan",
            socket_topic="fan",
            icon_selector=ThresholdIconSelector(
                ThresholdMap(96, 84, 72, 60, 48, 36, 24, 12, 1, 0),
                subpath="fan",
                path_dynamic_tpl="%s.png",
            ),
            title="Fan speed",
            states=[self._show_rpm],
        )

    def _render(self, msg: SocketMessage[FanInfo]):
        value = msg.data.max()
        rpm_perc = 100 * (value - self._val_range.min) / (self._val_range.max  - self._val_range.min)

        rpm_perc = max(rpm_perc, 1)  # to show OFF icon only when the fans are REALLY OFF
        if value == 0.0:
            rpm_perc = 0

        self._update_details("\n".join(f"· {v} RPM" for v in msg.data.values_rpm))
        value_str = str(value or "    0") if self._show_rpm else ""

        self._render_result(
            value_str,
            value_str,
            False,  # warning,
            self._icon_selector.select(rpm_perc),
        )
