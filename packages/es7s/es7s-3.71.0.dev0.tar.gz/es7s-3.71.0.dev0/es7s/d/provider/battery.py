# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import abc
import os
import re
from abc import abstractmethod
import typing as t

import psutil

from ._base import DataProvider
from es7s.shared import DataCollectionError
from es7s.shared import get_logger, run_subprocess, BatteryInfo


class BatteryProvider(DataProvider[BatteryInfo]):
    def __init__(self):
        super().__init__('battery', "battery")

    def _collect(self) -> BatteryInfo:
        for extractor in self._extractors():
            get_logger().debug(f"Invoking {extractor}")
            try:
                return extractor.extract()
            except Exception as e:
                get_logger().info(f"Extractor failed: {e}")
                continue
        raise DataCollectionError("Failed to get battery level info")

    def _extractors(self) -> t.Iterator[_IExtractor]:
        yield _PsutilExtractor()
        yield _UpowerExtractor()
        yield _ManualExtractor()


class _IExtractor(metaclass=abc.ABCMeta):
    @abstractmethod
    def extract(self) -> BatteryInfo:
        raise NotImplementedError


class _PsutilExtractor(_IExtractor):
    def extract(self) -> BatteryInfo:
        s = psutil.sensors_battery()
        return BatteryInfo(
            s.percent,
            s.power_plugged,
            s.secsleft,
        )


class _UpowerExtractor(_IExtractor):
    def extract(self) -> BatteryInfo:
        battery_path = self._get_battery_path()
        battery_info = self._extract_battery_info(battery_path)
        return battery_info

    def _get_battery_path(self) -> str | None:
        p = run_subprocess("upower", "-e", check=True)

        for line in p.stdout.splitlines():
            if re.search(r"(battery)|(BAT\d+)", line):
                get_logger().debug(f"Got battery path: {line}")
                return line.strip()
        raise RuntimeError("No battery info found in upower listing")

    def _extract_battery_info(self, battery_path: str) -> BatteryInfo:
        p = run_subprocess("upower", "-i", battery_path, check=True)
        result = BatteryInfo()

        for line in p.stdout.splitlines():
            if match := re.fullmatch(r"\s*percentage:\s*([0-9,.]+)%\s*", line):
                get_logger().debug(f'Found percentage line: "{line}"')
                result.level = int(match.group(1))
            elif match := re.fullmatch(r"\s*state:\s*(.+)\s*", line):
                get_logger().debug(f'Found state line: "{line}"')
                result.is_charging = map_state_to_is_charging(match.group(1))
        return result


class _ManualExtractor(_IExtractor):
    def extract(self) -> BatteryInfo:
        path_tpl = "/sys/class/power_supply/BAT{:d}/{:s}"
        results = {k: None for k in ["status", "capacity"]}
        logger = get_logger()

        for idx in [0, 1]:  # https://askubuntu.com/a/309146/1498488
            for filename in results.keys():
                path = path_tpl.format(idx, filename)
                logger.debug(f"Requesting path: {path}")

                if not os.path.isfile(path):
                    logger.debug(f"Path not found: {path}")
                    continue

                with open(path, "rt") as file:
                    results[filename] = (file.readlines(1))[0].strip()
                    logger.debug(f'Found {filename} line: "{results[filename]}"')

        if all(results.values()):
            return BatteryInfo(
                level=int(results["capacity"].strip()),
                is_charging=map_state_to_is_charging(results["status"]),
            )
        raise RuntimeError("No battery info found in predefined paths")


CHARGING_MSGS = [
    "full",
    "fully-charged",
    "charging",
]
NOT_CHARGING_MSGS = [
    "discharging",
    "not-charging",
    "pending-charge",
]


def map_state_to_is_charging(val: str) -> bool | None:
    val_opt = re.sub("[^a-z]", "-", val.lower())
    if val_opt in CHARGING_MSGS:
        return True
    if val_opt in NOT_CHARGING_MSGS:
        return False
    get_logger().warning(f'Unknown battery state value: "{val}"')
    return None
