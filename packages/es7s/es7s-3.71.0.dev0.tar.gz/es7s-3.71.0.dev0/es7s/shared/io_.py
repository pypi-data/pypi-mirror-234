# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import logging
import sys
import time
import typing as t
from dataclasses import dataclass
from io import StringIO

import click
import pytermor as pt
from pytermor import FT, RT, NOOP_STYLE
from typing.io import TextIO

from .exception import ArgCountError
from .io_debug import IoDebugger

_stdout: IoProxy | None = None
_stderr: IoProxy | None = None


@dataclass
class IoParams:
    color: bool | None = None
    tmux: bool = False


def get_stdout(require: object = True) -> IoProxy | None:
    global _stdout
    if not _stdout:
        if require:
            raise RuntimeError("Stdout proxy is uninitialized")
        return None
    return _stdout


def get_stderr(require=True) -> IoProxy | None:
    global _stderr
    if not _stderr:
        if require:
            raise RuntimeError("Stderr proxy is uninitialized")
        return None
    return _stderr


def set_stdout(proxy: IoProxy):
    global _stdout
    _stdout = proxy


def set_stderr(proxy: IoProxy):
    global _stderr
    _stderr = proxy


def init_io(
    io_params: IoParams = IoParams(),
    stdout: t.IO = sys.stdout,
    stderr: t.IO = sys.stderr,
) -> tuple[IoProxy, IoProxy]:
    global _stdout, _stderr
    if _stdout:
        raise RuntimeError("Stdout proxy is already initialized")
    if _stderr:
        raise RuntimeError("Stderr proxy is already initialized")

    _stdout = IoProxy(io_params, stdout)
    _stderr = IoProxy(IoParams(color=io_params.color, tmux=False), stderr)
    pt.RendererManager.set_default(_stdout.renderer)

    from .log import get_logger
    get_logger().setup_stderr_proxy(_stderr)  # noqa
    logging.getLogger(__package__).info("IO proxies initialized")

    return _stdout, _stderr


def destroy_io():
    global _stdout, _stderr
    if _stdout:
        _stdout.destroy()
    if _stderr:
        _stderr.destroy()
    _stdout = None
    _stderr = None

    logging.getLogger(__package__).info("IO proxies destroyed")


def make_dummy_io() -> IoProxy:
    io = StringIO()
    io.name = "dummy_io"
    return IoProxy(IoParams(), io)


def make_interceptor_io(io: StringIO = None) -> IoInterceptor:
    if not io:
        io = StringIO()
    io.name = "interceptor_io"
    actual_io = get_stdout()
    return IoInterceptor(actual_io.io_params, io, actual_io.io)


class IoProxy:
    CSI_EL0 = pt.make_clear_line_after_cursor().assemble()
    RESET = pt.SeqIndex.RESET.assemble()

    PBAR_MODE_ANY_MSG_START = pt.make_set_cursor_column(1).assemble() + CSI_EL0
    PBAR_MODE_ANY_MSG_END = pt.SeqIndex.BG_COLOR_OFF.assemble()

    _output_buffer: IoInterceptor = None

    _UNINITIALIZED = object()
    _INITIALIZING = object()

    def __init__(self, io_params: IoParams, io: t.IO, actual_io: t.IO = None):
        self._io_params = io_params
        self._color = io_params.color
        self._tmux = io_params.tmux

        self._renderer = self._make_renderer(actual_io or io)
        # pass original output device for correct auto-detection

        self._io: t.IO = io
        self._is_stderr = io == sys.stderr
        self._broken = False
        self._click_available = False
        self._tmp_file = None
        self._debug_io: TextIO | object | None = self._UNINITIALIZED
        self._debug_io_recnum = 0
        self._last_persist_ts = time.time()

        if actual_io:
            return  # disable click output proxying

        try:
            import click

            self._click_available = isinstance(click.echo, t.Callable)
        except ImportError:
            pass

    def __repr__(self):
        return pt.get_qname(self) + f"[{self.io}, {self.renderer}]"

    @property
    def io(self) -> t.IO:
        return self._io

    @property
    def io_params(self) -> IoParams:
        return self._io_params

    @property
    def renderer(self) -> pt.IRenderer:
        return self._renderer

    @property
    def color(self) -> bool:
        return self._color

    @property
    def tmux(self) -> bool:
        return self._tmux

    @property
    def sgr_allowed(self) -> bool:
        if isinstance(self._renderer, pt.SgrRenderer):
            return self._renderer.is_format_allowed
        return False

    @property
    def is_broken(self) -> bool:
        return self._broken

    def as_dict(self) -> dict:
        return {
            "renderer": self._renderer,
            "color": self._color,
            "tmux": self._tmux,
        }

    def render(self, string: RT | list[RT] = "", fmt: FT = NOOP_STYLE) -> str:
        return pt.render(string, fmt, self._renderer)

    @t.overload
    def echo_rendered(self, inp: str, style: pt.Style, *, nl=True) -> None:
        ...

    @t.overload
    def echo_rendered(self, inp: str | pt.IRenderable, *, nl=True) -> None:
        ...

    def echo_rendered(self, *args, nl=True) -> None:
        if 1 <= len(args) <= 2:
            rendered = self.render(*args[:2])
            self.echo(rendered, nl=nl)
        else:
            raise ArgCountError(len(args), 1, 2)

    def echo_raw(self, string: str | pt.ISequence = "", *, nl=True) -> None:
        """Remove all SGRs"""
        if isinstance(string, pt.ISequence):
            string = ""
        else:
            string = pt.apply_filters(string, pt.EscSeqStringReplacer)
        self.echo(string, nl=nl)

    def echo_direct(self, string: str | pt.ISequence = "", *, nl=True):
        """Bypass --color restrictions"""
        self.echo(string, nl=nl, bypass=True)

    def echo(self, string: str | pt.ISequence = "", *, nl=True, bypass=False) -> None:
        self._debug_echo(string, nl)

        if isinstance(string, pt.ISequence):
            string = string.assemble()
            nl = False

        if self.is_broken:
            return
        if IoProxy._buffered_mode and not bypass and not isinstance(self, IoInterceptor):
            string = self._wrap_ghost_message(string)
            IoProxy._output_buffer.echo(string)
            return

        try:
            if isinstance(
                self._io, OneLineStringIO
            ):  # fucking fuck... @REFINE IoInterceptor was introduced later
                self._io.truncate()

            if self._click_available and not bypass:
                click.echo(string, file=self._io, color=self._color, nl=nl)
            else:
                print(string, file=self._io, end=("", "\n")[nl], flush=not bool(string))

            if isinstance(self._io, OneLineStringIO):
                self._io.seek(0)

        except BrokenPipeError:
            self._broken = True
            self._pacify_flush_wrapper()

    def echo_status_line(self, frame: str = "", *, persist=False):
        if self._renderer.is_format_allowed:
            frame += self.CSI_EL0 + self.RESET
        else:
            frame += '\n'

        if IoProxy._output_buffer.getvalue():
            self._last_persist_ts = time.time()
            self.echo(frame, nl=False)  # will be intercepted

            bufval = IoProxy._output_buffer.popvalue().rstrip()
            self.echo(bufval,  bypass=True, nl=not self._renderer.is_format_allowed)
        else:
            if persist:
                self._last_persist_ts = time.time()
            frame = self._wrap_ghost_message(frame)
            self.echo(frame, bypass=True, nl=persist)

        self.io.flush()

    def _wrap_ghost_message(self, string: str) -> str:
        if self._renderer.is_format_allowed:
            return self.PBAR_MODE_ANY_MSG_START + string +  self.PBAR_MODE_ANY_MSG_END
        return string

    @classmethod
    @property
    def _buffered_mode(cls) -> bool:  # noqa
        return cls._output_buffer is not None

    def last_persist_ts(self) -> float:
        """ Buffered/Progress bar mode only """
        return self._last_persist_ts

    @classmethod
    def enable_output_buffering(cls):
        interceptor = make_interceptor_io()
        logging.getLogger(__package__).debug(f"Enabling buffered output with {interceptor!r}")
        IoProxy._output_buffer = interceptor

    def disable_output_buffering(self):
        if not IoProxy._output_buffer:
            return
        self.echo_status_line("")
        self.echo(nl=False, bypass=True)  # clear the bar
        IoProxy._output_buffer.destroy()
        IoProxy._output_buffer = None

        logging.getLogger(__package__).debug(f"Disabled buffered output, flushed interceptor buffer")

    def write(self, s: str) -> None:
        self.echo(s)

    def destroy(self):
        if isinstance(self._debug_io, IoDebugger):
            self._debug_io.destroy()

    def _debug_echo(self, string: str | pt.ISequence, nl: bool):
        if self._debug_io == self._UNINITIALIZED:
            from es7s.shared import get_merged_uconfig
            from es7s.shared import get_logger  # <<< there is something very very wrong somewhere around here

            with get_logger().silencio():
                if not get_merged_uconfig(False):
                    return
                if get_merged_uconfig().get_cli_debug_io_mode():
                    # rulers?
                    self._debug_io = self._INITIALIZING
                    self._debug_io = IoDebugger(self._io)
                else:
                    self._debug_io = None

        if isinstance(self._debug_io, IoDebugger):
            self._debug_io.mirror_echo(string, nl)

    def _make_renderer(self, io: t.IO) -> pt.IRenderer:
        if self.tmux:
            if self.color is False:
                return pt.renderer.NoOpRenderer()
            return pt.renderer.TmuxRenderer()
        return pt.SgrRenderer(self._output_mode, io)

    @classmethod
    def _pacify_flush_wrapper(cls) -> None:
        sys.stdout = t.cast(t.TextIO, click.utils.PacifyFlushWrapper(sys.stdout))
        sys.stderr = t.cast(t.TextIO, click.utils.PacifyFlushWrapper(sys.stderr))

    @property
    def _output_mode(self) -> pt.OutputMode:
        if self.color is None:
            return pt.OutputMode.AUTO
        if self.color:
            return pt.OutputMode.TRUE_COLOR
        return pt.OutputMode.NO_ANSI


class IoInterceptor(IoProxy):
    def __init__(self, io_params: IoParams, io: StringIO, actual_io: t.IO = None):
        self._io: StringIO = io
        super().__init__(io_params, io, actual_io)

    def reset(self) -> None:
        self._io.truncate(0)
        self._io.seek(0)

    def getvalue(self) -> str:
        return self._io.getvalue()

    def popvalue(self) -> str:
        val = self._io.getvalue()
        self.reset()
        return val


class BrokenPipeEvent(Exception):
    pass


class OneLineStringIO(StringIO):
    pass
