# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import math
import re
import shutil
import typing

import pytermor as pt
from pytermor.common import ExtendedEnum

from es7s.shared import get_stdout, ThemeColor, FrozenStyle
from .._base import CliCommand
from .._base_opts_params import CMDTRAIT_ADAPTIVE, CMDTYPE_BUILTIN, IntRange, EnumChoice
from .._base_opts_params import FloatRange
from .._decorators import catch_and_log_and_exit, cli_command
from .._decorators import cli_option


class RulerType(str, ExtendedEnum):  # @TODO str enums will be available in python 3.11
    TOP = "T"
    BOTTOM = "B"
    LEFT = "L"
    RIGHT = "R"
    CENTER_HORIZONTAL = "CH"

    def __str__(self):
        return self.value

    @classmethod
    def DEFAULT(cls):
        return [cls.TOP, cls.BOTTOM, cls.LEFT, cls.RIGHT]


@cli_option(
    "-R",
    "--no-rulers",
    is_flag=True,
    default=False,
    help="Disable all rulers. If '-R' is specified, all '-r' options will be ignored.",
)
@cli_option(
    "-r",
    "--rulers",
    type=EnumChoice(RulerType, inline_choices=True),
    default=RulerType.DEFAULT(),
    show_default=True,
    multiple=True,
    metavar="TYPE",
    help="Which rulers to draw. Can be specified multiple times: '-r B -r L' "
         "will result in drawing two rulers -- bottom and left. The legend for "
         "ruler types can be found below.",
)
@cli_option(
    "-p",
    "--position",
    type=FloatRange(_min=-math.inf, _max=math.inf, min_open=True, max_open=True),
    default=0.5,
    show_default=True,
    help="Position of center horizontal line (should be enabled with '-r CH'). "
         "Can be specified as a float number from 0.0 to 1.0, in which case the "
         "value is treated like relative position to the screen height (e.g. "
         "0.25=25%), or as an integer number representing the distance from the "
         "top side of the screen (in lines) to the ruler. For negative values "
         "logic is the same, except the reference side of the screen is bottom "
         "one instead of the top.",
)
@cli_option(
    "-g",
    "--grid",
    type=IntRange(0, 3, clamp=True),
    default=2,
    show_default=True,
    help="Grid details level.",
)
@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE],
    short_help="terminal char rulers",
)
@catch_and_log_and_exit
class invoker:
    """
    Draw four rulers at the top, bottom, left and right sides of the terminal and
    additionally draw a grid with specified details level.
    """

    _SECTIONS = {
        RulerType.TOP: "ˌˌˌˌ╷ˌˌˌˌ╷",
        RulerType.BOTTOM: "''''╵''''╵",
    }
    _SECTION_MARKS = {
        RulerType.TOP: '╷',
        RulerType.BOTTOM: '╵',
    }
    _SECTION_100_MARKS = {
        RulerType.TOP: '╻',
        RulerType.BOTTOM: '╹',
    }

    def __init__(self, rulers: list[RulerType], no_rulers: bool, grid: int, **kwargs):
        self._def_fmt = FrozenStyle(fg=ThemeColor(), bg=pt.cv.GRAY_0)
        self._hl_fmt = FrozenStyle(fg=ThemeColor('theme_bright'), bg=pt.cv.GRAY_0)

        _100_col = pt.cv.YELLOW
        if self._def_fmt.fg == _100_col:
            _100_col = pt.cv.HI_YELLOW
        self._100_fmt = FrozenStyle(fg=_100_col, bg=pt.cv.GRAY_0, bold=True)

        self._terminal_width = pt.get_terminal_width(pad=0)
        self._terminal_height = shutil.get_terminal_size().lines

        self._rulers = rulers
        if no_rulers:
            self._rulers = []
        self._grid = grid
        self._run()

    def _run(self):
        stdout = get_stdout()
        if not stdout.sgr_allowed:
            stdout.echo(self._print_hruler(self._terminal_width, RulerType.TOP), nl=False)
            return

        for y in range(1, self._terminal_height+1):
            stdout.echo(pt.make_set_cursor(y, 1))
            line_num_str_left = self._get_line_num_str(y, left=True)
            line_num_str_right = self._get_line_num_str(y, left=False)

            if y == 1:
                if RulerType.TOP in self._rulers:
                    stdout.echo(self._print_hruler(self._terminal_width, RulerType.TOP, line_num_str_left), nl=False)
            elif y == self._terminal_height:
                if RulerType.BOTTOM in self._rulers:
                    stdout.echo(self._print_hruler(self._terminal_width, RulerType.BOTTOM, line_num_str_left), nl=False)
            else:
                y_100 = (y % 50 == 0)
                y_fmt = self._100_fmt if y_100 else self._hl_fmt

                if y % 5 != 0:
                    y_fmt = self._def_fmt
                    line_num_str_left = re.sub(r'\d+', lambda m: '╶'.rjust(len(m[0])), line_num_str_left)
                    line_num_str_right = re.sub(r'\d+', lambda m: '╴'.ljust(len(m[0])), line_num_str_right)

                if RulerType.LEFT in self._rulers:
                    stdout.echo_rendered(line_num_str_left, y_fmt, nl=False)
                else:
                    line_num_str_left = ""

                for x in range(len(line_num_str_left)+1, self._terminal_width+1):
                    if x == 0:
                        continue
                    if self._grid < 1:
                        continue

                    hline = (y % 5 == 0)
                    vline = (x % 10 == 0)
                    if not hline and not vline:
                        continue

                    if self._grid < 2:
                        if not hline or not vline:  # intersections only
                            continue

                    chr = '·'
                    if self._grid == 3 and (not hline or not vline):  # not intersection
                        chr = '-' if hline else '|'
                    x_fmt = self._100_fmt if (x % 100 == 0 or y_100) else self._hl_fmt
                    if x % 2 == 1 and self._grid < 3:
                        chr = ' '

                    stdout.echo(pt.make_set_cursor_column(x), nl=False)
                    stdout.echo_rendered(chr, x_fmt, nl=False)

                if RulerType.RIGHT in self._rulers:
                    stdout.echo(pt.make_set_cursor_column(self._terminal_width-len(line_num_str_right)+1))
                    stdout.echo_rendered(line_num_str_right, y_fmt, nl=False)

    def _get_line_num_str(self, line_num: int, left: bool) -> str:
        l = len(str(self._terminal_height))
        if left:
            return str(line_num).rjust(l) + '┤'
        return '├' + str(line_num).ljust(l)

    def _print_hruler(self, width: int, rtype: RulerType, line_num_str: str = None) -> str:
        if not get_stdout().sgr_allowed:
            line_num_str = None

        def _iter() -> typing.Iterable[pt.Fragment]:
            top = (rtype is RulerType.TOP)
            ow_st = FrozenStyle(overlined=not top, underlined=top)
            def_fmt = pt.merge_styles(self._def_fmt, overwrites=[ow_st])
            hl_fmt = pt.merge_styles(self._hl_fmt, overwrites=[ow_st])
            num_100_fmt = pt.merge_styles(self._100_fmt, overwrites=[ow_st])

            for s in range(width//10 + 1):
                num = (s+1)*10
                num_str = str(num)
                num_fmt = hl_fmt

                section = self._SECTIONS[rtype][:-len(num_str)-1]
                if s == 0 and line_num_str is not None:
                    yield pt.Fragment(line_num_str, self._hl_fmt)
                    yield pt.Fragment(section[len(line_num_str):], def_fmt)
                else:
                    yield pt.Fragment(section, def_fmt)

                section_mark = self._SECTION_MARKS[rtype]
                if s % 10 == 9:
                    num_fmt = num_100_fmt
                    section_mark = self._SECTION_100_MARKS[rtype]

                yield pt.Fragment(num_str, num_fmt)
                yield pt.Fragment(section_mark, num_fmt)

        result = pt.Text().append(*_iter())
        result.set_width(width)
        return pt.render(result)

# original G1 version:
# --------------------------------------------------------------------------------------------------
# ruler() {
#     # args: [force=] [no_color=]
#     # if first arg is non-empty value, displays ruler even in normal mode
#     local f_inactive="$(_cs8 $I8_GRAY)"
#     local f_active="$(_cs 4 53)"$'\e'"[${ES7S_THEME_COLOR_SGR:-34}m"
#     local f_active_hl="$(_cs 4 53 33)"
#     local width=$(_ww) shift=1
#     # shift is needed because first char should be marked as 1, not 0
#
#     local logo="${_y}es7s|${f_inactive}"
#     local sep10="╹" section="#''''╵''''"
#
#     local i begin end output label
#     local n=$((1 + width / 10))
#     for (( i=0 ; i<n ; i++ )) ; do
#         [[ $i -eq 1 ]] && { shift=0 ; logo="│$logo" ; }
#         label=$(( i * 10 ))
#         local f=$f_active
#         if [[ $((i%10)) -eq 0 ]] ; then f=$f_active_hl ; fi
#         if [[ $((i%40)) -eq 0 ]] ; then begin="$f${logo}${f_inactive}"
#                                    else begin="$f${sep10}${label}${f_inactive}$(_s 1)"
#         fi ;  if [[ $i -eq 21 ]] ; then begin="$f${sep10}$(squeeze 9 <<< "weeeeeeeeee")$f_inactive"
#             elif [[ $i -eq 40 ]] ; then begin="$f${ES7S_OVERFLOW}eeees7s${logo::1}$f_inactive"
#         fi
#         end="${section:$(( $(_ccp <<< "$begin") + shift ))}" ;
#         output+="$begin$end"
#
#         if [[ $( _ccp <<< "$output" ) -ge $width ]] ; then
#             [[ -n $no_color ]] && output="$(_dcu <<< "$output")"
#             squeeze $width <<< "$output"
#             break
#         fi
#     done
# }
