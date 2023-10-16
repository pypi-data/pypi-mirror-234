# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import sys
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from collections.abc import Iterable
from dataclasses import dataclass
from shutil import get_terminal_size
from typing import TextIO

import click
import pytermor as pt
from pytermor import NOOP_STYLE

from es7s.shared import FrozenStyle, Styles as BaseStyles, get_logger, get_stdout
from es7s.commons import GimpGradientReader, GradientPoint
from .._base_opts_params import CMDTRAIT_ADAPTIVE, IntRange
from .._decorators import catch_and_log_and_exit, cli_argument, cli_command, cli_option
from ..demo import DemoGradients


class _Styles(BaseStyles):
    BORDER = pt.cv.GRAY_70

    FMT_SCALE = FrozenStyle(fg=BORDER)
    FMT_SCALE_MARK = FrozenStyle(fg=pt.cv.HI_WHITE)


SCALE_MARK_MID_PT = "△"
SCALE_MARK_EDGE_PT = "▲"
SCALE_LEFT_FMTD = pt.Fragment(" ▕", _Styles.FMT_SCALE_MARK)
SCALE_RIGHT_FMTD = pt.Fragment("▏ ", _Styles.FMT_SCALE_MARK)

MAIN_PAD = 2


ScaleMarksMap = OrderedDict[float, tuple[GradientPoint, bool]]


class IDetailsRenderer(metaclass=ABCMeta):
    DEBUG_FILTERS = [
        # NamedGroupStyler(re.compile(r"([^╎·]+)"), FrozenStyle(bg=pt.cvr.DARK_MIDNIGHT_BLUE), ""),
        # NamedGroupStyler(re.compile(r"(╎)$"), FrozenStyle(fg=pt.cvr.BLOOD_ORANGE), ""),
        # NamedGroupStyler(re.compile(r"(·+)"), _Styles.DEBUG, ""),
    ]

    def __init__(self, details: int, width: int) -> None:
        super().__init__()
        self._details = details
        self._width = width

    def _get_details(self, gp: GradientPoint):
        return [
            pt.format_auto_float(100 * gp.pos, 4, False).strip() + "%",
            "#{:06x}".format(gp.col.int),
            ",".join(map(str, (gp.col.red, gp.col.blue, gp.col.green))),
        ][: self._details]

    def _get_align_fn(self, gp_pos: float) -> callable:
        if gp_pos < 0.33:
            return str.ljust
        elif gp_pos < 0.66:
            return str.center
        return str.rjust

    @abstractmethod
    def render(self, scale_marks_map: ScaleMarksMap):
        ...


@cli_command(
    __file__,
    short_help="Launch a demonstration of Gradient component.",
    traits=[CMDTRAIT_ADAPTIVE],
)
@cli_argument("file", type=click.File(mode="r"), nargs=-1, required=False)
@cli_option(
    "-h",
    "--height",
    type=IntRange(1, max_open=True, show_range=False),
    default=1,
    show_default=True,
    help="Gradient scale height in characters.",
)
@cli_option(
    "-x",
    "--extend",
    type=IntRange(0, 3, clamp=True, show_range=False),
    default=0,
    count=True,
    help="Display detailed info about gradient segments. Can be used multiple times to increase "
    "the details amount even further ('-xx', '-xxx').",
)
@cli_option(
    "-d",
    "--demo",
    is_flag=True,
    default=False,
    help="Discard all FILEs and display a few library presets instead.",
)
@catch_and_log_and_exit
class invoker:
    """
    Read data from given FILE, build and display a gradient based on it. The only supported format is
    GIMP gradient (**.ggr*). If FILE is omitted or equals to ''-'', read standard input instead.
    Multiple FILEs supported.
    """

    def __init__(
        self,
        height: int,
        extend: int,
        demo: bool,
        file: tuple[TextIO, ...] | None,
        **kwargs,
    ):
        if file is None:
            file = click.open_file("-", "r")

        self._scale_height = height
        self._extend = extend

        if demo:
            file = [*DemoGradients.iter()]
        elif not file:
            file = [*file, sys.stdin]

        for f in file:
            if f.seekable():
                f.seek(0)
            data = f.readlines()

            self._width = pt.get_terminal_width(pad=MAIN_PAD * 2)
            _, self._height = get_terminal_size()
            self._details_renderer: IDetailsRenderer = self._get_details_renderer()

            try:
                reader = GimpGradientReader()
                self._gradient = reader.make(data)
                self._run()
            except RuntimeError as e:
                get_logger().exception(e)

    def _run(self):
        stdout = get_stdout()
        stdout.echo_rendered(" " + self._gradient._name, _Styles.TEXT_SUBTITLE)

        scale_frags = self._format_scale()
        scale = pt.FrozenText(*scale_frags)
        self._render_scale(scale)

        scale_marks_map = self._build_scale_marks_map()
        self._render_marks(scale_marks_map)

        if not self._details_renderer:
            return
        self._details_renderer.render(scale_marks_map)

    def _format_scale(self) -> Iterable[pt.Fragment]:
        result_frag = []
        for idx, c in enumerate(range(self._width)):
            pos_rel = c / self._width
            col = self._gradient.interpolate(pos_rel)
            result_frag.append(
                pt.Fragment(" ", FrozenStyle(fg="gray70", bg=col))
            )
        return result_frag

    def _get_overline_ctl_frag(self, base: pt.Style = NOOP_STYLE, open: bool = True) -> pt.Fragment:
        st = FrozenStyle(base, overlined=True)
        if open:
            return pt.Fragment("", st, close_this=False)
        else:
            return pt.Fragment("", st, close_prev=True)

    def _render_scale(self, scale: pt.FrozenText):
        stdout = get_stdout()

        for h in range(self._scale_height):
            result = scale
            if h == 0:
                result = pt.FrozenText(
                    self._get_overline_ctl_frag(open=True),
                    *scale.as_fragments(),
                    self._get_overline_ctl_frag(open=False),
                )
            result_fmtd = (
                stdout.render(SCALE_LEFT_FMTD)
                + stdout.render(result)
                + stdout.render(SCALE_RIGHT_FMTD)
            )
            stdout.echo(result_fmtd)

    def _build_scale_marks_map(self) -> ScaleMarksMap:
        width_gp = self._width + 1
        scale_marks_map: ScaleMarksMap = OrderedDict()
        for seg in self._gradient._segments:
            for gp in [seg.p_left, seg.p_mid, seg.p_right]:
                scale_marks_map.update(
                    {
                        1 + round(width_gp * gp.pos): (gp, gp is not seg.p_mid),
                    }
                )
        return scale_marks_map

    def _render_marks(self, scale_marks_map: ScaleMarksMap):
        cursor = 0
        marks = pt.Text()
        scale_left_pos = min(scale_marks_map.keys())
        scale_right_pos = max(scale_marks_map.keys())
        for (pos, (gp, is_edge)) in scale_marks_map.items():
            if pos > cursor:
                margin = (pos - cursor) * " "
                frag = pt.Fragment(margin, _Styles.FMT_SCALE)
                marks += frag
                cursor = pos
            if not gp.col:
                continue
            mark = SCALE_MARK_EDGE_PT if is_edge else SCALE_MARK_MID_PT
            if pos == scale_right_pos:
                marks += self._get_overline_ctl_frag(_Styles.FMT_SCALE_MARK, open=False)
            marks += pt.Fragment(mark, _Styles.FMT_SCALE_MARK)
            if pos == scale_left_pos:
                marks += self._get_overline_ctl_frag(_Styles.FMT_SCALE_MARK, open=True)
            cursor += len(mark)
        get_stdout().echo_rendered(marks)

    def _get_details_renderer(self) -> IDetailsRenderer | None:
        if self._extend > 0:
            return PrecalcDetailsRenderer(self._extend, self._width)
        return None


class PrecalcDetailsRenderer(IDetailsRenderer):
    def __init__(self, details: int, width: int):
        super().__init__(details, width)
        self._occmap = PrecalcOccupancyMap()
        self._prev_y = 0

    def render(self, scale_marks_map: ScaleMarksMap):
        stdout = get_stdout()

        edge_marks_map = {k: v for k, v in scale_marks_map.items() if v[1]}
        mid_marks_map = {k: v for k, v in scale_marks_map.items() if not v[1]}

        max_y = 1

        for (xpos_chr, (gp, is_edge)) in [*edge_marks_map.items(), *mid_marks_map.items()]:
            cur_y = 1
            strings: list[PrecalcText] = []

            for string_text in self._get_details(gp):
                xleft = xpos_chr - round((len(string_text) - 1) * gp.pos)
                xright = xleft + len(string_text)
                strings.append(PrecalcText(xleft, xright, string_text))

            while True:
                fits = 0
                for idx, pct in enumerate(strings):
                    if not self._occmap.is_occupied(cur_y + idx, pct.xleft, pct.xright):
                        fits += 1
                        continue
                    break

                if fits == len(strings):
                    for y in range(cur_y + len(strings)):
                        self._set_cursor(y, xpos_chr)
                    stdout.echo_rendered("@", FrozenStyle(fg="gray30"), nl=False)

                    for idx, pct in enumerate(strings):
                        self._occmap.occupy(cur_y + idx, pct)
                    break
                cur_y += 1
                while cur_y > max_y:
                    stdout.echo("")
                    max_y += 1

                if is_edge:
                    continue
                break

        for y, row in self._occmap:
            for pct in row:
                self._set_cursor(y, pct.xleft)
                stdout.echo(pct.text, nl=False)

    def _set_cursor(self, y: int, x: int):
        if self._prev_y is not None:
            diff = abs(y - self._prev_y)
            if y < self._prev_y:
                get_stdout().echo(pt.make_move_cursor_up(diff))
            elif y > self._prev_y:
                get_stdout().echo(pt.make_move_cursor_down(diff))
        self._prev_y = y

        get_stdout().echo(pt.make_set_cursor_column(x))


@dataclass(frozen=True)
class PrecalcText:
    xleft: int
    xright: int
    text: str


class PrecalcOccupancyMap:
    def __init__(self):
        self._data: OrderedDict[int, list[PrecalcText]] = OrderedDict()
        # {y: [(xl, xr, text), ...], ... }

    def is_occupied(self, y: int, out_xleft: int, out_xright: int) -> bool:
        self._ensure_row(y)
        if not (row := self._data.get(y, None)):
            return False

        for ins in row:
            # --------------------------------------------------------------
            #  CASES      inside element       outside element
            #            [!!!!!!!!!!!!!!!]  [@@@@@@@@@@@@@@@@@@@@]
            #            iL             iR  oL                  oR
            #
            # [1]-----------[2]-----------[3]-----------[4]-------------+
            # |   I << O    |   I <x O    |   I x> O    |    I >> O     |
            # |=============|=============|=============|===============|
            # |!!!!!        |!!!!!!!!     |     !!!!!!!!|         !!!!!!|
            # |       @@@@@@|     @@@@@@@@|@@@@@@@      |@@@@@@         |
            # |-------------|-------------|-------------|---------------|
            # | iL<iR<oL<oR | iL<oL<iR<oR | oL<iL<oR<iR |  oL<oR<iL<iR  |
            # +-------------+-------------+-------------+---------------+
            #

            case2 = ins.xleft < out_xleft <= ins.xright < out_xright
            case3 = out_xleft < ins.xleft <= out_xright < ins.xright
            if case2 or case3:
                return True

        return False

    def occupy(self, y: int, pct: PrecalcText):
        self._ensure_row(y)
        self._data.get(y).append(pct)

    def _ensure_row(self, y: int):
        if y not in self._data.keys():
            self._data.update({y: []})

    def __iter__(self) -> Iterable[tuple[int, list[PrecalcText]]]:
        for y in sorted(self._data.keys()):
            yield y, sorted(self._data.get(y), key=lambda pct: pct.xleft)


class RealTimeDetailsRenderer(IDetailsRenderer):
    def render(self, scale_marks_map: ScaleMarksMap):
        stdout = get_stdout()
        line_last_widths: dict[int, int] = dict()
        max_cursor_y = 0
        prev_cursor_y = 0
        cursor_y = 0

        def shift_cursor_y(current, target):
            delta = abs(target - current)
            if target > current:
                stdout.echo(pt.make_move_cursor_up(delta))
            else:
                stdout.echo(pt.make_move_cursor_down(delta))

        for (pos, (gp, is_edge)) in scale_marks_map.items():
            strings = self._get_details(gp)
            string_max = max(map(len, strings))
            string_num = len(strings)
            shift_x = (string_max - 1) * (-gp.pos) + 1
            fn = self._get_align_fn(gp.pos)
            strings = [fn(s, string_max) for s in strings]
            string_leftpads = [len(s) - len(s.lstrip()) for s in strings]
            pos_x_final = round(pos + shift_x)
            while True:
                fit = 0
                for idx, s in enumerate(strings):
                    if lw := line_last_widths.get(cursor_y + idx, None):
                        if lw >= pos_x_final + string_leftpads[idx]:
                            cursor_y += 1
                            break
                        else:
                            fit += 1
                    else:
                        fit += 1
                if fit != len(strings):
                    if not is_edge and cursor_y >= 3 * string_num - len(strings):
                        if len(strings) > 1:
                            strings.pop()
                            cursor_y = 0
                        else:
                            break  # по
                    continue
                for idx, s in enumerate(strings):
                    if prev_cursor_y != cursor_y:
                        shift_cursor_y(cursor_y, prev_cursor_y)
                    stdout.echo(pt.make_set_cursor_column(pos_x_final + string_leftpads[idx]))
                    stdout.echo(s.lstrip())

                    line_last_widths.update(
                        {cursor_y: pos_x_final + (len(s) - string_leftpads[idx]) + 1}
                    )
                    cursor_y += 1
                    max_cursor_y = max(max_cursor_y, cursor_y)
                    prev_cursor_y = cursor_y
                cursor_y = 0
                break
        max_cursor_y += 1
        if prev_cursor_y != max_cursor_y:
            shift_cursor_y(max_cursor_y, prev_cursor_y)
