#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------

_main() {
    local key="$1"
    [[ $key == ESC ]] && key=$'\x1b'
    [[ $key == TAB ]] && key=$'\t'
    printf %s "$key" | xsel --clipboard
    xvkbd -xsendevent -text '\Cv'
}

[[ $# -lt 1 ]] || [[ $* =~ (--)?help ]] && exit
_main "$@"
