# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from .._decorators import cli_command, cli_option, catch_and_log_and_exit
from es7s.shared import reset_config, get_stdout


@cli_command(name=__file__, short_help="reset config values to default")
@cli_option(
    "-p",
    "--prune",
    is_flag=True,
    default=False,
    help="Silently overwrite original config, do not make a backup.",
)
@catch_and_log_and_exit
def invoker(prune: bool):
    """
    Make a backup and replace current user config with the default one.
    The original file is preliminarily renamed to "<<filename>>.bak".
    """
    user_backup_filepath = reset_config(backup=not prune)
    if user_backup_filepath:
        get_stdout().echo(f'Saved current config as: "{user_backup_filepath}"')
    get_stdout().echo("Config was reset to default")
