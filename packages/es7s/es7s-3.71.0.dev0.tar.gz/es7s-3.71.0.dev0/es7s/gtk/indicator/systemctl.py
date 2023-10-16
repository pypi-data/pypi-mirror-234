# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from es7s.commons import SocketMessage
from es7s.shared import SystemCtlInfo, run_subprocess
from ._base import _BaseIndicator
from ._icon_selector import StaticIconSelector, StaticIconEnum
from ._state import _StaticState, MenuItemConfig


class IndicatorSystemCtl(_BaseIndicator[SystemCtlInfo, StaticIconSelector]):
    def __init__(self):

        self._reset = _StaticState(
            callback=self._enqueue_reset,
            gconfig=MenuItemConfig("Reset warnings", sep_before=True),
        )

        super().__init__(
            indicator_name="systemctl",
            socket_topic="systemctl",
            icon_selector=StaticIconSelector(StaticIconEnum.WARNING),
            title="[systemctl]",
            auto_visibility=True,
            states=[self._reset],
        )

    def _enqueue_reset(self, _=None):
        self._enqueue(self._reset_warnings)

    def _reset_warnings(self):
        run_subprocess("systemctl", "reset-failed")

    def _render(self, msg: SocketMessage[SystemCtlInfo]):
        self._hidden.value = msg.data.ok
        self._update_details(f"Status:\t{msg.data.status}")
        self._update_visibility()
