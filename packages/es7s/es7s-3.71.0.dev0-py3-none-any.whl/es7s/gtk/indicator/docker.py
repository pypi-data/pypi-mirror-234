# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from es7s.commons import SocketMessage
from es7s.shared import DockerInfo
from ._base import _BaseIndicator
from ._icon_selector import StaticIconSelector, StaticIconEnum


class IndicatorDocker(_BaseIndicator[DockerInfo, StaticIconSelector]):
    RESTART_VISIBLE_DELAY_SEC = 30

    def __init__(self):
        self.config_section = "indicator.docker"
        self._last_restart_visible_till_ts = 0
        self._last_restart_containers = set()

        super().__init__(
            indicator_name="docker",
            socket_topic="docker",
            icon_selector=StaticIconSelector(StaticIconEnum.WARNING),
            title="Docker",
            pseudo_hide=True,
        )

    def _render(self, msg: SocketMessage[DockerInfo]):
        running = msg.data.get("running")
        restarting = msg.data.get("restarting")

        restarts_now = restarting.match_amount > 0 or restarting.updated_in_prev_tick
        if msg.timestamp <= self._last_restart_visible_till_ts:
            self._hidden.value = False
        else:
            if restarts_now:
                self._last_restart_visible_till_ts = msg.timestamp + self.RESTART_VISIBLE_DELAY_SEC
                for cname in restarting.container_names:
                    self._last_restart_containers.add(cname)
            else:
                self._last_restart_containers.clear()
            self._hidden.value = not restarts_now

        self._update_title(
            self._title_base + f"\t\t{running.match_amount} +{restarting.match_amount}",
            for_mgr=True,
        )
        self._update_details(
            "\n".join(
                [
                    f"{running.match_amount} running",
                    f"{restarting.match_amount} restarting"
                    + (":" if restarting.match_amount else ""),
                ]
            )
            + "\n · ".join(["", *restarting.container_names])
            + "\n * ".join(["", *self._last_restart_containers])
        )
        self._update_visibility()
