# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os.path
import typing as t
from functools import update_wrapper

import pytermor as pt
import pytest

from . import get_logfile_path
from es7s.gtk.indicator import *
from es7s.shared import (
    UserConfigParams,
    init_config,
    UserConfig,
    init_logger,
    LoggerParams,
    get_logger, )


@pytest.fixture(scope="function", autouse=True)
def uconfig() -> UserConfig:
    yield init_config(UserConfigParams(default=True))


@pytest.fixture(scope="function", autouse=True)
def logger(request) -> UserConfig:
    os.environ.update(
        {
            "ES7S_DOMAIN": "GTK_TEST",
            "ES7S_TESTS": "true",
            "ES7S_TEST_NAME": "".join(request.node.name.split("[", 1)[:1]),
        }
    )
    try:
        verbosity = int(os.environ.get("ES7S_VERBOSITY", None))
    except TypeError:
        verbosity = 1

    logger = init_logger(
        params=LoggerParams(
            verbosity,
            out_stderr=False,
            out_syslog=False,
            out_file=get_logfile_path('gtk'),
        )
    )
    logger.info("=" * 80)
    logger.info(request.node.name)
    logger.info("-" * 80)
    yield logger

    try:
       logger.flush()
    except pt.exception.NotInitializedError:
        pass


F = t.TypeVar("F", bound=t.Callable[..., t.Any])


def log(func: F) -> F:
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            get_logger().exception(e)
            raise

    return update_wrapper(t.cast(F, wrapper), func)


class TestIcons:
    @pytest.mark.parametrize(
        "indicator_cls",
        [
            IndicatorManager,

            IndicatorCpuLoad,
            IndicatorDisk,
            IndicatorDocker,
            IndicatorFanSpeed,
            IndicatorMemory,
            IndicatorNetworkUsage,
            IndicatorShocks,
            IndicatorSystemCtl,
            IndicatorTemperature,
            IndicatorTimestamp,
        ],
    )
    @log
    def test_icon_files_match_selectors(self, indicator_cls: type[IIndicator]):
        if indicator_cls == IndicatorManager:
            indicator = indicator_cls([])
        else:
            indicator = indicator_cls()

        selector = indicator._icon_selector
        requests = selector.icon_names_set

        if selector.subpath:
            file_list = [f.name for f in selector.theme_path.iterdir()]
            files = {*filter(lambda f: not f.startswith('.'), file_list)}
            missing = (requests - files)
            unused = (files - requests)
            assert not missing, "Missing icon files"
            assert not unused, "Unused icon files"
        else:
            assert len(requests), "No icons provided"

        for icon in requests:
            path = selector.get_icon_path(icon)
            if not os.path.exists(path):
                raise AssertionError(f'Path does not exist: {path!r}')
