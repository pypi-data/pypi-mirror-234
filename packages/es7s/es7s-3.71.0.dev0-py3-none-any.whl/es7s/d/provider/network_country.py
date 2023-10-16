# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from ._base import DataProvider
from es7s.shared import NetworkCountryInfo
from es7s.shared import GeoIpResolver


class NetworkCountryProvider(DataProvider[NetworkCountryInfo]):
    def __init__(self):
        self._resolver = GeoIpResolver()
        super().__init__("network-country", "network-country", 17.0)

    def _reset(self) -> NetworkCountryInfo:
        return NetworkCountryInfo()

    def _collect(self) -> NetworkCountryInfo:
        resp = self._make_request(self._resolver.get_url())
        dto = self._resolver.handle_response(resp)
        return dto
