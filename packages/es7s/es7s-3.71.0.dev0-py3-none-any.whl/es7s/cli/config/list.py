# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import re

import pytermor as pt

from es7s.shared import get_dist_uconfig, get_merged_uconfig, get_stdout, FrozenStyle
from .._decorators import cli_command, catch_and_log_and_exit


@cli_command(
    name=__file__,
    short_help="display user/default config variables with values"
)
@catch_and_log_and_exit
class invoker:
    """
    Display user [by default] config variables with values.\n\n

    Note the common option '--default' which affects this command as well;
    the default config values will be listed in that case.
    """

    HEADER_STYLE = FrozenStyle(fg=pt.cv.GREEN, bold=True)
    OPT_NAME_STYLE = FrozenStyle(bold=True)
    OPT_DEFAULT_NAME_STYLE = FrozenStyle(fg=pt.cv.BLUE)
    OPT_VALUE_STYLE = FrozenStyle(fg=pt.cv.YELLOW, bold=True)
    OPT_DEFAULT_VALUE_STYLE = FrozenStyle(fg=pt.cv.HI_BLUE)

    def __init__(self):
        self._run()

    def _run(self):
        config = get_merged_uconfig()
        dist_config = get_dist_uconfig()
        stdout = get_stdout()
        for idx, section in enumerate(config.sections()):
            if idx > 0:
                stdout.echo()
            stdout.echo_rendered(f"[{section}]", self.HEADER_STYLE)
            for option in config.options(section):
                opt_st = self.OPT_NAME_STYLE
                val_st = self.OPT_VALUE_STYLE
                value = config.get(section, option)
                if (defvalue := dist_config.get(section, option, fallback=None)) is not None:
                    if value == defvalue:
                        opt_st = self.OPT_DEFAULT_NAME_STYLE
                        val_st = self.OPT_DEFAULT_VALUE_STYLE
                option_fmtd = stdout.render(option+ " = ", opt_st)
                value_fmtd = self._render_value(value, val_st)
                stdout.echo_rendered(option_fmtd + value_fmtd)

    def _render_value(self, val: str, val_st: pt.Style) -> str:
        val = re.sub('\n+', '\n    ', val)
        return get_stdout().render(val, val_st)
