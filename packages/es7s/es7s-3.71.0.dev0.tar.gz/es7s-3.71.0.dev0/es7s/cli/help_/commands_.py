# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t
from typing import cast

import click
import pytermor as pt

from es7s.shared import get_stdout, FrozenStyle
from .._base import (
    CliCommand,
    CliGroup,
    HelpFormatter,
    CliBaseCommand,
    HelpStyles,
)
from .._decorators import cli_pass_context, catch_and_log_and_exit, cli_command, cli_option


@cli_command(
    name=__file__,
    cls=CliCommand,
    short_help="tree of es7s commands",
)
@cli_option(
    "-r",
    "--raw",
    help="disable all formatting in the output and hide the legend; if output "
    "device is not a terminal, this option is enabled automatically (see "
    "'es7s help options' for the detials).",
    is_flag=True,
)
@cli_option(
    "--no-raw",
    help="disable the behaviour of redirect/pipe detection and do not apply the "
    "restrictions from raw mode; note that this alone does not guarantee "
    "that all the formatting will be kept; e.g., it can still be disabled with "
    "'--no-color'.",
    is_flag=True,
)
@cli_pass_context
@catch_and_log_and_exit
class invoker:
    """
    Print es7s commands with descriptions as grouped (default) or plain list.
    """

    def __init__(self, ctx: click.Context, raw: bool, **kwargs):
        self._raw = raw
        self._formatter = HelpFormatter()

        self._run(ctx)

    def _run(self, ctx: click.Context):
        root_cmd = cast(CliGroup, ctx.find_root().command)

        self._formatter.write_dl([*filter(None, self._iterate([*root_cmd.commands.values()], []))])

        if not self._raw:
            self._formatter.write_paragraph()
            with self._formatter.indentation():
                self._formatter.write_dl([*self._format_legend(root_cmd)])

            self._formatter.write_paragraph()
            with self._formatter.indentation():
                self._formatter.write_dl(
                    [
                        (
                            '› G1 ',
                            "First shell scripts later partially combined into "
                            "es7s/commons (Nov 21—Apr 22)",
                        ),
                        (
                            "» G2 ",
                            "Shell/Python scripts as es7s/tmux and leonardo "
                            "components (Apr 22~Nov 22)",
                        ),
                        (
                            '● G3 ',
                            "Python scripts as parts of centralized es7s "
                            "system (Nov 22+)",
                        ),
                        (
                            "✪ G4 ",
                            "Golang applications for bottlenecks where execution "
                            "speed is critical (May 23+)",
                        ),
                    ]
                )

        result = self._formatter.getvalue().rstrip("\n")
        if self._raw:
            get_stdout().echo_raw(result)
        else:
            get_stdout().echo(result)

    def _format_entry(
        self, cmd: CliBaseCommand, stack: list[str], cname_st_over: pt.Style = pt.NOOP_STYLE
    ) -> tuple[str, str] | None:
        cname = " ".join(stack + [cmd.name])
        if self._raw:
            return cname, ""

        offset = len(stack) * 2 * " "
        ctype_str = get_stdout().render(self._formatter.format_command_icon(cmd))
        cname_st = pt.merge_styles(cmd.get_command_type().get_name_fmt(), overwrites=[cname_st_over])
        cname_str = get_stdout().render(cname, cname_st)
        left_col = offset + ctype_str + " " + cname_str

        right_col = ""
        if not isinstance(cmd, CliGroup):
            right_col = cmd.get_short_help_str()

        return left_col, right_col

    def _format_command(self, cmd: CliBaseCommand, stack: list[str]) -> tuple[str, str] | None:
        return self._format_entry(cmd, stack)

    def _format_group(self, cmd: CliBaseCommand, stack: list[str]) -> tuple[str, str] | None:
        return self._format_entry(cmd, stack, FrozenStyle(HelpStyles.TEXT_HEADING, bold=True))

    def _iterate(self, cmds: t.Iterable[CliBaseCommand], stack: list[str] = None):
        for cmd in sorted(cmds, key=lambda c: c.name):
            if not isinstance(cmd, CliGroup):
                yield self._format_command(cmd, stack)
            else:
                yield self._format_group(cmd, stack)
                yield from self._iterate(cmd.get_commands().values(), stack + [cmd.name])

    def _format_legend(self, root_cmd: CliGroup) -> tuple[str, str]:
        for ct in sorted(
            {*root_cmd.get_command_attributes(recursive=True)},
            key=lambda el: el.sorter,
        ):
            if ct.hidden:
                continue
            yield get_stdout().render(self._formatter.format_command_attribute_legend(ct)), (
                ct.description % ""
            ).replace("|", " ").replace("  ", " ")
            # holy fuck  @refactorme
