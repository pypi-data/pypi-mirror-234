# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from subprocess import CalledProcessError, CompletedProcess

from es7s.shared import SystemCtlInfo
from ._base import DataProvider
from es7s.shared import get_logger, run_subprocess


class SystemCtlProvider(DataProvider[SystemCtlInfo]):
    def __init__(self):
        super().__init__("systemctl", "systemctl", poll_interval_sec=30.0)

    def _collect(self) -> SystemCtlInfo:
        status_maxlen = 255
        try:
            cp: CompletedProcess = run_subprocess("systemctl", "is-system-running", check=False)
        except CalledProcessError as e:
            get_logger().exception(e)
            return SystemCtlInfo(ok=False, status=str(e)[:status_maxlen])

        status_lines = (cp.stdout or cp.stderr or "").splitlines()
        status = " ".join(status_lines)[:status_maxlen]
        ok = (status_lines or [""])[0] == "running"

        if not ok:
            try:
                cp = run_subprocess(
                    "systemctl",
                    "list-units",
                    "--failed",
                    "--no-pager",
                    "--no-legend",
                    "--plain",
                    check=False,
                )
                if cp.stdout:
                    status += "\n" + cp.stdout
            except Exception as e:
                get_logger().exception(e)

        return SystemCtlInfo(status, ok)
