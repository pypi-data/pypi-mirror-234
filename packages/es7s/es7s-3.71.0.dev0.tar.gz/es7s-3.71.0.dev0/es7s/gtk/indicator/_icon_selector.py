# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import abc
import importlib.resources
import itertools
import typing as t
from typing import OrderedDict

import pytermor as pt
from abc import abstractmethod
from collections.abc import Iterable
from functools import cached_property, lru_cache
from importlib.abc import Traversable
from pathlib import Path

from pytermor import LogicError

from es7s import APP_VERSION
from es7s.shared import RESOURCE_PACKAGE, get_logger
from es7s.commons import format_attrs

IST = t.TypeVar("IST", bound="IIconSelector")


class IconEnum(str, pt.ExtendedEnum):
    def __str__(self) -> str:
        return self.value


class IIconSelector(metaclass=abc.ABCMeta):
    def __init__(self, name_default: str | IconEnum = "apport-symbolic", subpath: str = "common"):
        self._name_default = name_default
        self._subpath = subpath
        self._demo_state = False
        self._demo_icon_idx = 0

    def select(self, *args) -> str | IconEnum | None:
        if self._demo_state:
            return self._select_demo_next()
        return None

    @property
    @abstractmethod
    def icon_names_set(self) -> set[str | IconEnum]:
        ...

    @property
    def name_default(self) -> str:
        return str(self._name_default)

    @property
    def subpath(self) -> str:
        return self._subpath

    @cached_property
    def theme_path(self) -> Traversable:
        icons_dir = Path(f"icons@{APP_VERSION}")
        if self._subpath:
            icons_dir /= self._subpath
        theme_path = importlib.resources.files(RESOURCE_PACKAGE).joinpath(icons_dir)
        get_logger().debug(f"Theme resource path: '{theme_path}'")
        return theme_path

    @lru_cache
    def get_icon_path(self, name: str | IconEnum = None) -> str:
        path = str(self.theme_path / (name or self.name_default))
        get_logger().debug(f"Resolving icon path: {path!r}")
        return path

    @cached_property
    def icon_names_sorted(self) -> list[str | IconEnum]:
        return sorted(self.icon_names_set)

    def get_icon_demo_state(self) -> bool:
        return self._demo_state

    def set_icon_demo_state(self, enabled: bool):
        self._demo_state = enabled and len(self.icon_names_set) > 0

    def _select_demo_next(self) -> str | IconEnum:
        self._demo_icon_idx += 1
        if self._demo_icon_idx >= len(self.icon_names_sorted):
            self._demo_icon_idx = 0
        return self.icon_names_sorted[self._demo_icon_idx]


class StaticIconEnum(IconEnum):
    WARNING = "warning.svg"


class StaticIconSelector(IIconSelector):
    def select(self, *args) -> str:
        if override := super().select():
            return override
        return self.name_default

    @cached_property
    def icon_names_set(self) -> set[str]:
        return {self.name_default}


class ThresholdMap(OrderedDict[int, str]):
    def __init__(self, *values: int, caution: int = None, alert: int = None, **mappings):
        if values and mappings:
            raise LogicError("Args only or kwargs only can be used, not both at the same time")
        if not values and not mappings:
            raise LogicError("Threshold map should contain at least one key-value mapping")

        super().__init__(
            {
                **{v: str(v) for v in reversed(sorted(values))},
                **{kv[1]: kv[0] for kv in sorted(mappings.items(), key=lambda kv: -kv[1])},
            }
        )
        self._min = self[min(self.keys())]

    def get_threshold_by_cv(self, carrier_value: float | None) -> str:
        if not carrier_value:
            return self._min
        for k, v in self.items():
            if carrier_value >= k:
                return v
        return self._min


class ThresholdIconSelector(IIconSelector):
    def __init__(
        self,
        *thresholds: ThresholdMap,
        subpath: str,
        path_dynamic_tpl: str,
        name_default: str | IconEnum = None,
        name_parts_default: tuple[str] = ('0',)
    ):
        """
        `name_default` has a priority over `name_parts_default`. Examples:

        >>> ThresholdIconSelector(ThresholdMap(), "subdir", path_dynamic_tpl="%s.svg", name_default="wait.svg")
        >>> ThresholdIconSelector(ThresholdMap(), "subdir", path_dynamic_tpl="%s.svg", name_parts_default=("0",))
        """
        self._path_dynamic_tpl = path_dynamic_tpl
        self._maps = [*thresholds]
        if not name_default:
            name_default = self._compose_path(*name_parts_default)
        super().__init__(name_default, subpath)

    def select(self, *carrier_value: float | None) -> str:
        if override := super().select():
            return override
        if (
            not self._maps
            or not self._path_dynamic_tpl
            or any(map(lambda cv: cv is None, carrier_value))
        ):
            return self.name_default
        return self._compose_path(
            *(self._maps[idx].get_threshold_by_cv(cv) for idx, cv in enumerate(carrier_value))
        )

    @cached_property
    def icon_names_set(self) -> set[str]:
        def _iter() -> Iterable[str]:
            for pts in itertools.product(*map(lambda m: [*m.values()], self._maps)):
                yield self._compose_path(*pts)

        return set(_iter())

    def _compose_path(self, *frames: str | None) -> str:
        try:
            return self._path_dynamic_tpl % frames
        except TypeError:
            get_logger().warning(
                f"Invalid icon path args: {self._path_dynamic_tpl!r}, {format_attrs(frames)}"
            )
