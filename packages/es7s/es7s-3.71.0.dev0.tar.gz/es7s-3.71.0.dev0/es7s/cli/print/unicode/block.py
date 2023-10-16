# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

from ..._base import CliCommand
from ..._decorators import catch_and_log_and_exit, cli_command


@cli_command(
    name=__file__,
    cls=CliCommand,
    short_help="block drawings and other chars",
)
@catch_and_log_and_exit
def invoker():
    """
    Print frequently used Unicode characters cheatsheet.
    """
    from . import _block  # noqa
