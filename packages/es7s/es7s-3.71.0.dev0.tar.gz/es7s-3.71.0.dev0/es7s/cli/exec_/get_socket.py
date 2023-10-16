# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import click

from .._decorators import cli_pass_context, catch_and_log_and_exit, cli_command, cli_argument
from es7s.shared import get_stdout
from es7s.shared import get_socket_path


@cli_command(__file__, short_help="get monitor socket path")
@cli_argument("topic")
@cli_pass_context
@catch_and_log_and_exit
class invoker:
    """
    @TODO fix click ARGUMENT output
    """

    def __init__(self, ctx: click.Context, topic: str, **kwargs):
        self._run(topic)

    def _run(self, topic: str):
        socket_path = get_socket_path(topic)  # @TODO validate ?
        get_stdout().echo(socket_path)
