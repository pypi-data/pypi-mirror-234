# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

from collections.abc import Iterable

import pytermor as pt

from es7s.shared import get_stdout
from ..._base import CliCommand
from ..._base_opts_params import IntRange
from ..._decorators import catch_and_log_and_exit, cli_command, cli_option


@cli_command(name=__file__, cls=CliCommand, short_help="rgb spectre")
@cli_option("-i", "--invert", default=False, is_flag=True, help="Use inverted colors.")
@cli_option(
    "-w",
    "--width",
    default=77,
    show_default=True,
    type=IntRange(_min=3, max_open=True),
    help="Gradient width, in characters.",
)
@catch_and_log_and_exit
def invoker(invert: bool, width: int):
    """
    Display RGB color gradient.
    """

    def inv(*vv: int) -> Iterable[int]:
        yield from [255 - v for v in vv]

    s = " ·" * (width // 2 + 1)
    colors = []

    stdout = get_stdout()
    stdout.echo(pt.SeqIndex.BOLD)

    for c in range(width):
        r = 255 - (c * 255 // (width - 1))
        g = c * 510 // (width - 1)
        b = c * 255 // (width - 1)
        if g > 255:
            g = 510 - g
        if invert:
            r, g, b = inv(r, g, b)
        colors.append((r, g, b, s[c]))

    for col in [*colors]:
        if not col:
            stdout.echo()
            continue
        r, g, b, c = col
        stdout.echo_rendered(
            pt.Fragment(
                c,
                pt.Style(
                    # fg=pt.rgb_to_hex(pt.RGB(max(0, r - 128), max(0, g - 128), max(0, b - 128))),
                    fg=pt.ColorRGB(pt.RGB.from_channels(255 - r, 255 - g, 255 - b)),
                    bg=pt.ColorRGB(pt.RGB.from_channels(r, g, b)),
                ),
            ),
            nl=False,
        )
    stdout.echo(pt.SeqIndex.BOLD_DIM_OFF)
    stdout.echo()
