import re
from datetime import datetime

import pytermor as pt
from pytermor import RT

from es7s.commons import NamedGroupsRefilter
from .styles import FrozenStyle, Styles as BaseStyles


class _Styles(BaseStyles):
    REC_NO_FMT = FrozenStyle(fg=pt.cv.GREEN)
    REC_NO_SEP_FMT = FrozenStyle(fg=pt.cv.CYAN)
    COORD_ROW = FrozenStyle(fg=pt.cv.YELLOW)
    COORD_ROW_UPDATED = FrozenStyle(fg=pt.cv.HI_YELLOW, bold=True)
    COORD_COL = FrozenStyle(fg=pt.cv.BLUE)
    SEQ_DESC = BaseStyles.TEXT_LABEL
    WHITESPACE = FrozenStyle(fg=pt.cv.HI_CYAN, overlined=True)
    CONTROL_CHAR = FrozenStyle(fg=pt.cv.HI_RED, overlined=True)
    STR_LENGTH = BaseStyles.TEXT_DEFAULT
    ZERO_LENGTH_STR = FrozenStyle(fg=pt.cv.HI_RED)
    CC_LENGTH = BaseStyles.TEXT_ACCENT
    ESQ_LENGTH = FrozenStyle(fg=pt.cvr.ICATHIAN_YELLOW)


CONTROL_CHARS_EXCL_ESC = {*map(chr, (set(pt.CONTROL_CHARS) - {0x1B}))}
WHITESPACES = {"\x09", "\x0a", "\x0b", "\x0c", "\x0d", "\x20"}


class NonPrintablesRemover(pt.StringReplacer):
    def __init__(self):
        super().__init__(
            re.compile("[" + "".join([*WHITESPACES, *CONTROL_CHARS_EXCL_ESC]) + "]+"), ""
        )


class NonPrintablesVisualizer(NamedGroupsRefilter):
    TRANSLATION_MAP = {
        "\x09": "⇥",
        "\x0A": "↵",
        "\x0B": "⤓",
        "\x0C": "↡",
        "\x0D": "⇤",
        "\x20": "␣",
        **{k: "!" for k in CONTROL_CHARS_EXCL_ESC},
    }

    def __init__(self):
        ws_grp = "(?P<ws>[" + "".join(WHITESPACES) + "])"
        cc_grp = "(?P<cc>[" + "".join(CONTROL_CHARS_EXCL_ESC) + "])"
        super().__init__(re.compile(ws_grp + "|" + cc_grp),  {
            "ws": _Styles.WHITESPACE,
            "cc": _Styles.CONTROL_CHAR,
        })



class IoDebugger:
    SEQ_REPR = {
        "<CSI[25?l]>": "CSI :: Hide cursor",
        "<CSI[25?h]>": "CSI :: Show cursor",
        "<CSI[47?l]>": "CSI :: Restore screen",
        "<CSI[47?h]>": "CSI :: Save screen",
        "<CSI[1049?l]>": "CSI :: Disable alt screen buffer",
        "<CSI[1049?h]>": "CSI :: Enable alt screen buffer",
    }
    SEQ_ABBR = {
        "SGR": "Select Graphic Rendition",
        "CSI": "Control Sequence Introducer",
        "OSC": "Operating System Command",
        "CUP": "Cursor Position",
        "CUU": "Cursor Up",
        "CUD": "Cursor Down",
        "CUB": "Cursor Back",
        "CUF": "Cursor Forward",
        "CPL": "Cursor Previous Line",
        "CNL": "Cursor Next Line",
        "VPA": "Vertical Position Absolute",
        "CHA": "Cursor Character Absolute",
        "QCP": "Query Cursor Position",
        "ED": "Erase in Display",
        "EL": "Erase in Line",
        "DECSC": "Save cursor position",
        "DECRC": "Restore cursor position",
    }

    def __init__(self, io):
        self._io = io
        self._recnum = 0
        self._renderer = pt.SgrRenderer(pt.OutputMode.XTERM_256)
        self._filters = [
            NonPrintablesVisualizer(),
        ]
        self._formatter = StrlenFormatter()
        self._prev_pos_y = 0

        self._output = open("/tmp/es7s-" + re.sub(r"\W+", "", self._io.name), "at")
        self._output.write(
            "\n" + ("-" * 80) + "\n" + datetime.now().strftime("%c") + "\n" + ("-" * 80) + "\n"
        )
        self._output.flush()

    def mirror_echo(self, string: str | pt.ISequence, nl: bool):
        if self._output.closed:
            return

        self._recnum += 1
        self._write_rendered(
            pt.Fragment(str(self._recnum).rjust(3), _Styles.REC_NO_FMT)
            + pt.Fragment("│", _Styles.REC_NO_SEP_FMT),
        )

        pos_y, pos_x = self._get_tty_cursor_position()
        if pos_x and pos_y:
            row_st = _Styles.COORD_ROW if self._prev_pos_y == pos_y else _Styles.COORD_ROW_UPDATED
            self._write_rendered(
                pt.Fragment(f"{pos_y:>2d}", row_st)
                + pt.Fragment(f":{pos_x:<3d}", _Styles.COORD_COL)
            )
            self._prev_pos_y = pos_y
        else:
            self._write_rendered(":", _Styles.COORD_COL)
        self._write_rendered("│", _Styles.COORD_COL)

        if isinstance(string, str):
            string += "\n" if nl else ""

            st = _Styles.STR_LENGTH
            if len(string) == 0:
                st = _Styles.ZERO_LENGTH_STR

            no_esq_len = len(pt.apply_filters(string, pt.EscSeqStringReplacer("")))

            self._write_rendered(f"{self._formatter.format(no_esq_len):>3s}", st)
            if len(string) != no_esq_len:
                self._write_rendered('+'+self._formatter.format(len(string) - no_esq_len).ljust(3), _Styles.CC_LENGTH)
            else:
                self._write_rendered(' 0  ', BaseStyles.TEXT_DISABLED)
            self._write_rendered("│", st)

            self._output.write(pt.apply_filters(string, *self._filters))

        else:
            self._write_rendered('  0 ', BaseStyles.TEXT_DISABLED)
            esq_len = len(string.assemble())
            esq_len_fmtd = self._formatter.format(esq_len)
            self._write_rendered(esq_len_fmtd, _Styles.ESQ_LENGTH)
            self._output.write(pt.pad(3-len(esq_len_fmtd)))

            self._write_rendered(pt.Fragment('│', pt.NOOP_STYLE))
            self._output.write(self._render_esq_seq(string))
            self._write_rendered(pt.Fragment(" " + self._describe_seq(string), _Styles.SEQ_DESC))
        self._output.write("\n")
        self._output.flush()

    def destroy(self):
        if not self._output.closed:
            self._output.write(("-" * 80) + "\n")
            self._output.flush()
            self._output.close()

    def _render_esq_seq(self, seq: pt.ISequence) -> str:
        return pt.apply_filters(
            repr(seq).strip("<>")+" ",
            NamedGroupsRefilter(
                re.compile(r'(?P<abbr>\w+)(\[)(?P<param>\d*)(?P<var>\w*)(\])'), {
                    'abbr': pt.cvr.ICATHIAN_YELLOW,
                    'param': pt.cv.HI_RED,
                    'var': pt.cv.HI_YELLOW,
                }
            )
       )

    def _describe_seq(self, seq: pt.ISequence) -> str:
        if desc := self.SEQ_REPR.get(repr(seq), None):
            return desc
        if desc := self.SEQ_ABBR.get(seq._abbr, None):
            return desc
        return ""

    def _write_rendered(self, *args, **kwargs):
        self._output.write(pt.render(*args, renderer=self._renderer, **kwargs))

    def _get_tty_cursor_position(self):
        #return 0, 0
        self._io.write(pt.make_query_cursor_position().assemble())
        self._io.write("\r")

        response = ""
        while (pos := pt.decompose_report_cursor_position(response)) is None:
            response += pt.wait_key(block=True) or ""

        pos_y, pos_x = pos
        self._io.write(pt.make_set_cursor_column(pos_x).assemble())
        return pos_y, pos_x


class StrlenFormatter(pt.NumFormatter):
    """
    3-length output formatter
    """

    def __init__(self):
        super().__init__(auto_color=False, highlighter=pt.Highlighter())

    def format(self, val: float, auto_color: bool = False) -> RT:
        if val < 1000:
            return str(val)
        if val < 100_000:
            return str(round(val / 1e3)) + "k"
        if val < 1_000_000:
            return "{:.1f}".format(round(val / 1e6))[:-2] + "M"
        return "1M+"
