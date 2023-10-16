# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from ipaddress import IPv4Address, IPv6Address

from .dto import NetworkCountryInfo
from .requester import Requester


class GeoIpResolver:
    def __init__(self):
        self._request_fields = [
            "status",
            "message",
            *NetworkCountryInfo.response_field_names_list(),
        ]
        self.URL_TEMPLATE = "http://ip-api.com/json/%s?fields=%s"
        self.TIMEOUT = 10

    def get_url(self, ip: IPv4Address | IPv6Address = None) -> str:
        return self.URL_TEMPLATE % (str(ip or ""), (",".join(self._request_fields)))

    # requests.Response
    def handle_response(self, response) -> NetworkCountryInfo:
        data = response.json()
        if data.get("status") != "success":
            raise RuntimeError(f"Resolver service error: {data.get('message')}")
        filtered = {
            dto_f: data.get(resp_f)
            for dto_f, resp_f in NetworkCountryInfo.dto_to_response_fields_map().items()
        }
        return NetworkCountryInfo(**filtered)

    def make_request(self, ip: IPv4Address | IPv6Address = None) -> NetworkCountryInfo:
        resp = Requester().make_request(self.get_url(ip), self.TIMEOUT)
        return self.handle_response(resp)
