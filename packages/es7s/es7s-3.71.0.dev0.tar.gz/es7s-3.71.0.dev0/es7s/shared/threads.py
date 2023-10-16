# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import re
import os
import sys
import signal
import typing as t
import threading as th


_threads: set[ShutdownableThread] = set()
_shutdown_started = False


def _register(thread: ShutdownableThread):
    if _shutdown_started:
        thread.shutdown()
        return
    _threads.add(thread)


def exit_gracefully(
    signal_code: int = 0,
    exit_code: int = 0,
    callback: t.Callable[[int], None] | None = sys.exit,
):
    from .log import get_logger
    logger = get_logger(require=False)

    msg = f"Terminating (code {exit_code})"
    if signal_code:
        msg = f"Terminating (code {exit_code}, signal {signal_code})"

    if shutdown_started():
        logger.info("Forcing the termination")
        os._exit(2)  # noqa
    else:
        logger.info("Shutting threads down")
        shutdown()

    logger.info(msg)
    if callback is not None:
        callback(exit_code)


def shutdown():
    global _shutdown_started
    _shutdown_started = True
    for thread in _threads:
        thread.shutdown()
    for thread in _threads:
        if th.current_thread() == thread:
            continue
        if thread.is_alive():
            thread.join()
    _threads.clear()


def shutdown_started() -> bool:
    return _shutdown_started


def class_to_command_name(o: object) -> str:
    classname = o.__class__.__qualname__.removesuffix("Monitor").removesuffix("Provider")
    return re.sub(r"([a-z])([A-Z])", "\\1-\\2", classname).lower()


class ShutdownableThread(th.Thread):
    def __init__(self, command_name=None, thread_name=None, target=None, daemon=None):
        self._shutdown_event = th.Event()
        _register(self)

        super().__init__(name=command_name + ":" + thread_name, target=target, daemon=daemon)

    def run(self):
        from .log import get_logger
        get_logger().info(f"Starting {self!r}")

    def destroy(self):
        from .log import get_logger
        get_logger().info(f"Terminating {self!r}")

    def is_shutting_down(self):
        return self._shutdown_event.is_set()

    def shutdown(self):
        self._shutdown_event.set()

    def __repr__(self):
        if hasattr(self, '_native_id'):
            return super().__repr__() + f", PID {self._native_id}"
        return super().__repr__()


class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = th.Lock()

    def next(self) -> int:
        with self._lock:
            self._value += 1
            return self._value

    @property
    def value(self) -> int:
        return self._value
