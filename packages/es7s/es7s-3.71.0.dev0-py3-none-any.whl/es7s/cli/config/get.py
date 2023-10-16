# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from ._base import split_name
from .._decorators import cli_command, cli_argument, cli_option, catch_and_log_and_exit
from es7s.shared import get_merged_uconfig, get_stdout


@cli_command(name=__file__, short_help="display config variable value")
@cli_argument("name")
@cli_option(
    "-b",
    "--boolean",
    is_flag=True,
    default=False,
    help="Cast the value to boolean `True` or `False`.",
)
@catch_and_log_and_exit
def invoker(name: str, boolean: bool):
    """
    Display config variable value. NAME should be in format
    "<<SECTION>>.<<OPTION>>".
    """
    section, option = split_name(name)
    if boolean:
        value = get_merged_uconfig().getboolean(section, option)
    else:
        value = get_merged_uconfig().get(section, option)
    get_stdout().echo(value)
