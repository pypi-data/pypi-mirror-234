# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime

import psutil
from psutil._common import snetio, snicstats

from es7s.shared import get_merged_uconfig, run_subprocess
from es7s.shared import NetworkUsageInfo, NetworkUsageInfoStats
from es7s.commons import median
from ._base import DataProvider


@dataclass(frozen=True)
class DataSnapshot:
    ts: float
    data: snetio | None


@dataclass
class IntermDataChunk:
    avg: list[float] = field(default_factory=list)
    drops: int = 0
    errors: int = 0


class NetworkUsageProvider(DataProvider[NetworkUsageInfo]):
    def __init__(self):
        super().__init__("network-usage", "network-usage", 2.0)
        self._interfaces: list[str] = get_merged_uconfig().get(
            f"provider.{self._config_var}",
            "net-interface",
            fallback=None,
        ).splitlines()
        self._data_queue: deque[DataSnapshot] = deque(maxlen=1)
        self._max_bps: float = 100 * 1e6

    def _reset(self):
        return NetworkUsageInfo()

    def _find_first_up_interface(self) -> tuple[snicstats|None, str|None]:
        for interface in self._interfaces:
            if snic := psutil.net_if_stats().get(interface, None):
                if snic.isup:
                    return snic, interface
                continue
        return None, None

    def _collect(self) -> NetworkUsageInfo:
        snic, interface = self._find_first_up_interface()
        if not snic or not interface:
            return NetworkUsageInfo(interface)

        cdict: dict[str, snetio] = t.cast(dict, psutil.net_io_counters(pernic=True, nowrap=True))
        counters: snetio = cdict.get(interface, None)
        if not counters or not snic.isup:
            return NetworkUsageInfo(interface, snic.isup)

        p = run_subprocess("ip", "a", "show", interface)
        vpn = ('POINTOPOINT' in p.stdout)

        return NetworkUsageInfo(interface, snic.isup, *self._collect_stats(counters), vpn=vpn)

    def _collect_stats(self, counters: snetio) -> Iterable[NetworkUsageInfoStats]:
        now = datetime.now().timestamp()
        ds_now = DataSnapshot(now, counters)
        ds_prev = None
        sent, recv = IntermDataChunk(), IntermDataChunk()

        for ds in [*self._data_queue, ds_now]:
            if now - ds.ts > (2.0 * (self._data_queue.maxlen + 1)):
                continue
            if ds_prev is None:
                ds_prev = ds
                continue
            ts_delta = ds.ts - ds_prev.ts
            for bytesn, drop, err, idc in [
                (
                        ds.data.bytes_recv - ds_prev.data.bytes_recv,
                        ds.data.dropin - ds_prev.data.dropin,
                        ds.data.errin - ds_prev.data.errin,
                        recv,
                ),
                (
                        ds.data.bytes_sent - ds_prev.data.bytes_sent,
                        ds.data.dropout - ds_prev.data.dropout,
                        ds.data.errout - ds_prev.data.errout,
                        sent,
                ),
            ]:
                bps = 8 * bytesn / ts_delta
                idc.avg.append(bps)
                idc.drops += drop
                idc.errors += err

        self._data_queue.append(ds_now)

        for idc in (sent, recv):
            if not idc.avg:
                continue
            bps = median(sorted(idc.avg))
            ratio = bps / self._max_bps
            yield NetworkUsageInfoStats(bps, ratio, idc.drops, idc.errors)
