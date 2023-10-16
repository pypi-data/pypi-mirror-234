# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import json
import os
from pathlib import Path

from .styles import Styles
from .exception import SubprocessExitCodeError
from .log import get_logger
from .io_ import get_stdout
from .sub import run_subprocess
from .path import DOCKER_PATH, GH_LINGUIST_PATH


class Linguist:
    @classmethod
    def get_lang_statistics(cls, path: Path|str, docker: bool, breakdown: bool) -> dict:
        args = cls._get_linguist_args(path, docker, breakdown)
        cpout = cls._invoke_linguist(args)
        return json.loads(cpout)

    @classmethod
    def _invoke_linguist(cls, args: list[str | Path]) -> str:
        cp = run_subprocess(*args, check=False)
        if cp.returncode != 0:
            if get_logger().setup.print_subprocess_stderr_data:
                get_stdout().echo_rendered(cp.stderr, Styles.ERROR)
            raise SubprocessExitCodeError(cp.returncode, args)
        return cp.stdout

    @classmethod
    def _get_linguist_args(cls, path: Path, docker: bool, breakdown: bool) -> list:
        opts = ['--json']
        if breakdown:
            opts += ['-b']

        if not docker:
            return [GH_LINGUIST_PATH, *opts, path]
        return [
            DOCKER_PATH,
            "run",
            "--rm",
            "-v",
            f"{path}:/data",
            "-w",
            "/data",
            "-u",
            f"{os.getuid()}:{os.getgid()}",
            "-t",
            "github-linguist",
            "github-linguist",
            *opts,
            "/data",
        ]
