# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from __future__ import annotations

import re

import pytermor as pt

from es7s.shared import FrozenStyle, Styles, get_merged_uconfig, ThemeColor


class Separator:
    def __init__(self, label: str):
        self._label = label

    def _apply_style(self, label: str) -> pt.Fragment:
        st = FrozenStyle(
            bg=Styles.STATUSBAR_BG,
            fg=ThemeColor('monitor_separator'),
        )
        if get_merged_uconfig().get_monitor_debug_mode():
            if {*label} == {" "}:
                label = label.replace(" ", "␣")
            else:
                left_pad, label, right_pad = re.split(r"(\S+)", label)
                label = len(left_pad) * ">" + label + len(right_pad) * "<"
            st = Styles.DEBUG_SEP_EXT
        return pt.Fragment(label, st)

    @property
    def fragment(self) -> pt.Fragment:
        return self._apply_style(self._label)


EMPTY = Separator("")
SPACE = Separator(" ")
SPACE_2 = Separator(" " * 2)
SPACE_3 = Separator(" " * 3)
LINE = Separator("│")
LINE_2 = Separator(" ▏")
LINE_3 = Separator(" │ ")
EDGE_LEFT = Separator("▏")
EDGE_RIGHT = Separator("▕")
