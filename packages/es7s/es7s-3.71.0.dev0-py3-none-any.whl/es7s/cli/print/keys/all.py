# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from .tmux import TmuxBindCollector
from ._base import Formatter
from .x11 import X11BindCollector
from ..._base import CliCommand
from ..._base_opts_params import CMDTRAIT_X11, CMDTYPE_BUILTIN
from ..._decorators import catch_and_log_and_exit, cli_command, cli_option


@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_X11],
    short_help="all bindings combined",
)
@cli_option(
    "-d",
    "--details",
    is_flag=True,
    default=False,
    help="Include bind commands and other details",
)
@catch_and_log_and_exit
class invoker:
    """
    a
    """

    def __init__(self, details: bool, **kwargs):
        self.run(details)

    def run(self, details: bool, **kwargs):
        collectors = [
            TmuxBindCollector(details),
            X11BindCollector(details),
        ]
        Formatter(*collectors).print()
