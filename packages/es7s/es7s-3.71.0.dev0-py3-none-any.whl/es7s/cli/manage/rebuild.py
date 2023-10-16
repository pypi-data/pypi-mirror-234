# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import pytermor as pt

from es7s.shared import ProgressBar, with_progress_bar, get_stdout
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
@with_progress_bar
class invoker:
    """Rebuild dynamic resources."""

    def __init__(self, pbar: ProgressBar, dry_run: bool, **kwargs):
        self._pbar = pbar
        self._dry_run = dry_run
        self._run()

    def _run(self):
        from ._indicator_icons_network import NetworkIndicatorIconBuilder
        from ._indicator_icons_disk import DiskIndicatorIconBuilder

        builders = [
            NetworkIndicatorIconBuilder(self._pbar),
            DiskIndicatorIconBuilder(self._pbar),
        ]
        self._pbar.init_tasks(len(builders), task_num=0)
        for builder in builders:
            self._pbar.next_task(pt.get_qname(builder))
            builder.run(self._dry_run)
            from es7s.shared import get_logger
            get_stdout().echo(f"Successfully executed {pt.get_qname(builder)}")
