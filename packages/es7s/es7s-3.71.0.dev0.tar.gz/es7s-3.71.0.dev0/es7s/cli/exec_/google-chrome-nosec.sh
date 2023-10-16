#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
__SELF="$(basename "$0" | sed -Ee 's/\..+$//')"
__USAGE="$(cat <<-EOL
Launch Google Chrome with disabled web security for local development (solves the
problem with local self-signed TLS certificates).

Usage:
    ${__SELF} [--help]
EOL
)"

__main() {
    nohup google-chrome --disable-web-security --user-data-dir=/tmp/chrome_dev_test > "/tmp/nohup.$(date +%s).out"
}

[[ $# -gt 1 ]] || [[ $* =~ (--)?help ]] && echo "$__USAGE" && exit
(__main &)
