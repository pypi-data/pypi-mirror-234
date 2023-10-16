# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import logging
from dataclasses import dataclass

import pytermor as pt
from pytermor import DynamicColor
from pytermor.color import ExtractorT

from .log import get_logger
from .uconfig import UserConfig
from .uconfig import get_merged as get_merged_uconfig


@dataclass(frozen=True)
class _ThemeColors:
    theme: pt.Color
    theme_bright: pt.Color
    monitor_separator: pt.Color


class _ThemeColorResolver:
    _REGULAR_TO_BRIGHT_COLOR_MAP = {
        pt.cv.BLACK: pt.cv.GRAY,
        pt.cv.RED: pt.cv.HI_RED,
        pt.cv.GREEN: pt.cv.HI_GREEN,
        pt.cv.YELLOW: pt.cv.HI_YELLOW,
        pt.cv.BLUE: pt.cv.HI_BLUE,
        pt.cv.MAGENTA: pt.cv.HI_MAGENTA,
        pt.cv.CYAN: pt.cv.HI_CYAN,
        pt.cv.WHITE: pt.cv.HI_WHITE,
    }

    def resolve(self) -> _ThemeColors:
        return _ThemeColors(
            self.get_theme_color(),
            self.get_theme_bright_color(),
            self.get_monitor_separator_color(),
        )

    def get_color_name(self) -> str:
        return get_merged_uconfig().get("general", "theme-color", fallback="red")

    def get_theme_color(self) -> pt.Color:
        try:
            return pt.resolve_color(self.get_color_name())
        except (LookupError, TypeError):
            return pt.cv.RED

    def get_theme_bright_color(self) -> pt.Color:
        logger = logging.getLogger(__package__)

        def resolve_with_map(origin: pt.Color16) -> pt.Color:
            result = self._REGULAR_TO_BRIGHT_COLOR_MAP.get(origin)
            logger.debug(f"Resolved bright color using preset map: {result}")
            return result

        def resolve_by_shift(origin: pt.Color) -> pt.Color:
            hue, sat, val = origin.hsv
            val += 0.40
            if val > 1.0:
                # brightness increase by saturation decrease when value is max
                sat = max(0, sat - (val - 1.0) / 2)
                val = 1.0

            result_hsv = pt.HSV(hue, sat, val)
            msg = f"Resolving bright color via S/V channel shift: {origin.hsv} -> {result_hsv}"
            get_logger().debug(msg)
            return pt.ColorRGB(result_hsv)

        try:
            theme_color16 = pt.resolve_color(self.get_color_name(), pt.Color16)
            logger.debug(f"Theme color is valid Color16: {theme_color16}")
            if theme_color16 in self._REGULAR_TO_BRIGHT_COLOR_MAP.keys():
                return resolve_with_map(theme_color16)
        except LookupError:
            pass

        theme_color = self.get_theme_color()
        if isinstance(theme_color, pt.Color256):
            logger.debug(f"Theme color is valid Color256: {theme_color}")
            if theme_color16 := theme_color._color16_equiv:
                if theme_color16 in self._REGULAR_TO_BRIGHT_COLOR_MAP.keys():
                    return resolve_with_map(theme_color16)

        logger.debug(f"No mapped bright color: {theme_color}")
        return resolve_by_shift(theme_color)

    def get_monitor_separator_color(self) -> pt.Color:
        hue, _, _ = self.get_theme_color().hsv
        return pt.ColorRGB(pt.HSV(hue, 0.59, 0.50))


_resolver = _ThemeColorResolver()


class ThemeColor(DynamicColor[_ThemeColors]):
    _DEFERRED = True

    @classmethod
    def _update_impl(cls, **kwargs) -> _ThemeColors:
        try:
            return _resolver.resolve()
        except pt.exception.NotInitializedError:
            UserConfig.add_init_hook(cls.update)
            raise

    def __init__(self, extractor: ExtractorT[_ThemeColors] = None):
        super().__init__(extractor or 'theme')
