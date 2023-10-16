# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import logging
from dataclasses import dataclass
from logging import WARN, INFO

import click
import pytermor as pt

from es7s.commons import SocketMessage
from es7s.shared import Styles, get_logger, DockerStatus, DockerInfo, FrozenStyle
from ._base import CoreMonitor, MonitorCliCommand, CoreMonitorSettings, CoreMonitorConfig, \
    GenericDemoComposer
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="docker container status counters",
    output_examples=[
        "│` 23 +0 `│  # 23 running               ",
        "│`  4 +11`│  #  4 running, 11 restarting",
    ],
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    Indicator of docker container statuses. Involves 'docker ps' command.

    Output is a fixed string 7 chars wide: │`Cup·Crs`│, where Cup is the current amount
    of *running* containers, and Crs -- amount of *restarting* ones. When any of the
    values change, it will be highlighted for a short period of time; color depends
    on an indicator type.
    """
    DockerMonitor(ctx, demo, **kwargs)


class DockerMonitor(CoreMonitor[DockerInfo, CoreMonitorConfig]):
    HIGHLIGHT_UPDATE_DELAY_TICKS = 3
    OUTPUT_SEP = " "

    def __init__(self, ctx: click.Context, demo: bool, **kwargs):
        self.configs: list[_StatusConfig] = [
            _StatusConfig(
                "running",
                width=3,
                style_changed=FrozenStyle(fg=pt.cv.GREEN, bold=True),
                placeholder="Up",
            ),
            _StatusConfig(
                "restarting",
                width=3,
                style_static=FrozenStyle(fg=pt.cv.YELLOW),
                style_changed=FrozenStyle(fg=pt.cv.HI_YELLOW, bold=True),
                align="<",
                prefix="+",
                placeholder="Rs",
                log_level=WARN,
            ),
            # _StatusConfig("removing"),
            # _StatusConfig("dead"),
            # _StatusConfig("paused"),
            # _StatusConfig("created"),
            # _StatusConfig("exited"),
        ]
        self._states: dict[_StatusConfig, _StatusState] = {
            cfg: _StatusState() for cfg in self.configs
        }
        super().__init__(ctx, demo, **kwargs)

    def _init_settings(self, debug_mode: bool, force_cache: bool) -> CoreMonitorSettings:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="docker",
            config=CoreMonitorConfig("monitor.docker", debug_mode, force_cache),
            demo_composer=DockerDemoComposer,
        )

    def get_output_width(self) -> int:
        return 7

    def _format_data_impl(self, msg: SocketMessage[DockerInfo]) -> pt.Text:
        """OUTPUT SIZE: 7"""

        for cfg in self.configs:
            status = msg.data.get(cfg.name)
            state = self._states.get(cfg)
            state.updated_ticks_ago += 1
            if state.container_amount is None:
                state.updated_ticks_ago = self.HIGHLIGHT_UPDATE_DELAY_TICKS
            elif state.container_amount != status.match_amount or status.updated_in_prev_tick:
                msg_str = f"Status '{cfg.name}' changed: {state.container_amount} -> {status.match_amount}"
                if cfg.log_level > INFO and len(status.container_names) > 0:
                    msg_str += f" ({', '.join(status.container_names)})"
                get_logger().log(cfg.log_level, msg_str)
                state.updated_ticks_ago = 0
            state.container_amount = status.match_amount

        get_logger().debug(
            "Container status states: "
            + str({cfg.name: str(state) for cfg, state in self._states.items()})
        )
        output = pt.Text()
        output_sep = pt.Fragment(self.OUTPUT_SEP, Styles.TEXT_DISABLED)

        for idx, (cfg, state) in enumerate(self._states.items()):
            if idx > 0:
                output += output_sep
            output += self._format_state(cfg, state)
        return output

    def _format_state(self, cfg: _StatusConfig, state: _StatusState) -> pt.Fragment:
        """OUTPUT SIZE: 3"""

        style = cfg.style_static
        val = cfg.placeholder

        if state.container_amount is not None:
            if state.container_amount == 0:
                style = Styles.TEXT_DISABLED
            if state.updated_ticks_ago < self.HIGHLIGHT_UPDATE_DELAY_TICKS:
                style = cfg.style_changed

            prefix = cfg.prefix or ""
            val = prefix + str(state.container_amount)
            if len(val) > cfg.width:
                val = prefix.ljust(cfg.width, "9")
                style.blink = True

        return pt.Fragment(f"{val:{cfg.align}{cfg.width}.{cfg.width}s}", style)


@dataclass
class _StatusConfig:
    name: str
    width: int
    style_static: FrozenStyle = Styles.VALUE_PRIM_2
    style_changed: FrozenStyle = None
    align: str = ">"
    prefix: str = None
    placeholder: str = None
    log_level: int = INFO

    def __hash__(self) -> int:
        return int.from_bytes(self.name.encode(), byteorder="big")


@dataclass
class _StatusState:
    container_amount: int = None
    updated_ticks_ago: int = 0

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}[{self.container_amount} containers, "
            f"{self.updated_ticks_ago} ticks ago]"
        )


class DockerDemoComposer(GenericDemoComposer):
    def render(self):
        def make_msg(n1, n2):
            return SocketMessage(DockerInfo({
                "running": DockerStatus(n1),
                "restarting": DockerStatus(n2),
            }))

        get_logger().setLevel(logging.CRITICAL)

        last_msg = None
        for nrun in range(0, 15, 3):
            for nres in range(0, 2):
                last_msg = make_msg(nrun, nres)
                self._print_row(self._render_msg(last_msg))
        for _ in range(0, 3):
            self._print_row(self._render_msg(last_msg))
