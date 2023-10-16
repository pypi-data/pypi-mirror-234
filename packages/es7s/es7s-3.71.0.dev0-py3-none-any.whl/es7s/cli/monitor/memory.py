# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click
import pytermor as pt

from es7s.commons import SocketMessage
from es7s.shared import Styles, get_merged_uconfig, FrozenStyle
from es7s.shared import MemoryInfo
from ._base import (
    MonitorCliCommand,
    CoreMonitor,
    CoreMonitorSettings,
    CoreMonitorConfig,
    GenericDemoComposer,
)
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command

OUTPUT_WIDTH = 7


class _MemoryMonitorConfig(CoreMonitorConfig):
    swap_warn_threshold: float = 0.7

    def update_from_config(self):
        section = self._config_section
        self.swap_warn_threshold = get_merged_uconfig().getfloat(section, "swap-warn-threshold")


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="current RAM consumption",
    output_examples=[],
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    MemoryMonitor(ctx, demo, **kwargs)

class MemoryMonitor(CoreMonitor[MemoryInfo, _MemoryMonitorConfig]):
    def _init_settings(self, debug_mode: bool, force_cache: bool) -> CoreMonitorSettings:
        return CoreMonitorSettings(
            socket_topic="memory",
            alt_mode=True,
            ratio_styles_map=CoreMonitorSettings.alerting_ratio_stmap,
            config=_MemoryMonitorConfig("monitor.memory", debug_mode, force_cache),
            demo_composer=MemoryDemoComposer,
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[MemoryInfo]) -> pt.RT | list[pt.RT]:
        v_used = msg.data.phys_used
        v_total = msg.data.phys_total
        s_used = msg.data.swap_used
        s_total = msg.data.swap_total

        swap_ratio = (s_used / s_total) if (s_used and s_total) else 0.0
        swap_warning = swap_ratio > self._setup.config.swap_warn_threshold

        if self._state.is_alt_mode:
            self._state.ratio = swap_ratio
            used = s_used
        else:
            self._state.ratio = v_used / v_total
            used = v_used

        val, prefix = self._format_used_value(used)

        result = []
        val = val.strip().center(4)

        if swap_warning:
            swap_warning_st = FrozenStyle(
                fg=Styles.WARNING_ACCENT.fg,
                blink=True,
                class_name="warning",
            )
            frag_warning = pt.Fragment("!", swap_warning_st)
        else:
            frag_warning = pt.Fragment(" ", FrozenStyle(class_name="warning"))

        result.extend(self._renderer.render_frac(val, Styles.VALUE_PRIM_1))
        result.append(pt.Fragment(prefix, Styles.VALUE_UNIT_4))

        return [*self._renderer.wrap_progress_bar(*result, sep_left="▏", sep_right=""), frag_warning]

    def _format_used_value(self, used: int) -> tuple[str, str]:
        used_kb = used / 1024
        used_mb = used / 1024**2
        used_gb = used / 1024**3
        if used_kb < 1000:
            return pt.format_auto_float(used_kb, 4, False), "k"
        if used_mb < 10000:
            return pt.format_auto_float(used_mb, 4, False), "M"
        return pt.format_auto_float(used_gb, 4, False), "G"


class MemoryDemoComposer(GenericDemoComposer):
    def render(self):
        ROW_LEN = 5

        table_len = (OUTPUT_WIDTH + 1) * ROW_LEN - 1
        self._print_triple_header([("Current RAM usage", table_len)])

        vtotal = 32 * 1024**3
        cells = []
        vusedl = [*range(1, 1023, 23)]
        while len(vusedl) > 0 or len(cells) > 0:
            if len(vusedl) > 0:
                msg = SocketMessage(
                    MemoryInfo(
                        phys_total=vtotal,
                        phys_used=min(vtotal, vusedl.pop(0) * vtotal / 1000),
                        swap_used=1500 if len(vusedl) % 4 == 0 else None,
                        swap_total=2048,
                    )
                )
                cells.append(self._render_msg(msg))
            else:
                cells.append(" " * OUTPUT_WIDTH)

            if len(cells) == ROW_LEN:
                self._print_row(*cells)
                cells.clear()

        self._print_triple_header([("Alt mode: current SWAP usage", table_len)])
        self._switch_alt_mode(True)

        def render_swap_examples():
            s_total = 2 * 1024**3
            for s_used in [0.0, 0.3, 0.6, 0.8, 1.0]:
                yield self._render_msg(
                    SocketMessage(
                        MemoryInfo(
                            phys_total=0,
                            phys_used=0,
                            swap_used=s_used * s_total,
                            swap_total=s_total,
                        )
                    )
                )

        self._print_row(*render_swap_examples())
        self._print_footer(table_len)
