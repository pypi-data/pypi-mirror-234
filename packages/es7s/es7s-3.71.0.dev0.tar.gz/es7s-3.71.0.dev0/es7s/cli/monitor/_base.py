# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import math
import pickle
import re
import signal
import threading as th
import time
import typing
import typing as t
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from io import StringIO

import click
import pytermor as pt
from pytermor import RT, FT

from .._base import CliCommand
from .._base_opts_params import GroupOption, ScopedOption
from es7s.commons import (
    SocketClient,
    SocketMessage,
)
from es7s.shared import (
    FrozenStyle,
    get_logger,
    get_stdout,
    ShutdownableThread,
    Styles,
    get_merged_uconfig,
    init_config,
    IoProxy,
)
from ...commons.pt_ import format_attrs
from es7s.shared import make_dummy_io, make_interceptor_io
from es7s.shared import class_to_command_name, exit_gracefully, ThemeColor

DT = t.TypeVar("DT")
CT = t.TypeVar("CT", bound="CoreMonitorConfig")

SEPARATOR_MAP: t.Dict[str, str | pt.Fragment] = {
    "none": "",
}
SEPARATOR_DEFAULTS: list[str] = ["none", "none"]


class MonitorCliCommand(CliCommand):
    def _get_group_options(self) -> list[ScopedOption]:
        return [
            GroupOption(
                param_decls=["-d", "--demo"],
                is_flag=True,
                default=False,
                help="Do not start a monitor, display all output examples instead.",
            ),
        ]


# -----------------------------------------------------------------------------


class CoreMonitorConfig:
    """
    Public settings (allowed to change via config; in contrast with `CoreMonitorSettings`).
    """

    _config_section: str
    debugging_markup: bool = False
    force_cache: bool = False

    def __init__(self, config_section: str, debug_mode: bool, force_cache: bool):
        self._config_section = config_section
        self.debugging_markup = debug_mode
        self.force_cache = force_cache
        self.update_from_config()
        get_logger().debug("Monitor user config: " + format_attrs(self))

    def update_from_config(self):
        pass  # update specific monitors' settings


@dataclass
class RatioStyle:
    ratio_upper_threshold: float
    fmt: FT
    alert: bool = False
    _style: pt.Style = field(init=False)

    def __post_init__(self):
        self._style = pt.make_style(self.fmt)

    @property
    def style(self) -> pt.Style:
        return self._style


class RatioStyleMap(deque[RatioStyle]):
    def __init__(self, values: t.Sequence[RatioStyle] | None):
        if not values:
            return
        self._validate(values)
        super().__init__(values, maxlen=len(values))

    def init_delayed(self, values: t.Sequence[RatioStyle]):
        self._validate(values)
        super().__init__(values, maxlen=len(values))

    def __bool__(self):
        return len(self) > 0

    def _validate(self, values: t.Sequence[RatioStyle]):
        if len(values) < 2:
            raise ValueError("At least 2 elements required")

        directions = set()
        max_value = None
        min_value = None
        for idx, value in enumerate(values):
            if idx == 0:
                continue
            cur_value = values[idx].ratio_upper_threshold
            prev_value = values[idx - 1].ratio_upper_threshold
            direction = 1 if prev_value < cur_value else -1
            directions.add(direction)
            if len(directions) > 1:
                raise ValueError(
                    f"RSM values must be a monotonic increasing/decreasing sequence: {values}."
                )

            min_value = min(min_value or cur_value, cur_value)
            max_value = max(max_value or cur_value, cur_value)

    def find(self, cur_ratio: float) -> RatioStyle:
        for val in self:
            if val.ratio_upper_threshold > cur_ratio:
                return val
        if len(self):
            return self[-1]
        raise RuntimeError("Empty ratio style map")


@dataclass(frozen=True)
class CoreMonitorSettings(t.Generic[CT]):
    """
    Internal settings (for the developer only).
    """

    alerting_ratio_stmap = RatioStyleMap(
        [
            RatioStyle(0.70, Styles.PBAR_DEFAULT),
            RatioStyle(0.75, Styles.PBAR_ALERT_1, True),
            RatioStyle(0.80, Styles.PBAR_ALERT_2, True),
            RatioStyle(0.85, Styles.PBAR_ALERT_3, True),
            RatioStyle(0.90, Styles.PBAR_ALERT_4, True),
            RatioStyle(0.95, Styles.PBAR_ALERT_5, True),
            RatioStyle(0.99, Styles.PBAR_ALERT_6, True),
            RatioStyle(1.00, Styles.PBAR_ALERT_7, True),
        ]
    )

    socket_topic: str
    socket_receive_interval_sec: float = 1.0
    update_interval_sec: float = 1.0
    message_ttl: float = 5.0
    alt_mode: bool = False
    alt_mode_frame_dur: float = 2.0
    alt_mode_frames_num: int = 2
    network_comm_indic: bool = False
    inner_length_control: bool = False
    cache_ttl: float = 60.0  # see GenericRenderer._invalidate_cache
    ratio_styles_map: RatioStyleMap = None
    config: CT = None
    renderer: typing.Type[IMonitorRenderer] = None
    demo_composer: typing.Type[IDemoComposer] = None

    def __post_init__(self):
        get_logger().debug("Monitor settings: " + format_attrs(self))

    @property
    def eff_network_comm_indic(self) -> bool:
        return self.network_comm_indic and not self.config.force_cache

    @property
    def eff_socket_receive_interval_sec(self) -> float:
        if self.config.force_cache:
            return 2
        return self.socket_receive_interval_sec

    @property
    def eff_update_interval_sec(self) -> float:
        if self.config.force_cache:
            return 2
        return self.update_interval_sec


@dataclass
class CoreMonitorState:
    is_enabled: bool = True
    abs_running_time: float = 0
    tick_update_num: int = 0
    tick_render_num: int = 0
    error_amount: int = 0
    timeout: int = 0
    idle_timeout: int = 0
    alt_mode_timeout: int = 0
    last_valid_msg: SocketMessage[DT] | None = None
    data_hash: int | None = None
    data_hash_alt_mode: bool = False
    data_fmtd: RT = None
    ratio: float | None = None

    def __repr__(self):
        parts = (
            "+ON" if self.is_enabled else "-ON",
            f"Å={self.abs_running_time:.1f}",
            f"U={self.tick_update_num}",
            f"R={self.tick_render_num}",
            f"T={self.timeout:.1f}",
            f"I={self.idle_timeout:.1f}",
            f"A={self.alt_mode_timeout:.1f}",
            f"err={self.error_amount}",
            f"msg=" + (f"{self.last_valid_msg.timestamp}" if self.last_valid_msg else ""),
            f"ratio=" + (f"{100 * self.ratio:>.1f}%" if self.ratio else ""),
            f"data="
            + (f'"{self.data_fmtd!r}"' if isinstance(self.data_fmtd, pt.IRenderable) else ""),
        )
        return f"{self.__class__.__qualname__}[{' '.join(parts)}]"

    @property
    def is_alt_mode(self) -> bool:
        return self.alt_mode_timeout > 0

    @property
    def network_comm(self) -> bool:
        if self.last_valid_msg:
            return self.last_valid_msg.network_comm
        return False

    def log(self):
        get_logger().trace(f"State: " + repr(self))


# -----------------------------------------------------------------------------


class CoreMonitor(ShutdownableThread, t.Generic[DT, CT], ABC):
    TICK_DURATION_SEC = 0.1  # min sleep duration

    DEFAULT_ALT_MODE_DURATION_SEC = 4.0
    DEFAULT_ALT_FRAME_DURATION_SEC = 2  # switching every 2 seconds
    DEFAULT_ALT_FRAMES_NUM = 2  # ... between two different frames

    RETRY_ON_ERROR_BASE_DELAY_SEC = 5
    RETRY_ON_ERROR_MAX_ATTEMPTS = 5

    def __init__(
        self,
        ctx: click.Context,
        demo: bool,
        interceptor: StringIO = None,
        ui_update: th.Event = None,
        debug_mode: bool = None,
        force_cache: bool = False,
        **kwargs,
    ):
        command_name = ctx.command.name
        self._demo = demo
        self._combined_mode = interceptor is not None
        if self._combined_mode:
            command_name = class_to_command_name(self)
        else:
            debug_mode = get_merged_uconfig().get_monitor_debug_mode()
        super().__init__(command_name=command_name, thread_name="ui")

        self._setup: CoreMonitorSettings[CT] = self._init_settings(debug_mode, force_cache)
        self._state: CoreMonitorState = CoreMonitorState()
        self._monitor_data_buf = deque[bytes](maxlen=1)
        self._socket_client_pause = th.Event()
        self._socket_client_ready = th.Event()
        self._socket_client = SocketClient(
            self._monitor_data_buf,
            self._setup.eff_socket_receive_interval_sec,
            self._socket_client_pause,
            self._socket_client_ready,
            self._setup.socket_topic,
            command_name,
        )

        if demo:
            self._renderer = self._init_renderer()
            try:
                self._renderer.set_output_stream(make_dummy_io(), None)
                self._init_demo_composer().render()
            except Exception as e:
                get_logger().exception(e)
            finally:
                return

        elif self._combined_mode:
            self._renderer = self._init_renderer()
            self._renderer.set_output_stream(make_interceptor_io(interceptor), ui_update)
            self._socket_client.start()
            self._update_from_config()
            self.start()

        else:
            self._renderer = self._init_renderer()
            signal.signal(signal.SIGUSR1, self._preview_alt_mode)
            signal.signal(signal.SIGUSR2, self._update_settings_request)
            self._socket_client.start()
            self._update_from_config()
            self.start()
            self.join()

    @abstractmethod
    def _init_settings(self, debug_mode: bool, force_cache: bool) -> CoreMonitorSettings:
        raise NotImplementedError

    def _init_renderer(self) -> IMonitorRenderer:
        renderer_t = self._setup.renderer or AltItalicRenderer
        return renderer_t(self.get_output_width(), self._setup, self._state)

    def _init_demo_composer(self) -> IDemoComposer:
        return self._setup.demo_composer(self)

    def shutdown(self):
        super().shutdown()
        if hasattr(self, "_socket_client"):  # check for cases when app  crashes while initializing
            self._socket_client.shutdown()

    @abstractmethod
    def get_output_width(self) -> int:
        raise NotImplementedError

    def run(self):
        super().run()
        stdout = get_stdout()
        logger = get_logger()

        self._renderer.update_init()
        self._socket_client_ready.wait(self.TICK_DURATION_SEC)

        while True:
            if self.is_shutting_down():
                self.destroy()
                break
            if stdout.is_broken:
                logger.info("IoProxy detected broken pipe, terminating")
                self.shutdown()
                break

            if self._state.timeout > self.TICK_DURATION_SEC:
                self._sleep(self.TICK_DURATION_SEC)
                continue
            self._sleep(self._state.timeout)
            self._update()

    def _add_timeout(self, timeout_sec: float = 1.0):
        self._state.timeout += timeout_sec

    def _reset_timeout(self):
        self._state.timeout = 0

    def _sleep(self, timeout_sec: float):
        if timeout_sec == 0:
            return
        time.sleep(timeout_sec)
        self._state.abs_running_time += timeout_sec
        self._state.timeout = max(0.0, self._state.timeout - timeout_sec)
        self._state.idle_timeout = max(0.0, self._state.idle_timeout - timeout_sec)
        self._state.alt_mode_timeout = max(0.0, self._state.alt_mode_timeout - timeout_sec)
        self._state.log()

    @property
    def current_frame(self) -> int:
        return math.floor(
            self._state.abs_running_time
            // self._setup.alt_mode_frame_dur
            % self._setup.alt_mode_frames_num
        )

    def _get_retry_on_error_delay_sec(self) -> float:
        # progressive wait delay increasing:
        #   1 sec on 1st error
        #   5 sec on 2nd (if right after 1st)
        #   25 sec on 3rd
        #   2 min on 4th
        #   10 min on 5th
        #   exit on 6th, so that tmux can restart the monitor
        return math.pow(self.RETRY_ON_ERROR_BASE_DELAY_SEC, self._state.error_amount - 1)

    def _format_data(self, msg: SocketMessage[DT]):
        data_fmtd = self._format_data_impl(msg)
        if isinstance(data_fmtd, (pt.IRenderable, str)):
            self._state.data_fmtd = data_fmtd
        elif isinstance(data_fmtd, list) and self._state.ratio is not None:
            self._state.data_fmtd = self._renderer.render_progress_bar(
                data_fmtd, self.get_output_width()
            )
        else:
            raise TypeError(f"Expected RT or list[RT], got: {type(data_fmtd)}")

    @abstractmethod
    def _format_data_impl(self, msg: SocketMessage[DT]) -> RT | list[RT]:
        raise NotImplementedError

    def _update(self):
        logger = get_logger()

        if self._state.idle_timeout > 0:
            self._renderer.update_idle()
            self._sleep(1.0)
            return
        if not self._state.is_enabled:
            self._renderer.update_disabled()
            self._sleep(1.0)
            return

        self._state.tick_update_num += 1
        try:
            try:
                msg_raw = self._monitor_data_buf[0]
            except IndexError:
                raise EmptyDaemonQueueError()
            msg = self._deserialize(msg_raw)

            msg_ttl = self._setup.message_ttl
            now = time.time()

            if now - msg.timestamp > msg_ttl:
                self._monitor_data_buf.remove(msg_raw)
                raise ExpirationError(f"Expired socket message: {now} > {msg.timestamp}")

            if self._state.last_valid_msg:
                if now - self._state.last_valid_msg.timestamp > msg_ttl:
                    self._state.last_valid_msg = None

            if (
                not self._state.last_valid_msg
                or msg.timestamp != self._state.last_valid_msg.timestamp
            ):
                self._state.last_valid_msg = msg
                # logger.trace(msg_raw, label="Received data dump")

                data_hash = msg.data_hash
                if (
                    self._setup.config.force_cache
                    and self._state.data_hash == data_hash
                    and self._state.data_hash_alt_mode == self._state.is_alt_mode
                ):
                    self._add_timeout(self._setup.eff_update_interval_sec)
                    return
                else:
                    logger.debug("Deserialized changed message: " + repr(msg))

                    self._state.data_hash = data_hash
                    self._state.data_hash_alt_mode = self._state.is_alt_mode
                    self._state.tick_render_num += 1
                    self._format_data(msg)
                    self._renderer.update_primary()

        except EmptyDaemonQueueError:
            logger.warning("No data from daemon")
            self._renderer.update_no_data()
        except ExpirationError as e:
            logger.error(e)
            self._renderer.update_on_error()
        except Exception as e:
            logger.exception(e)
            self._renderer.update_on_error()
        else:
            self._state.error_amount = 0
            self._add_timeout(self._setup.eff_update_interval_sec)
            return

        self._increase_error_amount()

    def _preview_alt_mode(self, *args):
        if not self._setup.alt_mode:
            return
        self._state.alt_mode_timeout = self.DEFAULT_ALT_MODE_DURATION_SEC
        self._reset_timeout()
        self._state.last_valid_msg = None

        get_logger().debug("Switched to alt mode")
        self._state.log()

    def _deserialize(self, msg_raw: bytes) -> SocketMessage[DT]:
        msg = pickle.loads(msg_raw)
        return msg

    def _increase_error_amount(self):
        self._state.error_amount += 1
        self._state.idle_timeout = self._get_retry_on_error_delay_sec()

        if self._state.error_amount >= self.RETRY_ON_ERROR_MAX_ATTEMPTS:
            exit_gracefully(exit_code=1)

        err_count = f"{self._state.error_amount}/{self.RETRY_ON_ERROR_MAX_ATTEMPTS}"
        get_logger().debug(f"Acceptable errors: {err_count}")

    def _update_settings_request(self, signal_code: int, *args):
        self._renderer.update_busy()
        get_logger().info(f"Updating the setup: {signal.Signals(signal_code).name} ({signal_code})")
        if not self._combined_mode:
            init_config()
        self._update_from_config()

        prev_renderer = self._renderer
        self._renderer = self._init_renderer()
        if self._combined_mode:
            self._renderer.set_output_stream(prev_renderer)

        self._update()
        self._renderer._ui_event.set()
        self._state.log()

    def _update_from_config(self):
        self._setup.config.update_from_config()


# -----------------------------------------------------------------------------


class IMonitorRenderer(ABC):
    @abstractmethod
    def __init__(
        self,
        output_width: int,
        monitor_setup: CoreMonitorSettings,
        monitor_state: CoreMonitorState,
    ):
        raise NotImplementedError

    @typing.overload
    def set_output_stream(self, prev: IMonitorRenderer):
        ...

    @typing.overload
    def set_output_stream(self, io: IoProxy, ui_update: th.Event | None):
        ...

    @abstractmethod
    def set_output_stream(self, *args):
        ...

    @abstractmethod
    def update_primary(self) -> str:
        ...

    @abstractmethod
    def update_init(self) -> str:
        ...

    @abstractmethod
    def update_disabled(self) -> str:
        ...

    @abstractmethod
    def update_no_data(self) -> str:
        ...

    @abstractmethod
    def update_on_error(self) -> str:
        ...

    @abstractmethod
    def update_busy(self) -> str:
        ...

    @abstractmethod
    def update_idle(self) -> str:
        ...

    @abstractmethod
    def wrap_progress_bar(self, *frags: RT, sep_left: str, sep_right: str) -> list[RT]:
        ...

    @abstractmethod
    def render_progress_bar(self, result_parts: list[RT], max_len: int) -> RT:
        ...

    @abstractmethod
    def render_frac(self, val: str, int_st: pt.Style, frac_st=Styles.VALUE_FRAC_3) -> list[pt.RT]:
        ...

    @abstractmethod
    def render_time_delta(self, delta_str: str, value_fg: pt.Color) -> list[pt.RT]:
        ...


class GenericRenderer(IMonitorRenderer):
    def __init__(
        self,
        output_width: int,
        monitor_setup: CoreMonitorSettings,
        monitor_state: CoreMonitorState,
        output_alt_st: pt.Style = pt.NOOP_STYLE,
    ):
        self._output_width = output_width
        self._stdout: IoProxy = get_stdout()
        self._ui_event: th.Event | None = None
        self._msetup = monitor_setup
        self._mstate = monitor_state

        self._output_alt_st = output_alt_st
        self._output_network_comm = pt.Fragment("·", pt.Style(fg=ThemeColor()))

        self._output_init = self._make_fixed_width_output("...", Styles.TEXT_DISABLED)
        #        self._output_disabled = self._make_fixed_width_output(
        #            "-" * (min(3, self._output_width - 2)), Styles.TEXT_DISABLED
        #        )
        self._output_disabled = pt.FrozenText("---", Styles.TEXT_DISABLED, width=5, align="center")
        self._output_no_data = self._make_fixed_width_output("NODATA", Styles.WARNING_ACCENT)
        self._output_busy = self._make_fixed_width_output("BUSY", Styles.WARNING)
        self._output_idle = self._make_fixed_width_output("WAITING", Styles.TEXT_DISABLED)
        self._output_error = self._make_fixed_width_output("ERROR", Styles.ERROR_LABEL)

        self._debug_override = pt.Style(Styles.DEBUG)

        self._last_rendered: RT | None = None
        self._last_rendered_ts: float = 0.0

    @typing.overload
    def set_output_stream(self, prev: GenericRenderer):
        ...

    @typing.overload
    def set_output_stream(self, io: IoProxy, ui_update: th.Event | None):
        ...

    def set_output_stream(self, *args):
        if len(args) == 1:
            self._stdout, self._ui_event = args[0]._stdout, args[0]._ui_event
        elif len(args) == 2:
            self._stdout, self._ui_event = args

    def _make_fixed_width_output(self, string: str, style: pt.Style) -> pt.FrozenText:
        return pt.FrozenText(string, style, width=self._output_width, align="center")

    def _echo(self, string: RT) -> str:
        if self._msetup.config.debugging_markup:
            string = self._apply_debugging_markup(string)

        if self._msetup.config.force_cache:
            self._invalidate_cache()
            if self._last_rendered == string:
                return string
            self._last_rendered = string
            self._last_rendered_ts = time.time()

        self._stdout.echo_rendered(string)
        # if self._ui_event:
        #     self._ui_event.set()
        return string

    def _apply_debugging_markup(self, output: RT) -> pt.Text:
        if not isinstance(output, pt.FrozenText):
            output = pt.FrozenText(output)
        output_mod = pt.Text(width=len(output), align=output._align)
        for fdx, frag in enumerate(output._fragments):
            frag_style = frag.style
            if frag_style.bg != pt.NOOP_COLOR:
                frag_style = pt.merge_styles(frag_style, overwrites=[self._debug_override])
            for cdx, c in enumerate(frag.raw()):
                if self._msetup.eff_network_comm_indic and fdx == 0 and cdx == 0:
                    output_mod += pt.Fragment(c.replace(" ", "○", 1).replace("·", "●"), Styles.DEBUG_SEP_INT)
                elif c in "▏|▕":
                    output_mod += pt.Fragment(
                        c, pt.merge_styles(frag.style, overwrites=[Styles.DEBUG_SEP_INT])
                    )
                else:
                    output_mod += pt.Fragment(c.replace(" ", "␣"), frag_style)
        return output_mod

    def _invalidate_cache(self):
        # monitors terminate upon broken pipe detection, i.e., when parent process (tmux)
        # exits and closes the stream. the only way the monitor can detect it is when it
        # writes something to stdout. monitors cache the rendered output and if the monitor's
        # data changes rarely (e.g., system date, docker containers or battery level while
        # sitting on A/C power), it doesn't actually write anything to stdout for hours, just
        # sits in the background and consumes resources. the solution is to reset the cache
        # every N minutes (or seconds) to make monitor write to the stream periodically and
        # terminate itself when necessary (we don't need instant response to tmux exit, we
        # need just the response itself, even after a minute or so).

        if not self._last_rendered_ts:
            return
        if time.time() - self._last_rendered_ts >= self._msetup.cache_ttl:
            get_logger().debug("Invalidating expired output cache")
            self._last_rendered = None

    def update_init(self) -> str:
        return self._echo(self._output_init)

    def update_disabled(self) -> str:
        return self._echo(self._output_disabled)

    def update_primary(self) -> str:
        result: t.List[str | pt.Fragment] = []
        alt_active = self._msetup.alt_mode and self._mstate.is_alt_mode

        if alt_active and self._output_alt_st != pt.NOOP_STYLE:
            result.append(pt.Fragment(fmt=self._output_alt_st, close_this=False))

        if self._msetup.eff_network_comm_indic:
            if self._mstate.network_comm:
                result.append(self._output_network_comm)
                if self._ui_event:
                    self._ui_event.set()
            else:
                result.append(pt.Fragment(" "))

        data_fmtd = self._mstate.data_fmtd
        if not self._msetup.inner_length_control and len(data_fmtd) > self._output_width:
            get_logger().warning(f"Primary string length exceeds max: {data_fmtd!r}")
        result.extend(data_fmtd._fragments)

        return self._echo(pt.Text(*result))

    def update_no_data(self) -> str:
        return self._echo(self._output_no_data)

    def update_on_error(self) -> str:  # @refactor these omfg
        return self._echo(self._output_error)

    def update_busy(self) -> str:
        return self._echo(self._output_busy)

    def update_idle(self) -> str:
        return self._echo(self._output_idle)

    def _align_basic_output(self, s: str) -> str:
        return s[: self._output_width].center(self._output_width)

    def wrap_progress_bar(self, *frags: RT, sep_left="▏", sep_right=" ") -> list[RT]:
        st = pt.Style(
            bg=Styles.STATUSBAR_BG,
            fg=ThemeColor('monitor_separator'),
            class_name="separator",
        )
        sep_left = pt.Fragment(sep_left, st)
        sep_right = pt.Fragment(sep_right, st)
        return [sep_left, *frags, sep_right]

    def render_progress_bar(self, result_parts: list[RT], max_len: int) -> pt.Text:
        ov_st = pt.NOOP_STYLE
        fill_threshold = max_len + 1
        if self._mstate.ratio and self._msetup.ratio_styles_map:
            ratio_style = self._msetup.ratio_styles_map.find(self._mstate.ratio)
            ov_st = ratio_style.style
            fill_threshold = round(max_len * self._mstate.ratio)

        # result = pt.Text(pt.Fragment("", Styles.PBAR_BG, close_this=False))
        result = pt.Text("")
        while len(result_parts) > 0:
            result_part = result_parts.pop(0)
            if isinstance(result_part, pt.Fragment):
                frags = [result_part]
            else:
                frags = result_part._fragments

            for frag in frags:
                if frag.style.class_name == "separator":  # keep bg only
                    ov_local_sts = [pt.Style(bg=ov_st.bg)]
                else:
                    ov_local_sts = [ov_st]
                    if frag.style.class_name == "warning":
                        ov_local_sts = [frag.style]
                colorized_st = pt.merge_styles(frag.style, overwrites=ov_local_sts)

                if len(result) < fill_threshold <= len(result) + len(frag):
                    split_part_idx = fill_threshold - len(result)
                    left_part = frag.raw()[:split_part_idx]
                    right_part = frag.raw()[split_part_idx:]

                    if right_part:
                        result_parts = [pt.Fragment(right_part, frag.style), *result_parts]
                    result += pt.Fragment(left_part, colorized_st)

                elif len(result) < fill_threshold:
                    result += pt.Fragment(frag.raw(), colorized_st)
                else:
                    result += frag
        # result += pt.Fragment("", pt.Style(bg=pt.DEFAULT_COLOR), close_prev=True)
        return result

    def render_frac(self, val: str, int_st: pt.Style, frac_st=Styles.VALUE_FRAC_3) -> list[pt.RT]:
        if "." in val:
            val_int, val_frac = val.split(".", 1)
            return [
                pt.Fragment(val_int, int_st),
                pt.Fragment("." + val_frac, frac_st),
            ]
        return [pt.Fragment(val, int_st)]

    def render_time_delta(self, delta_str: str, value_fg: pt.Color = pt.NOOP_COLOR) -> list[pt.RT]:
        result = []

        def add_frag(m: t.Match) -> str:
            nonlocal result
            st = pt.NOOP_STYLE
            if m.group(1):
                st = Styles.VALUE_PRIM_2
                st = pt.Style(st, fg=value_fg)
            elif m.group(2):
                st = pt.Style(Styles.VALUE_UNIT_4, fg=value_fg)
            result.append(pt.Fragment(m.group(0), st))
            return ""

        re.sub(r"(\d+)|(\D+)", add_frag, delta_str)
        return result


class AltItalicRenderer(GenericRenderer):
    def __init__(
        self,
        output_width: int,
        monitor_setup: CoreMonitorSettings,
        monitor_state: CoreMonitorState,
    ):
        super().__init__(output_width, monitor_setup, monitor_state, pt.Style(italic=True))


class LetterIndicatorRenderer(GenericRenderer):
    def __init__(
        self,
        label: str,
        monitor_setup: CoreMonitorSettings,
        monitor_state: CoreMonitorState,
    ):
        super().__init__(len(label), monitor_setup, monitor_state)

        def _make_output(base_st: pt.Style) -> pt.FrozenText:
            return pt.FrozenText(label, FrozenStyle(base_st, bold=True, blink=True))

        self._output_init = pt.FrozenText("…", Styles.TEXT_DISABLED)
        self._output_disabled = pt.FrozenText(label, Styles.TEXT_DISABLED)
        self._output_no_data = _make_output(Styles.WARNING_ACCENT)
        self._output_busy = _make_output(Styles.WARNING)
        self._output_idle = _make_output(Styles.WARNING_LABEL)
        self._output_error = _make_output(Styles.ERROR_LABEL)


# -----------------------------------------------------------------------------


class IDemoComposer(ABC):
    @abstractmethod
    def __init__(self, monitor: CoreMonitor):
        raise NotImplementedError

    @abstractmethod
    def render(self):
        pass


class GenericDemoComposer(IDemoComposer):
    def __init__(self, monitor: CoreMonitor):
        self._monitor = monitor

        if get_merged_uconfig().get_monitor_debug_mode():
            self._monitor._setup.config.debugging_markup = True

        self._table_st = pt.Style(bg="full-black", fg="gray")
        self._table_sep = get_stdout().render("│", self._table_st)

    def render(self):
        self._print_row("NOT IMPLEMENTED")

    def _switch_alt_mode(self, enable: bool = None):
        mstate = self._monitor._state
        dest_state = enable
        if dest_state is None:
            dest_state = not mstate.is_alt_mode
        dest_val = 2**10 if dest_state else 0  # should be enough
        mstate.alt_mode_timeout = dest_val

    def _set_alt_frame(self, frame_num: int):
        self._monitor._state.abs_running_time = frame_num * self._monitor._setup.alt_mode_frame_dur

    def _format_row_label(self, label: str, width: int) -> pt.RT:
        return pt.FrozenText(label, self._table_st, width=width, align="right")

    def _render_msg(self, msg: SocketMessage) -> str:
        self._monitor._format_data(msg)
        return self._monitor._renderer.update_primary()

    def _print_rows(self, *rows: t.Iterable[pt.RT]):
        for row in rows:
            self._print_row(*row)

    def _print_row(self, *cells: pt.RT):
        stdout = get_stdout()
        for cell in ["", *cells]:
            stdout.echo_rendered(cell, pt.NOOP_STYLE, nl=False)
            stdout.echo_rendered(self._table_sep, pt.NOOP_STYLE, nl=False)
        stdout.echo()

    def _print_horiz_sep(self, label: str, width: int, fill: str = " ", tline=True, bline=True):
        stdout = get_stdout()
        label = label.center(width, fill)
        st = pt.Style(self._table_st, underlined=bline, overlined=tline)
        formatted = pt.FrozenText(label, st, width=width, align="center")
        stdout.echo(self._table_sep + stdout.render(formatted) + self._table_sep)

    def _print_header(self, cells: t.Iterable[t.Tuple[str, int]], tline=True, bline=True):
        stdout = get_stdout()
        for cell, width in [("", 0), *cells]:
            st = pt.Style(self._table_st, overlined=tline, underlined=bline)
            formatted = pt.FrozenText(cell.center(width), st, width=width)
            stdout.echo(stdout.render(formatted) + self._table_sep, nl=False)
        stdout.echo()

    def _print_triple_header(self, cells: t.Iterable[t.Tuple[str, int]], top=True, bottom=True):
        empty_cells = [("", c[1]) for c in cells]
        if top:
            self._print_header(empty_cells, tline=True, bline=False)
        self._print_header(cells, tline=False, bline=False)
        if bottom:
            self._print_header(empty_cells, tline=False, bline=True)

    def _print_footer(self, width: int):
        stdout = get_stdout()
        formatted = pt.FrozenText(
            pt.pad(width),
            pt.Style(self._table_st, overlined=True, bg=pt.DEFAULT_COLOR),
            width=width,
            align="center",
        )
        stdout.echo(" " + stdout.render(formatted))


class ExpirationError(Exception):
    pass


class EmptyDaemonQueueError(Exception):
    pass
