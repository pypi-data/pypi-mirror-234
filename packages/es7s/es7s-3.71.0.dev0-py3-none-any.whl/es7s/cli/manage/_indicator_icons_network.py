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
    IndicatorStyles,
    IndicatorColor,
    GenericSvgAction,
    IndicatorStyle,
)


class NetworkIndicatorIconBuilder(IndicatorIconBuilder):
    _TYPE =  "network"

    _BASE = [
        UpdatePathStyleAction(IndicatorColor.ACTIVE, Regex(R"path_arrow_\w+_fill_\d")),
        UpdatePathStyleAction(
            IndicatorStyle(stroke=IndicatorColor.DEFAULT), Regex(R"path_arrow_\w+_stroke")
        ),
        UpdatePathStyleAction(IndicatorColor.ACTIVE, "path_nc_inner"),
        UpdatePathStyleAction(IndicatorColor.DEFAULT, "path_nc_outer"),
        UpdatePathStyleAction(IndicatorColor.BACKGROUND, "path_vpn"),
        UpdatePathStyleAction(IndicatorColor.DEFAULT, "path_vpn_border"),
    ]

    _VARIATIONS = [
        # -VPN----------------------------------------------------------------------------
        [
            Variation(None, RemoveGroupAction("layer_vpn", "layer_vpn_foreign")),
            Variation("vpn", RemoveGroupAction("layer_vpn_foreign")),
            Variation(
                "vpnw",
                RemoveGroupAction("layer_vpn_foreign"),
                UpdatePathStyleAction(IndicatorStyles.WARN, "path_vpn", "path_vpn_border"),
            ),
            Variation(
                "vpnf",
                RemoveGroupAction("layer_vpn"),
                UpdatePathStyleAction(IndicatorColor.VPN_FOREIGN, "path_vpn_foreign"),
                UpdatePathStyleAction(
                    IndicatorColor.VPN_FOREIGN_ACCENT, "path_vpn_foreign_border", "path_nc_outer"
                ),
                UpdatePathStyleAction(
                    IndicatorStyle(stroke=IndicatorColor.VPN_FOREIGN_ACCENT),
                    Regex(R"path_arrow_\w+_stroke"),
                ),
            ),
        ],
        # -UPLOAD-------------------------------------------------------------------------
        [  # @TODO duplicated definitions with NetworkIconSelector
            Variation("0", RemoveGroupAction("layer_arrow_up_fill")),
            Variation("1", RemovePathAction(Regex("path_arrow_up_fill_[^1]"))),
            Variation("2", RemovePathAction(Regex("path_arrow_up_fill_[^2]"))),
            Variation("3", RemovePathAction(Regex("path_arrow_up_fill_[^3]"))),
            Variation("4", RemovePathAction(Regex("path_arrow_up_fill_[^4]"))),
            Variation("5", RemovePathAction(Regex("path_arrow_up_fill_[^5]"))),
            Variation(
                "6",
                RemovePathAction(Regex("path_arrow_up_fill_[^6]")),
                UpdatePathStyleAction(
                    IndicatorStyles.FULL, "path_arrow_up_fill_6", "path_arrow_up_stroke"
                ),
            ),
            Variation(
                "w",
                RemovePathAction(Regex("path_arrow_up_fill_[^6]")),
                UpdatePathStyleAction(
                    IndicatorStyles.WARN, "path_arrow_up_fill_6", "path_arrow_up_stroke"
                ),
            ),
            Variation(
                "e",
                RemovePathAction(Regex("path_arrow_up_fill_[^6]")),
                UpdatePathStyleAction(
                    IndicatorStyles.ERROR, "path_arrow_up_fill_6", "path_arrow_up_stroke"
                ),
            ),
        ],
        # -DOWNLOAD-----------------------------------------------------------------------
        [
            Variation("0", RemoveGroupAction("layer_arrow_down_fill")),
            Variation("1", RemovePathAction(Regex("path_arrow_down_fill_[^1]"))),
            Variation("2", RemovePathAction(Regex("path_arrow_down_fill_[^2]"))),
            Variation("3", RemovePathAction(Regex("path_arrow_down_fill_[^3]"))),
            Variation("4", RemovePathAction(Regex("path_arrow_down_fill_[^4]"))),
            Variation("5", RemovePathAction(Regex("path_arrow_down_fill_[^5]"))),
            Variation(
                "6",
                RemovePathAction(Regex("path_arrow_down_fill_[^6]")),
                UpdatePathStyleAction(
                    IndicatorStyles.FULL, "path_arrow_down_fill_6", "path_arrow_down_stroke"
                ),
            ),
            Variation(
                "w",
                RemovePathAction(Regex("path_arrow_down_fill_[^6]")),
                UpdatePathStyleAction(
                    IndicatorStyles.WARN, "path_arrow_down_fill_6", "path_arrow_down_stroke"
                ),
            ),
            Variation(
                "e",
                RemovePathAction(Regex("path_arrow_down_fill_[^6]")),
                UpdatePathStyleAction(
                    IndicatorStyles.ERROR, "path_arrow_down_fill_6", "path_arrow_down_stroke"
                ),
            ),
        ],
        # -NETCOMM------------------------------------------------------------------------
        [
            Variation(None, RemoveGroupAction("layer_nc")),
            Variation("nc"),
        ],
    ]

    def _get_type(self) -> str:
        return self._TYPE

    def _get_base_actions(self) -> t.Iterable[GenericSvgAction]:
        return self._BASE

    def _get_variation_lists(self) -> t.Iterable[t.Iterable[Variation]]:
        return self._VARIATIONS
