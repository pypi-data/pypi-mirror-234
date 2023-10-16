# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import logging
import select
import shlex
import subprocess
import typing as t
from subprocess import CompletedProcess, CalledProcessError

import pytermor as pt

from es7s.commons.pt_ import format_attrs
from .path import SHELL_PATH

args_filter = pt.NoopFilter() #pt.NonPrintsStringVisualizer()


def _filter_args(args: str | t.Iterable[str]) -> str:
    from .log import get_logger
    if not get_logger().setup.log_subprocess_arg_nonprints:
        return format_attrs(args)
    return args_filter.apply(format_attrs(args))


def run_detached(args: t.Iterable[str], cwd: str = None) -> int:
    """
    Run subprocess in a shell,
    do not capture anything.
    Return exit code.
    """
    logger = logging.getLogger(__package__)

    msg = f"Running detached: '{_filter_args(args)}'"
    logger.debug(msg)
    cp = subprocess.run(shlex.join(args), shell=True, cwd=cwd)

    logger.debug(f"Subprocess terminated with exit code {cp.returncode}")
    return cp.returncode


def run_subprocess(
    *args: t.Any,
    check: bool = True,
    shell: bool = False,
    executable: str = None,
    env: dict = None,
    timeout: int = None,
    cwd: str = None,
) -> CompletedProcess:
    """
    Run subprocess, wait for termination.
    Capture both stdout and stderr.
    """
    logger = logging.getLogger(__package__)

    def log_streams_dump(out: t.Any, err: t.Any):
        for name, data in {"stdout": out, "stderr": err}.items():
            if data:
                logger.debug(name)
                logger.debug(data)
        logger.debug(f"Subprocess terminated")

    msg = (
        f"Running subprocess{' (shell)' if shell else ''}: "
        f"{executable or ''} '{_filter_args(args)}'"
    )
    logger.debug(msg)

    try:
        cp = subprocess.run(
            args,
            capture_output=True,
            encoding="utf8",
            check=check,
            executable=executable,
            shell=shell,
            env=env,
            timeout=timeout,
            cwd=cwd,
        )
    except CalledProcessError as e:
        log_streams_dump(e.stdout.strip(), e.stderr.strip())
        raise e

    cp.stdout, cp.stderr = cp.stdout.strip(), cp.stderr.strip()
    log_streams_dump(cp.stdout, cp.stderr)
    return cp


def stream_subprocess(*args: t.Any) -> tuple[str | None, str | None]:
    """
    Run subprocess, yield stdout and stderr line by line.
    """
    logger = logging.getLogger(__package__)
    logger.info(f"Starting subprocess piped: '{_filter_args(args)}'")

    process = subprocess.Popen(
        args, stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding="utf8"
    )
    logger.info(f"Started subprocess [{process.pid}]")

    for line in iter(process.stdout.readline, ""):
        logger.debug(f"[{process.pid} stdout]\n"+line.rstrip())
        yield line, None

    if err := process.stderr.read():
        for line in err.splitlines():
            logger.trace(line.rstrip(), f"[{process.pid} stderr]")
            yield None, line
    logger.debug(f"Subprocess [{process.pid}] closed streams")


def stream_pipe(cmd: str, timeout_sec: float = 0.001) -> t.Any:
    """
    Run subprocess, yield stdout.
    Wait no longer than ``timeout_sec`` before each iteration.
    """

    def read_pipe(stream: t.IO, stream_name: str) -> str:
        res = b""
        while select.select([stream.fileno()], [], [], timeout_sec)[0]:
            res += stream.read(1)
        if res:
            logger.debug(f"[{process.pid} {stream_name}]\n"+str(res.rstrip()))
        return res.decode(errors="replace")

    logger = logging.getLogger(__package__)
    process = subprocess.Popen(
        SHELL_PATH,
        shell=False,
        bufsize=0,
        close_fds=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    logger.info(f"Opened shell pipe [{process.pid}]")

    while True:
        logger.debug(f"Invoking: {_filter_args(cmd)}")
        process.stdin.write(f"{cmd}\n".encode())

        while not select.select(
            [process.stdout.fileno(), process.stderr.fileno()], [], [], timeout_sec
        )[0]:
            pass
        if stdout_str := read_pipe(process.stdout, "stdout"):
            yield stdout_str
        if stderr_str := read_pipe(process.stderr, "stderr"):
            logger.error(f"Shell subprocess failure: {stderr_str}")
