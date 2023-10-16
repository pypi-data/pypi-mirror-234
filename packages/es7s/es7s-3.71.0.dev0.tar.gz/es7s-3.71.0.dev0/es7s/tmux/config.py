# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing
from abc import ABCMeta
from collections import OrderedDict

import pytermor as pt
from _fns import *


QUERY_SPLIT_REGEX = pt.color._ColorRegistry._QUERY_SPLIT_REGEX


class ConfigDef:
    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls)
        inst.__dict__["_map"] = OrderedDict[str, str]()
        return inst

    def __getattr__(self, key):
        # return self._map[key]
        return usrvarx(self.__name__(key))

    def __setattr__(self, key, value):
        self._map.update({key: value})

    def __name__(self, key):
        classname_parts = QUERY_SPLIT_REGEX.split(self.__class__.__name__)
        return "_".join(["es7s", *classname_parts, *key.split("_")]).lower().strip("_")

    def print(self):
        while len(self._map):
            key, value = self._map.popitem(0)
            # if key.startswith('_'):
            #     continue
            if isinstance(value, ConfigDef):
                value.print()
            else:
                valuestr = self._format_kv(key, value)
                if not valuestr:
                    continue
                print(valuestr)

    def _format_kv(self, key: str, value: any) -> str | None:
        return f'set -g @{self.__name__(key)} "{value}"'


Var = typing.TypeVar("Var", callable, str)


class Vars(ConfigDef):
    def __init__(self):
        self.cursor_x: Var = var
        self.cursor_y: Var = var
        self.copy_cursor_x: Var = var
        self.copy_cursor_y: Var = var

        self.pane_active: Var = var
        self.pane_index: Var = var
        self.pane_marked: Var = var
        self.pane_width: Var = var
        self.pane_input_off: Var = var
        self.pane_pipe: Var = var
        self.pane_title: Var = var
        self.pane_width: Var = var
        self.pane_height: Var = var

        self.selection_start_x: Var = var
        self.selection_start_y: Var = var
        self.selection_end_x: Var = var
        self.selection_end_y: Var = var

        self.es7s_theme_prim: Var = usrvarx
        self.es7s_theme_accent: Var = usrvarx

        self.es7s_show_pane_index: Var = usrvarx
        self.es7s_wd_path: Var = usrvarx
        self.es7s_wd_name: Var = usrvarx

    def __getattr__(self, key) -> str:
        return self._map[key](key)

    def _format_kv(self, key: str, value: any) -> str | None:
        return value(key)


vars = Vars()


class Theme(ConfigDef):
    def __init__(self):
        self.accent = vars.es7s_theme_accent

        self.primary_fg_if_active = if_("pane_active", then_="fg=" + vars.es7s_theme_prim)

        self.pane_border_fg = "colour238"
        self.pane_border_fg_active = "colour244"


th = Theme()


class InterfaceConfig(ConfigDef, metaclass=ABCMeta):
    def __init__(self):
        self.empty = ""


class PaneBorderGeneric(InterfaceConfig, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

        self.fmt_default = fmt(
            "fg=" + if_(vars.pane_active, then_=th.pane_border_fg_active, else_=th.pane_border_fg),
            "nobold",
            "noblink",
            "noreverse",
        )


class PaneBorderLeft(InterfaceConfig):
    def __init__(self):
        super().__init__()

        self.index = if_(
            vars.es7s_show_pane_index,
            then_=(
                self.fmt_default
                + fmt("bold", th.primary_fg_if_active)
                + vars.pane_index
                + self.fmt_default
            ),
        )
        self.path = (
            self.fmt_default
            + vars.es7s_wd_path
            + fmt(th.primary_fg_if_active)
            + "/"
            + vars.es7s_wd_name
            + self.fmt_default
        )
        self.title = self.fmt_default + strlim(
            s=var_or_empty("pane_title"),
            n=sub(vars.pane_width, "26"),
            sfx="‥",
        )
        self.sigil_mark = if_(
            vars.pane_marked,
            then_=self._make_sigil("^"),
        )
        self.sigil_input_off = if_(
            vars.pane_input_off,
            then_=self._make_sigil("####", vars.pane_active, "blink"),
        )
        self.sigil_pipe = if_(
            vars.pane_pipe,
            then_=self._make_sigil("%", vars.pane_active, "blink"),
        )
        self.sigils = "".join(
            [
                self.sigil_mark,
                self.sigil_input_off,
                self.sigil_pipe,
            ]
        )
        self.sigils_pad = if_(numcmp_gt(strwidth(self.sigils), "0"), then_=" ")
        self._ = (
            fmt("align=left")
            + self.index
            + self.sigils
            + self.sigils_pad
            + if_(vars.pane_title, then_=self.title, else_=self.path)
        )

    def _make_sigil(self, label: str, expr=None, *extra_fmt: str) -> str:
        f = fmt("fg=" + th.accent, "bold", *extra_fmt)
        if not expr:
            return f + label + self.fmt_default
        return if_(expr, then_=f) + label + self.fmt_default


class PaneBorderRight(PaneBorderGeneric):
    def __init__(self):
        super().__init__()

        self.label_size = vars.pane_width + "x" + vars.pane_height
        self.label_size_len = strwidth(self.label_size)
        self.label_cursor = vars.cursor_y + ":" + vars.cursor_x
        self.label_cursor_len = strwidth(self.label_cursor)
        self.label_cursor_sep = replace(
            ".", " ", strpadr(self.empty, sub(self.label_size_len, self.label_cursor_len))
        )
        self.label_cursor_copy = vars.copy_cursor_y + ":" + vars.copy_cursor_x
        self.label_cursor_copy_len = strwidth(self.label_cursor_copy)
        self.label_cursor_copy_sep = replace(
            ".", " ", strpadr(self.empty, sub(self.label_size_len, self.label_cursor_copy_len))
        )
        self.label_selection_copy_diffx = sub(vars.selection_end_x, vars.selection_start_x)
        self.label_selection_copy_diffy = sub(vars.selection_end_y, vars.selection_start_y)
        self.label_selection_copy = (
            if_(expr=rematch("^-", self.label_selection_copy_diffx), else_="+")
            + self.label_selection_copy_diffx
        ) + (
            if_(expr=rematch("^-", self.label_selection_copy_diffy), else_="+")
            + self.label_selection_copy_diffy
        )
        self.label_selection_copy_len = strwidth(self.label_cursor_copy)
        #
        # set -g @es7s-pane-border-selcopy-llen "#{n:#{E:@es7s-pane-border-selcopy-label}}"
        # set -g @es7s-pane-border-selcopy-sep "#{s|.| |:#{p-#{e|-:#{E:@es7s-pane-border-size-llen},#{E:@es7s-pane-border-selcopy-llen}}:@empty}}"


defs = [
    PaneBorderLeft(),
    PaneBorderRight(),
]

th.print()
[def_.print() for def_ in defs]

"""
set -g @es7s-pane-border-alter "#{E:@es7s-pane-border-style-default} #{?alternate_on,#[italics]A#[noitalics], } #{E:@es7s-pane-border-style-default}"
set -g @es7s-pane-border-size "#{E:@es7s-pane-border-style-default} (#{E:@es7s-pane-border-size-label}) #{E:@es7s-pane-border-style-default}"
set -g @es7s-pane-border-curcopy "#{?pane_in_mode,#{E:@es7s-pane-border-curcopy-sep}#{?pane_active,#[fg=$TMUX_COLOR_MODE_COPY],}[#{E:@es7s-pane-border-curcopy-label}]#{E:@es7s-pane-border-style-default},}"
set -g @es7s-pane-border-cur "#{?pane_in_mode,,#{E:@es7s-pane-border-cur-sep}#{E:@es7s-pane-border-style-default}[#{E:@es7s-pane-border-cur-label}]#{E:@es7s-pane-border-style-default}}"
set -g @es7s-pane-border-format-right "#[align=right]#{E:@es7s-pane-border-alter}#{E:@es7s-pane-border-size}#{E:@es7s-pane-border-cur}#{E:@es7s-pane-border-curcopy}"

set -g pane-border-format "#{E:@es7s-pane-border-format-left}#{E:@es7s-pane-border-format-right}"
"""
