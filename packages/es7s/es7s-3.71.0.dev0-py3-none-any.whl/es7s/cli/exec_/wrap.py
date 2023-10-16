# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t

import click
import pytermor as pt

from es7s.shared import get_stdout
from ..demo import DemoHilightNumText
from .._base_opts_params import IntRange
from .._decorators import cli_pass_context, catch_and_log_and_exit, cli_option, cli_argument, \
    cli_command


@cli_command(
    name=__file__,
    short_help="SGR-aware text folding to specified width",
)
@cli_argument("file", type=click.File(mode="r"), required=False)
@cli_option(
    "-d",
    "--demo",
    is_flag=True,
    default=False,
    help="Ignore FILE argument and use built-in example text as input.",
)
@cli_option(
    "-w",
    "--max-width",
    type=IntRange(_min=0),
    default=120,
    show_default=True,
    help="Set maximum length of one line of the output. Actual value can be smaller, e.g., when output is a "
    "terminal narrower than N characters. Also, 2 more spaces are added to lower the chances that characters with "
    "incorrect width will break the wrapping. Setting to 0 disables the limit.",
)
@cli_option(
    "-W",
    "--force-width",
    type=IntRange(_min=1),
    help="Force output lines to be N characters wide no matter what device/program is receiving it.",
)
@cli_pass_context
@catch_and_log_and_exit
class invoker:
    """
    Read text from given FILE and wrap it to specified width. If FILE is omitted
    or equals to ''-'', read standard input instead.

    Works like standard python's textwrap.wrap(), except that also correctly processes formatting sequences
    for terminals (i.e. SGRs).
    """

    PADDING_RIGHT = 2
    PRIVATE_REPLACER = "\U000E5750"

    def __init__(
        self,
        ctx: click.Context,
        file: click.File | None,
        demo: bool,
        force_width: int = None,
        max_width: int = None,
        **kwargs
    ):
        if file is None:
            file = click.open_file("-", "r")
        if demo:
            file = DemoHilightNumText.open()

        if force_width is not None:
            self._run(file, force_width)
            return
        width = pt.get_terminal_width()
        if max_width:
            width = min(max_width, width)
            width -= self.PADDING_RIGHT

        self._run(file, width)

    def _run(self, inp: t.IO, width: int):
        result = pt.wrap_sgr(inp.readlines(), width)
        get_stdout().echo(result)
