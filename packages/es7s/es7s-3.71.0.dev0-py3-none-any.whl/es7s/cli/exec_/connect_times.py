# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from collections import OrderedDict
from subprocess import CalledProcessError
import pytermor as pt
import click

from es7s.cli._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_X11
from es7s.cli._decorators import cli_command, cli_argument, cli_option, catch_and_log_and_exit
from es7s.commons import Scale
from es7s.shared import run_subprocess, get_stdout, get_logger, Styles


class CurlError(RuntimeError):
    ...


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    short_help="measure connection timings (lookups, redirects)",
)
@cli_argument(
    "url",
    type=click.STRING,
    required=True,
    nargs=-1,
)
@catch_and_log_and_exit
class invoker:
    """
    @TODO

    Requires ++curl++.
    """

    TIMINGS = OrderedDict(
        {
            "time_namelookup": ("DNS lookup", pt.cvr.AIR_SUPERIORITY_BLUE),
            "time_connect": ("Connect", pt.cvr.EMERALD_GREEN),
            "time_appconnect": ("App connect", pt.cvr.EMERALD),
            "time_pretransfer": ("Pre-transfer", pt.cvr.SAFETY_ORANGE),
            "time_redirect": ("Redirectons", pt.cvr.SAFETY_YELLOW),
            "time_starttransfer": ("Start transfer", pt.cvr.PACIFIC_BLUE),
            "time_total": ("Total", pt.cvr.FULL_WHITE),
        }
    )
    CURL_EXIT_CODES = {
        1: "Unsupported protocol",
        5: "Could not resolve proxy",
        6: "Could not resolve host",
        7: "Failed to connect to host",
        28: "Operation timeout",
    }
    FMT = "%{stderr}" + "\t".join("%{" + t + "}" for t in TIMINGS.keys()) + "\n"

    SHARED_SCALE_LEN = 80
    SHARED_SCALE_CHAR = "━"  # "━▁"
    SHARED_SCALE_CHAR_START = "╺"

    def __init__(self, url: tuple[str], **kwargs):
        self.run(*url)

    def run(self, *urls: str):
        stdout = get_stdout()
        for url in urls:
            get_stdout().echo(url)
            try:
                result = self._invoke_curl(url)
            except CurlError as e:
                get_logger().non_fatal_exception(e)
                stdout.echo_rendered("\t" + str(e), Styles.ERROR)
                continue

            if len(parts := result.split("\t")) != len(self.TIMINGS):
                stdout.echo_rendered(f"\tMalformed result: {result!r}", Styles.WARNING)
                continue

            kvs = OrderedDict({1e3 * float(v): k for k, v in zip(self.TIMINGS.keys(), parts)})

            cursor = 0
            char_shift = 0
            max_name_len = max(map(lambda kv: len(kv[0]), self.TIMINGS.values()))
            total_ms = [*kvs.keys()][-1]

            skvs = [*sorted(kvs.keys())]
            while len(skvs):
                val_ms = skvs.pop(0)
                if not len(skvs):
                    print()
                val_str = pt.format_time_ms(val_ms)
                if val_ms > 1000:
                    val_str = f"{1e-3*val_ms:4.2f}s"
                name, scale_st = self.TIMINGS.get(kvs.get(val_ms))
                pre_scale = Scale(
                    (cursor) / total_ms,
                    pt.NOOP_STYLE,
                    pt.Style(fg=pt.cvr.GRAY_KALM, overlined=True),
                    self.SHARED_SCALE_LEN,
                    full_block_char="░" if len(skvs) else "'",
                    allow_partials=False,
                ).blocks

                scale = ""
                if len(skvs):
                    scale = Scale(
                        (val_ms - cursor) / total_ms,
                        pt.NOOP_STYLE,
                        scale_st,
                        self.SHARED_SCALE_LEN,
                        full_block_char='▇',
                        allow_partials=False,
                        require_not_empty=True,
                    ).blocks

                stdout.echo(f"{name:>{2+max_name_len}s}  {val_str:>6s}  {pre_scale}{scale}")
                cursor = val_ms
                char_shift += len(scale)


    def _invoke_curl(self, url: str):
        args = [
            "curl",
            "-w",
            self.FMT,
            *("-o", "/dev/null"),
            "-Lks",
            *("--max-time", "10"),
            # *("--proxy", "socks5h://127.0.0.1:1080"),
            url,
        ]
        try:
            return run_subprocess(*args).stderr
        except CalledProcessError as e:
            if error_desc := self.CURL_EXIT_CODES.get(e.returncode, None):
                raise CurlError(error_desc) from e
            raise CurlError(f"Exit code {e.returncode}")
