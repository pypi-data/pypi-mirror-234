# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from datetime import datetime
import pickle
import re
import threading as th
import time
from os import environ

import pytermor as pt
import typing as t
from abc import ABC, abstractmethod
from collections import OrderedDict, deque
from os.path import abspath

from es7s.commons import (
    SocketClient,
    SocketMessage,
)
from es7s.shared import (
    ShutdownableThread,
    get_logger,
    get_merged_uconfig,
)
from ._icon_selector import IST, StaticIconSelector, IconEnum
from ._state import (
    IndicatorUnboundState,
    _State,
    _StaticState,
    _BoolState,
    MenuItemConfig,
    CheckMenuItemConfig,
    StateMap,
)
from .. import AppIndicator
from .. import Menu, CheckMenuItem, SeparatorMenuItem
from .. import Notify  # noqa
from es7s.shared.uconfig import UserConfigSection

DT = t.TypeVar("DT")

WAIT_PLACEHOLDER = ""  # "…"
_DEFAULT_TITLE = object()


class SocketClientConn:
    SOCKRCV_INTERVAL_SEC = 1.0

    def __init__(self, socket_topic: str, indicator_name: str):
        self._socket_topic: str = socket_topic
        self._indicator_name: str = indicator_name
        self._monitor_data_buf: deque[bytes] = deque[bytes](maxlen=1)
        self._pause_event: th.Event = th.Event()
        self._ready_event: th.Event = th.Event()
        self._socket_client: SocketClient | None = None

        if not self._socket_topic:
            return
        self._socket_client = SocketClient(
            self._monitor_data_buf,
            eff_recv_interval_sec=self.SOCKRCV_INTERVAL_SEC,
            pause_event=self._pause_event,
            ready_event=self._ready_event,
            socket_topic=self._socket_topic,
            command_name=self._indicator_name,
        )

    @property
    def monitor_data_buf(self) -> deque[bytes]:
        return self._monitor_data_buf

    @property
    def pause_event(self) -> th.Event:
        return self._pause_event

    @property
    def ready_event(self) -> th.Event:
        return self._ready_event

    @property
    def socket_client(self) -> SocketClient | None:
        return self._socket_client


class _BaseIndicator(ShutdownableThread, t.Generic[DT, IST], ABC):
    TICK_DURATION_SEC = 0.5

    RENDER_INTERVAL_SEC = 2.0
    RENDER_ERROR_TIMEOUT_SEC = 5.0
    NOTIFICATION_INTERVAL_SEC = 60.0
    NOTIFY_ENQUEUE_INTERVAL_SEC = 15.0

    APPINDICATOR_ID: str

    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls)
        inst._action_queue = deque()
        inst.config_section = None

        return inst

    def __init__(
        self,
        *,
        indicator_name: str,
        socket_topic: str | list[str] = None,
        icon_selector: IST = StaticIconSelector(),
        title: str = None,
        details: bool = True,
        states: list[_State] = None,
        auto_visibility: bool = False,  # not controllable via config (e.g. systemctl)
        pseudo_hide: bool = False,  # controllable via config, visible only when needed (e.g. docker)
    ):
        # fmt: off
        if not isinstance(socket_topic, list):
            socket_topic = [socket_topic]
        self._socket_client_conn: OrderedDict[str, SocketClientConn] = OrderedDict({
            st: SocketClientConn(socket_topic=st, indicator_name=indicator_name) for st in socket_topic
        })
        self._last_dto = dict[type, DT]()
        super().__init__(command_name=indicator_name, thread_name="ui")
        # fmt: on

        self._icon_selector: IST = icon_selector
        self._title_base = title
        self._title_for_mgr = title
        self._auto_visibility = auto_visibility
        self._pseudo_hide = pseudo_hide

        self.public_hidden_state = th.Event()  # костыль

        if not self._auto_visibility:
            uconfig = get_merged_uconfig()
            display_config_val = None
            if uconfig.has_section(self.config_section):
                display_config_val = uconfig.getboolean(self.config_section, "display")
            initial_visibility = display_config_val is True
        else:
            initial_visibility = False

        if not initial_visibility:
            self.public_hidden_state.set()
        self._hidden = _BoolState(value=(not initial_visibility), callback=self._update_visibility)

        title_cfg = CheckMenuItemConfig(title or indicator_name, sensitive=False)
        details_cfg = CheckMenuItemConfig("", sensitive=False)
        self._title_state = _StaticState()
        self._details_state = _StaticState()

        self._state_map: StateMap = StateMap({title_cfg: self._title_state})
        if details:
            self._state_map.put(details_cfg, self._details_state)
        self._init_state(states)

        if environ.get("ES7S_TESTS"):  # no actual interaction with gtk api
            return

        self.APPINDICATOR_ID = f"es7s-indicator-{indicator_name}"

        self._indicator: AppIndicator.Indicator = AppIndicator.Indicator.new(
            self.APPINDICATOR_ID,
            "apport-symbolic",
            AppIndicator.IndicatorCategory.SYSTEM_SERVICES,
        )
        self._indicator.set_attention_icon("dialog-warning")
        self._indicator.set_icon_theme_path(abspath(str(self._icon_selector.theme_path)))
        self._indicator.set_icon(self._icon_selector.get_icon_path())

        self._init_menu()
        self._update_visibility()

        Notify.init(self.APPINDICATOR_ID)
        for client in self._get_socket_clients():
            client.start()
        self.start()

    def uconfig(self) -> UserConfigSection:
        return get_merged_uconfig().get_section(self.config_section)

    def _init_state(self, states: list[_State] = None):
        self._state = IndicatorUnboundState()
        get_logger().trace(f"{id(self._state):06x}", repr(self._state))

        for v in states or []:
            self._state_map.put(v.gconfig, v)

    def _init_menu(self):
        self._menu = Menu()
        for config, state in self._state_map.items():
            self._make_menu_item(config, state)
        self._menu.show()
        self._indicator.set_menu(self._menu)

    def shutdown(self):
        super().shutdown()
        for client in self._get_socket_clients():
            client.shutdown()
        if hasattr(self, "_menu"):
            self._menu.hide()

    def _enqueue(self, fn: callable):
        self._action_queue.append(fn)

    def _make_menu_item(self, config: MenuItemConfig, state: _State = None) -> CheckMenuItem:
        if config.sep_before:
            sep = SeparatorMenuItem.new()
            sep.show()
            self._menu.append(sep)

        item = config.make(state)
        item.connect("activate", lambda c=config: self._click_menu_item(config))
        item.show()
        self._menu.append(item)
        state.gobject = item

        return item

    def _click_menu_item(self, config: MenuItemConfig):
        if (state := self._state_map.get(config)) is not None:
            state.click()

    def _update_visibility(self, _: _State = None):
        if self._hidden:
            self._indicator.set_status(AppIndicator.IndicatorStatus.PASSIVE)
            self.public_hidden_state.set()
            if not self._auto_visibility and not self._pseudo_hide:
                for scc in self._socket_client_conn.values():
                    scc.pause_event.set()
        else:
            self._indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
            self.public_hidden_state.clear()
            if not self._auto_visibility and not self._pseudo_hide:
                for scc in self._socket_client_conn.values():
                    scc.pause_event.clear()

    def run(self):
        super().run()

        if clients := [*self._get_socket_clients()]:
            sockrecvs = ", ".join(f"'{c.name}'" for c in clients)
            get_logger().info(f"Thread '{self.name}' waits for ({len(clients)}): {sockrecvs}")

        self._get_scc_current(rotate=True).ready_event.wait(self.TICK_DURATION_SEC)

        while True:
            self._on_before_update()
            if self.is_shutting_down():
                self.destroy()
                break
            self._notify()
            if self._state.timeout > self.TICK_DURATION_SEC:
                self._sleep(self.TICK_DURATION_SEC)
                continue
            self._sleep(self._state.timeout)

            if self.public_hidden_state.is_set() != self._hidden.value:
                self._hidden.click()

            try:
                act = self._action_queue.popleft()
            except IndexError:
                act = self._update
            act()

    def _sleep(self, timeout_sec: float):
        if timeout_sec == 0:
            return

        time.sleep(timeout_sec)
        self._state.abs_running_time_sec += timeout_sec
        self._state.timeout = max(0.0, self._state.timeout - timeout_sec)
        self._state.wait_timeout = max(0.0, self._state.wait_timeout - timeout_sec)
        self._state.notify_timeout = max(0.0, self._state.notify_timeout - timeout_sec)
        self._state.notify_enqueue_timeout = max(
            0.0, self._state.notify_enqueue_timeout - timeout_sec
        )
        self._state.log()

    def _add_timeout(self, timeout_sec: float = None):
        self._state.timeout += timeout_sec or self.RENDER_INTERVAL_SEC

    def _on_before_update(self):
        pass

    def _update(self):
        logger = get_logger()

        self._state.tick_update_num += 1
        # @REFINE self._hidden should NOT be set automatically like in docker and set
        #         from config at the same time
        if self._hidden.value and not self._auto_visibility and not self._pseudo_hide:
            self._add_timeout()
            return

        monitor_data_buf = self._get_scc_current(rotate=True).monitor_data_buf
        try:
            try:
                msg_raw = monitor_data_buf[0]
            except IndexError:
                logger.warning("No data from daemon")
                self._add_timeout()
                self._render_no_data()
                return

            msg = self._deserialize(msg_raw)

            # msg_ttl = self._setup.message_ttl
            msg_ttl = 5.0  # @TODO
            now = time.time()

            if now - msg.timestamp > msg_ttl:
                monitor_data_buf.remove(msg_raw)
                raise RuntimeError(
                    "Expired socket message: {:s} > {:s}".format(
                        *[
                            datetime.fromtimestamp(ts).strftime("%e-%b %T")
                            for ts in [now, msg.timestamp]
                        ]
                    )
                )

            else:
                # logger.trace(msg_raw, label="Received data dump")
                msg_props = f"(ts={msg.timestamp}, netcom={msg.network_comm})"
                if msg.data:
                    logger.debug(f"Deserialized message{msg_props}: " + repr(msg.data))
                else:
                    logger.debug(f"Deserialized empty message{msg_props}")
                self._add_timeout()
                self._state.tick_render_num += 1
                self._update_dto(msg)
                self._render(msg)

        except Exception as e:
            logger.exception(e)
            self._add_timeout(self.RENDER_ERROR_TIMEOUT_SEC)
            self._update_details(pt.wrap_sgr(f"Error: {e}", 40).strip())
            self._render_error()

    def _get_scc_current(self, *, rotate: bool) -> SocketClientConn | None:
        if len(self._socket_client_conn.keys()) == 0:
            return None
        first_key = [*self._socket_client_conn.keys()][0]
        if rotate:
            self._socket_client_conn.move_to_end(first_key)
        return self._socket_client_conn[first_key]

    def _get_socket_clients(self) -> t.Iterable[SocketClient]:
        if not hasattr(self, "_socket_client_conn"):
            return
        for scc in self._socket_client_conn.values():
            if scc.socket_client:
                yield scc.socket_client

    def _deserialize(self, msg_raw: bytes) -> SocketMessage[DT]:
        msg = pickle.loads(msg_raw)
        return msg

    @property
    def _show_any(self) -> bool:
        return True

    def _get_last_dto(self, type_: type[DT]) -> DT | None:
        return self._last_dto.get(type_, None)

    def _update_dto(self, msg: SocketMessage[DT]):
        self._last_dto.update({type(msg.data): msg.data})

    @abstractmethod
    def _render(self, msg: SocketMessage[DT]):
        ...

    def _render_no_data(self):
        self._set(WAIT_PLACEHOLDER, None, AppIndicator.IndicatorStatus.ACTIVE)

    def _render_result(
        self,
        result: str,
        guide: str = None,
        warning: bool = False,
        icon: str | IconEnum = None,
    ):
        # result = result.replace(' ', ' ')
        status = AppIndicator.IndicatorStatus.ACTIVE
        if warning and self._state.warning_switch:
            status = AppIndicator.IndicatorStatus.ATTENTION

        if isinstance(icon, IconEnum):
            icon = icon.value

        if icon and get_merged_uconfig().indicator_debug_mode:
            result += "|" + icon

        if not self._show_any:
            result = guide = ""

        self._set(result, guide, status)
        if icon:
            self._set_icon(icon)

        if self._icon_selector.get_icon_demo_state():
            self._title_state.prepend_label(icon)

    def _render_error(self):
        self._set("ERR", None, AppIndicator.IndicatorStatus.ATTENTION)

    def get_title_base(self) -> str:
        return self._title_base or "<noname>"

    def get_title_for_mgr(self) -> str:
        return self._title_for_mgr or self.get_title_base()

    def get_title_for_details(self) -> str:
        return self._title_state._label_value or self.get_title_base()

    def _update_title(self, title: str = _DEFAULT_TITLE, for_mgr=False):
        if not isinstance(title, str):
            title = self._title_base
        if for_mgr:
            self._title_for_mgr = title
        else:
            self._title_state.update_label(title)

    def _update_details(self, details: str = None):
        if not isinstance(details, str):
            details = "..."
        details = re.sub("\t$", "", details, flags=re.MULTILINE)
        if get_merged_uconfig().indicator_debug_mode:
            details = details.replace(" ", "␣").replace("\t", "⇥\t")
        self._details_state.update_label(details)

    def _set(self, label: str, guide: str | None, status: AppIndicator.IndicatorStatus):
        if self._hidden:
            return
        logger = get_logger()
        logger.debug("SET Label: "+label)
        logger.debug("SET Status: "+str(status.value_name))

        if get_merged_uconfig().indicator_debug_mode:
            label = label.replace(" ", "␣")
        self._indicator.set_label(label, guide or label)
        self._indicator.set_status(status)

    def _set_icon(self, icon: str) -> None:
        get_logger().trace(icon, "SET Icon")
        self._indicator.set_icon_full(self._icon_selector.get_icon_path(icon), icon)

    def _enqueue_notification(self, msg: str) -> None:
        ...  # @TODO
        # if not self._state.notify_enqueue_timeout:
        #     self._state.notify_enqueue_timeout += self.NOTIFY_ENQUEUE_INTERVAL_SEC
        #     get_logger().trace(str(self._state.notify_enqueue_timeout), "ADD notify_enqueue_timeout")
        #     new = Notification(msg)
        #     for ex in self._state.notification_queue:
        #         if ex == new:
        #             return
        #     self._state.notification_queue.append(Notification(msg))
        #     get_logger().trace(msg, "ENQUEUE")

    def _notify(self) -> None:
        ...  # @TODO
        # if not self._state.notify_timeout and len(self._state.notification_queue):
        #     self._state.notify_timeout += self.NOTIFICATION_INTERVAL_SEC
        #     get_logger().trace(str(self._state.notify_timeout), "ADD notify_timeout")
        #
        #     notification = self._state.notification_queue.popleft()
        #     Notify.Notification.new(
        #         self.APPINDICATOR_ID,
        #         notification.msg,
        #         None
        #     ).show()
        #     get_logger().trace(notification.msg, "NOTIFY")


IIndicator = t.TypeVar("IIndicator", bound=_BaseIndicator)
