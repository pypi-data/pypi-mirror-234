# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import os
import re
import typing as t
from collections import OrderedDict
from collections.abc import Iterable
from copy import copy
from dataclasses import dataclass
from datetime import datetime, timedelta
from math import ceil

import click
import pytermor as pt

from es7s.shared import IFileIconRenderer, FileIconRendererFactory, IFile
from ...commons.pt_ import format_attrs
from es7s.shared import LS_PATH
from es7s.shared import get_cur_user
from es7s.shared import (
    get_stdout,
    get_logger,
    stream_subprocess,
    Styles as BaseStyles,
    FrozenStyle,
)
from .._base_opts_params import IntRange
from .._decorators import (
    cli_pass_context,
    catch_and_log_and_exit,
    cli_option,
    cli_argument,
    cli_command,
)

SGR_RESET = pt.SeqIndex.RESET.assemble()


@cli_command(name=__file__, short_help="list directory contents with bells and whistes")
@cli_argument("file", type=str, required=False, nargs=-1)
@cli_option(
    "-g",
    "--groups",
    is_flag=True,
    help="Display group column.",
)
@cli_option(
    "-G",
    "--grid",
    type=IntRange(min_open=True, _max=4, clamp=True),
    count=True,
    help="Display names and icons as a grid. If used multiple times, cut off file names to compact "
         "the output; the more '-G'\'s specified, the shorter the file names will get.",
)
@cli_option(
    "-h",
    "--hard-links",
    is_flag=True,
    help="Display amount of hard links to the file.",
)
@cli_option(
    "-i",
    "--inode",
    is_flag=True,
    help="Display index number of each file.",
)
@cli_option(
    "-L",
    "--dereference",
    is_flag=True,
    help="Follow the symlinks and print actual file properties instead of link file properties.",
)
@cli_option(
    "-n",
    "--numeric",
    is_flag=True,
    help="Do not resolve user and group names, show their numeric IDs instead.",
)
@cli_option(
    "-o",
    "--octal-perms",
    is_flag=True,
    help="Display extra column with permissions in octal form (e.g., 0644, 0755).",
)
@cli_option(
    "-q",
    "--quote-names",
    is_flag=True,
    help="Enclose filenames in quotes and escape non-printables.",
)
@cli_option(
    "-r",
    "--reverse",
    is_flag=True,
    help="Reverse sorting order.",
)
@cli_option(
    "-R",
    "--recursive",
    is_flag=True,
    help="Descend into subdirectories.",
)
@cli_option(
    "-s",
    "--sort-by-size",
    is_flag=True,
    help="Sort list by file size (directories are unaffected), biggest last.",
)
@cli_option(
    "-t",
    "--sort-by-time",
    is_flag=True,
    help="Sort list by modification time, newest last.",
)
@cli_option(
    "-x",
    "--sort-by-ext",
    is_flag=True,
    help="Sort list alphabetically by entry extension.",
)
@cli_option(
    "--fallback-icons",
    is_flag=True,
    help="Use shorter icon set (5 items) which should be supported by literally everything down "
         "to a potato (inclusive). Useful when a terminal's font does not support Nerd Fonts "
         "file type icons (glyphs around U+E650).",
)
@cli_pass_context
@catch_and_log_and_exit
class invoker:
    """
    Wrapper around GNU 'ls' with preset settings for \\'one-button\\' usage.
    FILE is a path(s) to directories and files of interest and can be used
    multiple times, default is current/working directory. Runs and formats
    the output of '/bin/ls'. Default format is long, entries are sorted by
    file name, file sizes are in human-readable SI-form. No dereferencing
    is performed by default.\n\n

    File types indicators ('mc' nomenclature):\n\n

      `   ` regular file       ` | ` pipe              ` = ` socket\n
      ` * ` executable file    ` @ ` symlink to file   ` + ` block device\n
      ` / ` directory          ` ~ ` symlink to dir    ` - ` character device\n\n

    This command requires ++/bin/ls++ to be present and available.
    """

    # COUNT_CHILDREN_CMD = [
    #     "find",
    #     "%(file)s",
    #     "-maxdepth", "1",
    #     "-type", "d",
    #     "-exec", "sh", "-c", "find {} -maxdepth 1 | wc -l",
    #     ";",
    #     "-print",
    # ]

    SPLIT_REGEX = re.compile(r"(\d+,\s+\d+|\S+)")
    ATTR_AMOUNT = 9
    OUT_COL_SEPARATOR = " "
    SORT_ARGS_TO_LS_ARGS_MAP = {
        "sort_by_size": "-S",
        "sort_by_time": "-t",
        "sort_by_ext": "-X",
    }

    def __init__(
        self,
        ctx: click.Context,
        *,
        file: t.Tuple[str],
        dereference: bool,
        groups: bool,
        grid: int,
        hard_links: bool,
        inode: bool,
        numeric: bool,
        octal_perms: bool,
        quote_names: bool,
        recursive: bool,
        reverse: bool,
        fallback_icons: bool,
        **kwargs,
    ):
        sort_args = [
            ls_arg
            for sort_arg, ls_arg in self.SORT_ARGS_TO_LS_ARGS_MAP.items()
            if kwargs.get(sort_arg, None)
        ]
        ls_reverse_arg = reverse
        if kwargs.get("sort_by_size", None) or kwargs.get("sort_by_time", None):
            ls_reverse_arg = not reverse
        color = "always" if get_stdout().sgr_allowed else "never"
        quoting_style = "shell-escape-always" if quote_names else "literal"

        ls_args = [
            LS_PATH,
            "-l",
            "--classify",
            "--almost-all",
            "--si",
            "--group-directories-first",
            "--time-style=+%s",
            "--color=" + color,
            "--quoting-style=" + quoting_style,
            "--inode",
            "-n" if numeric else "",
            *sort_args,
            "--reverse" if ls_reverse_arg else "",
            "--recursive" if recursive else "",
            "--dereference" if dereference else "",
            "--no-group" if not groups else "",
        ]
        self._grid = grid
        self._custom_columns = dict(
            inode=inode,
            octperms=octal_perms,
            hlinks=hard_links,
            group=groups,
        )
        self._icon_renderer = FileIconRendererFactory.make(fallback_icons)
        self._rwx_map = _Styles.get_rwx_map()

        self._run(file, *filter(None, ls_args))

    def _run(self, file: t.Tuple[str], *ls_args: str):
        ls_args += ("--", *file)
        buf: list[tuple[str, int]] = []
        max_len = 0

        for out, err in stream_subprocess(*ls_args):
            if out and (line := self._process_ls_output(out.rstrip())):
                if self._grid:
                    cur_len = len(pt.apply_filters(line, pt.EscSeqStringReplacer))
                    max_len = max(max_len, cur_len)
                    buf.append((line, cur_len))
                else:
                    get_stdout().echo(line)
            if err:
                get_logger().error(err.rstrip())

        if self._grid and len(buf):
            self._print_grid(buf, max_len)

    def _process_ls_output(self, line: str) -> str:
        if line.startswith("total"):
            return get_stdout().render(_highligher.colorize(line))
        try:
            return self._process_regular_line(line)
        except ValueError as _:
            return line

    def _get_split_limit(self) -> int:
        return self.ATTR_AMOUNT - 1 - (1 if not self._custom_columns.get("group") else 0)

    def _process_regular_line(self, line: str) -> str:
        splitted = list(self._split_ls_line(line))

        if not self._custom_columns.get("group"):
            splitted.insert(4, " ")

        if len(splitted) != self.ATTR_AMOUNT:
            return line

        file = File(*splitted)
        columns = file.render(self._custom_columns, self._icon_renderer, self._rwx_map, self._grid)
        filtered_columns = self._assemble_line(columns)
        return self.OUT_COL_SEPARATOR.join(filtered_columns)

    def _assemble_line(self, render_parts: OrderedDict) -> t.Iterable[str]:
        for k, v in render_parts.items():
            if not self._custom_columns.get(k, True):
                continue
            if self._grid and k != "fname":
                continue
            yield v

    def _split_ls_line(self, s: str) -> tuple[str, ...]:
        splitted = self.SPLIT_REGEX.split(s, self._get_split_limit())
        pairs = [iter(splitted)] * 2
        for value in zip(*pairs, strict=False):
            yield "".join(value)  # value ex.: (' ', '461')
        yield splitted[-1]

    def _print_grid(self, buf: list[tuple[str, int]], max_len: int):
        terminal_width = pt.get_terminal_width(pad=len(self.OUT_COL_SEPARATOR))
        max_len = min(max_len, terminal_width)
        if self._grid == 2:
            max_len = min(max_len, (terminal_width // 2**1) - 1)
        if self._grid == 3:
            max_len = min(max_len, (terminal_width // 2**2) - 1)
        if self._grid == 4:
            max_len = min(max_len, (terminal_width // 2**3) - 1)
        columns_amount = max(1, terminal_width // (max_len + len(self.OUT_COL_SEPARATOR)))
        rows_amount = ceil(len(buf) / columns_amount)
        get_logger().debug(format_attrs({
            'max_len': max_len,
            'columns_amount': columns_amount,
            'rows_amount': rows_amount,
        }))

        rows = []
        cursor = 0
        while len(buf):
            fname, flen = buf.pop(0)
            if flen < max_len:
                fname += " " * (max_len - flen) + self.OUT_COL_SEPARATOR
            else:
                fname = fname[:max_len-1]+'…'
            if len(rows) < rows_amount:
                rows.append(fname)
            else:
                rows[cursor] += fname
                cursor += 1
                if cursor >= rows_amount:
                    cursor = 0

        stdout = get_stdout()
        while len(rows):
            stdout.echo(rows.pop(0))


class _Styles(BaseStyles):
    @staticmethod
    def _make_rwx(r: pt.FT, w: pt.FT, x: pt.FT, base: FrozenStyle = pt.NOOP_STYLE) -> t.Dict:
        return {k: FrozenStyle(base, fg=v) for k, v in dict(r=r, w=w, x=x).items()}

    INACTIVE = BaseStyles.TEXT_LABEL
    INACTIVE_ATTR = BaseStyles.TEXT_DISABLED
    INODE = [
        FrozenStyle(fg=pt.cv.BLUE),
        FrozenStyle(fg=pt.cv.BLUE, dim=True),
        FrozenStyle(fg=pt.cv.BLUE),
    ]
    OCTAL_PERMS = FrozenStyle(fg=pt.cv.MAGENTA, bold=True)
    OCTAL_PERMS_SPECIAL = FrozenStyle(fg=pt.cv.MAGENTA)
    HARD_LINKS_DIR = INACTIVE
    HARD_LINKS_FILE = FrozenStyle(fg=pt.cv.RED, bold=True)
    HARD_LINKS_FILE_GT1 = FrozenStyle(fg=pt.cv.YELLOW, bg=pt.cv.DARK_RED_2, bold=True)
    SPECIAL_ATTR_STICKY = FrozenStyle(fg=pt.Color256.get_by_code(68), bg=pt.cv.BLACK)
    SPECIAL_ATTR_SETID = FrozenStyle(fg=pt.Color256.get_by_code(74), bg=pt.cv.BLACK, bold=True)
    # INACTIVE_SPECIAL_ATTR = FrozenStyle(fg=pt.Color256.get_by_code(62))
    EXTENDED_ATTR = FrozenStyle(fg="true-white")
    OWNER_COLOR_ROOT = pt.cv.HI_RED
    OWNER_COLOR_CURUSER = pt.NOOP_COLOR
    OWNER_COLOR_OTHER = pt.Color256.get_by_code(187)  # not current and not root
    RWX_DIR_OTHERS_WRITABLE = FrozenStyle(fg=pt.cv.DARK_GOLDENROD, bg=pt.cv.BLACK)
    RWX_MAP_RGB = {
        "user": _make_rwx("hi-red kalm", "yellow kalm", "hi-yellow kalm", FrozenStyle(bold=True)),
        "group": _make_rwx(0x794544, 0x79513D, 0x8D7951),
        "others": _make_rwx(0x5F4A49, 0x635149, 0x625E56),
        "dir_others_writable": RWX_DIR_OTHERS_WRITABLE,
    }
    RWX_MAP_256 = {
        "user": _make_rwx(
            pt.cv.INDIAN_RED_3,
            pt.cv.LIGHT_SALMON_2,
            pt.cv.LIGHT_GOLDENROD_5,
            FrozenStyle(bold=True),
        ),
        "group": _make_rwx(
            pt.cv.LIGHT_PINK_1, pt.cv.NAVAJO_WHITE_1, pt.cv.WHEAT_1, FrozenStyle(dim=True)
        ),
        "others": _make_rwx(pt.cv.GRAY_30, pt.cv.GRAY_35, pt.cv.GRAY_42),
        "dir_others_writable": RWX_DIR_OTHERS_WRITABLE,
    }
    RWX_MAP_16 = {
        "user": _make_rwx(pt.cv.HI_RED, pt.cv.YELLOW, pt.cv.HI_YELLOW, FrozenStyle(bold=True)),
        "group": _make_rwx(pt.cv.HI_RED, pt.cv.YELLOW, pt.cv.HI_YELLOW, FrozenStyle(dim=True)),
        "others": _make_rwx(pt.cv.WHITE, pt.cv.GRAY, pt.cv.GRAY),
        "dir_others_writable": pt.cv.YELLOW,
    }

    @staticmethod
    def get_rwx_map():
        if isinstance((stdout := get_stdout()).renderer, pt.SgrRenderer):
            if isinstance((upper_bound := stdout.renderer._color_upper_bound), pt.Color256):
                return _Styles.RWX_MAP_256
            elif isinstance(upper_bound, pt.ColorRGB):
                return _Styles.RWX_MAP_RGB
        return _Styles.RWX_MAP_16


_highligher = pt.Highlighter(dim_units=False)


@dataclass
class File(IFile):
    NO_SIZE_PERM_REGEX = re.compile(R"^d")
    UNKNOWN_SIZE_PERM_REGEX = re.compile(R"^l")
    INACTIVE_ATTR_REGEX = re.compile(R"([-?]+)")
    FILE_CLASS_REGEX = re.compile(R"([*/=>@|]?)$")  # there will be \e[m or \e]K
    SGR_SEQ_REGEX = re.compile(R"(\x1b)(\[)([0-9;]*)(m)")

    def __post_init__(self):
        self._inactive_attr_replace = get_stdout().render(R"\1", _Styles.INACTIVE)

        self.name_prefix = ""
        self.name += self.name_extra
        self.name_extra = ""

        if cls_match := self.FILE_CLASS_REGEX.search(self.name):
            self.cls_char = cls_match.group(1) or " "
            self.name = self.name.removesuffix(self.cls_char)

        match self.cls_char:
            case "/":
                self.is_dir = True
            case "*":
                self.is_exec = True

        match self.perm[0]:
            case "l":
                self.is_link = True
            case "c":
                self.is_char = True
            case "b":
                self.is_block = True
            case "s":
                self.is_socket = True
            case "p":
                self.is_pipe = True

    def render(
        self,
        custom_columns: dict,
        icon_renderer: IFileIconRenderer,
        rwx_map: dict[str, dict[str, pt.FT]],
        grid: bool,
    ) -> OrderedDict:
        stdout = get_stdout()
        filefmt: str = ""

        def found(sgrm: re.Match):
            # to correctly process lines like: 4-Oct␣14:00␣⢸θ⡇⢸ǝF66⡇.aptitude⢸θ⡇/↵
            # adding resetter 0m to fmt will make it useless, so omit it
            nonlocal filefmt
            if sgrm.group(3) in ["", "0"] and len(filefmt) > 0:
                return ""
            filefmt += sgrm.group()
            return ""

        if stdout.renderer.is_format_allowed:
            # extract existing SGRs (from ls) and reapply them to bigger set of fields
            self.name = pt.SGR_SEQ_REGEX.sub(found, self.name)
            if name_prefix := re.match(r"^\s+", self.name):
                self.name_prefix = name_prefix.group()
                self.name = self.name[len(self.name_prefix) :]
            if self.name.startswith(".") and self.is_dir:
                filefmt += pt.SeqIndex.DIM.assemble()
            if self.is_exec:
                filefmt += pt.SeqIndex.ITALIC.assemble()

        classfmt_resetters = pt.SeqIndex.BG_COLOR_OFF + pt.SeqIndex.ITALIC_OFF
        if pt.contains_sgr(filefmt, pt.SeqIndex.BLACK.params[0]):
            classfmt_resetters += pt.SeqIndex.COLOR_OFF
        classfmt = filefmt + classfmt_resetters.assemble()

        iconfmt_resetters = pt.SeqIndex.ITALIC_OFF
        iconfmt = filefmt + iconfmt_resetters.assemble()

        # if not pt.contains_sgr(filefmt, 39):
        #     filefmt = pt.NOOP_SEQ.assemble()

        self.perm = self.perm.lstrip(" ")
        if self.perm.endswith("+"):
            self.is_special = True
            self.perm = self.perm[:-1]

        perm_render, perm_raw = self._render_perm(rwx_map)

        if perm_raw.count("?") > 3:
            self.is_invalid = True
            if perm_raw.count("?") >= 10:  # :nu_ebana:
                self.is_special = True
                perm_raw = re.sub(R"(\?{9})\?", R"\1", perm_raw)  # (」°ロ°)」
                self.hlinks = " " + self.hlinks
            perm_raw = re.sub(R"\S", "?", perm_raw)  # X_X
            perm_render = stdout.render(perm_raw, _Styles.INACTIVE_ATTR)

        if not custom_columns.get("octperms", False):
            perm_render = " " + perm_render

        return OrderedDict(
            inode="".join(reversed([*self._render_inode(custom_columns.get("inode", False))])),
            octperms=self._render_oct_perm(perm_raw),
            perms=perm_render,
            hlinks=self._render_hlinks(),
            owner=self._render_user(self.owner),
            group=self._render_group(self.group),
            size=self._render_size(),
            date=self._render_datetime(),
            fclass=(classfmt + self._render_class() + SGR_RESET),
            fname=(
                iconfmt
                + icon_renderer.render(self)
                + SGR_RESET
                + filefmt
                + self._render_name(filefmt, grid)
                + SGR_RESET
                + pt.make_clear_line_after_cursor().assemble()
            ),
        )

    def _render_inode(self, show: bool) -> Iterable[str]:
        if not show:
            return
        inode = self.inode
        sts = copy(_Styles.INODE)
        while len(inode) and len(sts):
            st = sts.pop(0)
            yield get_stdout().render(inode[-3:], st)
            inode = inode[:-3]
        if len(inode):
            yield inode

    def _render_oct_perm(self, perm_raw: str) -> str:
        if self.is_invalid:
            return " ???"

        def get_st(v: int, pos: int) -> FrozenStyle:
            if pos > 0 or v > 0:
                if pos == 0:
                    return _Styles.OCTAL_PERMS_SPECIAL
                return _Styles.OCTAL_PERMS
            return _Styles.TEXT_DISABLED

        perms = pt.Text()
        for n in range(3):
            ppart = perm_raw[n * 3 : (n + 1) * 3]
            ppart_int = 0
            for idx, val in enumerate([4, 2, 1]):
                if ppart[idx].islower():
                    ppart_int += val
            perms.append(pt.Fragment(str(ppart_int), get_st(ppart_int, n + 1)))

        specials = perm_raw[2] + perm_raw[5] + perm_raw[8]
        spart_int = 0
        for idx, val in enumerate([4, 2, 1]):
            if specials[idx].lower() in ("s", "t"):
                spart_int += val
        perms.prepend(pt.Fragment(str(spart_int or " "), get_st(spart_int, 0)))

        return get_stdout().render(perms)

    def _render_perm(self, rwx_map: dict[str, dict[str, pt.FT]]) -> tuple[str, str]:
        raw = self.perm[1:]
        if self.is_special:
            raw += "+"
        else:
            raw += " "

        result = pt.Text()
        for idx, c in enumerate(raw):
            result += pt.Fragment(*self._render_perm_chars(idx, c, rwx_map))
        return get_stdout().render(result), result.render(pt.renderer.NoOpRenderer)

    def _render_perm_chars(
        self, idx: int, c: str, rwx_map: dict[str, dict[str, pt.FT]]
    ) -> tuple[str, pt.FT]:
        if idx < 3:
            rwx_set = rwx_map.get("user")
        elif idx < 6:
            rwx_set = rwx_map.get("group")
        else:
            rwx_set = rwx_map.get("others")

        if idx >= 6 and self.is_dir and not self.is_link and c == "w":
            return c, rwx_map.get("dir_others_writable")

        match c:
            case "+":
                return c, _Styles.EXTENDED_ATTR
            case "-":
                return c, _Styles.INACTIVE_ATTR
            case "s" | "S":
                if self.is_dir:
                    return c, _Styles.TEXT_DEFAULT
                return c, _Styles.SPECIAL_ATTR_SETID
            case "t" | "T":
                if not self.is_dir:
                    return c, _Styles.TEXT_DEFAULT
                return c, _Styles.SPECIAL_ATTR_STICKY
            case "r" | "w" | "x":
                return c, rwx_set.get(c)
            case " ":  # padding
                return c, pt.NOOP_STYLE
            case _:  # unknown
                return c, _Styles.CRITICAL_ACCENT

    def _render_group(self, group: str) -> str:
        default = self._render_user(group)
        if self.is_invalid:
            return default
        return get_stdout().render(default, FrozenStyle(dim=True))

    def _render_user(self, user: str) -> str:
        if self.is_invalid:
            return get_stdout().render(
                "?".rjust(len(user) - 1),
                _Styles.INACTIVE,
            )
        owner = user.removeprefix(" ")
        if owner.strip() in ("root", "0"):
            st = _Styles.OWNER_COLOR_ROOT
        elif owner.strip() in (get_cur_user(), str(os.getuid())):
            st = _Styles.OWNER_COLOR_CURUSER
        else:
            st = _Styles.OWNER_COLOR_OTHER

        return get_stdout().render(owner, st)

    def _render_hlinks(self) -> str:
        if self.is_invalid:
            return "?".rjust(len(self.hlinks))

        hlinks_raw = self.hlinks
        if self.is_special:
            hlinks_raw = " " + hlinks_raw

        hlinks_style = _Styles.INACTIVE
        if not self.is_dir:
            hlinks_style = _Styles.HARD_LINKS_FILE
            if int(self.hlinks) > 1:
                hlinks_style = _Styles.HARD_LINKS_FILE_GT1
        return get_stdout().render(f"{hlinks_raw}", hlinks_style)

    def _render_size(self) -> str:
        def get_inactive_label() -> str | None:
            if self.is_invalid:
                return "?"
            if self.UNKNOWN_SIZE_PERM_REGEX.match(self.perm):
                return "?"
            if self.NO_SIZE_PERM_REGEX.match(self.perm):
                return "-"

        if inactive_label := get_inactive_label():
            return get_stdout().render(inactive_label.rjust(len(self.size)), _Styles.INACTIVE)
        return get_stdout().render(_highligher.colorize(self.size))

    def _render_datetime(self) -> str:
        if self.is_invalid:
            return "?".rjust(13)

        filedt = datetime.fromtimestamp(int(self.timestamp))
        diff = datetime.now() - filedt

        datefmt = pt.NOOP_SEQ
        if get_stdout().renderer.is_format_allowed:
            datefmt = self._get_date_format(diff)

        if diff.days >= 180:
            filedt_str = filedt.strftime(" %e %b  %Y")
        else:
            filedt_str = filedt.strftime(" %e %b %R")
        return f"{datefmt}{filedt_str}{pt.ansi.get_closing_seq(datefmt)}"

    def _render_class(self) -> str:
        if self.is_block:
            return "+"
        if self.is_char:
            return "-"
        if self.is_link:
            return "~" if self.is_dir else "@"
        if self.is_socket:
            return "="
        if self.is_pipe:
            return "|"
        return self.cls_char

    def _render_name(self, filefmt: str, grid: bool) -> str:
        if self.is_link:
            if grid:
                self.name = self.name.split(" -> ")[0]
            else:
                self.name = self.name.replace(" -> ", SGR_RESET + " → " + filefmt)
        return self.name_prefix + self.name

    def _auto_apply_inactive_style(self, string: str) -> str:
        return re.sub(self.INACTIVE_ATTR_REGEX, self._inactive_attr_replace, string)

    @staticmethod
    def _get_date_format(diff: timedelta) -> pt.SequenceSGR:
        if diff < timedelta(hours=1):
            code = 231  # true white
        elif diff < timedelta(days=7):
            code = 254  # 89% gray
        elif diff < timedelta(days=30):
            code = 253 - (3 * diff.days // (30 - 7))  # 253-250 (85-74%)
        elif diff < timedelta(days=365 * 12):
            code = 249 - (diff.days // 365)  # 249-237 (70-23%)
        else:
            code = 237  # 23% gray
        return pt.make_color_256(code)
