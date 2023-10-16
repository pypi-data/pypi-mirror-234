# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from es7s.cli._base_opts_params import CMDTYPE_BUILTIN, IntRange
from es7s.cli._decorators import cli_command, cli_argument, cli_option, catch_and_log_and_exit
from es7s.shared.decorators import with_progress_bar
from es7s.shared import ProgressBar, sub, get_stdout, get_logger


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    short_help="extract emojis from emoji font to png files",
)
@cli_argument(
    "char",
    type=str,
    required=False,
    nargs=-1,
)
@cli_option(
    "-s",
    "--size",
    default=128,
    show_default=True,
    type=IntRange(1, max_open=True),
    help="Output image(s) width and height (which are equal).",
)
@cli_option(
    "-f",
    "--font",
    default="Noto Color Emoji",
    show_default=True,
    help="Font name to use for rendering.",
)
@cli_option(
    "-o",
    "--output",
    default="emoji-%s",
    show_default=True,
    help='Output filename template, must contain ""%s"".',
)
@catch_and_log_and_exit
@with_progress_bar(task_label="Rendering file")
class invoker:
    """
    Extract emojis from an emoji font to separate PNG files.
    """

    def __init__(self, pbar: ProgressBar, font: str, size: int, output: str, char: tuple[str], **kwargs):
        import emoji.core

        if not char:
            char = emoji.core.distinct_emoji_list('🐍🙈🧊️')

        get_stdout().echo_rendered(f"")

        self._pbar = pbar
        self.run(font, size, output, "".join(char))

    def run(self, font: str, size: int, out_filename_tpl: str, chars: str) -> tuple[int, int]:
        from emoji import distinct_emoji_list

        size_norm = 80000    # originally 20000
        emojis = distinct_emoji_list(chars)
        success, total = 0, len(emojis)
        self._pbar.init_steps(steps_amount=total, step_num=1)

        for idx, emoji in enumerate(emojis):
            filename = f"{out_filename_tpl}.png" % emoji
            self._pbar.next_step(step_label=f'{filename}')

            args = [
                "convert", "-background", "transparent", "-size", "%sx%s" % (size, size),
                "-set", "colorspace", "sRGB",
                "pango:<span font=\"%s\" size=\"%d\">%s</span>" % (font, size_norm, emoji),
                filename
            ]
            exitcode = sub.run_detached(args)
            if exitcode != 0:
                get_logger().error(f"Failed to write '{filename}', exit code: {exitcode}")
            else:
                success += 1
        return success, total
