# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click
import pytermor as pt

from .._base_opts_params import CMDTRAIT_ADAPTIVE, CMDTYPE_BUILTIN
from es7s.shared import get_stdout, FrozenStyle
from .._base import CliCommand
from .._decorators import cli_pass_context, catch_and_log_and_exit, cli_command


@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE],
    short_help="python regular expressions",
)
@cli_pass_context
@catch_and_log_and_exit
class invoker:
    """
    Display python regular expressions cheatsheet.\n\n

    For best results view it on a terminal at least 180 characters wide, although
    anything down to 88 chars is good enough, too. Consider piping the output to
    a pager if width of your terminal is less than that. Use '-c' option to force
    formatting in the output, because the app disables it by default, if detects
    a pipe or redirection.
    """

    CUSTOM_STYLES = {
        "title": FrozenStyle(
            fg="true-white",
            bold=True,
            underlined=True,
            overlined=True,
        ),
        "header": FrozenStyle(fg="gray-89", bold=True),
        "t": FrozenStyle(fg="green"),
        "g": FrozenStyle(fg="hi-yellow", bold=True),
        "o": FrozenStyle(fg="light-salmon-2", bold=True),
        "i": FrozenStyle(bold=True),
        "n": FrozenStyle(fg="red"),
        "c": FrozenStyle(fg="gray_50"),
        "fn": FrozenStyle(fg="blue"),
        "fa": FrozenStyle(fg="hi-blue", bold=True),
        "url": FrozenStyle(underlined=True),
        "hl": FrozenStyle(italic=True),
        "comment": FrozenStyle(fg=pt.cv.GRAY_35),
    }
    PADDING = 4

    DATA_SEGS = [
        r"""
 :[|title]PYTHON REGULAR EXPRESSIONS:[-title]                                             :[comment]relevant for:[-comment]
 #[      ]                          #[      ]                                               :[comment]3.8 — 3.11:[-comment]
 :[header]SPECIAL CHARACTERS:[-header]
 
  :[i].:[-i]         Matches any character except a newline.
  :[o]^:[-o]         Matches start of string.
  :[o]$:[-o]         Matches end of string or just before the newline at end of string.
  :[fn]*:[-fn]         Matches 0 or more (:[hl]greedy:[-hl]) repetitions of the preceding RE.
  #[ ] #[  ]         :[hl]Greedy:[-hl] means that it will match as many repetitions as possible.
  :[fn]+:[-fn]         Matches 1 or more (:[hl]greedy:[-hl]) repetitions of the preceding RE.
  :[fn]?:[-fn]         Matches 0 or 1 (:[hl]greedy:[-hl]) of the preceding RE.
  :[|fn]*? +? ??:[-fn]  :[hl]Non-greedy:[-hl] versions of the previous three special characters.
  :[t]a:[-]:[g]{:[-]:[fn]m:[o],:[-]n:[-fn]:[g]}:[-g]    Matches from :[fn]m:[-] to :[fn]n:[-] repetitions of the :[t]a:[-].
  :[t]a:[-]:[g]{:[-]:[fn]m:[o],:[-]n:[-fn]:[g]}:[-g]:[fn]?:[-]   :[hl]Non-greedy:[-hl] version of the above.
  :[g]\:[-g]         Either escapes special characters or signals a special sequence.
  :[g][]:[-g]        Set of characters. :[t]^:[-t] as the 1st char indicates a complementing set.
  :[t]a:[o]|:[-o]b:[-t]       Creates an RE that will match either :[t]a:[-t] or :[t]b:[-t].
  :[g](:[-]:[t]abc:[-]:[g]):[-]     Matches :[t]abc:[-t]; the contents can be retrieved or matched later.
  :[g](?::[-]:[t]abc:[-]:[g]):[-]   :[hl]Non-grouping:[-hl] version of regular parentheses.
  :[c](?#abc):[-c]   A comment; ignored.
  :[g](?:[-]aiLmsux:[g]):[-]       The letters set the corresponding :[hl]flags:[-hl] defined below.
  :[g](?:[-]-imsx:[g]):[-]         The letters unset the corresponding :[hl]flags:[-hl] below. :[comment][3.11+]:[-]
  :[g](?P<:[-]name:[g]>:[-]:[t]abc:[-]:[g]):[-]    The substring matched by the group is accessible by :[i]name:[-].
  :[g](?P=:[-]name:[g]):[-]        Matches the text matched earlier by the group named :[i]name:[-].
  :[g](?(:[-]idxname::[g]):[-]:[t]y:[-]:[o]|:[-]:[t]n:[-]:[g]):[-]  Matches :[t]y:[-t] pattern if the group with :[i]idx/name:[-i] matched,
  #[ ]   #[ ]        #[ ] #[ ]#[ ] #[ ]#[ ] #[ ]#[ ] #[ ]#[ ] #[ ]  the (optional) :[t]n:[-t] pattern otherwise.
  :[g](?>:[-]:[t]abc:[-]:[g]):[-]   :[hl]Atomic group:[-hl]: fails fast, no backtracking (non-capturing). :[comment][3.11+]:[-]
  :[g](?=:[-]:[t]abc:[-]:[g]):[-]   :[hl]Positive lookahead:[-hl]: matches if :[t]abc:[-t] matches next, doesn't consume it.
  :[g](?!:[-]:[t]abc:[-]:[g]):[-]   :[hl]Negative lookahead:[-hl]: matches if :[t]abc:[-t] doesn't match next.
  :[g](?<=:[-]:[t]abc:[-]:[g]):[-]  :[hl]Positive lookbehind:[-hl]: matches if preceded by :[t]abc:[-t] (must be fixed length).
  :[g](?<!:[-]:[t]abc:[-]:[g]):[-]  :[hl]Negative lookbehind:[-hl]: matches if not preceded by :[t]abc:[-t] (must be fixed length).""",
        r"""
 :[header]SPECIAL SEQUENCES:[-header]
 
  :[i]\1 \2 …:[-i]  Matches the contents of the group with corresponding :[i]number:[-].
  :[g]\A:[-]       Matches only at the start of the string.
  :[g]\Z:[-]       Matches only at the end of the string.
  :[g]\b:[-]       Matches the empty string, but only at the start or end of a word.
  :[g]\B:[-]       Matches the empty string, but not at the start or end of a word.
  :[g]\d:[-]       Matches any decimal digit; equivalent to the set :[g][:[-]:[t]0:[o]-:[-]9:[-t]:[g]]:[-g] in
  #[ ]  #[ ]       bytes patterns or string patterns with the :[fn]ASCII:[-fn] flag.
  #[ ]  #[ ]       In string patterns without the :[fn]ASCII:[-fn] flag, it will match the whole
  #[ ]  #[ ]       range of Unicode digits.
  :[g]\D:[-]       Matches any non-digit character; equivalent to :[g][:[o]^:[-]\d]:[-g].
  :[n]\p{<L>}:[-n]  Unicode properties shortcuts (incl. :[n]\P{<L>}:[-n]). Python doesn't
  #[ ]       #[  ]  support them out-of-the-box; see :[url]https://pypi.org/project/regex/:[-url].
  :[g]\s:[-]       Matches any whitespace character; equivalent to :[g][ \t\n\r\f\v]:[-g] in
  #[ ]  #[ ]       bytes patterns or string patterns with the :[fn]ASCII:[-fn] flag.
  #[ ]  #[ ]       In string patterns without the :[fn]ASCII:[-fn] flag, it will match the whole
  #[ ]  #[ ]       range of Unicode whitespace characters.
  :[g]\S:[-]       Matches any non-whitespace character; equivalent to :[g][:[o]^:[-]\s]:[-g].
  :[g]\w:[-]       Matches any alphanumeric character; equivalent to :[g][:[-]:[t]a:[o]-:[-]zA:[o]-:[-]Z0:[o]-:[-]9_:[-t]:[g]]:[-]
  #[ ]  #[ ]       in bytes patterns or string patterns with the :[fn]ASCII:[-fn] flag.
  #[ ]  #[ ]       In string patterns without the :[fn]ASCII:[-fn] flag, it will match the
  #[ ]  #[ ]       range of Unicode alphanumeric characters (letters plus digits
  #[ ]  #[ ]       plus underscore). With :[fn]LOCALE:[-fn], it will match the set :[g][:[-]:[t]0:[o]-:[-]9_:[-t]:[g]]:[-g]
  #[ ]  #[ ]       plus characters defined as letters for the current locale.
  :[g]\W:[-]       Matches the complement of :[g]\w:[-g].
  :[o]\\:[-]       Matches a literal backslash.""",
        r""":[header]MODULE (re) FUNCTIONS:[-header]
        
  :[fn]match:[-fn]      Match a regular expression pattern to the beginning of a string.
  :[fn]fullmatch:[-fn]  Match a regular expression pattern to all of a string.
  :[fn]search:[-fn]     Search a string for the presence of a pattern.
  :[fn]sub:[-fn]        Substitute occurrences of a pattern found in a string.
  :[fn]subn:[-fn]       Same as sub, but also return the number of substitutions made.
  :[fn]split:[-fn]      Split a string by the occurrences of a pattern.
  :[fn]findall:[-fn]    Find all occurrences of a pattern in a string.
  :[fn]finditer:[-fn]   Return an iterator yielding a :[fn]Match:[-fn] object for each match.
  :[fn]compile:[-fn]    Compile a pattern into a :[fn]Pattern:[-fn] object.
  :[fn]purge:[-fn]      Clear the regular expression cache.
  :[fn]escape:[-fn]     Backslash all non-alphanumerics in a string.

  Each function other than :[fn]purge:[-fn] and :[fn]escape:[-fn] can take an optional :[hl]flags:[-hl] argument
  consisting of one or more of the following module constants, joined by :[t]|:[-t].""",
        r""":[header]FLAGS:[-header]
        
  :[fa]A:[-]  :[fn]ASCII:[-]       For string patterns, make :[,g]\w, \W, \b, \B, \d, \D:[-] match
  #[  ] #[ ]  #[  ]     #[ ]       the corresponding :[fn]LOCALE:[-fn] character categories (rather
  #[  ] #[ ]  #[  ]     #[ ]       than the whole Unicode categories, which is the default).
  #[  ] #[ ]  #[  ]     #[ ]       For bytes patterns, this flag is the only available
  #[  ] #[ ]  #[  ]     #[ ]       behaviour and needn't be specified.
  #[  ] #[ ]  :[fn]DEBUG:[-]       Display debug info about compiled expression. No inline flag.
  :[fa]I:[-]  :[fn]IGNORECASE:[-]  Perform case-insensitive matching.
  :[fa]L:[-]  :[fn]LOCALE:[-]      Make :[,g]\w, \W, \b, \B:[-] dependent on the current locale.
  :[fa]M:[-]  :[fn]MULTILINE:[-]   :[o]^:[-] matches the beginning of lines (after a newline)
  #[  ] #[ ]  #[  ]         #[ ]   as well as the string.
  #[  ] #[ ]  #[  ]         #[ ]   :[o]$:[-] matches the end of lines (before a newline) as well
  #[  ] #[ ]  #[  ]         #[ ]   as the end of the string.
  #[  ] #[ ]  :[fn]NOFLAG:[-]      Indicates no flag being applied, may be used as a default value.
  :[fa]S:[-]  :[fn]DOTALL:[-]      :[i].:[-] matches any character at all, including the newline.
  :[fa]X:[-]  :[fn]VERBOSE:[-]     Ignore whitespace and comments for nicer looking RE's.
  :[fa]U:[-]  :[fn]UNICODE:[-]     For compatibility only. Ignored for string patterns (it
  #[  ] #[ ]  #[  ]       #[ ]     is the default), and forbidden for bytes patterns.

  :[,fa]A, L,:[-] and :[fa]U:[-] are mutually exclusive.
""",
    ]

    def __init__(self, ctx: click.Context, **kwargs):
        engine = pt.TemplateEngine(self.CUSTOM_STYLES)
        parsed_segs = [engine.substitute(data_seg) for data_seg in self.DATA_SEGS]
        max_left_line_len = self._find_longest_line_len([parsed_segs[0], parsed_segs[2]])
        max_right_line_len = self._find_longest_line_len([parsed_segs[1], parsed_segs[3]])

        result = ""
        if pt.get_terminal_width() > max_left_line_len + max_right_line_len + self.PADDING:
            left_lines = "\n\n".join(
                get_stdout().render(" " + p) for p in [parsed_segs[0], parsed_segs[2]]
            ).splitlines()
            right_lines = "\n\n".join(
                get_stdout().render(p) for p in [parsed_segs[1], parsed_segs[3]]
            ).splitlines()
            left_justified = [pt.ljust_sgr(ln, max_left_line_len) for ln in left_lines]
            for idx in range(0, max(len(left_justified), len(right_lines))):
                result += (
                    left_justified[idx]
                    if idx < len(left_justified)
                    else "".ljust(max_left_line_len)
                )
                result += " " * self.PADDING
                result += right_lines[idx] if idx < len(right_lines) else ""
                result += "\n"
        else:
            result += "\n\n".join(get_stdout().render(p) for p in parsed_segs)

        get_stdout().echo(result.rstrip())

    def _find_longest_line_len(self, segs: list[pt.Text]) -> int:
        result = 0
        for seg in segs:
            lines = ""
            for frag in seg._fragments:
                lines += frag.raw()
            for line in lines.splitlines():
                result = max(result, len(line))
        return result
