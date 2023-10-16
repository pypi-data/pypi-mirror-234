# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from es7s.shared import get_stdout
from es7s.shared import GIT_PATH
from es7s.shared import run_detached
from es7s.shared import (
    get_default_filepath as get_default_uconfig_filepath,
    get_local_filepath as get_local_uconfig_filepath,
)
from .._decorators import catch_and_log_and_exit, cli_command


@cli_command(name=__file__, short_help="show differences between current and default configs")
@catch_and_log_and_exit
def invoker():
    """
    Compare current user config with the default one and show the differences.\n\n

    This command requires ++git++ to be present and available.
    """

    color_args = ["--color", "--color-moved"] if get_stdout().sgr_allowed else []
    run_detached(
        [
            GIT_PATH,
            "diff",
            "--no-index",
            "--minimal",
            "--ignore-all-space",
            *color_args,
            get_default_uconfig_filepath(),
            get_local_uconfig_filepath(),
        ]
    )
    get_stdout().echo("Done")
