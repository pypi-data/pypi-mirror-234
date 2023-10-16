# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import psutil
import time
from collections.abc import Iterable

from psutil._common import sdiskio

from es7s.shared import DiskIoInfo, DiskIoInfoStats
from ._base import DataProvider


class DiskIoProvider(DataProvider[DiskIoInfo]):
    def __init__(self):
        self._prev_ts: int = time.time_ns()
        self._prev_counters: sdiskio | None = None

        self._read_max_mbps = 0.0
        self._write_max_mbps = 0.0
        super().__init__("disk-io", "disk-io", poll_interval_sec=1.0)

    def _collect(self) -> DiskIoInfo:
        counters = psutil.disk_io_counters()
        now_ts = time.time_ns()

        result = self._collect_internal(counters, now_ts)

        self._prev_ts = now_ts
        self._prev_counters = counters
        return result

    def _collect_internal(self, counters: sdiskio, now_ts: int) -> DiskIoInfo:
        delta_t_sec = 1e-9 * (now_ts - self._prev_ts)  # ns -> sec
        if not delta_t_sec or not self._prev_counters:
            return DiskIoInfo()

        return DiskIoInfo(
            *self._collect_speed(counters, delta_t_sec),
            busy_ratio=self._collect_busy_ratio(counters, delta_t_sec),
        )

    def _collect_speed(self, counters: sdiskio, delta_t_sec: float) -> Iterable[DiskIoInfoStats]:
        mbps_read = 1e-6 * (counters.read_bytes - self._prev_counters.read_bytes) / delta_t_sec
        mbps_write = 1e-6 * (counters.write_bytes - self._prev_counters.write_bytes) / delta_t_sec
        # bytes -> megabytes

        self._read_max_mbps = max(self._read_max_mbps, mbps_read)
        self._write_max_mbps = max(self._write_max_mbps, mbps_write)

        yield DiskIoInfoStats(mbps_read, self._read_max_mbps)
        yield DiskIoInfoStats(mbps_write, self._write_max_mbps)

    def _collect_busy_ratio(self, counters: sdiskio, delta_t_sec: float) -> float | None:
        if hasattr(counters, "busy_time") and hasattr(self._prev_counters, "busy_time"):
            return 1e-3 * (counters.busy_time - self._prev_counters.busy_time) / delta_t_sec
            # ms -> sec
        return None
