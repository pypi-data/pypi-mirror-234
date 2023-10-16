# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import math
import re

import click
import pytermor as pt

from ._base import (
    CoreMonitorConfig,
    CoreMonitor,
    MonitorCliCommand,
    CoreMonitorSettings,
    GenericDemoComposer,
    RatioStyle,
    RatioStyleMap,
)
from .._decorators import cli_pass_context, catch_and_log_and_exit, catch_and_print, cli_command
from es7s.commons import SocketMessage
from es7s.shared import Styles
from es7s.shared import DiskUsageInfo

OUTPUT_WIDTH = 6


@cli_command(
    name=__file__,
    cls=MonitorCliCommand,
    short_help="current disk usage stats",
    output_examples=[],
)
@cli_pass_context
@catch_and_log_and_exit
@catch_and_print
def invoker(ctx: click.Context, demo: bool, **kwargs):
    """
    ``
    """
    DiskUsageMonitor(ctx, demo, **kwargs)


class DiskUsageMonitor(CoreMonitor[DiskUsageInfo, CoreMonitorConfig]):
    def __init__(self, *args, **kwargs):
        self._formatter = pt.StaticFormatter(pt.formatter_bytes_human, max_value_len=3)
        super().__init__(*args, **kwargs)
        ## а то

    def _init_settings(self, debug_mode: bool, force_cache: bool) -> CoreMonitorSettings[CoreMonitorConfig]:
        return CoreMonitorSettings[CoreMonitorConfig](
            socket_topic="disk-usage",
            update_interval_sec=5,
            #alt_mode=True,
            ratio_styles_map=RatioStyleMap(
                [
                    RatioStyle(0.90, Styles.PBAR_DEFAULT),
                    RatioStyle(0.92, Styles.PBAR_ALERT_1, True),
                    RatioStyle(0.94, Styles.PBAR_ALERT_2, True),
                    RatioStyle(0.96, Styles.PBAR_ALERT_3, True),
                    RatioStyle(0.98, Styles.PBAR_ALERT_4, True),
                    RatioStyle(0.99, Styles.PBAR_ALERT_5, True),
                    RatioStyle(0.995, Styles.PBAR_ALERT_6, True),
                    RatioStyle(1.00, Styles.PBAR_ALERT_7, True),
                ]
            ),
            config=CoreMonitorConfig("monitor.disk-usage", debug_mode, force_cache),
            demo_composer=DiskUsageDemoComposer,
        )

    def get_output_width(self) -> int:
        return OUTPUT_WIDTH

    def _format_data_impl(self, msg: SocketMessage[DiskUsageInfo]) -> pt.RT | list[pt.RT]:
        self._state.ratio = msg.data.used_perc / 100
        is_full = msg.data.free < 1000

        result = []
        if self._state.is_alt_mode:
            if self.current_frame == 0:
                if is_full:
                    return [pt.Fragment("FULL".center(OUTPUT_WIDTH))]
                val = msg.data.total - msg.data.free
                label = "U"
            else:
                val = msg.data.total
                label = "C"
            val_pfx = self._formatter.format(val).center(OUTPUT_WIDTH)
            result += [pt.Fragment(label + " ", Styles.TEXT_LABEL)]
        else:
            if is_full:
                return self._renderer.wrap_progress_bar(pt.Fragment("FULL".center(OUTPUT_WIDTH-2)))
            val_pfx = self._formatter.format(msg.data.free).center(OUTPUT_WIDTH)
            result += [pt.Fragment(" ")]

        _, int_val, frac_val, pfx, _ = re.split(r"([\d]+)(.\d+)?(\D)", val_pfx, maxsplit=1)
        int_val = int_val or ""
        frac_val = (frac_val or "")[:2]
        pfx = (pfx or "").strip()
        pad_val = OUTPUT_WIDTH - len(int_val + frac_val + pfx) - 2
        pad_val_right = min(1, math.ceil(pad_val / 2))
        result += [
            pt.Fragment(" " * (pad_val - pad_val_right)),
            pt.Fragment(int_val, Styles.VALUE_PRIM_2),
            pt.Fragment(frac_val, Styles.VALUE_FRAC_3),
            pt.Fragment(" " * (pad_val_right)),
            pt.Fragment(pfx, Styles.VALUE_UNIT_4),
        ]
        if self._state.is_alt_mode:
            return pt.Text(*result)
        return self._renderer.wrap_progress_bar(*result[1:])


class DiskUsageDemoComposer(GenericDemoComposer):
    def render(self):
        ROW_LEN = 6

        table_len = (OUTPUT_WIDTH + 1) * ROW_LEN - 1
        self._print_triple_header([('Root ("/") disk space left', table_len)])

        dtotal = 1000**4
        cells = []
        dusedl = [
            *range(0, 850, 49),
            850,
            877,
            900,
            933,
            965,
            977,
            980,
            990,
            997.221,
            999.99994,
            999.9999987,
            1000,
        ]
        while len(dusedl) > 0 or len(cells) > 0:
            if len(dusedl) > 0:
                dused = min(dtotal, dusedl.pop(0) * dtotal / 1000)
                dusedp = 100 * dused / dtotal
                dfree = dtotal - dused
                msg = SocketMessage(DiskUsageInfo(free=dfree, used_perc=dusedp, total=dtotal))
                cells.append(self._render_msg(msg))
            else:
                cells.append(" " * OUTPUT_WIDTH)

            if len(cells) == ROW_LEN:
                self._print_row(*cells)
                cells.clear()

        # self._print_triple_header([("Alt mode: Space used/disk capacity", table_len)])
        #
        # def render_alter():
        #     def render_total():
        #         for dusedp in [
        #             0.01,
        #             0.40,
        #             0.90,
        #             0.95,
        #             0.99,
        #             1.0,
        #         ]:
        #             dused = dusedp * dtotal
        #             yield self._render_msg(
        #                 SocketMessage(
        #                     DiskUsageInfo(
        #                         used_perc=dusedp,
        #                         free=(dtotal - dused),
        #                         total=dtotal,
        #                     )
        #                 )
        #             )
        #     self._print_row(*render_total())
        #
        # self._switch_alt_mode(True)
        # render_alter()
        # self._set_alt_frame(1)
        # render_alter()
        self._print_footer(table_len)
