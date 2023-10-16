# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import psutil

from ._base import DataProvider
from es7s.shared import CpuInfo


class CpuProvider(DataProvider[CpuInfo]):
    def __init__(self):
        super().__init__('cpu', 'cpu')

    def _collect(self) -> CpuInfo:
        return CpuInfo(
            freq_mhz=psutil.cpu_freq().current,
            load_perc=psutil.cpu_percent(),
            load_avg=psutil.getloadavg(),
            core_count=psutil.cpu_count(False),
            thread_count=psutil.cpu_count(True),
        )
