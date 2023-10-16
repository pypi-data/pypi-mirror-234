# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os.path

import click

from .._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_X11
from .._decorators import cli_pass_context, catch_and_log_and_exit, cli_command, cli_argument
from es7s.shared import get_merged_uconfig, get_logger, run_subprocess


@cli_command(
    name=__file__,
    short_help="open image in a graph editor",
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_X11],
)
@cli_argument("path", type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@cli_pass_context
@catch_and_log_and_exit
class invoker:
    """
    @TODO fix click ARGUMENT output
    """

    def __init__(self, ctx: click.Context, path: click.Path, **kwargs):
        self._config_section = f"exec.{ctx.command.name}"
        self._run(path)

    def _run(self, path: click.Path):
        _, ext = os.path.splitext(path)
        get_logger().debug(f'Target file extension: "{ext}"')

        ext_vector: list[str] = get_merged_uconfig().get(self._config_section, "ext-vector")
        editor_type = "raster"
        if ext.removeprefix(".") in ext_vector:
            editor_type = "vector"
        get_logger().debug(f"Selected editor type: {editor_type}")

        editor = get_merged_uconfig().get(self._config_section, f"editor-{editor_type}")
        run_subprocess(editor, path)
