# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import os

from es7s.shared import run_detached
from .._decorators import cli_command, catch_and_log_and_exit
from es7s.shared import  get_stdout, get_logger
from es7s.shared import get_local_filepath as get_local_uconfig_filepath


@cli_command(name=__file__, short_help="open current user config in text editor")
@catch_and_log_and_exit
def invoker():
    """
    Open current user config in text editor.\n\n

    Note that this command ignores the common option '--default'.
    """
    logger = get_logger()
    editor = os.getenv("EDITOR", "xdg-open")
    logger.debug(f"Selected the editor executable: '{editor}'")

    run_detached([editor, get_local_uconfig_filepath()])
    get_stdout().echo("Done")
