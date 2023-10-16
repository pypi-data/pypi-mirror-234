# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import pytermor as pt

from ..._base import CliCommand
from ..._decorators import catch_and_log_and_exit, cli_command
from es7s.shared import get_stdout


@cli_command(name=__file__, cls=CliCommand, short_help="xterm-256 colors as HSV table")
@catch_and_log_and_exit
class invoker:
    """
    Display xterm-256 color chart (with xterm-16 as a part of it)
    aligned using HSV channel values for easier color picking.
    """

    H_VALUES = [*range(0, 360, 10)]
    # S_VALUES = [*range(0, 110, 10)]
    S_VALUES = [15, 30, 40, 56, 100]
    # V_VALUES = [*range(0, 110, 10)]
    V_VALUES = [30, 50, 70, 85, 100]

    XTERM_16_VALUES = [
        [*range(0, 8)],
        [*range(8, 16)],
    ]
    GRAYSCALE_VALUES = [16, *range(232, 256), 231]

    H_FMT = pt.Style(fg=pt.cv.GRAY_30, overlined=True)
    S_FMT = pt.Style(fg=pt.cv.GRAY_93, bg=pt.cv.GRAY_0)

    V_FMT = pt.Style(fg=pt.cv.GRAY_30)
    A_FMT = pt.Style(fg=pt.cv.GRAY_70, bold=True)

    def __init__(self, **kwargs):
        self._run()
        self._last_cell_code: int|None = None

    def _format_col_label(self, h: int) -> str:
        return (f"{h:3d}°" if h % 30 == 0 else "").center(5)

    def _format_row_label(self, v: int | None, sep: str = "│") -> str:
        return " " + (f"{v:>3d}%".strip() if isinstance(v, int) else "").ljust(5) + sep

    def _get_border_fmt(self, s: int, v: int) -> pt.Style:
        return self.H_FMT if (v == self.V_VALUES[0] and s > self.S_VALUES[0]) else self.V_FMT

    def _print_row_label(self, s: int, v: int | None):
        get_stdout().echo_rendered(self._format_row_label(v), self._get_border_fmt(s, v), nl=False)

    def _print_row_label_right(self, s: int, v: int):
        get_stdout().echo_rendered(
            self._format_row_label(s if v == self.V_VALUES[len(self.V_VALUES) // 2] else None),
            self._get_border_fmt(s, v),
        )

    def _print_table_header(self, s: int):
        self._print_attribute("  V", "↓  ")
        self._print_vert_sep()
        for idx, h in enumerate(self.H_VALUES):
            if h == self.H_VALUES[len(self.H_VALUES) // 2]:
                self._print_attribute("← H", " →")
            else:
                get_stdout().echo_rendered(self._format_col_label(h), self.V_FMT, nl=False)
        self._print_vert_sep()
        self._print_attribute("  S", "↓  ")
        self._print_vert_sep()
        get_stdout().echo()

    def _print_attribute(self, name: str, arrow: str):
        get_stdout().echo_rendered(f"{name}{arrow}", self.A_FMT, nl=False)

    def _print_vert_sep(
        self,
    ):
        get_stdout().echo_rendered(f"│", self.V_FMT, nl=False)

    def _print_horiz_sep(self, sep, hidden=False, double=False, over=False):
        sep = (
                self._format_row_label(None, sep=sep)
                + "".ljust(len(self.H_VALUES) * 5)
                + sep
                + self._format_row_label(None, sep=sep)
        )
        st = self.V_FMT
        if over:
            st = pt.Style(st, overlined=True)
        if hidden:
            return get_stdout().echo_rendered(sep.replace(" ", " "), st)
        if double:
            return get_stdout().echo_rendered(sep.replace(" ", "═"), st)
        return get_stdout().echo_rendered(sep.replace(" ", "─"), st)

    def _print_cell(self, h: int, s: int, v: int, code: int = None):
        col = None
        if code is None:
            approx = pt.approximate(pt.HSV(h, s / 100, v / 100), pt.Color256, max_results=5)
            cols = [c for c in approx if not c.color._color16_equiv]
            if not cols:
                get_stdout().echo_rendered("".ljust(5), nl=False)
                return
            col = cols[0].color
            code = col.code
        if not col:
            col = pt.Color256.get_by_code(code)

        label_val = f"▏{col.code:3d} " if col.code != self._last_cell_code else " "
        self._last_cell_code = col.code
        get_stdout().echo_rendered(label_val.center(5), pt.Style(bg=col, overlined=True).autopick_fg(), nl=False)

    def _run(self):
        self._print_horiz_sep("╷")
        self._print_table_header(0)
        self._print_horiz_sep("│")

        for s in self.S_VALUES:
            for v in self.V_VALUES:
                self._print_row_label(s, v)
                self._last_cell_code = None
                for h in self.H_VALUES:
                    self._print_cell(h, s, v)
                get_stdout().echo_rendered("│", self.V_FMT, nl=False)
                self._print_row_label_right(s, v)

        self._print_horiz_sep("│", hidden=True, over=True)

        for cidx, cc in enumerate(self.XTERM_16_VALUES):
            self._print_row_label(0, None)
            get_stdout().echo_rendered(pt.pad(3), nl=False)
            for c in cc:
                self._print_cell(0, 0, 0, code=c)
            if cidx == 0:
                get_stdout().echo_rendered(pt.pad(5), nl=False)
                for c in self.GRAYSCALE_VALUES:
                    self._print_cell(0, 0, 0, code=c)
                get_stdout().echo_rendered(pt.pad(2), nl=False)
            else:
                get_stdout().echo_rendered(pt.pad(5*(1+len(self.GRAYSCALE_VALUES))+2), nl=False)
            get_stdout().echo_rendered("│", self.V_FMT, nl=False)
            self._print_row_label_right(0, 0)

        self._print_horiz_sep("│", hidden=True)
        self._print_horiz_sep(" ", hidden=True, over=True)
