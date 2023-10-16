#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
# shellcheck disable=SC2059

.s() { printf "\e[%sm" "$(tr -s ' ' \; <<<"$*")"; }
_f=$(.s 0)

DEST_PATH=/etc/systemd/system

SYSTEMD_PATHS=(
    /etc/systemd/system
    /usr/local/lib/systemd/system
    /usr/lib/systemd/system
)

declare -a SERVICES
declare services_num=0

__main() {
    # shellcheck disable=SC2178
    SERVICES=$(__find_services)
    services_num=$(wc -w <<<"${SERVICES[*]}")

    printf "Services found: $(.s 1)%s$_f\n" "$services_num"

    __uninstall
    __install

    printf "$(.s 32 1)DONE$_f\n"
}

__find_services() {
    local source_path="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
    find "$source_path" -type f \
        -regextype posix-extended \
        -regex '.+\.(service|target)' \
        -print0 |
        xargs -0 -n1 |
        sort -k1n -t.
}

__uninstall() {
    printf "$(.s 33)Uninstall$_f current $(.s 1)es7s$_f services?"
    __prompt || return

    for svcpath in ${SERVICES[*]}; do
        __uninstall_service "$svcpath"
    done
    __scall systemctl daemon-reload
    __scall systemctl reset-failed
}
__uninstall_service() {
    local svcpath="${1:?Required}"
    local svcfile="$(basename "$svcpath")"
    local svcname="${svcfile#*.}"

    printf "Uninstalling $(.s 1)%s$_f\n" "$svcname"

    set -e
    if __callq systemctl -q is-active "$svcname"; then __scall systemctl stop "$svcname"; fi
    if __callq systemctl -q is-enabled "$svcname"; then __scall systemctl disable "$svcname"; fi

    for systemd_path in ${SYSTEMD_PATHS[*]}; do
        local realpath="$systemd_path/$svcname"
        [[ -f "$realpath" ]] && __scall rm "$realpath"
    done
    set +e
}

__install() {
    local idx=1
    for svcpath in ${SERVICES[*]}; do
        __install_service "$svcpath" "$((idx++))"
    done
    __scall systemctl daemon-reload
}
__install_service() {
    local svcpath="${1:?Required}"
    local svcfile="$(basename "$svcpath")"
    local svcname="${svcfile#*.}"
    local idx="${2:-?}"

    echo
    printf "$(.s 34)[$(.s 1)%2d$(.s 22)/%2d]$_f Install $(.s 1)%s$_f?" \
                          "$idx"   "$services_num"    "${svcname/.*/}"
    __prompt || return 0

    set -e
    __scall cp "$svcpath" "$DEST_PATH/$svcname"
    __scall sed "$DEST_PATH/$svcname" -i -Ee "s/%UID/$(id -u)/g; s/%USER/$(id -un)/g"
    __scall systemctl enable "$svcname"
    if [[ ! $svcname =~ @ ]]; then
        __scall systemctl restart "$svcname"
        __scall systemctl status "$svcname" --lines 5 --no-pager --quiet
    fi
    set +e
}

__prompt() {
    local msg="${1:-} (y/n/q): "
    while true; do
        read -n1 -sr -p "$msg" yn
        echo
        case $yn in
            [Yy]*) return 0 ;;
            [Nn]*) return 1 ;;
            [Qq]*)   exit 1 ;;
                *) continue ;;
        esac
    done
}

__fmtcmd() { printf "$(.s 34 1)>$_f $(.s 34 2)%s$_f" "$*"; }
__callq() { "$@" &>/dev/null ; }
__call()  { __fmtcmd "$@" ; echo ; "$@" ; }
__callp() { __fmtcmd "$@" ; __prompt "Continue?" && "$@" ; }
__scall()  {  __call sudo "$@" ; }
__scallp() { __callp sudo "$@" ; }

echo -ne "$(.s 30 103 1)TODO: make appropriate .env files in .es7s dir for shocks\e[0K "
read -sn1 -p "(y/y):" && echo "$_f"
__main "$@"
