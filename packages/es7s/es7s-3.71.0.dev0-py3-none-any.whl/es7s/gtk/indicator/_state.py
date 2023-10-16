# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t
from abc import abstractmethod
from collections import deque, OrderedDict
from dataclasses import dataclass
from typing import ClassVar

from gi.repository.Gtk import MenuItem, CheckMenuItem, RadioMenuItem  # noqa

from es7s.shared import get_logger, rewrite_value
from es7s.commons import pt_
from es7s.shared.uconfig import get_merged as get_merged_uconfig


@dataclass(frozen=True, eq=True)
class Notification:
    msg: str


@dataclass
class IndicatorUnboundState:
    abs_running_time_sec: float = 0
    tick_update_num: int = 0
    tick_render_num: int = 0
    timeout: int = 0
    wait_timeout: int = 0
    notify_timeout: int = 0
    notify_enqueue_timeout: int = 0
    notification_queue: deque[Notification] = deque()

    def __repr__(self):
        parts = (
            f"Å={self.abs_running_time_sec:.1f}",
            f"U={self.tick_update_num}",
            f"R={self.tick_render_num}",
            f"T={self.timeout:.1f}",
            f"W={self.wait_timeout:.1f}",
            f"N={self.notify_timeout:.1f}({len(self.notification_queue):d})",
            f"NQ={self.notify_enqueue_timeout:.1f}",
        )
        return f"{self.__class__.__qualname__}[{' '.join(parts)}]"

    @property
    def warning_switch(self) -> bool:
        return self.tick_update_num % 2 == 0

    @property
    def is_waiting(self) -> bool:
        return self.wait_timeout > 0

    def cancel_wait(self):
        self.wait_timeout = 0

    def log(self):
        get_logger().debug("State:\n"+repr(self))


@dataclass
class _State:
    active = False
    gobject: MenuItem = None
    gconfig: "MenuItemConfig" = None

    @abstractmethod
    def click(self):
        ...


@dataclass
class _StaticState(_State):
    callback: t.Callable[[_State], None] = None
    _label_value: str|None = None

    def click(self):
        if self.callback:
            self.callback(self)

    def update_label(self, text: str):
        if not self.gobject:
            return
        self._label_value = text
        self.gobject.set_label(self._label_value)

    def prepend_label(self, text: str):
        self.gobject.set_label(pt_.joincoal(text, self._label_value, sep='\n'))


@dataclass
class _BoolState(_StaticState):
    value: bool = True
    config_var: tuple[str, str] = None  # (section, name)
    config_var_value: str = None  # for radios
    gobject: CheckMenuItem | RadioMenuItem = None
    callback: t.Callable[["_BoolState"], None] = None

    def __post_init__(self):
        if self.config_var is not None and self.config_var[0]:
            uconfig = get_merged_uconfig()
            if self.config_var_value is None:
                self.value = uconfig.getboolean(*self.config_var)
            else:
                self.value = uconfig.get(*self.config_var) == self.config_var_value

    def __bool__(self):
        return self.value

    @property
    def active(self) -> bool:
        return self.value

    def click(self):
        if self.gobject and self.value == self.gobject.get_active():
            return  # prohibits value toggling after clicking on active radio item
        self.value = not self.value
        self._update_config(self.value)
        super().click()

    def activate(self):
        if self.value:
            return
        self.gobject.set_active(True)

    def deactivate(self):
        if not self.value:
            return
        self.gobject.set_active(False)

    def _update_config(self, val: bool):
        if self.config_var is None:
            return
        if self.config_var_value is None:
            rewrite_value(*self.config_var, "on" if val else "off")
        else:
            if not val:
                return
            rewrite_value(*self.config_var, self.config_var_value)


@dataclass(frozen=True)
class MenuItemConfig:
    label: str
    sensitive: bool = True
    sep_before: bool = False

    def make(self, state: _State) -> MenuItem:
        return MenuItem.new_with_label(self.label)


@dataclass(frozen=True)
class CheckMenuItemConfig(MenuItemConfig):
    def make(self, state: _BoolState) -> MenuItem:
        item = CheckMenuItem.new_with_label(self.label)
        item.set_active(state.active)
        item.set_sensitive(self.sensitive)
        return item


@dataclass(frozen=True)
class RadioMenuItemConfig(MenuItemConfig):
    """
    Current implementation allows only one group.
    """

    group: str = ""

    def make(self, state: _BoolState) -> MenuItem:
        item = RadioMenuItem.new_with_label([], self.label)
        RadioMenuItem.join_group(item, RadioMenuItemGroups.get(self.group))
        item.set_active(state.active)
        RadioMenuItemGroups.assign(self.group, item)
        return item


class RadioMenuItemGroups:
    _last: ClassVar[t.Dict[str, RadioMenuItem]]

    @classmethod
    def get(cls, group: str) -> RadioMenuItem | None:
        if not hasattr(cls, "_last"):
            return None
        return cls._last.get(group)

    @classmethod
    def assign(cls, group: str, item: RadioMenuItem):
        if not hasattr(cls, "_last"):
            cls._last = dict()
        cls._last[group] = item


class StateMap(OrderedDict[MenuItemConfig, _State]):
    def put(self, k: MenuItemConfig, v: _State):
        super().update({k: v})
