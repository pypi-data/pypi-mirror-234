# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
from importlib import resources
from os.path import expanduser

from es7s.shared import RESOURCE_PACKAGE, SHELL_COMMONS_FILE, SHELL_PATH, USER_ES7S_BIN_DIR
from es7s.shared import (
    SubprocessExitCodeError,
    get_logger,
    get_merged_uconfig,
    run_subprocess,
)
from ..commons.pt_ import format_attrs
from es7s.shared import LESS_PATH, ThemeColor
from ._base import CliCommand
from ._base_opts_params import CommandType, HelpPart
from ._decorators import catch_and_log_and_exit, cli_command, cli_pass_context
import pytermor as pt


class ForeignCliCommand(CliCommand):
    """
    Launch the external/integrated component. PASSARGS are the arguments that
    will be passed to an external app. Long options can also be used, but make
    sure to prepend PASSARGS with "--" to help `click` library to distinguish
    them from its own options. Short options are known to be buggy, better just
    avoid using them on indirect invocations of standalone apps.
    """

    EPILOG_PARTS = [
        HelpPart(
            "This first command will result in 'es7s' command help text, along with "
            "embedded help from the external component, while the second will result in "
            "'watson's direct call and only its own usage being displayed:",
            title="Invocation (generic):",
            group="ex1",
        ),
        HelpPart("  (1) 'es7s exec watson --help'", group="ex1"),
        HelpPart("  (2) 'es7s exec watson -- --help'", group="ex1"),
        HelpPart(
            "Another way to invoke an external component is to call it directly:",
            group="ex2",
        ),
        HelpPart("  (3) 'watson --help'", group="ex2"),
    ]

    def __init__(self, **kwargs):
        kwargs.update(
            {
                "help": self.__doc__,
                "epilog": self.EPILOG_PARTS,
            }
        )
        super().__init__(**kwargs)


class ForeignInvoker:
    def __init__(self, target: str = "bash"):
        self._target = target

    def spawn(self, *args: str, wait=True) -> None:
        cmd_target, cmd_args = self._get_spawn_cmd(*args)
        get_logger().info(f"Launching: {cmd_target} {format_attrs(cmd_args)}")
        code = os.spawnvpe(
            os.P_WAIT if wait else os.P_NOWAIT,
            cmd_target,
            cmd_args,
            self._build_env(),
        )
        # if code == 127:
        #    raise ExecutableNotFoundError(self._target)
        if wait and code != 0:
            raise SubprocessExitCodeError(code, args)
        if not wait:
            get_logger().debug(f"Spawned PID: {code}")

    def _get_spawn_cmd(self, *args: str) -> tuple[str, list]:
        return self._target, [self._target, *args]

    def get_help(self) -> str:
        _, cmd_args, cmd_shell = self._get_help_cmd()
        cp = run_subprocess(
            " ".join(cmd_args),
            shell=cmd_shell,
            env=self._build_env(),
            timeout=10,
        )
        if cp.stderr:
            get_logger().non_fatal_exception(cp.stderr)
        return cp.stdout

    def _get_help_cmd(self) -> tuple[str, list, bool]:
        return SHELL_PATH, [self._target, "--help"], True

    def _build_env(self) -> dict:
        logger = get_logger()
        commons_path = resources.path(RESOURCE_PACKAGE, SHELL_COMMONS_FILE)
        user_repos_path = get_merged_uconfig().get("general", "user-repos-path", fallback="")
        theme_seq = ThemeColor().to_sgr()
        result = {
            # ---[@temp]--- filter out all G1/G2 es7s env vars:
            **{k: v for (k, v) in os.environ.items() if not k.lower().startswith("es7s")},
            # ---[@temp]---
            "PATH": self._build_path(),
            # "COLORTERM": os.environ.get("COLORTERM"),
            # "TERM": os.environ.get("TERM"),
            "ES7S_SHELL_COMMONS": commons_path,
            "ES7S_DATA_DIR": resources.path(RESOURCE_PACKAGE, "."),
            "ES7S_USER_REPOS_PATH": user_repos_path,
            "ES7S_THEME_COLOR_SGR": ";".join(map(str, theme_seq.params)),
        }
        for k, v in sorted(result.items(), key=lambda k: k):
            logger.debug(
                f"Subprocess environ: {k:30s}={format_attrs(v)}"
            )  # , out_plain=False, out_sanitized=True)
        return result

    def _build_path(self) -> str:
        current = os.environ.get("PATH", "").split(":")
        filtered = ":".join(
            [
                # ---[@temp]----- remove all deprecated es7s parts from PATH:
                # *filter(lambda s: "es7s" not in s, current),
                *current,
                expanduser("~/bin/es7s"),
                # ---[@temp]----- ^ restore legacy path
                str(USER_ES7S_BIN_DIR),  # add G3 path
            ]
        )
        return filtered


def ForeignCommand(target: str, attributes: dict, type: CommandType) -> ForeignCliCommand:
    inv = ForeignInvoker(target)
    cmd = lambda ctx, inv=inv: inv.spawn(*ctx.args)
    cmd = catch_and_log_and_exit(cmd)
    cmd = cli_pass_context(cmd)
    cmd = cli_command(
        **(attributes or dict()),
        name=target.removesuffix(".sh"),
        cls=ForeignCliCommand,
        type=type,
        ignore_unknown_options=True,
        allow_extra_args=True,
        ext_help_invoker=lambda ctx, inv=inv: inv.get_help(),
        usage_section_name="Usage (generic)",
        include_common_options_epilog=False,
    )(cmd)
    return cmd


class Pager(ForeignInvoker):
    def __init__(self, max_line_len: int = None):
        super().__init__(target=LESS_PATH)

        term_width = pt.get_terminal_width(pad=0)
        self._scrollx = term_width

        if max_line_len and max_line_len < term_width * 1.5:
            self._scrollx = term_width // 5

    def open(self, filename: str) -> None:
        super().spawn(
            f"-# {self._scrollx}",
            "-R",
            filename,
            wait=True,
        )

    def _build_env(self) -> dict:
        env = super()._build_env()
        env.pop("LESSOPEN", None)
        return env
