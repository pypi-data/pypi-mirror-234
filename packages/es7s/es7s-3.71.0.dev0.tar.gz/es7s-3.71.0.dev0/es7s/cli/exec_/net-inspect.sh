#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
# shellcheck disable=SC2059,SC2120

_main() {
    local __SELF="${0##*/}"
    local __USAGE="$__SELF [-i INTERFACE] [-a ACTION... | --help]"
    local -r VERSION=1.8
    local -r default_iface="$(ip -br link | sed -Ee '/\sUP\s/!d; s/^(\S+).+/\1/; q')"
    local iface=$default_iface
    local start_mode help_invoked

    __parse_args() {
        while getopts :i:a:h-: OPT; do
            if [ "$OPT" = "-" ]; then
                OPT="${OPTARG%%=*}"
                OPTARG="${OPTARG#$OPT}"
                OPTARG="${OPTARG#=}"
            fi
            # shellcheck disable=SC2214
            case "$OPT" in
            i|interface) iface="$OPTARG" ;;
               a|action) start_mode="$OPTARG" ;;
                 h|help) help_invoked=true ;;
                  ??*|?) echo "Illegal option -${OPTARG:--$OPT}. Usage: $__USAGE"
                         exit 1 ;;
            esac
        done
        shift $((OPTIND-1))
    }
    _build_cmds() {
      CMDS=(
          [i]="select-interface"
          [l]="sudo netstat -tulpaN"
          [o]="port-occupancy"
          [m]="sudo tcptrack -f -r10 -i $iface"
          [h]="sudo iftop -i $iface"
          [p]="sudo nethogs -v3 -s -d1 $iface"
          [t]="sudo tcpdump -qlQ in -i $iface"
          [u]="bmon -p $iface -o curses:ngraph=1;gwidth=30;gheight=4;minlist=1"
          [q]="_quit"
          [?]="_usage"
      )
    }
    _menuitem() {
        local -r DESC_WIDTH=21
        local key=$1 desc=$2 prefix=${3:-} suffix=
        local cmd="${CMDS[$key]}"
        [[ -z "$prefix" ]] && suffix="  "
        [[ "$cmd" =~ ^_ ]] && cmd=
        [[ -n "${CMD_DESCS[$key]}" ]] && cmd="${CMD_DESCS[$key]}"
        printf " $(_menubtn "$key") \x1b[22;32m${prefix}%-${DESC_WIDTH}s${suffix}\x1c\x1b[34m$cmd\x1b[m\n" "$desc" |
          sed --unbuffered -Ee "s/sudo/\x1b[2m&\x1b[22m/g; s/$iface/\x1b[1;36m&\x1b[34m/g; s/&(\w)/\x1b[1;33m\1\x1b[22;32m/; Tb; s/\x1c/ /; :b s/\x1c//;"
    }
    _menubtn() {
        local key=$1
        local bfmt=39 cmd=${CMDS[$key]}
        [[ -n "$cmd" ]] && bfmt=33 || key=" "
        printf "\x1b[37;2m[\x1b[22${bfmt:+;$bfmt}m${key}\x1b[37;2m]\x1b[39;22m"
    }
    _usage() {
        echo -e "USAGE:\n    $__USAGE\n"
        printf "\x1b[93mWhat do?\x1b[m\n"
        _menuitem i "&interface selection"
        _menuitem l "&list connections"
        _menuitem o "port &occupancy"
        _menuitem m "&monitor connections"
        _menuitem h "grouped by &host" "└─"
        _menuitem p "grouped by &process" "└─"
        _menuitem t "&tcp packet monitor"
        _menuitem u "&usage monitor"
        _menuitem q "exit"
        echo
    }
    select-interface() {
      local lineno=0
      while read -r line; do
        [[ -z $line ]] && echo && break
        local -A iface_map
        if [[ "$lineno" -gt 1 ]] ; then
          line=$(sed -Ee "s/$iface.+/\x1b[1;36m&\x1b[m/" <<< "$line")
          ino=$((lineno-1))
          iface_map+=([$ino]="$(tr -s ' ' <<<"$line" | cut -f1 -d' ')")
          printf "\x1b[35;3m %-3d\x1b[m%s\n" "$ino" "$line"
        else
          echo "   $line"
        fi
        ((lineno++))
      done < <(es7s print netifs)

      read -r -p "IFACE NUM: "$'\e[35;3m' ino
      printf "\x1b[m"
      if [[ -n "$ino" ]] ; then
          [[ -z "${iface_map[$ino]}" ]] && printf "\x1b[31mInvalid interface number: \x1b[1m$ino\x1b[m\n" && return
          iface="${iface_map[$ino]}"
          _build_cmds
      fi
      printf "network interface: \x1b[36;1m$iface\x1b[m\n\n"
    }
    port-occupancy() {
        read -r -p "PORT: "$'\x1b[35;3m' port
        printf "\x1b[m"
        net-inspect -al | grep "$port"
    }

    __parse_args "$@"

    declare -A CMDS=()
    _build_cmds

    # shellcheck disable=SC2016
    declare -Ar CMD_DESCS=(
        [i]=' '
        [o]='sudo netstat -tulpaN | grep \"$port\"'
    )

    local one_time resp header=1
    local helphint=$'\x1b[37m(? to help)\x1b[39m'
    if [[ -n $start_mode ]] ; then
        one_time=true && resp=$start_mode && helphint=
    elif [[ -n $help_invoked ]] ; then
        one_time=true && resp="?" && header=
    else
        resp=
    fi

    if [[ -n $header ]] ; then
        printf "\x1b[37mes7s/net-inspect v${VERSION}\x1b[m\n"
        printf "network interface: \x1b[36;1m$iface\x1b[m\n"
        echo
    fi

    local redraw=true
    while true ; do
        if [[ -z $resp ]] ; then
            [[ -n $redraw ]] && printf $'\e[mACTION\x1b[m: \x1b[37;2m[\x1b[m\x1b7 \x1b[37;2m]\x1b[22;39m '"$helphint"'\x1b8'
            read -sr -N1 -p $'\x1b8' resp
        fi
        [[ -z $one_time ]] && echo -en "\x1b[1D$(_menubtn "${resp::1}")"

        case "${resp::1}" in
         i|l|o|m|h|p|t|u|q|\?) cmd=${CMDS[${resp::1}]}
                               resp="${resp:1}"
                               printf "\x1b[0K"
                               [[ -z $one_time ]] && printf " "
                               [[ $cmd =~ ^_ ]] || printf "> \x1b[34;1m$cmd\x1b[m\n"
                               [[ $cmd == _quit ]] && echo && return
                               #[[ $cmd == select-interface ]] && one_time=
                               echo
                               $cmd
                               redraw=1
                               ;;
            ??*|?) echo -ne "\x1b[0K $helphint \x1b[31m Invalid action: \x1b[91m${resp::1}\x1b[39m\r\a"
                   resp=
                   redraw=
                   ;;
        esac
        [[ -n $one_time ]] && [[ -z $resp ]] && return
    done

}

_main "$@"
