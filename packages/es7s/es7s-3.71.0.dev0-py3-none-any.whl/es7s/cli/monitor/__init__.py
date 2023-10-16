# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from . import *  # noqa
from ._base import CoreMonitor


from ._separator import Separator as Separator
from ._separator import EMPTY as EMPTY
from ._separator import SPACE as SPACE
from ._separator import SPACE_2 as SPACE_2
from ._separator import SPACE_3 as SPACE_3
from ._separator import LINE as LINE
from ._separator import LINE_2 as LINE_2
from ._separator import LINE_3 as LINE_3
from ._separator import EDGE_LEFT as EDGE_LEFT
from ._separator import EDGE_RIGHT as EDGE_RIGHT

from .battery import BatteryMonitor as BatteryMonitor
from .combined import CombinedMonitor as CombinedMonitor
from .cpu_freq import CpuFreqMonitor as CpuFreqMonitor
from .cpu_load import CpuLoadMonitor as CpuLoadMonitor
from .cpu_load_avg import CpuLoadAvgMonitor as CpuLoadAvgMonitor
from .datetime import DatetimeMonitor as DatetimeMonitor
from .disk_usage import DiskUsageMonitor as DiskUsageMonitor
from .docker import DockerMonitor as DockerMonitor
from .fan_speed import FanSpeedMonitor as FanSpeedMonitor
from .memory import MemoryMonitor as MemoryMonitor
from .network_country import NetworkCountryMonitor as NetworkCountryMonitor
from .network_latency import NetworkLatencyMonitor as NetworkLatencyMonitor
from .shocks import ShocksMonitor as ShocksMonitor
from .systemctl import SystemCtlMonitor as SystemCtlMonitor
from .temperature import TemperatureMonitor as TemperatureMonitor
from .timestamp import TimestampMonitor as TimestampMonitor
from .weather import WeatherMonitor as WeatherMonitor

autodiscover_extras = None


def ensure_dynload_allowed(cls: type):
    if isinstance(cls, Separator):
        return
    if isinstance(cls, type) and issubclass(cls, CoreMonitor):
        return
    raise RuntimeError(
        f"Dynamically loaded monitors must be classes based on {CoreMonitor}"
        f" or instances of {Separator}, got: {cls}"
    )
