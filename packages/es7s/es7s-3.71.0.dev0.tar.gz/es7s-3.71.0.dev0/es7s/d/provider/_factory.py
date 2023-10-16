# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from ._base import DataProvider
from .battery import BatteryProvider
from .cpu import CpuProvider
from .datetime import DatetimeProvider
from .disk_io import DiskIoProvider
from .disk_usage import DiskUsageProvider
from .docker import DockerStatusProvider
from .fan_speed import FanSpeedProvider
from .memory import MemoryProvider
from .network_country import NetworkCountryProvider
from .network_latency import NetworkLatencyProvider
from .network_usage import NetworkUsageProvider
from .shocks import ShocksProvider
from .systemctl import SystemCtlProvider
from .temperature import TemperatureProvider
from .timestamp import TimestampProvider
from .weather import WeatherProvider


class DataProviderFactory:
    @classmethod
    def make_providers(cls) -> list[DataProvider]:
        return [
            BatteryProvider(),
            CpuProvider(),
            DatetimeProvider(),
            DiskUsageProvider(),
            DiskIoProvider(),
            DockerStatusProvider(),
            FanSpeedProvider(),
            MemoryProvider(),
            NetworkCountryProvider(),
            NetworkLatencyProvider(),
            NetworkUsageProvider(),
            ShocksProvider(),
            SystemCtlProvider(),
            TemperatureProvider(),
            TimestampProvider(),
            WeatherProvider(),
        ]
