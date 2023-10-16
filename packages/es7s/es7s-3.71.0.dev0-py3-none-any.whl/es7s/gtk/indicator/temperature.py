# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from pytermor import fit

from es7s.commons import SocketMessage
from es7s.shared import TemperatureInfo
from ._base import _BaseIndicator
from ._icon_selector import ThresholdIconSelector, ThresholdMap
from ._state import _BoolState, RadioMenuItemConfig


class IndicatorTemperature(_BaseIndicator[TemperatureInfo, ThresholdIconSelector]):
    def __init__(self):
        self.config_section = "indicator.temperature"

        self._show_none = _BoolState(
            config_var=(self.config_section, "label"),
            config_var_value="off",
            gconfig=RadioMenuItemConfig("No label", sep_before=True, group=self.config_section),
        )
        self._show_one = _BoolState(
            config_var=(self.config_section, "label"),
            config_var_value="one",
            gconfig=RadioMenuItemConfig("Show 1 sensor (°C)", group=self.config_section),
        )
        self._show_three = _BoolState(
            config_var=(self.config_section, "label"),
            config_var_value="three",
            gconfig=RadioMenuItemConfig("Show 3 sensors (°C)", group=self.config_section),
        )

        super().__init__(
            indicator_name="temperature",
            socket_topic="temperature",
            icon_selector=ThresholdIconSelector(
                ThresholdMap(*range(100, -80, -10), -273),
                subpath="temperature",
                path_dynamic_tpl="%s.svg",
            ),
            title="Thermal sensors",
            states=[self._show_none, self._show_one, self._show_three],
        )

    def _render(self, msg: SocketMessage[TemperatureInfo]):
        orig_values = msg.data.values_c
        sorted_values = sorted(orig_values, key=lambda v: v[1], reverse=True)

        max_value = 0
        values_limit = 6
        if len(sorted_values) > 0:
            max_value = sorted_values[0][1]

        top_values_origin_indexes = []
        for (k, v) in sorted_values[:values_limit]:
            top_values_origin_indexes.append(orig_values.index((k, v)))

        values_str = []
        guide = []
        warning = False
        for oindex in sorted(top_values_origin_indexes):
            _, val = orig_values[oindex]
            if val > 90:  # @TODO to config
                warning = True
            val_str = str(round(val)).rjust(2)
            values_str.append(val_str)
            guide.append("1" + val_str[-2:])

        self._update_details(
            "\n".join(
                [*(f"{fit(v[0], 15)}\t{v[1]:.0f}°C" for v in sorted_values[:10])]
                + [f"(+{len(sorted_values[10:])} more)" if len(sorted_values) > 10 else ""]
            )
        )

        values_limit = 3 if self._show_three else 1
        self._render_result(
            self._format_results(values_str[:values_limit]),
            self._format_results(guide[:values_limit]),
            warning,
            icon=self._icon_selector.select(max_value),
        )

    def _format_results(self, result: list[str]) -> str:
        if self._show_three:
            return self._format_result(3, result)
        elif self._show_one:
            return self._format_result(1, result)
        return ""

    def _format_result(self, num: int, result: list[str]) -> str:
        parts = result[:num]
        return " ".join(parts) + ("", "°")[len(parts)]
