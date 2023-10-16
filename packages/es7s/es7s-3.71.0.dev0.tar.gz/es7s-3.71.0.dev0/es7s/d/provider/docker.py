# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re

from ._base import DataProvider
from es7s.commons import UNIT_SEPARATOR
from es7s.shared import DockerStatus, DockerInfo, run_subprocess
from es7s.shared import DOCKER_PATH


class DockerStatusProvider(DataProvider[DockerInfo]):
    SEP = UNIT_SEPARATOR
    DOCKER_ARGS = [
        "ps",
        '--format="{{.Status}}{{"' + SEP + '"}}{{.Names}}{{"' + SEP + '"}}"',
    ]
    STATUS_FILTER_TEMPLATE = "--filter=status={:s}"
    STATUS_CHANGE_DELTA_REGEX = re.compile(r"(less than a)|(\d+) second", flags=re.IGNORECASE)

    STATUS_TO_SEARCH_REGEX_MAP = {
        "running": re.compile('^"up', re.IGNORECASE),
        "restarting": re.compile('^"restarting', re.IGNORECASE),
    }

    def __init__(self):
        super().__init__("docker", "docker")

    def _collect(self) -> DockerInfo:
        filter_args = [
            self.STATUS_FILTER_TEMPLATE.format(status)
            for status in self.STATUS_TO_SEARCH_REGEX_MAP.keys()
        ]
        args = [DOCKER_PATH, *self.DOCKER_ARGS, *filter_args]
        cp = run_subprocess(*args, check=True)
        lines = (cp.stdout or "").splitlines()

        result = DockerInfo()
        for status, search_regex in self.STATUS_TO_SEARCH_REGEX_MAP.items():
            status_dto = DockerStatus()
            result[status] = status_dto

            for line in lines:
                if line.count(self.SEP) != 2 or not search_regex.match(line):
                    continue
                status, names, _ = line.split(self.SEP)
                status_dto.match_amount += 1
                status_dto.container_names.extend(s.strip() for s in names.split(","))
                if status_change_delta_m := self.STATUS_CHANGE_DELTA_REGEX.search(status):
                    if status_change_delta_m.group(1):
                        status_dto.updated_in_prev_tick = True
                    elif status_change_secs := status_change_delta_m.group(2):
                        status_dto.updated_in_prev_tick = (
                            int(status_change_secs) <= self._poll_interval_sec
                        )
        return result
