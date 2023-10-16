# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re
from collections.abc import Iterator

from es7s.shared import get_user_data_dir, run_subprocess
from es7s.shared.path import XDOTOOL_PATH
from .._base_opts_params import CMDTYPE_BUILTIN, CMDTRAIT_X11, FloatRange
from .._decorators import cli_command, cli_argument, catch_and_log_and_exit, cli_option


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_X11],
    short_help="run specified xdotool command(s) or preset(s)",
    command_examples=[
        "es7s exec xdotool -t 5 chrome-img-to-tg chrome-close-tab",
        "es7s exec xdotool -d -- search --onlyvisible --sync --class telegram windowraise",
    ],
    ignore_unknown_options=True,
    allow_extra_args=True,
)
@cli_argument(
    "args",
    type=str,
    required=True,
    nargs=-1,
)
@cli_option(
    "-d",
    "--direct",
    is_flag=True,
    help="Treat ARGs as 'xdotool' commands, not as preset filenames.",
)
@cli_option(
    "-t",
    "--timeout",
    type=FloatRange(_min=0.0, max_open=True, show_range=False),
    default=0.0,
    help="Set maximum execution time for all the commands *combined*. 0 is "
         "unlimited [which is a default].",
)
@catch_and_log_and_exit
class invoker:
    """
    Read 'xdotool' preset file(s) with names specified as ARGS and run the
    content of each of these like a command list; or (with '-d') pass the
    ARGS to 'xdotool' like commands directly.\n\n

    In the latter case it\\'s recommended to separate the argument list with
    '--' in order to avoid possible collisions between 'es7s' options and
    ones that are meant for 'xdotool'.\n\n
    
    This command requires ++/usr/bin/xdotool++ to be present and available.
    """
    PRESET_SLEEP_INTERVAL = 0.25

    def __init__(self, direct: bool, timeout: float, **kwargs):
        self._direct = direct
        self._timeout: float|None = timeout or None
        self.run([*kwargs.pop('args')])

    def run(self, args: list[str]):
        cmd = [XDOTOOL_PATH]
        if self._direct:
            cmd.extend(args)
        else:
            while args:
                filename = args.pop(0)
                cmd.extend(self._read_preset(filename))
                if len(args):
                    cmd.extend(['sleep', str(self.PRESET_SLEEP_INTERVAL)])
        run_subprocess(*cmd, timeout=self._timeout)

    def _read_preset(self, filename: str) -> Iterator[str]:
        path = None
        for fname in (filename, f"{filename}.xdo"):
            path = get_user_data_dir() / "xdotool" / fname
            if not path.is_file():
                continue
            with open(path, 'rt') as f:
                for line in f.readlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    yield from re.split(r'\s+', line)
                break
        else:
            raise FileNotFoundError(path or filename)
