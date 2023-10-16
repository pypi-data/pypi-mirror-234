# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from .._decorators import catch_and_log_and_exit, cli_option, cli_command


@cli_command(__file__)
@cli_option(
    "-n",
    "--dry-run",
    is_flag=True,
    default=False,
    help="Don't actually do anything, just pretend to.",
)
@catch_and_log_and_exit
class invoker:
    """Update es7s system."""

    def __init__(self, dry_run: bool, **kwargs):
        self._dry_run = dry_run
        self._run()

    def _run(self):
        raise NotImplementedError
