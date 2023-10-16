#!/bin/bash
# -----------------------------------------------------------------------------
# es7s/core (G1/legacy shell shared code)
# (C) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# -----------------------------------------------------------------------------
# shellcheck disable=SC2059
# shellcheck disable=SC2120
# -----------------------------------------------------------------------------
if [[ -n "${ES7S_DEBUG:-}" ]] ; then
    printf "$(basename "${BASH_SOURCE[-1]^^}") %s\n" \
        "es7s/commons load request from ${BASH_SOURCE[-1]@Q}" \
        " Self-path: ${BASH_SOURCE[0]@Q}" \
        "Phys. path: $(stat "${BASH_SOURCE[0]}" -c %N)" \
        "      Size: $(stat -L "${BASH_SOURCE[0]}" -c %s)" \
        "Modif.time: $(stat -L "${BASH_SOURCE[0]}" -c %y)" \
        "     SHA-1: $(cat "${BASH_SOURCE[0]}" | sha1sum)"
fi
[[ $(type -t __es7s_com) =~ ^fu && -z $ES7S_RELOADING ]] && return
# -----------------------------------------------------------------------------
# FLOW CONTROL

_exit() { printn ; exit "${1:-126}" ; }
_die()  { error "$*" ; _exit 1 ; }
_diew() { error "${*:2}" ; _exit "${1:?}" ; }
_help_if() { [[ $1 =~ ^--?h(elp)? ]] && cat || return 1 ; }
_which() { command -v "$1" ; }
_is_callable() { _which "$@" &>/dev/null ; }

# -----------------------------------------------------------------------------
# MATH, LOGIC, DATETIME

declare -x SECONDS_IN_MINUTE=$((60))
declare -x SECONDS_IN_DAY=$((SECONDS_IN_MINUTE * 60 * 24))
declare -x SECONDS_IN_MONTH=$((SECONDS_IN_DAY * 30))
declare -x SECONDS_IN_YEAR=$((SECONDS_IN_MONTH * 12))

min() {
    # args: <num1> <num2> [decimals=0]
    local num1=$(( ${1:?Num1 required} ))
    local num2=$(( ${2:?Num2 required} ))
    local fmt="%.${3:-0}f"
    if [[ $(( num1 )) -lt $(( num2 )) ]]
        then printf $fmt $num1
        else printf $fmt $num2 ; fi
}

max() {
    # args: <num1> <num2> [decimals=0]
    local num1=$(( ${1:?Num1 required} ))
    local num2=$(( ${2:?Num2 required} ))
    local fmt="%.${3:-0}f"
    if [[ $(( num1 )) -gt $(( num2 )) ]]
        then printf $fmt $num1
        else printf $fmt $num2 ; fi
}

round() {
    # args: <expression> [accuracy=0]
    # accuracy is number of fraction digits
    local expr="${1?Expr required}" acc="${2:-0}"
    LC_NUMERIC="en_US.UTF-8" printf "%.${acc}f" "$(bc <<< "$expr")"
}

oct2bin() {
    # args: <oct> [len=9]
    # first arg is oct value needed to transform
    # second is total result length
    # example: translation of access attribute to bit mask: "oct2bin 0644 9" -> 110100100
    printf "%0${2:-9}d" "$(printf "obase=2\n%d\n" ${1:?Value required} | bc)"
}

timedelta() {
    local usage="usage: timedelta timestamp1 [timestamp2=now]"
    local ts1=${1:?Required}
    if [[ $ts1 =~ \. ]] ; then
        local ts2=${2:-$(date +%s.%N)}
        local delta=$(bc <<< "scale=3"$'\n'"$ts2 - $ts1")
    else
        local ts2=${2:-$(date +%s)}
        local delta=$(($ts2 - $ts1))
    fi
    local sign=
    if [[ $delta =~ ^- ]] ; then
        delta=${delta#-}
        sign=-
    fi
    idelta=$(round $delta)

    if [[ $delta =~ ^[0.] ]]; then
        printf "%s%.3f ms" "$sign" "$(bc <<< "scale=3"$'\n'"$delta * 1000")"
        echo
        return
    fi
    if [[ $idelta -le $SECONDS_IN_MINUTE ]]; then
        printf "%s%.2f sec" "$sign" "$delta"
        echo
        return
    fi
    delta=$idelta

    if [[ $delta -le $SECONDS_IN_DAY ]]; then
        TZ=UTC0 printf '%s%(%-Hh %Mmin)T' "$sign" "$delta"
    elif [[ $delta -le $SECONDS_IN_MONTH ]] ; then
        printf "%s%d day(s)+" "$sign" "$((delta / SECONDS_IN_DAY))"
    elif [[ $delta -le $SECONDS_IN_YEAR ]] ; then
        printf "%s%d month(s)+" "$sign" "$((delta / SECONDS_IN_MONTH))"
    else
        printf "%s%d year(s)+" "$sign" "$((delta / SECONDS_IN_YEAR))"
    fi
    echo
}

function _is_int { [[ ${1-} =~ ^-?[0-9]+$ ]] && return 0 ; return 1 ; }
function _not  { [[ -n ${1-} ]] || return 1 ; } # exit with code > 0 for non-empty arg1
function _nots { [[ -n ${1-} ]] || printf "${2:-true}" ; } # print arg2 (or "true") if arg1 is non-empty
function _pp { [[ ${1-} -ne 1 ]] && local end=s ; printf "%d%s%s%s" "${1:-0}" "${2:+ }" "${2:-}" "${2:+${end:-}}" ; } # print plurals, ex.: _pp 3 file -> "3 files"

function _ps {
    # print size of <filepath> in human format or in bytes if <1kb
    # args: filepath
    local ex="$(stat --printf=%s ${1:?})"
    if [[ $ex -ge 1024 ]] ; then
        ls "$1" -sh --si | cut -f1 -d' ' | tr A-Z a-z | _ttn
    else
        printf %s $ex
    fi
}

# -----------------------------------------------------------------------------
# COLOR

# MODE 4
declare -x I_BOLD=1       I_UNDERLx2=21  
declare -x I_DIM=2        I_NO_DIM_BOLD=22  # turns off both
declare -x I_ITALIC=3     I_NO_ITALIC=23  
declare -x I_UNDERL=4     I_NO_UNDERL=24  
declare -x I_BLINK_SW=5   I_NO_BLINK=25   
declare -x I_BLINK_FT=6                   
declare -x I_INV=7        I_NO_INV=27     
declare -x I_HIDDEN=8     I_NO_HIDDEN=28  
declare -x I_CROSSL=9     I_NO_CROSSL=29  
declare -x I_OVERL=53     I_NO_OVERL=55   

declare -x I_BLACK=30     IB_BLACK=40     I_GRAY=90     
declare -x I_RED=31       IB_RED=41       IH_RED=91     
declare -x I_GREEN=32     IB_GREEN=42     IH_GREEN=92   
declare -x I_YELLOW=33    IB_YELLOW=43    IH_YELLOW=93  
declare -x I_BLUE=34      IB_BLUE=44      IH_BLUE=94    
declare -x I_MAGNETA=35   IB_MAGNETA=45   IH_MAGNETA=95 
declare -x I_CYAN=36      IB_CYAN=46      IH_CYAN=96    
declare -x I_WHITE=37     IB_WHITE=47     IH_WHITE=97   
declare -x I_EXTMODE=38   IB_EXTMODE=48   
declare -x I_DEFAULT=39   IB_DEFAULT=49   

# MODE 8
declare -x I8_LIGHT_SEA_GREEN=37 
declare -x I8_WHITE=231            I8_GRAY=243 

function _jb { local d=${1-""} ; shift ; local f=${1-""} ; shift ; printf %s "$f" "${@/#/$d}" ; } # join [arg2...] by arg1, e.g. "_jb , 1 2" -> 1,2
function _cs  { printf '\e[%bm' "$(_jb \; "${@}")" ; }  # integer codes to escaped codes / 4bit color
function _pcs { printf '\[\e[%bm\]' "$(_jb \; "${@}")" ; } # integer codes to prompt-escaped codes / 4bit color
function _cs8  { _cs $I_EXTMODE 5 ${1:-196} ; } # integer codes to escaped codes / 8bit color (text)
function _cs8b { _cs $IB_EXTMODE 5 ${1:-196} ; } # integer codes to escaped codes / 8bit color (bg)
function _csr  { _cs $I_EXTMODE 2 ${1:-255} ${2:-128} ${3:-64} ; } # integer codes to RGB/fg SGR
function _csrb  { _cs $IB_EXTMODE 2 ${1:-255} ${2:-128} ${3:-64} ; } # integer codes to RGB/bg SGR

declare -x  _esq=$'\033\[[0-9;]*m' # SGR escape sequence regex
declare -x  _tab=$'\t' _t=$'\t' _n=$'\n' _f=$(_cs) # filter reset
#declare -x  _imk=$'\ufeff' # unicode invisible marker # though it IS visible when using a fallback font that provides
                                                       # graphics to all characters -- Unifont or (i assume) Last Resort
declare -x  _b=$(_cs $I_BOLD);   function  _b { printf %s  "$_b$*$_f" ; }
declare -x  _d=$(_cs $I_DIM);    function  _d { printf %s  "$_d$*$_f" ; }
declare -x  _u=$(_cs $I_UNDERL); function  _u { printf %s  "$_u$*$_f" ; }
declare -x  _U=$(_cs $I_NO_UNDERL);
declare -x  _i=$(_cs $I_INV);    function  _i { printf %s  "$_i$*$_f" ; }
declare -x _ni=$(_cs $I_NO_INV); function _ni { printf %s "$_ni$*$_f" ; }
declare -x _ov=$(_cs $I_OVERL);  function _ov { printf %s "$_ov$*$_f" ; }
declare -x  _r=$(_cs $I_RED);    function  _r { printf %s  "$_r$*$_f" ; }
declare -x _gn=$(_cs $I_GREEN);  function _gn { printf %s "$_gn$*$_f" ; }
declare -x  _y=$(_cs $I_YELLOW); function  _y { printf %s  "$_y$*$_f" ; }
declare -x _be=$(_cs $I_BLUE);   function _be { printf %s "$_be$*$_f" ; }
declare -x  _m=$(_cs $I_MAGNETA);function  _m { printf %s  "$_m$*$_f" ; }
declare -x  _c=$(_cs $I_CYAN);   function  _c { printf %s  "$_c$*$_f" ; }
declare -x _gy=$(_cs $I_GRAY);   function _gy { printf %s "$_gy$*$_f" ; }
declare -x  _hr=$(_cs $IH_RED);    function  _hr { printf %s  "$_hr$*$_f" ; }
declare -x _hgn=$(_cs $IH_GREEN);  function _hgn { printf %s "$_hgn$*$_f" ; }
declare -x  _hy=$(_cs $IH_YELLOW); function  _hy { printf %s  "$_hy$*$_f" ; }
declare -x _hbe=$(_cs $IH_BLUE);   function _hbe { printf %s "$_hbe$*$_f" ; }
declare -x  _hm=$(_cs $IH_MAGNETA);function  _hm { printf %s  "$_hm$*$_f" ; }
declare -x  _hc=$(_cs $IH_CYAN);   function  _hc { printf %s  "$_hc$*$_f" ; }

# underline words only, not spaces in between
function _uu { sed -Ee "s/\S+/$_u&$_U/g" <<<"$@" ; }
# underline words only, not spaces in between and not separators
function _uuu { sed -Ee "s/[^ :-]+/$_u&$_U/g" <<<"$@" ; }

# -----------------------------------------------------------------------------
# FORMATTING / SEPARATORS AND LINE BREAKS

declare -x RE_NOPAD="<~"

function _ww  {
    local width=$COLUMNS
    [[ -z $width ]] && width=$(tput cols)
    [[ -z $width ]] && width=$(stty size | cut -f2 -d" " )
    printf %s "${width:-80}"
}
function _w   { printf %s "$(( $(_ww) - 2 ))" ; }
function _s   { printf "%${1:-1}s" | sed "s/ /${2:- }/g" ; } # prints spaces/specified chars ; args: [len] [char]
function _sep { printfn "%s%s%s" "${1:-""}" "$(_s "${2:-40}" "${3:--}")" "${1:+$_f}" ; } # prints separator; args: [color] [len] [fill]
function _spl { _s $(( 2 * ${1:-1} )) ; } # get padding by level
function _sbp() { # separate-by-places, args: sep place num, example: (_sbp "," 3 1000000) -> "1,000,000"
    local d="${1:-" "}" p=$((${2:-3})) s="${*:3}"
    for (( i=0; i<${#s}; i++ )) ; do
        [[ $i != 0 ]] && [[ $(((${#s} - i) % p)) -eq 0 ]] && printf %s "$d"
        printf %s "${s:$i:1}"
    done
}

declare -x _sp=$(_spl 1) # default padding
function pad { local s="${1+"$(_spl ${1:-1})"}" ; sed --unbuffered "s/^/${s:-$_sp}/g" ; }
function printfn { [[ "$#" -le 1 ]] && printf "%s\n" "${1-}" || printf "${1-}\n" "${@:2}" ; } # @TODO deprecate
function printn  { printf "%${1:-1}s" | sed "s/./\n/g" ; }
function printb { [[ -n "${1-}" ]] && printf true || printf false ; } # print as boolean
function prepend_nl { printn "${1:-1}" ; cat ; } # print newline(s) with stdin (before it)
function append_nl { cat ; printn "${1:-1}" ; } # print newline(s) with stdin (after it)
function addnl { append_nl "$@" ; }
function head_skip { tail -n +$((${1:-1}+1)) ; } # skip <arg1> lines from start, default is 1

# +----  control char separators  ---------+
declare -x _CCS0=$'\x1c'  # FILE SEPARATOR    |
declare -x _CCS1=$'\x1d'  # GROUP SEPARATOR   |
declare -x _CCS2=$'\x1e'  # RECORD SEPARATOR  |
declare -x _CCS3=$'\x1f'  # UNIT SEPARATOR    |
# +----  first 3 are recognised  ----------+
#        by pythons splitlines()

# -----------------------------------------------------------------------------
# FORMATTING / TEXT COLOR & ATTRIBUTES                 # ᴏᴷ success ᴡᴬ warn ᴇᴿ error ɪⁱ notice ʏᶰ Continue? (y/n)   ⁽ᴏᴷᵏᴼᴋᵒₖˢⱽⅴᵥ⁾ success ⁽ᵂᴡᴿʀᵣrᴬᴀᵃ⁾ warn
                                                      # (ᴼₖ) success (ᵂₐ) warn (ᴱᵣ) error (ᴵᵢ) notice (ʸₙ) Continue? (y/n)    ⁽ˣᴱᴇᵉₑᴿʀᵣr⁾ error  ⁽ɪᴵᵢⁱᵎ⁾ notice ⁽ᵞʏʸᴺɴᶰⁿₙˀˁˤ⁾ Continue?
declare -x RAW_MODE                                      # ᴼᴋ ᴏᴷ success ᵂᴀ ᴡᴬ warn ᴱʀ ᴇᴿ error ᴵᵢ ɪⁱ notice ʏₙ ʏᴺ Continue? (y/n):   A B C
declare -x _F_SUCCESS=$(_cs $I_GREEN)           _IC_SUCCESS="${_hgn}✓$(_cs 39)" #_IC_SUCCESS="$_hgn$_b✓" ✔
declare -x _F_WARNING=$(_cs $I_YELLOW)          _IC_WARNING="${_hy}!$(_cs 39)" #_IC_WARNING="$_hy$_b" ⁈ ⁉
declare -x _F_ERROR=$(_cs $IH_RED)              _IC_ERROR="${_r}✕$(_cs 39)" #_IC_ERROR="$_hr$_b✗"✘  ✕ ✖
declare -x _F_NOTICE=$(_cs $I_CYAN)             _IC_NOTICE="${_c}⋅$(_cs 39)" #"${_c}ⓘ·•∗*‣◦$(_cs 39)" #"${_be}$(_b i)${_be}"
declare -x _F_DISABLED=$(_cs8 239)              _IC_DISABLED="╌"
declare -x _F_VERBOSE=$(_cs $I_BLUE)
declare -x _F_PROMPT=$(_cs $IH_MAGNETA)         #; _IC_INPUT="" #"${_hm}${_b}${_hc}?${_f}${_hm}${_f}"
declare -x _F_PROMPT_PARAM=$(_cs $IH_CYAN)      #; _IC_SELECT="" #${_IC_INPUT/\?/?}
declare -x _F_PROMPT_DESC=$(_cs $IH_MAGNETA)
declare -x _F_DEBUG=$(_cs8 60)           # ; $(_cs8 $I8_LIGHT_SEA_GREEN) # _IC_DEBUG=$'\u25ce'

function apply {
    # args: format [str]
    # reads stdin if <str> is empty
    local input format=${1:-$_f}
    shift 1

    printf %s "$format"
    if [[ -z "${*}" ]] ; then
        cat | _ttn
    else
        printf %s "$*"
    fi
    printf %s "$_f"
}

function header_separator {
    # args: [color] [prefix] [alignfn=alignc]
    local title="$(cat)" color="${1-$_i}" alignfn="${3:-alignc}"
    title="$(squeeze $(( $(_w) - ${#2} )) <<< "$title")"
    if [[ -z "$RAW_MODE" ]] ; then
        ${alignfn} $(_ww) "$title" | sed -E "s/\s{${#2}}/$2/" | apply "$color" | append_nl
    else
        spaces=$(( $(_ww) -  $(_ccp <<< "$title") ))
        spaces_left=$(( spaces / 2 ))
        _s $((spaces_left - 1)) -
        printf " %s " "$title"
        _s $((spaces - spaces_left - 1)) -
        printn
    fi
}
function header  {
    # args: [label]...
    # env: HEADER_LVL HEADER_LABEL
    local lvl=${HEADER_LVL:-1}
    local label="${HEADER_LABEL-"${*-"HEADER LVL $lvl"}"}"
    if ! header"$lvl" "${label[@]}" 2>/dev/null ; then
        error "Invalid header level: $lvl"
        RAW_MODE=true \
            header1 "${label[@]}"
    fi
}
function header1 {
    # args: [label...]
    [[ -n "$RAW_MODE" ]] && { printfn "%s" "${*^^}" ; return ; }
    printfn "$_b%s$_f" "${*^^}"
}
function header2 {
    # args: [label...]
    # makes part before first encountered '/' primary label
    [[ -n "$RAW_MODE" ]] && { printfn "$_sp%s" "${*^^}" ; return ; }
    # find first '/' occurrence or string terminator and insert styles terminator:
    printfn "$_sp$_b%s$_f" "${*^^}" | sed -E -e "s/\s*(\/|$)\s*/$_f&/"
}
function header3 { printfn "$(_spl 2)%s" "${*}" ; } # args: [label...]
function table { column -e -t -s "$_tab" ; }         # reads stdin
function tablec { table | sed -Ee 's/( +) /\1/g' ; }  # condensed. reads stdin

# == raw-mode-aware output ==
function verbose { debug_enabled || return 0 ; apply $_F_VERBOSE <<< "$*" ; echo ; }
#function notice  { echo "$*" ; }
function disabled { _fmt_message <<< "$*" "$_F_DISABLED"  "$_IC_DISABLED"  "-" ; }
function notice  { _fmt_message <<< "$*" "$_F_NOTICE"  "$_IC_NOTICE"    "." 1 ; }
function success { _fmt_message <<< "$*" "$_F_SUCCESS" "$_IC_SUCCESS"   "+" 1 ; }
function warn    { _fmt_message <<< "$*" "$_F_WARNING" "$_IC_WARNING"   "!" ; }
function error_in { _fmt_message "$_F_ERROR"   "$_IC_ERROR"    "x" ; }
function error   { error_in <<< "$*" ; }
function prompt_options {
    # args: [title]
    # stdin: option lines, no formatting
    echo "${1:+$1? }Options:"
    if [[ -n "$RAW_MODE" ]] ; then pad ; else
        sed -Ee "s/^(\S+)(.+)$/$_F_PROMPT_PARAM\1$_F_PROMPT_DESC\2$_f/" | pad
    fi
}
function prompt_yn {
    # args: [prompt_question] [print_newline] [auto_substitute]
    local prompt_question="${1:+$1. }Continue?" print_newline=${2:+true} auto_substitute="$3"
    [[ -n "$auto_substitute" ]] && print_newline=true

    while true; do
        printf %s "$prompt_question"
        if [[ -n "$RAW_MODE" ]] ; then
            printf %s " y/n: "
            printf %s "${auto_substitute:+"$auto_substitute <auto>"}"
        else
            printf %s " ${_F_PROMPT_DESC}(${_F_PROMPT_PARAM}y${_F_PROMPT_DESC}/${_F_PROMPT_PARAM}$(_u n)${_F_PROMPT_DESC})$_f: "
            printf %s "${auto_substitute:+"$auto_substitute $_F_PROMPT_PARAM<auto>$_f"}"
       fi
        printf %s "${print_newline:+$_n}"
        if [[ -n "$auto_substitute" ]] ; then
            yn="$auto_substitute"
        else
            read -r -p "" yn
        fi
        case $yn in
          [Yy]*) return 0 ;;
          [Nn]*) return 1 ;;
              *) return 2 ;;
        esac
    done
}
function _ic_caution { _fmt_message <<< "${1:-[!]}" "${_F_WARNING}${_b}" ; } # args: [icon]

function _fmt_message {
    # args: [color] [icon] [label] [no-text-color]
    # stdin: input
    local prefix="${1:-}" icon="${2-}" label="${3}" no_text_color=${4:+true}
    debug "" "${FUNCNAME[0]}" <<< "args: ${*@Q}"
    local input="$(_stdin)"
    if [[ -z "$input" ]] ; then return ; fi
    if [[ -n "$RAW_MODE" ]] ; then
        printfn "(%1.1s) %s" "$label" "$input"
    elif [[ -n "$ES7S_MESSAGE_PREFIX_STYLE" ]]; then
        printfn "${prefix}${_b}%s${_f} %s" "$label" "$input"
    else
        apply "$prefix" <<< "${icon:+$icon}$_f$prefix${no_text_color:+$_f} $input"
        printn
    fi
}

function _is_direct_output {
    # returns 0 if direct, 1 if redirection/pipe
    [[ -t 1 ]] && return 0 || return 1
}
function _set_raw_mode_if_not_direct {
    # disables formatting if pipe or redirect
    if ! _is_direct_output ; then RAW_MODE=true ; fi
}

# -----------------------------------------------------------------------------
# FORMATTING / PRECISE CHAR CONTROL

squeeze() {
    # args: [req_len]
    # stdin: text to fit
    # - - -
    # color-aware string shrinker, fits string to specified
     #  length, adds overflow indicator ($ES7S_OVERFLOW)

    local req_len=${1:-0} __e=$'\033'
    local input suffix clean_str output control_seqs
    local overflow_ind="${ES7S_OVERFLOW:-~}"
    shift 2
    [[ $req_len -le 0 ]] && return 0

    input="$(cat)"
    clean_str="$(_dcu <<< "$input")"
    control_seqs=$(_cesq <<< "$input")
    if [[ ${#clean_str} -le $req_len ]] ; then
        [[ $control_seqs -gt 0 ]] && input+="$_f"
        printf "%s" "$input"
        return 0
    fi

    # overflow indicator is always visible now
    req_len=$((req_len - 1))
    if [[ $control_seqs -le 0 ]] ; then
        output="${clean_str:0:$((req_len))}"
        printf "%s%s" "${output}" "${overflow_ind}"
        return 0
    fi

    # main idea: iterate through beginnings of control sequences in the string
     #            and move them to the output always as a whole, or don't move at all

    while [[ $req_len -gt 0 ]] ; do
        local next_esc_excluded_pos next_esc_included_pos
        # find position of first (relative to   # count how many seq bytes are following
        #  string start) control seq byte:      #  first one in a row:
         #     .*...2.3\e[1m\e[2m.A.B.C...       #   .*...2.3\e[1m\e[2m.A.B.C.D.X\e[38...
          #    0 > > >^                           #         & > > > > ^          ^? this one doesn't matter (yet)

        next_esc_excluded_pos=$(( $( sed -Ee "s/$__e.+//" <<< "$input" | _ccp ) ))
        next_esc_included_pos="$( sed -Ee "s/([^$__e]*)($__e\[[0-9;]+m)[^$__e]+(.+)/\1\2/" <<< "$input" | _cca )"

        if [[ $req_len -le $next_esc_excluded_pos ]] ; then
            # if there are no control chars to the left of desired line cut
            #  just copy regular chars, it's safe:

            output+="${input:0:req_len}"
            req_len=0

        else
             #  + ---- control-seq ----- +
            #  |        included          |
            #  0.1.2.3.4.5.6.7..3\e[1m\e[2m.A.B.C.D.X\e[38..
            #  ^                ^
            #  \_ control-seq _/     that's the key - we copy all chars (including control sequences),
            #      excluded        but _count_ as "copied" only printable characters

            output+="${input:0:$next_esc_included_pos}"                                   # ------------ #       ~
            req_len=$((req_len - next_esc_excluded_pos))                               #-|  OH NO! WHY..  |
            input="${input:$next_esc_included_pos}"                                   #   # ------------ #
                                                                                      #
            # that makes the result string to have required length and also           "                     ~
            # prevents control sequences from becoming broken - when one half     ..\e[1 . ;32m..    ~
        fi  # of it cut out, while the other one stays in place, like this:              |
    done                                                                         # cut > ^              ~
    # this algorithm can be improved, though. first version was designed                       ~
     # to iterate chars one by one, but was never developed. second (this)
      # version uses seds for finding closest control sequences to the
       # beginning and then handles them. even more optimized algorithm would
        # be to start searching from cut position, not the 1st char .. NEVERMIND
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 0
       # if we want to keep ALL the formatting, the only way
      # to accomplish this is like the above. but it
     # can still be improved

    printf "%s%s" "${output}${_f}" "${overflow_ind}"
}

# shellcheck disable=SC2086
alignl() { _arg_stdin "${@:2}" | align -1 ${1-0} ; }
alignc() { _arg_stdin "${@:2}" | align 0 ${1-0} ; }
alignr() { _arg_stdin "${@:2}" | align 1 ${1-0} ; }
align() {
    # args: -1|0|1 req_len [pad|shift]
    # stdin: text
    # first is mode: 0 = center, 1 = right, -1 = left
    # pad counts from edge to center when mode=left|right
    #  and from center when center
    local input result spaces man_pad left_pad right_pad
    local mode=${1:-0}
    local req_len=${2-""}
    local arg3=${3:-0}
    shift 3
    [[ -z "$req_len" ]] && return 0

    input="$(cat)"
    [[ $req_len -le 0 ]] && { printf %s "$input" ; return 0 ; }
    local clean_str="$(printfn "%s" "$input" | _dcu)"
    local clean_len=${#clean_str}

    result="$input"
    if [[ $clean_len -lt $req_len ]] ; then
        spaces=$(( req_len - clean_len ))
        [[ $spaces -lt 0 ]] && spaces=0

        if [[ $mode -eq 0 ]]; then
            local req_shift=$arg3
            left_pad=$(( spaces / 2 ))
            spaces=$(( spaces - left_pad ))
            [[ $spaces -lt 0 ]] && spaces=0
            [[ $left_pad -gt $spaces ]] && left_pad=$spaces

            right_pad=$(( spaces ))
            spaces=0
            [[ $right_pad -lt 0 ]] && right_pad=0

            local left_ss="$(printf "%${left_pad}s" "")"
            local right_ss="$(printf "%${right_pad}s" "")"
            result="$(printf "%s%s%s" "$left_ss" "$result" "$right_ss")"
        else
            man_pad=$(( arg3 )) # force_pad
            [[ $man_pad -gt $spaces ]] && man_pad=$spaces
            man_ss="$(printf "%${man_pad}s" "")"

            spaces=$(( spaces - man_pad ))
            [[ $spaces -lt 0 ]] && spaces=0
            auto_ss="$(printf "%${spaces}s" "")"

            if [[ $mode -eq -1 ]]; then
                result="$(printf "%s%s%s" "$man_ss" "$result" "$auto_ss")"
            elif [[ $mode -eq 1 ]]; then
                result="$(printf "%s%s%s" "$auto_ss" "$result" "$man_ss")"
            fi
        fi
    fi
    printf "%s" "$result"
}

trim() {
    # reads stdin, trims it to <max_len> chars and adds dots if input was longer
    # args: [max_len=10]
    sed -Ee "s/(.{${1:-10}}).{2,}/\1$ES7S_OVERFLOW/"
}

function _stdin { cat - ; } # stdin read wrapper
function _arg_stdin {
    # Reads args from stdin when none is supplied.
    # Usage: _arg_stdin "$@" | ...
    [[ -n "$*" ]] && printfn %s "$@" && return
    _stdin
}

# -----------------------------------------------------------------------------
# FORMATTING / HARDCORE

vesq() {
    # args: [esq_details] [omit_esq]
    # visualize escape sequences and whitespaces
    if [[ "$1" = -h ]] || [[ "$1" = --help ]] ; then
    printfn %s "Set first argument to a non-empty value to get more information about printed control sequences." "By default recognized escape sequences apply to original text as well as seq markers; to disable it set second argument to a non-empty value." | pad
    return 0 ; fi
    local detailed_esq="${1:+"\\2"}"
    local apply_esq=$(_nots "${2-}" "&")
    local __e=$'\033'
#@TODO допилить поток сука блять заебало
    # https://en.wikipedia.org/wiki/ANSI_escape_code
    sed -E -e "s/($__e\[)(0?)(m)/\10\3/g" \
           -e "s/($__e\[)([0-9;]*)(m)/${_f}${_i}ɘ${detailed_esq}${apply_esq}${_ni}/g" \
           -e "s/($__e\[0m)($__e\[7m)ɘ0*/\1\2Ǝ/g" \
           -e "s/ /␣/g"  -e "s/\t/${_i}»${_ni}&/g"  \
           -e "s/$/$_i$_b$_gy"$'\u21b5'"$_f/g" -e "s/\v/$_i$_b$_gy\\\v$_f/g" -e "s/\f/$_i$_b$_gy\\\f$_f/g" \
           -e "s/\r/$_i$_b$_y↤$_f/g"  -e "s/\x00/${_hr}${_i}${_b}Ø$_f/g" \
           -e "s/($__e)([^_@A-Z\x5c\x5b\x5d])/${_r}${_i}æ${detailed_esq}${_f}/g" # \
#| sed -z           -e "s/(\e\[)([0-9:;<=>?[\]]*[!\"#$%&\'()*+,\-\.\/]*[A-Za-z_\[\]])/$_hr$_i\\\2$_f/g"
#           -e "s/(\e)([0-9:;<=>?[\]]*[!\\\"#$%&'()*+,\-\.\/]*[A-Za-z[\]_\`\{\|\}~^])/\2/g"

   #        -e "s/($__e)([0-9:;<=>?[\]]*[ \!\"\#\$\%\&\'\(\)\*\+,\-\.\/]*[A-Za-z\[\\\]\^_\`\{\|\}~]) /$_b${_y}$_i"$'\u241b'"\2${_u}$_f/g"



}

# == trimming whitespaces, context - line ==
function _trim { _triml | _trimr ; }
function _triml { sed -Ee "1 s/^(\s*)//" ; }
function _trimr { sed -Ee "$ s/(\s*)$//" ; }

# == trimming whitespaces, context - byte stream/multiline ==
function _ttn { sed -z '$ s/\n$//' ; } # trim trialing newline
function _ttw { sed -zEe 's/[[:space:]]*$//' ; } # trim trialing whitespace

# == char counting ==
function  _cca { _ttn | wc -m ; } # count chars - all
function  _ccp { _dc | _ttn | wc -m ; } # count chars - printable
function _cesq { tr -cd '\033' | wc -c ; } # count \e[*m seqs in stdin

# == deformatting ==
function _dc  { decolorize ; }
function _dcu { decolorize-clean-up ; }

# read stdin, remove \e[*m seqs:
decolorize() { sed --unbuffered -Ee 's/\x1b\[[0-9\;]*m//g' ; }

# read stdin, remove \e[*m seqs and ASCII control chars:
decolorize-clean-up() { sed --unbuffered -Ee 's/\x1b\[[0-9\;]*m//g' | tr -d '\000-\011\013-\037';  }

# remove \[ "\\\[" and \] "\\\]" sequences from stdin (used to tell shell to skip chars between when counting printable):
remove-prompt-escaped-brackets() { sed -zEe 's/\\(\[|\])//g' ; }

# translate/remove UNICODE control chars:
tr-unicode-controls() {
    # args: [replacement="."]
    #sed -Ee "s/((\xc2[\x7f-x9f])[|]?+)/${1-}/g"
    # ^ breaks watson U+0080-009F displaying @see #225
    sed -Ee "s/\xc2\x7f|\xc2\x80|\xc2\x81|\xc2\x82|\xc2\x83|\xc2\x84|\xc2\x85|\xc2\x86|\xc2\x87|\xc2\x88|\xc2\x89|\xc2\x8a|\xc2\x8b|\xc2\x8c|\xc2\x8d|\xc2\x8e|\xc2\x8f|\xc2\x90|\xc2\x91|\xc2\x92|\xc2\x93|\xc2\x94|\xc2\x95|\xc2\x96|\xc2\x97|\xc2\x98|\xc2\x99|\xc2\x9a|\xc2\x9b|\xc2\x9c|\xc2\x9d|\xc2\x9e|\xc2\x9f/${1-''}/g"
}

# -----------------------------------------------------------------------------
# GIT SHARED HELPERSq

function __git_current_branch {
    git rev-parse --abbrev-ref HEAD 2> /dev/null
}

# -----------------------------------------------------------------------------
# HIGH ORDER ALCHEMY

# forces terminal to ignore all user input except Ctrl+C:
hide-user-input() { trap __terminal_cleanup EXIT ; trap __hide_input CONT ; __hide_input ; }
function __hide_input { if [ -t 0 ]; then stty -echo -icanon time 0 min 0 ; fi }
function __terminal_cleanup { if [ -t 0 ]; then stty sane ; fi }

# determine current cursor position:
function _curpos_request { printf "\e[6n" ; }
function _curpos_response_getx {
    local CURPOS_TIMEOUT_SECONDS=1
    local CURPOS_WAIT_SECONDS=1.1
    # timeout is needed to prevent infinite hanging up ;
    #  an alternative is to check if stdout is a terminal: [[ -t 1 ]]
    #  and disable this feature if it is not

    start_time=$(date +%s.%3N)
    read -t $CURPOS_WAIT_SECONDS -sdR CURPOS_STREAM
    elapsed_time=$(round "$(date +%s.%3N) - $start_time")
    if [[ $elapsed_time -ge $CURPOS_TIMEOUT_SECONDS ]] ; then return 2 ; fi

    # originally: ${CURPOS_STREAM#*[}
    CURPOS="$(sed <<< "${CURPOS_STREAM##*[}" -Ee "s/^[0-9]+;([0-9]+)$/\1/" -e "s/([^;]+)(;.+|$)/\1/")"
    if ! _ttw <<< "$CURPOS" | grep -qEe "^[0-9]+$" ; then return 1 ; fi
    printf %s "$CURPOS"
}

set-title() {
    printf "\e]0;%s\007" "$*";
}
set-title-and-run() {
    set-title "$*"
    "$@"
}

# -----------------------------------------------------------------------------
# DEBUGGING (KIND OF)

declare -x ES7S_DEBUG_BUF
enable-debug() { ES7S_DEBUG=true ; }
debug-char-ruler() {
    # args: [force=] [no_color=]
    # if first arg is non-empty value, displays ruler even in normal mode
    local force="${1:+true}" no_color="${2:+true}"
    debug_enabled || [[ -n $force ]] || return 0

    local f_inactive="$(_cs8 $I8_GRAY)"
    local f_active="$_u$_ov$_be"
    local f_active_hl="$_u$_ov$_y"
    local width=$(_ww) shift=1
    # shift is needed because first char should be marked as 1, not 0

    local logo="${_y}es7s|${f_inactive}"
    local sep10="╹" section="#''''╵''''"

    local i begin end output label
    local n=$((1 + width / 10))
    for (( i=0 ; i<n ; i++ )) ; do
    printf "%d " $i >> /tmp/ruler
        [[ $i -eq 1 ]] && { shift=0 ; logo="│$logo" ; }
        label=$(( i * 10 ))
        local f=$f_active
        if [[ $((i%10)) -eq 0 ]] ; then f=$f_active_hl ; fi
        if [[ $((i%40)) -eq 0 ]] ; then begin="$f${logo}${f_inactive}"
                                   else begin="$f${sep10}${label}${f_inactive}$(_s 1)"
        fi ;  if [[ $i -eq 21 ]] ; then begin="$f${sep10}$(squeeze 9 <<< "weeeeeeeeee")$f_inactive"
            elif [[ $i -eq 40 ]] ; then begin="$f${ES7S_OVERFLOW}eeees7s${logo::1}$f_inactive"
        fi
        end="${section:$(( $(_ccp <<< "$begin") + shift ))}" ;
        output+="$begin$end"

        if [[ $( _ccp <<< "$output" ) -ge $width ]] ; then
            [[ -n $no_color ]] && output="$(_dcu <<< "$output")"
            squeeze $width <<< "$output"
            break
        fi
    done
}
var-dump-v1() {
    # args: [filter_names=]
    # dump all variables, filter var name by egrep -e "$1" if provided
    local filter_names="${1-}"
    local skipped=0 vars
    vars=$(set -o posix; IFS=$'\n' set)
    for v in "$vars" ; do
        if [[ -z "$filter_names" ]] || grep -qEe "$filter_names" <<< "$v" ; then
            sed <<< "$v$_f" -E -e "s/^/$_gn/" -e "s/=/$_be&$_f/"
        else
            ((skipped++))
        fi
    done
    [[ -n "$filter_names" ]] && notice "${skipped} results filtered"
}
var-dump-v2() {
    vars=$(set -h -o allexport; IFS=$'\n' set)
    echo "$vars" \
    | sed --unbuffered -Ee '/^vars/d; /^[\x09\x27 ]/d;' \
    | sed --unbuffered -zEe 's/\n\s*\{[^}]+\}\n/{...}\n/g' \
    | sed --unbuffered -Ee '/^[{}*]/d' \
    | tr -d $'\x1b' \
    | LESSOPTS=-+S bat -l bash --wrap=never
}

debug_enabled() { [[ -n "${ES7S_DEBUG-""}" ]] ; } # usage: debug_enabled && <cmd> || return
debug() { # can be used to flush previously buffered output
    # args: [add_newline=true] [src_override=]
    # stdin: text
    debug_enabled || return 0
    debug_buf "${1:-true}"
    debug_flush "${2:-}"
}
function debug_flush {
    # args: [src_override=]
    # stdin: text
    debug_enabled || return 0
    local func_name="$(echo "${FUNCNAME[-1]//[^A-Za-z0-9_]/}" | tr -s _)"
    local source_name="$(basename "${BASH_SOURCE[-1]//.sh/}")"
    [[ $source_name == "bash-alias" ]] && source_name="(${source_name}) ${func_name}"
    [[ -n "$1" ]] && source_name="$source_name:$1"
    if [[ -n "$RAW_MODE" ]] ; then
        printf %s "${ES7S_DEBUG_BUF}" | sed -Ee "s/^/(DEBUG)[${source_name^^}] /;"
    else
        printf %s "${ES7S_DEBUG_BUF}" |
            sed -E -e "s/^.*/${_F_DEBUG}${_i}${source_name^^}${_ni}${_F_DEBUG} &${_f}/g"
    fi
    ES7S_DEBUG_BUF=
}
function debug_buf {
    # args: [add_newline=]
    # stdin: text
    debug_enabled || return 0
    local append_nl_arg="${1:+1}"
    mapfile -c1 -C "_debug_buf_line_callback" < <( _stdin | append_nl "${append_nl_arg:-0}" | _ttn)
}
function _debug_buf_line_callback { shift 1 ; ES7S_DEBUG_BUF+="$*" ; }

# -----------------------------------------------------------------------------
# DEBUGGING (PROPER)

enable-etrace() { trap '__trace_errors' ERR ; set -o errtrace ; }
function __trace_errors {
  local err=$?
  set +o xtrace
  local code="${1:-1}"
  echo "Error in ${BASH_SOURCE[1]}:${BASH_LINENO[0]}. '${BASH_COMMAND}' exited with status $err"
  # print out the stack trace described by $function_stack
  if [ ${#FUNCNAME[@]} -gt 2 ]
  then
    echo "Call tree:"
    for ((i=1;i<${#FUNCNAME[@]}-1;i++))
    do
      echo " $i: ${BASH_SOURCE[$i+1]}:${BASH_LINENO[$i]} ${FUNCNAME[$i]}(...)"
    done
  fi
  echo "Exiting with status ${code}"
  exit "${code}"
}

################################################################################
# DEPRECATIONS / DO NOT USE

function _deprecated {
    printf %s "$_f$_b$_i${_r}DEPRECATION WARNING $_f$_u${_y}$(_jb " <- " "${FUNCNAME[@]}")"
    printfn %b " $(_cs $IH_YELLOW $I_BOLD 5)DO NOT USE OR YOU WILL REGRET$_f"
    printf %s "$*"
}
#function _g { _deprecated "$*" ; } ; declare _g="$(_g nested call)"
#function _gr { _deprecated "$*" ; } ; declare _gr="$(_gr nested call)"
#function info { _deprecated "$*" ; }
#function sb { _deprecated "$*" ; }
declare _imk=$(_deprecated _imk)

################################################################################
# DONE

function __es7s_com { echo "ES7S commons loaded"; }
debug <<< "Loaded es7s/commons"
