# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re

import click
import pytermor as pt

from .._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_ADAPTIVE
from es7s.shared import get_stdout, get_merged_uconfig
from es7s.commons import WeatherIconSet, WEATHER_ICON_SETS, get_wicon, justify_wicon
from .._base import CliCommand
from .._decorators import cli_pass_context, catch_and_log_and_exit, cli_option, cli_command


@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE],
    short_help="weather icon table display/measure",
)
@cli_option(
    "-m",
    "--measure",
    is_flag=True,
    default=False,
    help="Also perform a character width measuring.",
)
@cli_pass_context
@catch_and_log_and_exit
class invoker:
    """
    ...
    """

    PAD = " " * 1

    def __init__(self, ctx: click.Context, measure: bool, **kwargs):
        self._run(measure)

    def _run(self, measure: bool):
        max_width = get_merged_uconfig().getint("monitor.weather", "weather-icon-max-width")
        result = "inp|"
        for set_id in range(WeatherIconSet.MAX_SET_ID + 1):
            set_idstr = f"s{set_id}".center(max_width)
            result += set_idstr + "|"

        sepm = "|" + re.sub("[^|]", "=", result[1:])
        sepb = re.sub("=", "_", sepm)
        sept = "." + re.sub("\|", "_", sepb[1:-1]) + "."
        get_stdout().echo(self.PAD + sept)
        get_stdout().echo_rendered(self.PAD + result)
        get_stdout().echo(self.PAD + sepm)

        for origin in WEATHER_ICON_SETS.keys():
            renders = ["|"]
            measurements = []
            for set_id in range(-1, WeatherIconSet.MAX_SET_ID + 1):
                icon, term, style = get_wicon(origin, set_id)
                justified, real_width = justify_wicon(icon, max_width, measure)
                if measure:
                    measurements += [real_width]
                term += pt.SeqIndex.RESET.assemble()
                renders += [get_stdout().render(justified + term + "|", style)]

            get_stdout().echo(self.PAD, nl=False)
            for render in renders:
                get_stdout().echo(render, nl=False)

            for measurement in measurements:
                get_stdout().echo("  ", nl=False)
                get_stdout().echo(measurement, nl=False)

            get_stdout().echo()
        get_stdout().echo(self.PAD + sepb)
