#!/usr/bin/env bash
# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
# shellcheck disable=SC2119,SC2016,SC2086
# shellcheck source=../../data/es7s-shell-commons.sh
__E7SL() { local c="$(realpath "$(dirname "$(readlink -f "$0")")")" ; local l=\
"es7s-shell-commons.sh" ; local p=( "$ES7S_SHELL_COMMONS" "$HOME/.es7s/data/$l"
"$c/../$l" ); while [[ ! $(type -t __es7s_com) =~ ^fu ]];do [[ -f "${p[0]}" ]]\
&& source "${p[0]}"; p=("${p[@]:1}"); [[ "${#p[@]}" -gt 0 ]] && continue; echo\
'ERROR: es7s/commons is missing (ES7S_SHELL_COMMONS)'; exit 57; done } ; __E7SL
# ------------------------------------------------------------- loader v.3B ---

# Changes:
#   - disabled upscaling to the terminal width (downscale is still performed,
#     when neccessary)
#   - added directives for alpha channel removing
#   - made common format default
#   - removed colon/wrong/official format selection options
#   - added "--help" option handling
#   - fixed shellcheck warnings (in addition to disabling 2086)
# ------------------------------------------------------------------------------
# ORIGINAL LICENSE
#
# Image viewer for terminals that support true colors.
# Copyright (C) 2014  Egmont Koblinger
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

declare -A ARGS

_usage() {
    local SELF=$(basename "${0%.*}")
    echo "Usage: $SELF [OPTIONS] FILE..."
    echo
    echo 'Each image will be rendered with width equal to min(120, wMax, wI, wT), where:'
    echo '  - wMax is a value of "-w" option'
    echo '  - wI is an image width'
    echo '  - wT is a terminal width'
    echo
    echo 'Specify "-w 0" / "-w" to disable image displaying (to print names and sizes only).'
    echo
    echo 'OPTIONS'
    echo '  -d, --demo                Ignore FILEs, open preset demonstration image instead.'
    echo '  -w, --max-width N         Set maximum image width to N (in characters) (N>=0).'
    echo '  -W, --force-width N       Ignore the logic above and force image to be rescaled'
    echo '                            to N pixels/characters (N>=0).'
    echo '  -b, --background COLOR    Replace transparent background with a specified color,'
    echo '                            valid values include: "black", "#101010", "none", etc.'
    echo '                            (default: "gray").'
    echo '  -q, --quiet               Do not print errors and image filenames and sizes.'
}

_main() {
    [[ $* =~ --help ]] && _usage && exit 0

        if ! _is_callable convert || ! _is_callable identify ; then
        echo 'ImageMagick is required' >&2
        exit 1
    fi
    # shellcheck disable=SC2214
    while getopts :w:W:b:dq-: OPT; do
        if [ "$OPT" = "-" ]; then
            OPT="${OPTARG%%=*}"
            OPTARG="${OPTARG#$OPT}"
            OPTARG="${OPTARG#=}"
        fi
        case "$OPT" in
             d|demo) ARGS[demo]=${ES7S_DATA_DIR?:Required}/demo/demo-image.png ;;
        w|max-width) ARGS[maxwidth]=$((OPTARG)) ;;
      W|force-width) ARGS[forcewidth]=$((OPTARG)) ;;
       b|background) ARGS[background]=$OPTARG ;;
            q|quiet) ARGS[quiet]=true ;;
              ??*|?) echo "Illegal option -${OPTARG:--$OPT}" >&2
                     _usage
                     exit 1 ;;
        esac
    done
    shift $((OPTIND-1))

    [[ ${ARGS[quiet]} ]] && exec 2>/dev/null

    # This is so that "upper" is still visible after exiting the while loop.
    shopt -s lastpipe

    local -a upper lower
    upper=()
    lower=()

    _process() {
        local file="$1" imgw="$2"
        [[ $imgw -le 0 ]] && return 0
        local convargs=(
            -thumbnail "${imgw}x "
            -alpha remove
            -background "${ARGS[background]:-gray}"
            -define "txt:compliance=SVG"
            "${file}" txt:-
        )
        local i col

        convert "${convargs[@]}" |
            while IFS=',:() ' read -r col row _ red green blue rest; do
                if [ "$col" = "#" ]; then
                    continue
                fi

                if [ $((row % 2)) = 0 ]; then
                    upper[$col]="$red;$green;$blue"
                else
                    lower[$col]="$red;$green;$blue"
                fi

                # After reading every second image row, print them out.
                if [ $((row % 2)) = 1 ] && [ $col = $((outw - 1)) ]; then
                    i=0
                    while [ $i -lt $outw ]; do
                        echo -ne "\e[38;2;${upper[$i]};48;2;${lower[$i]}m▀"
                        i=$((i + 1))
                    done
                    # \e[K is useful when you resize the terminal while this script is still running.
                    echo -e "\e[0m\e[K"
                    upper=()
                fi
            done

        # Print the last half line, if required.
        if [ "${upper[0]}" != "" ]; then
            i=0
            while [ $i -lt "$imgw" ]; do
                echo -ne "\e[38;2;${upper[$i]}m▀"
                i=$((i + 1))
            done
            echo -e "\e[0m\e[K"
        fi

    }

    [[ -n "${ARGS[demo]}" ]] && set - "${ARGS[demo]}"
    [[ -z "$*" ]] && echo "ERROR: No arguments" >&2 && return 1

    for file in "$@" ; do
        _print_filename "$file" >&2
        [[ -d "$file" ]] && _print_failure "Not file" >&2 && continue
        [[ ! -f "$file" ]] && _print_failure "Not found" >&2 && continue

        local imgsize
        if ! imgsize=$(identify -format "%wx%h\n" "$file"[0] 2>/dev/null) ; then
            _print_failure "Not image" >&2 && continue
        fi
        [[ -z "$imgsize" ]] && _print_failure "Not image" >&2 && continue

        local firstsize=$(head -1 <<<"$imgsize" | tr -d '\n')
        local firstw=${firstsize%%x*}
        local firsth=${firstsize##*x}
        { _print_status "$file" $firstw $firsth ; echo ; } >&2

        local imgw=$(cut <<<$firstsize -f1 -dx)
        local defw=120
        local termw=$(tput cols)
        local outw=$(min $defw "$(min $imgw $termw)")

        local maxw=${ARGS[maxwidth]}
        [[ -n $maxw ]] && outw=$(min $maxw $outw)

        local forcew=${ARGS[forcewidth]}
        [[ -n $forcew ]] && outw=$forcew

        if ! _process "$file"[0] $outw ; then
            continue
        fi
    done
}
_print_failure() { printf "%10.10s \n" "$1:" ; }
_print_filename() { _print_status "$1"$'\r' ; }
_print_status() {
    local file="${1:?}" imgw=${2:-} imgh=${3:-}
    local xmk=
    [[ -n $imgw ]] && [[ -n $imgh ]] && xmk=x
    printf "\e[K%10s %s" "$imgw$xmk$imgh" "$file"
}

_main "$@"
