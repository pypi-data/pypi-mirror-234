# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import datetime
import itertools
import time
from collections.abc import Iterable
from functools import cached_property

import pytermor as pt

from es7s.commons import SocketMessage
from es7s.shared import TimestampInfo
from ._base import (
    WAIT_PLACEHOLDER,
    _BaseIndicator,
)
from ._icon_selector import IIconSelector, IconEnum
from ._state import _BoolState, CheckMenuItemConfig


class TimestampModeIconEnum(IconEnum):
    DEFAULT = "default%s.png"
    NODATA = "nodata%s.png"
    OUTDATED = "outdated%s.png"
    FUTURE = "future%s.png"

    def compose(self, netcom: bool = False) -> str:
        return self.value % (["", "-nc"][netcom])


class TimestampValueIconEnum(IconEnum):
    TPL_5_MINUTES = "%s5m%s.png"
    TPL_1_HOUR = "%s1h%s.png"
    TPL_3_HOURS = "%s3h%s.png"
    TPL_1_DAY = "%s1d%s.png"

    def compose(self, negative: bool, netcom: bool) -> str:
        return self.value % (["", "-"][negative], ["", "-nc"][netcom])


class TimestampIconSelector(IIconSelector):
    def __init__(self):
        super().__init__(TimestampModeIconEnum.DEFAULT.compose(), subpath="delta")

    def select(
        self, now: float, remote: int | None, ok: bool, network_comm: bool = None
    ) -> str:
        if override := super().select():
            return override

        if not ok:
            return TimestampModeIconEnum.OUTDATED.compose(network_comm)
        if not remote:
            return TimestampModeIconEnum.NODATA.compose(network_comm)

        negative = now < remote
        adiff = abs(now - remote)
        if adiff < 300:  # @TODO to config
            return TimestampValueIconEnum.TPL_5_MINUTES.compose(negative, network_comm)
        if adiff < 3600:
            return TimestampValueIconEnum.TPL_1_HOUR.compose(negative, network_comm)
        if adiff < 3 * 3600:
            return TimestampValueIconEnum.TPL_3_HOURS.compose(negative, network_comm)
        if adiff < 24 * 3600:
            return TimestampValueIconEnum.TPL_1_DAY.compose(negative, network_comm)
        if now < remote:
            return TimestampModeIconEnum.FUTURE.compose(network_comm)
        return TimestampModeIconEnum.DEFAULT.compose(network_comm)

    @cached_property
    def icon_names_set(self) -> set[str]:
        def _iter() -> Iterable[str]:
            yield from [
                tpl.compose(netcom)
                for tpl, netcom in itertools.product(
                    TimestampModeIconEnum,
                    [False, True],
                )
            ]
            yield from [
                tpl.compose(negative, netcom)
                for tpl, negative, netcom in itertools.product(
                    TimestampValueIconEnum,
                    [False, True],
                    [False, True],
                )
            ]

        return set(_iter())


class IndicatorTimestamp(_BaseIndicator[TimestampInfo, TimestampIconSelector]):
    """
    ╭──────────╮                         ╭────────────╮
    │ Δ │ PAST │                         │ ∇ │ FUTURE │
    ╰──────────╯                         ╰────────────╯
              -1h  -30min   ṇọẉ   +30min  +1h
         ▁▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁
       ⠄⠢⠲░░░░│▁│░░░░│▃│░░░░│█│░░░░│▀│░░░░│▔│░⣊⠈⣁⢉⠠⠂⠄
          ▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔
             ← 0%   +50%   +100%    │      │
                           -100%  -50%    -0% →
    """

    RENDER_INTERVAL_SEC = 1.0

    def __init__(self):
        self.config_section = "indicator.timestamp"
        self._formatter = pt.dual_registry.get_by_max_len(6)
        self._formatter._allow_fractional = False  # @FIXME (?) copied from monitor
        self._last_remote: int = 0
        self._invalidated_remote: int = 0

        # self._reset = _StaticState(
        #     callback=self._enqueue_reset,
        #     gconfig=MenuItemConfig("Reset remote", sep_before=False),
        # )
        self._show_value = _BoolState(
            config_var=(self.config_section, "label-value"),
            gconfig=CheckMenuItemConfig("Show value", sep_before=True),
        )

        super().__init__(
            indicator_name="timestamp",
            socket_topic="timestamp",
            icon_selector=TimestampIconSelector(),
            title="Remote timestamp",
            states=[
                # self._reset,
                self._show_value,
            ],
        )

    # def _enqueue_reset(self, _=None):
    #     self._enqueue(self._reset_remote)

    # def _reset_remote(self):
    #     self._invalidated_remote = self._last_remote
    #     self._update_title("")
    #     ForeignInvoker().spawn("-ic", 'remote "nalog add; nalog delete"', wait=False)

    def _render(self, msg: SocketMessage[TimestampInfo]):
        now = time.time()
        if (remote := msg.data.ts) is None:
            self._render_result(
                "N/A", "N/A", icon=self._icon_selector.select(now, remote, True, msg.network_comm)
            )
            return
        self._last_remote = remote

        if self._invalidated_remote:
            if remote != self._invalidated_remote:
                self._invalidated_remote = 0
            else:
                self._render_result(
                    WAIT_PLACEHOLDER,
                    WAIT_PLACEHOLDER,
                    icon=self._get_icon("nodata", msg.network_comm),
                )
                return

        icon = self._icon_selector.select(now, remote, msg.data.ok, msg.network_comm)

        delta_str = self._formatter.format(now - remote)
        self._update_details(
            "∆ "
            + delta_str
            + " · "
            + datetime.datetime.fromtimestamp(remote).strftime("%-e %b  %R")
        )

        if not self._show_value:
            delta_str = ""

        self._render_result(delta_str, delta_str, icon=icon)

    @property
    def _show_any(self) -> bool:
        return bool(self._show_value)
