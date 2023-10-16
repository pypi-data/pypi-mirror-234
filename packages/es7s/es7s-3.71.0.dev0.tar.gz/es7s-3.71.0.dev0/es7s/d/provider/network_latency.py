# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import socket
import time
from collections import deque
from itertools import zip_longest
from timeit import default_timer as timer

import pytermor as pt

from ._base import DataProvider
from es7s.shared import get_logger, get_merged_uconfig
from es7s.shared import NetworkLatencyInfo
from es7s.commons import percentile


class NetworkLatencyProvider(DataProvider[NetworkLatencyInfo]):
    def __init__(self):
        self._timer = _Timer()
        self._last_results = deque[bool](maxlen=50)
        super().__init__("network-latency", "network-latency", 13.0)

    def _reset(self):
        return NetworkLatencyInfo()

    def _collect(self) -> NetworkLatencyInfo:
        attempts = 4
        timeout = 5
        host = get_merged_uconfig().get('provider.' + self._config_var, 'host')
        port = get_merged_uconfig().getint('provider.' + self._config_var, 'port')

        conn_times_s = []

        get_logger().info(f"Pinging {host}:{port}...")
        for n in range(attempts):
            s = _Socket(socket.AF_INET, socket.SOCK_STREAM, timeout)
            try:
                self._network_req_event.set()
                time.sleep(.25)
                cost_time_s = self._timer.cost((s.connect, s.shutdown), ((host, port), None))
                conn_times_s.append(cost_time_s)
                conn_time_ns = pt.format_auto_float(cost_time_s*1000, 3)
                get_logger().info(f"PING {n}/{attempts} {conn_time_ns}ms")
            except (socket.timeout, OSError):
                self._last_results.append(False)
            else:
                self._last_results.append(True)
            finally:
                self._network_req_event.clear()
                s.close()

        if len(conn_times_s) == 0:
            return NetworkLatencyInfo(failed_ratio=1.0)

        self._ping_failrate = 1 - len([*filter(None, self._last_results)])/len(self._last_results)
        self._ping_latency_s = percentile(sorted(conn_times_s), 0.5)

        info = NetworkLatencyInfo(
            failed_ratio=self._ping_failrate,
            latency_s=self._ping_latency_s,
        )
        return info


class _Socket(object):
    def __init__(self, family, type_, timeout):
        s = socket.socket(family, type_)
        s.settimeout(timeout)
        self._s = s

    def connect(self, host, port=80):
        self._s.connect((host, int(port)))

    def shutdown(self):
        self._s.shutdown(socket.SHUT_RD)

    def close(self):
        self._s.close()


class _Timer(object):
    def __init__(self):
        self._start = 0
        self._stop = 0

    def start(self):
        self._start = timer()

    def stop(self):
        self._stop = timer()

    def cost(self, funcs, args):
        self.start()
        for func, arg in zip_longest(funcs, args):
            if arg:
                func(*arg)
            else:
                func()

        self.stop()
        return self._stop - self._start
