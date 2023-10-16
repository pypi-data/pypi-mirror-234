#!/usr/bin/bash
# -----------------------------------------------------------------------------
# es7s/core (G1/legacy)
# (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# -----------------------------------------------------------------------------
# shellcheck disable=SC2119,SC2016
# shellcheck source=../../data/es7s-shell-commons.sh
__E7SL() { local c="$(realpath "$(dirname "$(readlink -f "$0")")")" ; local l=\
"es7s-shell-commons.sh" ; local p=( "$ES7S_SHELL_COMMONS" "$HOME/.es7s/data/$l"
"$c/../$l" ); while [[ ! $(type -t __es7s_com) =~ ^fu ]];do [[ -f "${p[0]}" ]]\
&& source "${p[0]}"; p=("${p[@]:1}"); [[ "${#p[@]}" -gt 0 ]] && continue; echo\
'ERROR: es7s/commons is missing (ES7S_SHELL_COMMONS)'; exit 57; done } ; __E7SL
# ------------------------------------------------------------- loader v.3B ---

_illegal_opt() { error "Illegal option -${OPTARG:-"-"$OPT}" ; _print_help_hint ; exit 1 ; }
_ensure_arg() { if [[ -z "${OPTARG:-""}" ]] ; then error "No arg for --$OPT option" ; _print_help_hint ; exit 1 ; fi }
fmt_def() { printf "${_y}$*$(_cs 39)"; }
fmt_ex() { printf "$_b%s$(_cs 22)" "$*" ; }
_print_help_hint() { echo "Show usage: $SELF --help" ; }
_print_help() {
    local vname=$(_u "<name>")
    echo "Print terminal colors table(s)"
    echo
    echo "Usage:"
    echo "    $SELF [<options>]..."
    echo
    echo "Options:"
    echo "  -m, --mode=$vname     allowed values: $(fmt_ex 16), $(fmt_ex 256), $(fmt_ex rgb) "$(fmt_def "[default: $(fmt_ex 16)]")
    echo "  -a, --all             runs the program in all combinations of allowed modes (total 6)."
    echo "                        disables all other options. implies $(fmt_ex -e)."
    echo "  -b, --bg              colored background mode $(fmt_def "[default: colored text mode]")"
    echo "  -e, --extended        display extra formats (16-colors mode only)"
    echo
    echo "Mandatory or optional arguments to long options are also mandatory or optional for any corresponding short options."
    echo
    echo "Examples:"
    echo "    $SELF -e [-m 16]   print 16-color table in extended mode"
    echo "    $SELF -b -m 256    print 256-color table in background mode"
    echo "    $SELF --mode=rgb   print True Color table"
    echo "    $SELF --all        print all three tables, in colored text mode and colored background mode each"
    echo
}
_print_colors_4bit() {
    local -a color_x_places_1=(0 1 2 3 4 5 6 7)
    local -a color_x_places_2=(30 90)
    local -a color_y_values=("" 1 2 7)
    local -a color_y_values_ext=("7;1" "7;2" "OSC8")
    local -a color_preset_prefix=""
    local -a color_presets_before=("" 3 4 4:3 "4;58;5;1" 5 8 9 21 51 53 39)
    local -a color_presets_after=("")
    local -a colors
    local margin=6

    if [[ -n "$MODE_BACKGROUND" ]] ; then
        color_x_places_2=(40 100)
        color_y_values=("" 1 2 3 7)
        color_y_values_ext=("7;1" "7;2" 30 "OSC8")
        color_preset_prefix="30;47;"
        color_presets_before=(4 4:3 "4;58;5;1" 5 8 9 21 51 53 49)
        color_presets_before=( "${color_presets_before[@]/#/$color_preset_prefix}" )
        margin=8
    fi
    if [[ -z "$MODE_EXTENDED" ]] ; then
        color_y_values_ext=()
        color_presets_before=("")
        color_presets_after=("")
        margin=0
    fi

    local -A descriptions=()
    descriptions[0]="none"
    descriptions[1]="bold"
    descriptions[2]="dim"
    descriptions[3]="italic"
    descriptions[4]="underline"
    descriptions[4:3]="curly underline"
    descriptions[5]="slow blink"
    descriptions[7]="inv"
    descriptions["7;1"]="inv+bold"
    descriptions["7;2"]="inv+dim"
    descriptions["OSC8"]="hyperlink"
    descriptions[8]="hide"
    descriptions[9]="strike"
    descriptions[21]="double underline"
    descriptions[30]="black"
    descriptions[39]="default text color"
    descriptions[49]="default background color"
    descriptions["4;58;5;1"]="custom underline color"
    descriptions[51]="framed"
    descriptions[53]="overline"

    for color_place_2 in "${color_x_places_2[@]}" ; do
        local prefix
        [[ $color_place_2 -ge 90 ]] && prefix="bright " || prefix=""
        descriptions[$((color_place_2))]="$(printf "%s" "$mode_print${prefix}black" | sed -Ee "s/bright black/gray/")"
        descriptions[$((color_place_2 + 1))]="$mode_print${prefix}red"
        descriptions[$((color_place_2 + 2))]="$mode_print${prefix}green"
        descriptions[$((color_place_2 + 3))]="$mode_print${prefix}yellow"
        descriptions[$((color_place_2 + 4))]="$mode_print${prefix}blue"
        descriptions[$((color_place_2 + 5))]="$mode_print${prefix}magenta"
        descriptions[$((color_place_2 + 6))]="$mode_print${prefix}cyan"
        descriptions[$((color_place_2 + 7))]="$mode_print${prefix}white"
    done

    color_y_values+=("${color_y_values_ext[@]}")
    printf "%$((margin + 6))s" " "
    for color_extra in "${color_y_values[@]}" ; do
        local bleft="[" bright="]"
        [[ $color_extra =~ ^OSC ]] && { bleft=" " && bright=" " ; }
        printf "%s%4s%s" "$bleft" "$color_extra" "$bright" | sed -Ee "s/[];[]+/$_d&$(_cs 22)/g; s/ (OSC8) / ${_be}${_b}OSC8$(_cs 22 39) /g; s/ +/$_u&$(_cs 24)/g;  s/$/$_f/"
    done
    printn

    colors+=("${color_presets_before[@]}")
    for color_place_1 in "${color_x_places_1[@]}" ; do
        for color_place_2 in "${color_x_places_2[@]}" ; do
            colors+=( $(( color_place_1  + color_place_2 )) )
        done
    done
    colors+=("${color_presets_after[@]}")

    for color_main in "${colors[@]}" ; do
        local color_main_orig="$color_main"
        [[ "$color_main" == $"\n" ]] && printn && continue
        [[ "$color_main" =~ 58\;5\;[0-9]+ ]] && color_main="${color_main//5;160/5;\*}"
        if [[ ${#color_main} -ge 12 ]] ; then
            printf "%12.12s${_d}…${_f}│" "$color_main" | sed -Ee "s/${color_preset_prefix:-"^$"}/$_gy$_d&$_f/; s/:/$_b$_gn&$(_cs 22 39)/"
        else
            printf "%s${_d}[]${_f}│" "$(printf "%$(( margin + 3 ))s"  "${color_main}" | sed -Ee "s/${color_preset_prefix:-"^$"}/$_gy$_d&$_f/;  s/;+/$_d&$(_cs 22)/g;  s/:/$_b$_hr&$(_cs 22 39)/; ")"
        fi
        for color_extra in "${color_y_values[@]}" ; do
            local color="${color_main_orig}${color_extra:+";$color_extra"}"
            if [[ $color_extra == "OSC8" ]] ; then
                printf "%s%s" "$(_cs "${color_main_orig}")" $'\x1b]8;;https://dlup.link\x1b\\ es7s \x1b]8;;\x1b\\\x1b[m'
            else
                printf "%s es7s %s" "$(_cs "${color}")" $'\x1b[m'
            fi
        done
        local description_key="${color_main_orig#$color_preset_prefix}"
        local description="${descriptions[${description_key:-0}]}"
        printfn "│ %s" "${description//none/$(_cs 3)none$(_cs 23)}"
    done

    declare -a additional_desc_lines=()
    local current_margin

    current_margin=$(( margin + 6 ))
    printf "%${current_margin}s" " "
    for color_extra in "${color_y_values[@]}" ; do
        local description_key="${color_extra#$color_preset_prefix}"
        local description="${descriptions[${description_key:-0}]}"
        if [[ ${#description} -gt 6 ]] && [[ ${color_extra} != "${color_y_values[-1]}" ]] ; then
            for index in "${!additional_desc_lines[@]}" ; do
                additional_desc_lines[$index]+="$(alignc 6 " ")"
            done
            additional_desc_lines+=("$(printf "%${current_margin}s" " ")$description")
            printf "%1s%-5s" "" "|" | sed -Ee 's/.+/\x1b[53m&\x1b[m/g'
        else
            if [[ ${#description} -le 6 ]] ; then
                alignc 6 "${description//none/$(_cs 3)none$(_cs 23)}" | sed -Ee 's/.+/\x1b[53m&\x1b[m/g'
            else
                sed <<< " $description"  -Ee 's/.{,6}/\x1b[53m&\x1b[m/' | tr -d '\n'
            fi
        fi
        current_margin=$(( current_margin + 6 ))
    done
    printn
    for additional_desc_line in "${additional_desc_lines[@]}" ; do
        printfn "%s" "$additional_desc_line"
    done

    printn
    printfn "%s" "16 colors $mode_print \\e[$(_y "*")m"
    printn

    if [[ -n "$MODE_EXTENDED" ]] || [[ -n "$MODE_BACKGROUND" ]] ; then return ; fi
    printfn "%s" "${_d}Hint: try options ${_f}${_b}-b${_f}${_d} and ${_f}${_b}-e${_f}${_d} or modes \"${_f}${_b}-m${_f} 256${_d}\", \"${_f}${_b}-m${_f} rgb${_d}\""
}

_print_colors_8bit() {
    local -a colors_start=(16 52 88 124 160 196 28 64 100 136 172 208 40 76 112 148 184 220 232 244)
    local -a prefix=(38 5)
    local prefix_print="$(_b 38)"

    if [[ -n "$MODE_BACKGROUND" ]] ; then
        prefix=(30 48 5)
        prefix_print="30;$(_b 48)"
    fi

#    for color_std in {0..15} ; do
#        local size=1
#        #[[ $(( $color_std % 4 )) -eq 2 ]] && size=
#        [[ $color_std -eq 0 ]] || [[ $color_std -eq 15 ]] && size=
#        printf "$(_cs "${prefix[@]}" "$color_std")%${size}s%02d%${size}s$_f" "" "$color_std" ""
#    done
    for color_std in {0..15} ; do
        local comp=
        [[ $color_std -eq 0 ]] || [[ $color_std -eq 7 ]] || [[ $color_std -eq 8 ]] || [[ $color_std -eq 15 ]] && comp=1
        printf "$(_cs "${prefix[@]}" "$color_std")%${comp}s  %03d  %${comp}s$_f" "" "$color_std" ""
        [[ $color_std -eq 7 ]] && printfn
    done
    printfn

    for color_start in "${colors_start[@]}" ; do
        for color_shift in {0..11} ; do
            local color=$(( color_start + color_shift ))
            printf "%s %03d %s" "$(_cs "${prefix[@]}" "$color")" "$color" "$_f"
        done
        printfn
    done

    printn
    printfn "%s" "256 colors $mode_print \\e[${prefix_print};5;$(_y "*")m"
    printn
}

_print_colors_24bit() {
    local -a prefix=(38 2)
    local text="@"
    if [[ -n "$MODE_BACKGROUND" ]] ; then
        prefix=(48 2)
        text=" "
    fi
    local prefix_print="$_b$(_jb ";" "${prefix[@]}")$_f"

    for b in {0..255..64}  ; do
        for r in {0..255..32} ; do
            for g in {0..255..32} ; do
                printf '\e[%sm%s\e[m' "$(_jb ";" "${prefix[@]}" $r $g $b)" "$text"
            done
        done
        printn
    done

    for x in {0..255..8} ; do printf '\e[%sm%s\e[m' "$(_jb ";" "${prefix[@]}" $x 0 0)" "$text" ; done
    for x in {0..255..8} ; do printf '\e[%sm%s\e[m' "$(_jb ";" "${prefix[@]}" $x $x 0)" "$text" ; done ; printn
    for x in {0..255..8} ; do printf '\e[%sm%s\e[m' "$(_jb ";" "${prefix[@]}" 0 $x 0)" "$text" ; done
    for x in {0..255..8} ; do printf '\e[%sm%s\e[m' "$(_jb ";" "${prefix[@]}" $x 0 $x)" "$text" ; done ; printn
    for x in {0..255..8} ; do printf '\e[%sm%s\e[m' "$(_jb ";" "${prefix[@]}" 0 0 $x)" "$text" ; done
    for x in {0..255..8} ; do printf '\e[%sm%s\e[m' "$(_jb ";" "${prefix[@]}"  0 $x $x)" "$text" ; done ; printn
    for x in {0..255..4} ; do printf '\e[%sm%s\e[m' "$(_jb ";" "${prefix[@]}"  $x $x $x)" "$text" ; done ; printn

    printn
    printfn "%s" "16M colors $mode_print \\e[${prefix_print};$(_y "RRR;GGG;BBB")m"
    printn
}

# -----------------------------------------------------------------------------
SELF="${0##*/}"
MODE=16
MODE_BACKGROUND=
MODE_EXTENDED=

while getopts :m:abeh-: OPT; do
    if [ "$OPT" = "-" ]; then
        OPT="${OPTARG%%=*}"
        OPTARG="${OPTARG#$OPT}"
        OPTARG="${OPTARG#=}"
    fi
    # shellcheck disable=SC2214
    case "$OPT" in
         m|mode) _ensure_arg
                 MODE="$OPTARG" ;;
          a|all) MODE=all ; break ;;
           b|bg) MODE_BACKGROUND=true ;;
     e|extended) MODE_EXTENDED=true ;;
         h|help) _print_help
                 exit 0 ;;
         ??*|?) _illegal_opt ;;
    esac
done

if [[ $MODE == "all" ]] ; then
    "$0" -m16 -e
    "$0" -m16 -eb
    "$0" -m256
    "$0" -m256 -b
    "$0" -mrgb
    "$0" -mrgb -b
    exit 0
fi

mode_print="fg: "
echo
[[ -n "$MODE_BACKGROUND" ]] && mode_print="bg: "

if [[ $MODE == "16" ]] ; then _print_colors_4bit
elif [[ $MODE == "256" ]] ; then _print_colors_8bit
elif [[ $MODE == "rgb" ]] ; then _print_colors_24bit
else
    error "Invalid mode $MODE"
    _print_help_hint
fi
