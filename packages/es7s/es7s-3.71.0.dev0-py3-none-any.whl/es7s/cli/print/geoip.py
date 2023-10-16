# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from dataclasses import asdict
from ipaddress import IPv4Address, IPv6Address

import pytermor as pt

from .._base_opts_params import CMDTYPE_BUILTIN, IpParamType
from .._decorators import catch_and_log_and_exit, cli_argument, cli_command
from es7s.shared import Styles, get_stdout
from es7s.shared import format_variable


@cli_command(
    name=__file__,
    short_help="get associated country for IP address",
    type=CMDTYPE_BUILTIN,
)
@cli_argument("ADDRESS", type=IpParamType(), required=False)
@catch_and_log_and_exit
class invoker:
    """
    @TODO fix click ARGUMENT output
    """

    def __init__(self, **kwargs):
        from es7s.shared import GeoIpResolver
        self._geo_ip_resolver = GeoIpResolver()
        self._run(**kwargs)

    def _run(self, address: IPv4Address | IPv6Address = None):
        kv = asdict(self._geo_ip_resolver.make_request(address))
        longest_key = max(len(k) for k in kv.keys())
        for k, v in kv.items():
            get_stdout().echo_rendered(
                pt.Fragment(k.rjust(longest_key), Styles.VARIABLE_KEY_FMT)
                + pt.Fragment(": ", Styles.VARIABLE_PUNCT_FMT)
                + format_variable(v)
            )
