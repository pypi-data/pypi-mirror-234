#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
# shellcheck disable=SC2059,SC2120

function _ww () {
    local width=$COLUMNS
    [[ -z $width ]] && width=$(tput cols 2>/dev/null)
    [[ -z $width ]] && width=$(stty size 2>/dev/null | cut -f2 -d" " )
    printf %s "${width:-80}"
}
function _date() { printf "[$(date '+%H:%M:%S')]" ; }
function _sep() { printf "${_gy}%${1:-40}s${_f}\n" "" | tr " " - ; }
function _pp_desc() { printf "${1}" ; }
function _pgrek_prompt() {
    printf "$(_date) $last_result\n"
    while true; do
        read -N1 -r -p "$opts> " input
        case $input in
         [Hh?]*) printf    "\r\e[0K$opts> ${_b}h${_f}${_d}[elp]${_f}\n"
                 printf    "$(_sep)$keys\n$(_date) $last_result\n"
                 continue ;;
          [Tt]*) printf    "\r\e[0K$opts> ${_b}${_y}t${_d}[erm]${_f}\n"   ; return 1 ;;
          [Kk]*) printf    "\r\e[0K$opts> ${_b}${_r}k${_d}[ill]${_f}\n"   ; return 2 ;;
   [$'\x04'Rr]*) printf    "\r\e[0K$opts> ${_b}r${_f}${_d}[epeat]${_f}\n" ; return 3 ;;
       [$'\n']*) printf "\e[1F\e[0K$opts> ${_b}r${_f}${_d}[epeat]${_f}\n" ; return 3 ;;
          [Qq]*) printf    "\r\e[0K$opts> ${_b}q${_f}${_d}[uit]${_f}\n"   ; return 0 ;;
              *) printf    "\b${_rbg}${_b}${input:0:1}${_f}${_d}"
                 printf    "(press h to see help)${_f}\r"
                 sleep 0.1 ;;
        esac
    done
}

function _pgrek_iter() {
    local cmd=("pgrep" "-ifa" "$@")
    local cmdkill cmd_out pids pids_raw pids_exclude pg_exc pp_exc
    local pids_amount pids_fmt

    _sep
    format_cmd_run "${cmd[*]}"
    pids_raw="$("${cmd[@]}" 2> >(sed -Ee 's/^/'$_r'  /; s/$/'$_f'/;' >&2))"
    pg_exc=$?
    format_cmd_exit "$pg_exc"

    pids_exclude="${0//\//\\\/}|^$$|^$PPID"
    pids="$(
        sed -E <<<"$pids_raw" -e '/('$pids_exclude')/d' |
        tee /dev/stderr 2> >(
            sed -Ee 's/^([0-9]+)/\x1b[m\t&\t/; 1s/^/\x1b[m\t_______\t\n/' |
            column -ts$'\t' |
            sed -Ee '1d; s/^\x1b\[m(\s*)(\S+)(\s*)(\s\s\s)/\1\3\2\4/' |
            sed -Ee 's/^(\s\s.{3})(.{3})(.{3})(\s+)/\x1b[31m\1\x1b[91m\2\3\x1b[39m\4/' >&2
        ) |
        cut -d' ' -f1 |
        tr $'\n' ' '
    )"
    pids_amount="$(wc -w <<<"${pids}")"
    sed -E <<<"$pids_raw" -e "/($pids_exclude)/!d; s/^([0-9]+)/$_d\t&$_f$_gy$_d\t/; s/$/$_f/"  | column -ts$'\t'
    echo

    pids_fmt="" ; [[ $pids_amount != 0 ]] && pids_fmt=${_y}
    last_result="$(printf "Matched ${_b}${pids_fmt}${pids_amount}${_f} PID(s)")"

    if _pgrek_prompt >&2 ; then
        return 126
    else
        pp_exc=$?

        if [[ $pp_exc -eq 1 ]] ; then cmdkill="kill $pids"
        elif [[ $pp_exc -eq 2 ]] ; then cmdkill="kill -9 $pids"
        fi
        [[ $pp_exc -eq 3 ]] && return 0
        [[ $pids_amount -eq 0 ]] && _sep &&  printf "No active PIDs, skipping\n" && echo && return 0

        _sep
        format_cmd_run "${cmdkill}"
        cmd_out="$($cmdkill 2> >(sed -Ee "/^$/d; s/^/    $_r/" | tr -d $"\n"))"
        format_cmd_exit "$?"
    fi
}
function format_cmd_run() {
    printf "${_be} ▶  ${*}${_f}\n"
}
function format_cmd_exit() {
    if [[ $1 -eq 0 ]] ; then
        printf "${_gn} ⏺ ${_f} Exit code ${_b}$1${_f}\n"
    else
        printf "${_whbg}${_r}${_i} × ${_f}${_r} Exit code ${_hr}${_b}$1${_f}\n"
    fi
    if [[ -n "$cmd_out" ]] ; then
        printf "$cmd_out\n"
    fi
    echo
 }

function _main() {  # [pgre]p and p[k]ill
    local _f=$'\e[m' _b=$'\e[1m' _be=$'\e[34m' _y=$'\e[33m' \
          _r=$'\e[31m' _d=$'\e[2m' _i=$'\e[7m' _fb=$'\e[22m' \
          _w=$'\e[97m' _u=$'\e[4m' _fu=$'\e[24m' _gy=$'\e[37m' \
          _gn=$'\e[32m' _hr=$'\e[91m' _actbg=$'\e[48;5;16;3m' _ff=$'\e[39m' \
          _rbg=$'\e[41m' _whbg=$'\e[48;5;231m'
    local opts="Select an action: (${_actbg}${_y}t${_ff}/${_r}k${_ff}/r/h/q${_f})"
    local last_result

    local   KEY_TERM="${_actbg}${_y}t${_f}${_d}[erm]${_f}      send SIGTERM to all listed PIDs"
    local   KEY_KILL="${_actbg}${_r}k${_f}${_d}[ill]${_f}      send SIGKILL to all listed PIDs"
    local KEY_REPEAT="${_actbg}${_w}r${_f}${_d}[epeat]${_f}    discard the results, call pgrep again"
    local   KEY_HELP="${_actbg}${_w}h${_f}${_d}[elp]${_f}      show this help"
    local  KEY_ABORT="${_actbg}${_w}q${_f}${_d}[uit]${_f}      exit the program"

    local SEP="\n    "
    local keys="\n  Current query:${SEP}${_b}$*${_f}\n"
    keys+="\n  Available actions:${SEP}$KEY_TERM${SEP}$KEY_KILL${SEP}$KEY_REPEAT${SEP}$KEY_HELP${SEP}$KEY_ABORT\n"
    keys+="\n  First letters indicate key that triggers corresponding action."
    keys+="\n  ${_actbg}?${_f} is an alias for ${_actbg}h${_f}${_d}[elp]${_f}, "
    keys+="${_actbg}Enter${_f} and ${_actbg}Ctrl+D${_f} are aliases for ${_actbg}r${_f}${_d}[epeat]${_f}\n"
    keys+="\n  ${_d}es7s/pgrek (c) 2023 A. Shavykin <${_be}0${_ff}.delameter@gmail.com>${_f}\n"

    local USAGE="$(cat <<-EOL
Interactive tool for repeated invocation of ${_u}pgrep${_f}, displaying the current
result, and killing all of the found processes. ${_u}pgrep${_f} is called with ${_b}-f${_f}
flag, which enables matching the pattern with the full process command path, not only
the executable name.

Usage:
    $(basename "$0") es7s
    $(basename "$0") telegram
EOL
    )"

    [[ $* =~ (--)?help ]] && { echo "$USAGE" ; exit ; }
    [[ -z "$*" ]] && printf "Starting without arguments disabled for safety\n" && return 0

    while true ; do
        if _pgrek_iter "$@" ; then
            :
        else
            break
        fi
    done
}

_main "$@"
