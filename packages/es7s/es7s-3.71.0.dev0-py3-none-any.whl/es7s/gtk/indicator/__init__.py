# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from ._base import IIndicator as IIndicator
from ._base import _BaseIndicator
from .cpu_load import IndicatorCpuLoad as IndicatorCpuLoad
from .disk import IndicatorDisk as IndicatorDisk
from .docker import IndicatorDocker as IndicatorDocker
from .manager import IndicatorManager as IndicatorManager
from .fan_speed import IndicatorFanSpeed as IndicatorFanSpeed
from .memory import IndicatorMemory as IndicatorMemory
from .network import IndicatorNetwork as IndicatorNetworkUsage
from .shocks import IndicatorShocks as IndicatorShocks
from .systemctl import IndicatorSystemCtl as IndicatorSystemCtl
from .temperature import IndicatorTemperature as IndicatorTemperature
from .timestamp import IndicatorTimestamp as IndicatorTimestamp


def ensure_dynload_allowed(cls: type):
    if isinstance(cls, type) and issubclass(cls, _BaseIndicator):
        return
    raise RuntimeError(
        "Dynamically loaded indicators must be classes "
        f"based on {_BaseIndicator.__name__}, got: {cls}"
    )
