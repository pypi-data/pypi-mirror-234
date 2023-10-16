# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re
import time

from ._base import DataProvider
from es7s.shared import get_merged_uconfig
from es7s.shared import TimestampInfo


class TimestampProvider(DataProvider[TimestampInfo]):
    def __init__(self):
        super().__init__("timestamp", "timestamp", 23.0)
        self._last_ts: int|None = None

    def _collect(self) -> TimestampInfo:
        url = get_merged_uconfig().get('provider.' + self._config_var, 'url')
        try:
            self._network_req_event.set()
            time.sleep(.25)

            response = self._make_request(url)
            data = response.text
            data_match = re.match(r'(\d{10})', data.strip())
            if not data_match:
                raise ValueError(f"Unexpected response: '{data}'")
            self._last_ts = int(data_match.group(1))

        finally:
            self._network_req_event.clear()

        return TimestampInfo(ts=self._last_ts, ok=True)

    def _reset(self) -> TimestampInfo:
        return TimestampInfo(ts=self._last_ts, ok=False)
