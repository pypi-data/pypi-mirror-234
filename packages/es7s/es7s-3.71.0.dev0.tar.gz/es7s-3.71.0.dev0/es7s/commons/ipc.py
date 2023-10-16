# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os.path
import pickle
import socket as s
import threading as th
import time
import typing as t
from abc import ABCMeta, abstractmethod
from collections import deque
from dataclasses import dataclass, Field, field, fields
from logging import getLogger

from es7s.commons import now

from es7s.shared.threads import ShutdownableThread
from es7s.shared.system import get_socket_path
import pytermor as pt
_T = t.TypeVar("_T")


@dataclass(frozen=True)
class SocketMessage(t.Generic[_T]):
    data: _T
    timestamp: int = field(default_factory=now)
    network_comm: bool = False

    @property
    def data_hash(self) -> int:
        if isinstance(self.data, dict):
            return hash(frozenset(self.data.items()))
        return hash(self.data)


@dataclass(frozen=True)
class IDTO(metaclass=ABCMeta):
    @classmethod
    def _map(cls, response_field: str = None, default=None, **kwargs) -> Field:
        """None means the response field name is equal to DTO field name"""
        if response_field is not None:
            kwargs.update({"metadata": {"response_field": response_field}})
        return field(default=default, **kwargs)

    @classmethod
    def dto_to_response_fields_map(cls) -> dict[str, str]:
        return {f.name: cls._get_response_field(f) for f in fields(cls)}

    @classmethod
    def response_field_names_list(cls) -> list[str]:
        return [cls._get_response_field(f) for f in fields(cls)]

    @staticmethod
    def _get_response_field(field: Field):
        return field.metadata.get("response_field", field.name)


class SocketServer(ShutdownableThread):
    LISTEN_TIMEOUT_SEC = 1

    def __init__(
        self,
        daemon_buf: deque[any],
        socket_path_suffix: str,
        provider_name: str,
        network_req_event: th.Event,
    ):
        # setting daemon to True so that the main process doesn't wait for this thread to terminate
        super().__init__(command_name=provider_name, thread_name="ssnd", daemon=True)

        self._daemon_buf = daemon_buf
        self._socket_path = get_socket_path(socket_path_suffix, write=True)
        self._network_req_event = network_req_event
        self._unlink_socket_path()

        getLogger(__package__).debug(f"Binding to {self._socket_path}")
        self._socket = s.socket(s.AF_UNIX, s.SOCK_STREAM)
        self._socket.bind(self._socket_path)
        self._socket.settimeout(self.LISTEN_TIMEOUT_SEC)

    def run(self):
        logger = getLogger(__package__)
        logger.info(f'Starting {self} at: "{self._socket_path}"')
        self._socket.listen()

        while True:
            if self.is_shutting_down():
                self.destroy()
                break

            try:
                conn, _ = self._socket.accept()
            except TimeoutError:
                continue

            try:
                data = self._daemon_buf[0]
                msg = SocketMessage[_T](data, network_comm=self._network_req_event.is_set())
                logger.debug(f"Composed msg {msg}")

                serialized_msg = pickle.dumps(msg, protocol=pickle.HIGHEST_PROTOCOL)
                logger.debug(f"Writing {len(serialized_msg)} bytes to daemon buffer")
                logger.debug(pt.dump(serialized_msg))
                conn.send(serialized_msg)
            except BrokenPipeError:
                pass
            except IndexError:
                # let the client log this, will be significantly
                # less spam errors in syslog
                pass
            except Exception as e:
                logger.exception(e)
            finally:
                conn.close()

    def destroy(self):
        super().destroy()
        try:
            self._socket.close()
        except Exception as e:
            getLogger(__package__).exception(e)
        self._unlink_socket_path()

    def _unlink_socket_path(self):
        try:
            os.unlink(self._socket_path)
        except OSError:
            if os.path.exists(self._socket_path):
                raise


class IClientIPC(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def shutdown(self):
        ...


class NullClient(IClientIPC):
    def start(self):
        pass

    def shutdown(self):
        pass


class SocketClient(ShutdownableThread, IClientIPC):
    RECV_CHUNK_SIZE = 1024

    def __init__(
        self,
        monitor_data_buf: deque[bytes],
        eff_recv_interval_sec: float,
        pause_event: th.Event,
        ready_event: th.Event,
        socket_topic: str,
        command_name: str,
    ):
        # setting daemon to True so that the main process doesn't wait for this thread to terminate
        super().__init__(command_name=socket_topic, thread_name="srcv", daemon=True)

        self._monitor_data_buf = monitor_data_buf
        self._eff_recv_interval_sec = eff_recv_interval_sec
        self._pause_event = pause_event
        self._ready_event = ready_event
        self._socket_path = get_socket_path(socket_topic)
        self._socket = None

    def run(self):
        logger = getLogger(__package__)
        logger.info(f'Starting {self} at: "{self._socket_path}"')
        recv_interval_sec = 0.1  # first one only

        while True:
            if self.is_shutting_down():
                self.destroy()
                break
            if self._pause_event.is_set():
                time.sleep(1)
                continue

            try:
                self._socket = s.socket(s.AF_UNIX, s.SOCK_STREAM)
                self._socket.connect(self._socket_path)
            except (ConnectionRefusedError, FileNotFoundError) as e:
                logger.error(f"Unable to connect to {self._socket_path}: {e}")
            except Exception as e:
                logger.exception(e)
            else:
                if data := self._socket.recv(self.RECV_CHUNK_SIZE):
                    self._monitor_data_buf.append(data)
                    if not self._ready_event.is_set():
                        self._ready_event.set()
                        logger.debug("Received first message from daemon")
                    logger.debug(f"Received {len(data)} bytes of data")
                self._socket.close()
            time.sleep(recv_interval_sec)
            recv_interval_sec = self._eff_recv_interval_sec

    def destroy(self):
        super().destroy()
        try:
            self._socket.close()
        except Exception as e:
            getLogger(__package__).exception(e)
