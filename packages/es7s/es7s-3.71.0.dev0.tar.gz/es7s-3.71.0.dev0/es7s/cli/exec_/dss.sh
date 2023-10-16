#!/bin/bash

USAGE="
  Take a screenshot after 3-second delay.

  Usage:
    $(basename "$0")
"

[[ $* =~ (--)?help ]] && { printf "$USAGE" ; exit ; }

target="$HOME"
user="$(id -nu)"
host="$(hostname)"

if command -v es7s >/dev/null ; then
    es7s exec notify "es7s/core" "[~3s] Capture to: $target"
fi

cd $target || exit 127
scrot '%Y-%m-%d_%H.%M.%S_'$user@$host'_$wx$h.png' -pc -d3 -e 'xdg-open $f'
