# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t

from es7s.commons import (
    Regex,
)
from ._indicator_icons import (
    UpdatePathStyleAction,
    RemoveGroupAction,
    RemovePathAction,
    Variation,
    IndicatorIconBuilder,
    IndicatorColor,
    GenericSvgAction,
)


class DiskIndicatorIconBuilder(IndicatorIconBuilder):
    _TYPE = "disk"

    _BASE = [
        UpdatePathStyleAction(IndicatorColor.ACTIVE, Regex(R"path_usage_fill_\d")),
        UpdatePathStyleAction(IndicatorColor.BACKGROUND, "path_io_indicator"),
        UpdatePathStyleAction(IndicatorColor.DEFAULT, "path_outer_border"),
        UpdatePathStyleAction(IndicatorColor.NOOP, "path_usage_fill_over"),
    ]

    _VARIATIONS = [
        # -BUSY-----------------------------------------------------------------------
        [
            Variation("low", UpdatePathStyleAction(IndicatorColor.DEFAULT, "path_io_indicator")),
            Variation("medium", UpdatePathStyleAction(IndicatorColor.ACTIVE, "path_io_indicator")),
            Variation(
                "high",
                UpdatePathStyleAction(IndicatorColor.WARN, "path_io_indicator"),
                UpdatePathStyleAction(IndicatorColor.WARN_DARK, "path_outer_border"),
            ),
            Variation(
                "max",
                UpdatePathStyleAction(IndicatorColor.ERROR, "path_io_indicator"),
                UpdatePathStyleAction(IndicatorColor.ERROR_DARK, "path_outer_border"),
            ),
        ],
        # -USAGE-------------------------------------------------------------------------
        [  # @REFINE duplicated definitions
            Variation("0", RemoveGroupAction("layer_usage")),
            Variation("10", RemovePathAction(Regex("path_usage_fill_[^1]"))),
            Variation("20", RemovePathAction(Regex("path_usage_fill_[^2]"))),
            Variation("30", RemovePathAction(Regex("path_usage_fill_[^3]"))),
            Variation("40", RemovePathAction(Regex("path_usage_fill_[^4]"))),
            Variation("50", RemovePathAction(Regex("path_usage_fill_[^5]"))),
            Variation("60", RemovePathAction(Regex("path_usage_fill_[^6]"))),
            Variation("70", RemovePathAction(Regex("path_usage_fill_[^7]"))),
            Variation("80", RemovePathAction(Regex("path_usage_fill_[^8]"))),
            Variation(
                "90",
                RemovePathAction(Regex("path_usage_fill_[^9]")),
                UpdatePathStyleAction(IndicatorColor.WARN, "path_usage_fill_9"),
            ),
            Variation(
                "92",
                RemovePathAction(Regex("path_usage_fill_[^a]")),
                UpdatePathStyleAction(IndicatorColor.WARN, "path_usage_fill_a"),
            ),
            Variation(
                "95",
                RemovePathAction(Regex("path_usage_fill_[^b]")),
                UpdatePathStyleAction(IndicatorColor.WARN, "path_usage_fill_b"),
            ),
            Variation(
                "98",
                RemovePathAction(Regex("path_usage_fill_[^b]")),
                UpdatePathStyleAction(IndicatorColor.ERROR, "path_usage_fill_b"),
            ),
            Variation(
                "99",
                RemovePathAction(Regex("path_usage_fill_[^c]")),
                UpdatePathStyleAction(IndicatorColor.ERROR, "path_usage_fill_c"),
            ),
            Variation(
                "100",
                RemoveGroupAction("layer_usage"),
                RemovePathAction("path_io_indicator"),
                UpdatePathStyleAction(IndicatorColor.ERROR, "path_usage_fill_over"),
            ),
        ],
    ]

    def _get_type(self) -> str:
        return self._TYPE

    def _get_base_actions(self) -> t.Iterable[GenericSvgAction]:
        return self._BASE

    def _get_variation_lists(self) -> t.Iterable[t.Iterable[Variation]]:
        return self._VARIATIONS
