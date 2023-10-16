# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import threading as th
import time
import typing as t
from collections import deque

from requests import Response

from es7s.commons import SocketServer
from es7s.shared import ShutdownableThread, get_logger, UserConfigSection, uconfig
from es7s.shared import DataCollectionError
from es7s.shared import Requester
from es7s.shared import class_to_command_name, get_merged_uconfig

T = t.TypeVar("T")


class DataProvider(ShutdownableThread, t.Generic[T]):
    def __init__(self, config_var: str | None, socket_topic: str, poll_interval_sec=1.0):
        self._config_var = config_var
        self._socket_topic = socket_topic
        self._poll_interval_sec = poll_interval_sec
        self._pvname = class_to_command_name(self) + "-pv"
        super().__init__(command_name=self._pvname, thread_name="coll")

        self._daemon_buf = deque[any](maxlen=1)
        self._network_req_event = th.Event()
        self._requester = Requester(self._network_req_event)
        self._socket_server = SocketServer(
            self._daemon_buf,
            self._socket_topic,
            self._pvname,
            self._network_req_event,
        )

    def prestart(self) -> None:
        if not self._is_enabled():
            self.shutdown()
            self.start()
            return

        self._socket_server.start()
        self.start()

    def run(self):
        super().run()
        logger = get_logger()
        wait_sec = 0

        while True:
            if self.is_shutting_down():
                self.destroy()
                break

            if 0 < wait_sec <= 1:
                time.sleep(wait_sec)
            elif wait_sec > 1:
                time.sleep(1)
                wait_sec -= 1
                continue

            data = None
            try:
                data = self._collect()
                logger.debug(f"Collected {data}")
                self._daemon_buf.append(data)
            except DataCollectionError as e:
                logger.error(e.msg)
            except Exception as e:
                logger.exception(e)

            if not data:
                if data := self._reset():
                    self._daemon_buf.append(data)

            wait_sec = self._poll_interval_sec

    def uconfig(self) -> UserConfigSection:
        return uconfig.get_for(self)

    def _is_enabled(self) -> bool:
        return get_merged_uconfig().get('provider', self._config_var, fallback=False)

    def _reset(self) -> T | None:
        pass

    def _collect(self) -> T:
        raise NotImplementedError()

    def _get_request_timeout(self) -> float:
        return max(1.0, self._poll_interval_sec / 2)

    def _make_request(
        self, url: str, request_fn: t.Callable[[], Response] = None, log_response_body: bool = True
    ) -> Response:
        return self._requester.make_request(
            url,
            self._get_request_timeout(),
            request_fn,
            log_response_body,
        )
