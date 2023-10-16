# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from ._base import split_name
from .._decorators import catch_and_log_and_exit, cli_argument, cli_command
from es7s.shared import get_stdout
from es7s.shared import rewrite_value


@cli_command(name=__file__, short_help="set config variable value")
@cli_argument("name")
@cli_argument("value")
@catch_and_log_and_exit
def invoker(name: str, value: str):
    """
    Set config variable value. NAME should be in format
    "<<SECTION>>.<<OPTION>>".
    """
    section, option = split_name(name)
    rewrite_value(section, option, value)
    get_stdout().echo("Done")
