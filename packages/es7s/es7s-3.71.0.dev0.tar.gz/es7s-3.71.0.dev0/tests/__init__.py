# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from datetime import datetime
from pathlib import Path

_START_TIME = datetime.now().strftime('%Y-%0m-%0eT%H:%M:%S')


def get_logfile_path(suffix: str) -> str:
    return str(Path(__file__).parent.parent / 'logs' / f'testrun.{_START_TIME}.{suffix}.log')
