# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import copy
import os
import re
import signal
import sys
from sys import addaudithook

import click
import pytermor as pt

from es7s import APP_NAME, APP_UPDATED, APP_VERBOSITY, APP_VERSION
from es7s.shared import (
    UserConfigParams,
    FrozenStyle,
    IoParams,
    LoggerParams,
    destroy_io,
    destroy_logger,
    get_logger,
    get_stderr,
    get_stdout,
    init_config,
    init_io,
    init_logger,
    uconfig,
    get_signal_desc,
)
from ..commons.pt_ import format_path
from es7s.shared import exit_gracefully
from ._base import (
    CliGroup,
    Context,
    HelpFormatter,
)
from ._base_opts_params import CommandOption, HelpPart
from ._decorators import catch_and_log_and_exit, cli_group, cli_option, cli_pass_context


def invoker():
    os.environ.update({"ES7S_DOMAIN": "CLI"})
    init_cli()
    try:
        callback()
    except SystemExit:
        # if stdout := get_stdout(False):
        #     stdout.echo('')
        destroy_io()
        destroy_logger()
        raise


def init_cli():
    pre_filtered_args = copy.copy(sys.argv)
    logger_params, io_params, ucp_params, spec_args = _filter_common_args(sys.argv)
    sys.argv = spec_args

    logger = init_logger(params=logger_params)
    _, _ = init_io(io_params)
    init_config(ucp_params)

    post_filtered_args = sys.argv

    logger.log_init_params(
        ("Executable:", format_path(sys.executable)),
        ("Entrypoint:", format_path(__file__)),
    )
    if hasattr(sys, "orig_argv"):
        logger.log_init_params(("Original app args:", getattr(sys, "orig_argv")))
    logger.log_init_params(
        ("Pre-init app args:", pre_filtered_args),
        ("Post-init app args:", post_filtered_args),
        ("Log configuration:", logger_params),
        ("Logger setup:", {"handlers": logger.handlers}),
        ("IO configuration:", io_params),
        ("Stdout proxy setup:", get_stdout().as_dict()),
        ("Stderr proxy setup:", get_stderr().as_dict()),
    )
    addaudithook(_audit_event)

    [signal.signal(s, c) for s, c in [
        (signal.SIGINT, _exit),
        (signal.SIGTERM, _exit),
        (signal.SIGALRM, _clock_tick),
    ]]
    signal.setitimer(signal.ITIMER_REAL, 1.0, 1.0)


def _audit_event(ev: str, *args):
    match ev.split(".")[0]:
        case "os" | "subprocess" | "shutil" | "tempfile" | "importlib":
            if logger := get_logger(require=False):
                logger.log_audit_event(ev, *args)
            return


def _exit(signal_code: int, *args):
    _log_signal(signal_code)
    exit_gracefully(signal_code)


def _clock_tick(signal_code: int, *args):
    _log_signal(signal_code)


def _log_signal(signal_code: int, frame=None):
    get_logger(require=False).debug("Received " + get_signal_desc(signal_code))


class EntrypointCliGroup(CliGroup):
    def _make_command_name(self, orig_name: str) -> str:
        return APP_NAME

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        if ctx.failed:
            super().format_usage(ctx, formatter)
            return

        class LogoFormatter(pt.StringReplacer):
            REGEX = re.compile(r"(\^+)|((╲╲╲)|(╱╲|╲╱))(╲+(╱+(?!╲))?|╱+(?!╲)|)")
            LOGO_ACCENT = FrozenStyle(fg=pt.cv.YELLOW, overlined=True)
            LOGO_DEFAULT = FrozenStyle(fg=pt.cv.BLUE, overlined=True)

            def __init__(self):
                super().__init__(self.REGEX, self.replace)

            def replace(self, m: re.Match) -> str:
                group_overline_marks = m.group(1)
                group_accent_left = m.group(3)
                group_accent = m.group(4)
                group_default = m.group(5)
                result = ""

                if group_overline_marks:
                    result += render(
                        " " * len(group_overline_marks), FrozenStyle(self.LOGO_DEFAULT)
                    )
                if group_accent_left:
                    result += render(
                        group_accent_left, FrozenStyle(self.LOGO_ACCENT, overlined=False)
                    )
                if group_accent:
                    if group_accent.endswith("╲"):
                        result += render(
                            group_accent[0], FrozenStyle(self.LOGO_ACCENT, overlined=False)
                        )
                        result += render(
                            group_accent[1:], FrozenStyle(self.LOGO_ACCENT, overlined=True)
                        )
                    else:
                        result += render(
                            group_accent, FrozenStyle(self.LOGO_ACCENT, overlined=False)
                        )
                if group_default:
                    if group_default.endswith("╲"):
                        result += render(group_default[:-1], self.LOGO_DEFAULT)
                        result += render(
                            group_default[-1],
                            FrozenStyle(self.LOGO_DEFAULT, overlined=False),
                        )
                    else:
                        result += render(group_default, self.LOGO_DEFAULT)
                return result

        render = get_stdout().render

        version_main, sep, version_sub = APP_VERSION.partition("-")
        version_sub = (sep + version_sub if version_sub else "").ljust(13 - len(version_main))
        version_str = (
            render("v", LogoFormatter.LOGO_ACCENT)
            + render(version_main, FrozenStyle(LogoFormatter.LOGO_DEFAULT, bold=True))
            + render(version_sub, LogoFormatter.LOGO_DEFAULT)
        )

        formatter.buffer.append(
            "\n".join(
                pt.apply_filters(line, LogoFormatter)
                for line in f"""
                                                                             
 ╱╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲     ╱╲╲╲╲╲╲╲╲╲╲╲    ╱╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲   ╱╲╲╲╲╲╲╲╲╲╲╲        
 ╲╲╲╲╲╱╱╱╱╱╱╱╱╱╱╱    ╱╲╲╲╱╱╱╱╱╱╱╱╱╲╲╲ ╲╱╱╱╱╱╱╱╱╱╱╱╱╱╲╲╲ ╱╲╲╲╱╱╱╱╱╱╱╱╱╲╲╲     
  ╲╲╲╲╲^^^^^^^^^     ╲╱╱╲╲╲╲^^^^^╲╱╱╱  ^^^^^^^^^^^╱╲╲╲╱ ╲╱╱╲╲╲╲^^^^^╲╱╱╱     
   ╲╲╲╲╲╲╲╲╲╲╲╲╲      ^╲╱╱╱╱╲╲╲╲  ^^             ╱╲╲╲╱   ^╲╱╱╱╱╲╲╲╲  ^^      
    ╲╲╲╲╲╱╱╱╱╱╱╱        ^^^╲╱╱╱╱╲╲╲╲            ╱╲╲╲╱      ^^^╲╱╱╱╱╲╲╲╲      
     ╲╲╲╲╲^^^^^             ^^^╲╱╱╱╱╲╲╲        ╱╲╲╲╱           ^^^╲╱╱╱╱╲╲╲   
      ╲╲╲╲╲              ╱╲╲╲   ^^^╲╱╱╲╲╲     ╱╲╲╲╱         ╱╲╲╲   ^^^╲╱╱╲╲╲ 
       ╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲ ╲╱╱╱╲╲╲╲╲╲╲╲╲╲╲╱    ╱╲╲╲╱          ╲╱╱╱╲╲╲╲╲╲╲╲╲╲╲╱ 
        ╲╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱  ^^╲╱╱╱╱╱╱╱╱╱╱╱     ╲╱╱╱            ^^╲╱╱╱╱╱╱╱╱╱╱╱              
         {version_str }      ^^^^^^^^^^       ^^                ^^^^^^^^^^ """.splitlines()
            )
            + "\n"
        )
        super().format_usage(ctx, formatter)


class VersionOption(CommandOption):
    SPACE_SQUASHER = pt.StringReplacer(r"(\s)\s+", r"\1")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("count", True)
        kwargs.setdefault("expose_value", False)
        kwargs.setdefault("is_eager", True)
        kwargs["callback"] = self.callback
        super().__init__(*args, **kwargs)

    def callback(self, ctx: click.Context, param: click.Parameter, value: int):
        if not value or ctx.resilient_parsing:
            return
        stdout = get_stdout()
        vfmt = lambda s: pt.Fragment(s, "green")
        ufmt = lambda s: pt.Fragment(s, "gray")

        stdout.echo(f"{APP_NAME:<10s} {vfmt(APP_VERSION):<14s} {ufmt(APP_UPDATED)}")
        stdout.echo(f"{'pytermor':<10s} {vfmt(pt.__version__):<14s} {ufmt(pt.__updated__)}")
        self._echo_python_version(vfmt, ufmt)
        self._echo_gi_version()

        if value > 1:
            def _echo_path(label: str, path: str):
                stdout.echo_rendered(
                    pt.Composite(
                        pt.Text(label+":", width=17),
                        format_path(path, color=True, repr=False),
                    )
                )

            stdout.echo()
            _echo_path("Executable", sys.executable)
            _echo_path("Entrypoint", __file__)
            _echo_path("Local config", uconfig.get_local_filepath())
            _echo_path("Default config", uconfig.get_default_filepath())

        ctx.exit()

    def _echo_python_version(self, vfmt, ufmt):
        get_stdout().echo(
            re.sub(
                r"^(\S+) *\(\S+, *(\S+) *\S+( *\S+),.+?\) *.+$",
                lambda m: " ".join(
                    [
                        f'{"python":<10s}',
                        f"{vfmt(m[1]):<14s}",
                        f"{ufmt(self.SPACE_SQUASHER.apply((m[2]+m[3]).strip())):s}",
                    ]
                ),
                sys.version,
            )
        )

    def _echo_gi_version(self):
        try:
            import gi
        except ImportError:
            return
        else:
            gi_v = ".".join(str(p) for p in gi.version_info)
            get_stdout().echo(f"{'[gtk]':<10s} " + pt.render(gi_v, "blue"))


@cli_group(
    name=__file__,
    cls=EntrypointCliGroup,
    epilog=HelpPart(
        "Run 'es7s --version' (or '-V') to get the application version, or '-VV' to also include path info.",
        group="run",
    ),
)
@cli_option("--version", "-V", cls=VersionOption, help="Show the version and exit.")
@cli_pass_context
@catch_and_log_and_exit
def callback(ctx: click.Context, *args, **kwargs):
    """
    Entrypoint of es7s system CLI.
    """
    # triggers before subcommand invocation


def _filter_common_args(
    args: list[str],
) -> tuple[LoggerParams, IoParams, UserConfigParams, list[str]]:
    """
    Process common options manually because we want to allow specifying
    them everywhere: 'es7s -v print colors' and  'es7s print colors -v'
    should be equivalent, but this logic should not be applied to command-specific
    options, only to the common ones.
    """
    filtered = []
    lp = LoggerParams()
    iop = IoParams()
    ucp = UserConfigParams()

    if APP_VERBOSITY:
        lp.verbosity = APP_VERBOSITY

    def process_arg(arg: str):
        is_lopt = arg.startswith("--")
        is_shopt = arg.startswith("-") and not is_lopt

        if is_lopt or (is_shopt and len(arg) == 2):
            match arg:
                case "--verbose" | "-v":
                    lp.verbosity += 1
                case "--trace":
                    lp.verbosity += 3
                case "--quiet" | "-Q":
                    lp.quiet = True
                case "--tmux":
                    iop.tmux = True
                case "--color" | "-c":
                    iop.color = True
                case "--no-color" | "-C":
                    iop.color = False
                case "--default":
                    ucp.default = True
                case _:
                    filtered.append(arg)
        elif is_shopt:
            for c in arg.lstrip("-"):
                process_arg("-" + c)
        else:
            filtered.append(arg)

    while (len(args)) and (a := args.pop(0)):
        if a == "-":
            filtered.append(a)
            continue
        if a == "--":
            filtered += ["--"] + args
            break
        process_arg(a)

    return lp, iop, ucp, filtered
