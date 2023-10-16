#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
# shellcheck disable=SC2120

_log() {
    local channel=${ES7S_SHOCKS_CHANNEL:-manual}
    logger -p local7."${1:-debug}" -t "es7s/shocks.${channel}[$$]"
}

_shocks.usage(){
    cat <<-EOF
	⚡ es7s/shocks
	  s[sh] s[ocks] proxy tunnel

	USAGE:
	  shocks SPEC [USERNAME@]HOSTNAME [ARGS...]

	ARGUMENTS:
	  SPEC        Specification of local port binding for SOCKS proxy, e.g. "-D1080".
	  USERNAME    Remote server login
	  HOSTNAME    Remote server hostname/IP that will be used as a relay
	  ARGS        Extra arguments for (auto)ssh, e.g. "-i <PATH_TO_SSH_KEY>"

	ENVIRONMENT:
	  ES7S_SHOCKS_MONITOR
	              Non-empty string enables real-time monitoring of the connection
	              between local SOCKS proxy and the relay. The value should be
	              a name or a name mask of relay network interface the monitor
	              should connect to, e.g. "vpn0" or "eth*".

	DEPENDENCIES:
	  Requires installed 'ssh' and 'autossh' utilities.

	EXAMPLES:
	  shocks -D1080 coolvps.com
	              Creates a port forwarding from localhost:1080 to the remote
	              host which tunnels the traffic through.

EOF
}

_shocks.main() {
    local SPEC=${1:?Port specification required}
    local DEST=${2:?Destination required}

    local MODE_ARGS=(-N)  # no remote commands, background mode
    [[ -n $ES7S_SHOCKS_MONITOR ]] && \
        MODE_ARGS=(-t "/usr/bin/env ES7S_NO_AUTOSTART=true \$SHELL -c 'bmon -p $ES7S_SHOCKS_MONITOR --use-si'")

    autossh "$DEST" -v "$SPEC" "${MODE_ARGS[@]}" "${@:3}" 2> >(_log)
    #/bin/ssh "$DEST" -v "$SPEC" "${MODE_ARGS[@]}" "${@:3}" 2> >(_log)
}

[[ $* =~ (--)?help ]] && _shocks.usage && exit
_shocks.main "$@"
