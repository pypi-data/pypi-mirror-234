# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import psutil

from ._base import DataProvider
from es7s.shared import TemperatureInfo


class TemperatureProvider(DataProvider[TemperatureInfo]):
    def __init__(self):
        super().__init__("temperature", "temperature")

    def _collect(self) -> TemperatureInfo:
        values = list()
        for k, v in psutil.sensors_temperatures().items():
            for shwt in v:
                if not shwt.current:
                    continue
                result_key = k + ("/" + shwt.label if shwt.label else "")
                values.append((result_key, shwt.current))

        return TemperatureInfo(values_c=values)
