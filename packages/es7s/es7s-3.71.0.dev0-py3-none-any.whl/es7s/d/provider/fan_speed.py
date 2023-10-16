# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import psutil

from ._base import DataProvider
from es7s.shared import FanInfo


class FanSpeedProvider(DataProvider[FanInfo]):
    def __init__(self):
        super().__init__("fan", "fan")

    def _collect(self) -> FanInfo:
        vals = psutil.sensors_fans().values()
        vals_cur = [val.current for sens in vals for val in sens]
        vals_flt = filter(lambda v: v < 64000, vals_cur)
        # ^ filter parasite values ≈65500, 8-bit "-1" maybe
        return FanInfo([*vals_flt])
