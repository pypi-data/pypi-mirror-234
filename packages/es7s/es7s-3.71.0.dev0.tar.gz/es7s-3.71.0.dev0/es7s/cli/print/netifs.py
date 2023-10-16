# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import psutil
import typing as t

from .._decorators import cli_command


@cli_command(__file__, short_help="network interface list")
class invoker:
    """
    .
    """
    def __init__(self, **kwargs):
        self._run()

    def _run(self):
        def row(val: t.Iterable, pad=0, transfn=lambda s: s or '-') -> str:
            def make(tval):
                tval = [*tval]
                yield ' '*pad + tval.pop(0)[:18-pad].ljust(18-pad)
                yield from [cc[:16].ljust(16) for cc in tval[:-1]]
                yield tval[-1][:12].ljust(12)
            return ' '.join(make(transfn(v) for v in val))
        print(row(['network interface', 'address', 'net mask', 'broadcast', 'ptp', 'family'], 0, lambda v: v.upper()))
        print(row(6*['='*24], 0))
        for k in (ifs := psutil.net_if_addrs()):
            for c in ifs[k]:
                if ':' in c.address:
                    continue
                print(row([k, *[*c][1:], c.family.name], pad=1))
