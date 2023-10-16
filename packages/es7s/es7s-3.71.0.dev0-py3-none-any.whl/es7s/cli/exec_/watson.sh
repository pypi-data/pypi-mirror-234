#!/usr/bin/bash
# -----------------------------------------------------------------------------
# es7s/watson (G1/legacy)
# (C) 2021-2022 A. Shavykin <0.delameter@gmail.com>
# -----------------------------------------------------------------------------
# shellcheck source=../es7s-shell-commons.sh
__E7SL() { local c="$(realpath "$(dirname "$(readlink -f "$0")")")" ; local l=\
"es7s-shell-commons.sh" ; local p=( "$ES7S_SHELL_COMMONS" "$HOME/.es7s/data/$l"
"$c/../$l" ); while [[ ! $(type -t __es7s_com) =~ ^fu ]];do [[ -f "${p[0]}" ]]\
&& source "${p[0]}"; p=("${p[@]:1}"); [[ "${#p[@]}" -gt 0 ]] && continue; echo\
'ERROR: es7s/commons is missing (ES7S_SHELL_COMMONS)'; exit 57; done } ; __E7SL
# ------------------------------------------------------------- loader v.3B ---

_illegal_opt() { error "Illegal option -${OPTARG:-"-"$OPT}" ; _print_help_hint ; exit 1 ; }
_ensure_arg() { if [[ -z "${OPTARG:-""}" ]] ; then error "No arg for --$OPT option" ; _print_help_hint ; exit 1 ; fi }
_print_help_hint() { printfn "Show usage: $SELF --help" ; printn ; }
_print_help() {
    printfn ".--.      .--.   ____   ,---------.   .-'''-.     ,-----.    ,---.   .--."
    printfn "|  |_     |  | .'  __ '.\          \ / _     \  .'  .-,  '.  |    \  |  | "
    printfn "| _( )_   |  |/   '  \  \'--.  ,---'('' )/'--' / ,-.|  \ _ \ |  ,  \ |  | "
    printfn "|(_ o _)  |  ||___|  /  |   |   \  (_ o _).   ;  \  '_ /  | :|  |\_ \|  | "
    printfn "| (_,_) \ |  |   _.-'   |   :_ _:   (_,_). '. |  _',/ \ _/  ||  _( )_\  | "
    printfn "|  |/    \|  |.'   _    |   (_I_)  .---.  \  :: (  '\_/ \   ;| (_ o _)  | "
    printfn "|  '  /\  '  ||  _( )_  |  (_(=)_) \    '-'  | \ '^/  \  ) / |  (_,_)\  | "
    printfn "|    /  \    |\ (_ o _) /   (_I_)   \       /   '. \_/''^.'  |  |    |  | "
    printfn "'---'    '---' '.(_,_).'    '---'    '-...-'      '-----'    '--'    '--' "
    printn
    printfn "Print Unicode char table and UTF-8/UTF-16/UTF-32 summary"
    printn
    header "USAGE"
    pad <<< "$SELF [<options>]"
    printn
    header "OPTIONS"
    pad < <(printfn %s \
        "-s, --start=<number>     byte to start from (inclusive, default is 0x20, max is 0x10ffff)" \
        "-n, --count=<number>     bytes to print (default is 100)" \
        "-c, --columns=<number>   format output as <number> columns (default is 4)" \
        "-e, --every=<number>     print every <number> char (default is 1 (all))" \
        "-v, --verbose=<level>    how much extra info to print (0-4, default is 3)" \
        "-a, --all                print out control characters as well (by default replaced with dot)" \
        "-r, --raw                disable all formatting and alignment (equivavlent to $(_b -c0 -v1))" \
        "-h, --help               get help information"
    )
    printn
    pad <<< "Mandatory or optional arguments to long options are also mandatory or optional for any corresponding short options."
    printn
    header "EXAMPLES"
    pad < <(
        printfn "$SELF -c 10 -e 2 -n 1000 -s 10000"
        pad <<< "Print every 2nd char from 10000 to 11000 formatted as 10-column table"
        printn
        printfn "$SELF -s 0x1f611 -n 50 -c0 -v1"
        pad <<< "Some $(printf '\U0001F631') emojis, plain list without any additional info"
        printn
        printfn "$SELF -n 0x10ffff -v4 -c1 -e7000"
        pad <<< "Print characters all across the Unicode with maximum verbosity (but very sparse)"
        printn
        printfn "$SELF -n 0x20 -c0 -v0 -a | od -t azx"
        pad <<< "Print control chars as is (do not replace them), od is necessary to actually see something"
        printn
    )
    header "TROUBLESHOOTING"
    pad <<< "There is a built-in variable character width compensation mechanism, but it's based on ANSI control sequences and can be shaky sometimes. It is involved for table-printing only, so setting verbosity level lower than 3 disables it (e.g. \"$(_b -v2)\"). Alternatively, pass an environment variable $(_b NO_STABILIZING) with a non-empty value to disable it specifically: \"NO_STABILIZING=1 $SELF [<options>]\""
    printn
}
_print_init_info() {
    debug_enabled || return 0
  ( local fmt="%s\t %8d\t0x%08x\t%s\t%s\t%8s\t%s\t%s"
    printfn "$fmt" "START BYTE" "$START_BYTE" "$START_BYTE" "|" "COLS" "$COLS" "ENABLE_TABLE" "$(printb $ENABLE_TABLE)"
    printfn "$fmt" "END BYTE" "$END_BYTE" "$END_BYTE" "|"  "ROWS" "~$(( ROWS / PRINT_EVERY ))"
    printfn "$fmt" "MAX BYTE" "$MAX_BYTE" "$MAX_BYTE" "|"
  ) | table | debug
  ( local fmt="%s\t%5s\t%s\t%s\t%s\t%s\t%s"
    printfn $fmt "COLUMN STABILIZING" "$(printb $ENABLE_STABILIZING)" "|" "MAX CHARS:"
    printfn $fmt "VERBOSITY LEVEL" "$VERBOSITY" "|" "NUM" "$mc_num" "UID" "$mc_uid"
    printfn $fmt "PRINT EVERY <n> CHAR" "$PRINT_EVERY" "|"  "ID" "$mc_id" "UTF-8" "$mc_utf8"
    printfn $fmt "PRINT CONTROL CHARS" "${PRINT_CONTROL_CHARS:-false}" "|" "UTF-16" "$mc_utf16" "UTF-32" "$mc_utf32"
  ) | table | debug
}
# -----------------------------------------------------------------------------
_print_chars() {
    local mc_num=0 mc_uid=0 mc_id=0
    local mc_utf8=0 mc_utf16=0 mc_utf32=0 # max chars
    local i j n is_first_col

    [[ $(( START_BYTE )) -lt 0 ]] && START_BYTE=0
    END_BYTE=$(( START_BYTE + COUNT ))
    [[ $(( END_BYTE )) -gt $MAX_BYTE ]] && END_BYTE=$MAX_BYTE
    ROWS=$(( $(( END_BYTE - START_BYTE )) / $(max 1 $COLS) ))

    [[ $(( END_BYTE )) -le 0xFF ]] && ENABLE_STABILIZING=  # ASCII 8-bit only, no stab required

    mc_num=$( format_pval_number $((END_BYTE - 1)) | _dcu | _ttw | wc -c )
    mc_uid=$( format_pval_uid $((END_BYTE - 1)) | _dcu | _ttw | wc -c )
    #mc_id=$mc_uid ; [[ $mc_num -gt $mc_uid ]] && mc_id=$mc_num
    mc_utf8=$( format_pval_utf8 $((END_BYTE - 1)) | _dcu | _ttw | wc -c )
    if [[ $((VERBOSITY)) -gt 3 ]] ; then
        mc_utf16=$( format_pval_utf16 $((END_BYTE - 1)) | _dcu | _ttw | wc -c )
        mc_utf32=$( format_pval_utf32 $((END_BYTE - 1)) | _dcu | _ttw | wc -c )
    fi
    _print_init_info

    row_idx=0
    for ((i=START_BYTE; i<START_BYTE+ROWS+1; i+=PRINT_EVERY)); do
        column_idx=0
        [[ -n $ENABLE_TABLE ]] && debug_buf <<< " ║ "

        debug_enabled && printf "$_c$_i"
        printf "%s" "$PADDING"
        debug_enabled && printf "$_f"

        for ((j=i; j<END_BYTE; j+=$((ROWS + 1)))); do
            n=$j
            [[ $(( n )) -gt $END_BYTE ]] && n=$END_BYTE

            if [[ $j != $i ]] && [[ -n $ENABLE_TABLE ]] ; then
                if [[ -n $ENABLE_STABILIZING ]] ; then
                    _stabilize_column
                else
                    apply "$SEPARATOR_FORMAT" <<< "$SEPARATOR"
                fi
            fi
            is_first_col= ; [[ $j == $i ]] && is_first_col=true
            is_last_col= ; [[ $(( column_idx + 1 )) -eq $((COLS)) ]] && is_last_col=true

            _print_pval_id $n $is_first_col
            _print_pval_utf $n
            _print_pval_char $n

            if [[ $((VERBOSITY)) -eq 1 &&  $is_last_col ]] ; then
                printf "%s " "$SEPARATOR"
                _print_pval_id $n true
            fi

            column_idx=$((column_idx + 1))
            [[ $(( n )) -gt $END_BYTE ]] && continue
        done

        ((row_idx++))
        debug_flush
        if [[ -n $ENABLE_TABLE ]] ; then
            printn
            [[ $((row_idx % 10)) -eq 0 ]] && debug-char-ruler
        fi
    done

    [[ -n $ENABLE_TABLE ]] && printn
}

_encode_cid() {
    # arg: <unicode char ID, ex.: 128676 for U+1F6A4>
    printf "\\U$(printf %08x "$*")"
}
_encode_cid_utf16() {
    # arg: <char id>
    _encode_cid "$*" | iconv -f utf-8 -t utf-16le 2>/dev/null
}
_encode_cid_utf32() {
    # arg: <char id>
    _encode_cid "$*" | iconv -f utf-8 -t utf-32le 2>/dev/null
}
_utf16_surrogate_check() {
    # arg: <char id>
    [[ $(($*)) -ge 0xd800 ]] && [[ $(($*)) -le 0xdfff ]] && return 1
    return 0
}


format_pval_char() {
    # arg: <char id>
    if [[ $(($*)) -eq CHAR_CODE_DOT ]] ; then alignc $W_CHAR " ." | apply $_b ; return 0
    elif [[ $(($*)) -eq CHAR_CODE_SPACE ]] ; then printf %s " SP" | apply $_y ; return 0
    fi

    char="$(_encode_cid "$*" | _postprocess_char | _trim)"
    if [[ "${#char}" == 3 ]] && [[ -z "$PRINT_CONTROL_CHARS" ]] ; then
        local invalid_char="err"
        if ! _utf16_surrogate_check "$*" ; then
            invalid_char="SRG"
        fi
        printf %s "$invalid_char" | apply $_r$_i

    elif [[ -z "$char" ]] || [[ "$char" == "." ]] ; then
        pval_escaped="$(format_pval_escaped "$*")"
        if [[ -n "$pval_escaped" ]] ; then
            printf %s "$pval_escaped"
        else
            pval_short="$(format_pval_short_name "$*")"
            if [[ -n "$pval_short" ]] ; then
                printf %s "$pval_short"
            else
                alignr $W_CHAR "SEP" | apply $_r
            fi
        fi
    else
        alignc $W_CHAR "$char" | apply $_b
    fi
}
format_pval_number() {
    # arg: <char id> <dim_mode>
    local hl_format="$(_cs $IH_BLUE $I_BOLD)"
    local dim_format="$(_cs $I_BLUE)"
    if [[ -n "$2" ]] ; then
        _sbp ',' 3 "$1" | apply "$dim_format" | alignr ${mc_num-0}
    else
        _sbp ',' 3 "$1" | \
            sed -E -e "s/[0-9]+/$hl_format&$_f/g" \
                   -e "s/,/$dim_format&$_f/g" | \
            alignr ${mc_num-0}
    fi
}
format_pval_uid() {
    # arg: <char id>
    printf "${_be}U+$_f${_hbe}${_b}%X$_f" "$*" | alignr ${mc_uid:-}
}
format_pval_utf8() {
    # arg: <char id>
    _encode_cid "$*" | od -An -t x1 | tr -d "\n" | _trim | apply "$(_cs $IH_CYAN)" | alignr ${mc_utf8-}
}
format_pval_utf16() {
    # arg: <char id>
    if ! _utf16_surrogate_check "$*" ; then
        apply "$(_cs $I_RED)" "utf-16" | alignr ${mc_utf16-}
        return 0
    fi
    local v_utf16="$(_encode_cid_utf16 "$*" | od -An -t x2 | tr -d "\n" | _trim)"
    if [[ -z "$v_utf16" ]] ; then
        printf "${_r}%04x$_f" "$*" | alignr ${mc_utf16-}
    else
        printf %s "$v_utf16" | _colorize_hex $_hm $_m | alignr ${mc_utf16-}
    fi
}
format_pval_utf32() {
    # arg: <char id>
    if ! _utf16_surrogate_check "$*" ; then
        apply "$(_cs $I_RED)" "surrogate" | alignr ${mc_utf32-}
        return 0
    fi
    local v_utf32="$(_encode_cid_utf32 "$*" | od -An -t x4 | tr -d "\n" | _trim)"
    if [[ -z "$v_utf32" ]] ; then
        printf "${_r}%08x$_f" "$*" | alignr ${mc_utf32-}
    else
        printf %s "$v_utf32" | _colorize_hex $_hm $_m | alignr ${mc_utf32-}
    fi
}
format_pval_escaped() {
    # arg: <char id>
    local pval="$(_encode_cid "$*" | od -An -t c | tr -d "\n" | _triml)"
    local cid_oct="$(printf %03o "$*")"
    if [[ -z "$pval" ]] || [[ "${pval:0:3}" == "$cid_oct" ]] ; then
        printf ''
    elif [[ "${pval:0:3}" == "302" ]] ; then
        apply "$(_cs $I_RED)" "UCC"
    elif [[ "${pval:0:3}" == "341" ]] || [[ "${pval:0:3}" == "342" ]] || [[ "${pval:0:3}" == "343" ]] ; then
        apply "$(_cs $I_RED)" "SEP"
    else
        apply "$(_cs $I_YELLOW)" "${pval:0:$W_CHAR}" | alignr "$W_CHAR"
    fi
}
format_pval_short_name() {
    # arg: <char id>
    _encode_cid "$*" | od -An -t a | tr -d "\n" | tr "[:lower:]" "[:upper:]" | \
        _trim | sed -Ee "s/^(.{,$W_CHAR}).*/\1/" | apply $_r | alignr "$W_CHAR"
}


_print_pval_id() {
    # arg: <char id> <force-print>
    [[ $((VERBOSITY)) -eq 0 ]] && return 0

    if [[ $((VERBOSITY)) -eq 1 && -z $2 ]] ; then
        return 0
    elif [[ $((VERBOSITY)) -lt 4 ]] ; then
        format_pval_uid $1
        #if [[ $1 -lt 128 ]] ; then
        #    format_pval_number $1 | alignr ${mc_id-0}
        #else
        #    format_pval_uid $1 | alignr ${mc_id-0}
        #fi
    else
        format_pval_uid $1
        printf " "
        format_pval_number $1
    fi
}
_print_pval_utf() {
    # arg: <char id>
    [[ $((VERBOSITY)) -lt 3 ]] && return 0
    printf " "
    format_pval_utf8 "$*"
    if [[ $((VERBOSITY)) -gt 3 ]] ; then
        printf " "
        format_pval_utf16 "$*"
        printf " "
        format_pval_utf32 "$*"
    fi
}
_print_pval_char() {
    # arg: <char id>
    debug_enabled && printf "$_c$_i"
    printf "%s" "$PADDING"
    debug_enabled && printf "$_f"

    if [[ $((VERBOSITY)) -lt 2 ]] ; then
        _encode_cid "$*" | _postprocess_char
    else
        format_pval_char "$*"
    fi
}
_postprocess_char() {
    # stdin: <char/text>
    if [[ -n "$PRINT_CONTROL_CHARS" ]] ; then
        tr "\0" "."
    else
        tr "[:cntrl:]" "." | tr-unicode-controls "."
    fi
}

_stabilize_column() {
    local cursor_x prev_row_cursor_x cursor_dx
    local right_separator="$SEPARATOR"
    local separator_fmt="$SEPARATOR_FORMAT"

    _curpos_request ; cursor_x="$(_curpos_response_getx)" ; code=$?
    if [[ $code == 2 ]] ; then
        ENABLE_STABILIZING=
        debug <<< "DISABLED: COLUMN_STABILIZING"
    fi
    debug_buf <<< "${cursor_x:-"?"} "

    if [[ -n "${cursor_x-}" ]] && \
        [[ ${CURRENT_COL_SHIFTS[$column_idx]+"exists"} ]] && \
        [[ -n "${CURRENT_COL_SHIFTS[$column_idx]}" ]]
    then
        prev_row_cursor_x=${CURRENT_COL_SHIFTS[$column_idx]}
        cursor_dx=$((prev_row_cursor_x - cursor_x))
        if [[ $((cursor_dx)) -gt 0 ]] ; then
            debug_enabled && separator_fmt="$_gn$_i"
            debug_buf < <(apply "$_hgn$_b$_i" ">")
            printf "%${cursor_dx}s" "" | apply "$separator_fmt"
            cursor_x=$((cursor_x + cursor_dx))
        else
            while [[ $((cursor_dx)) -lt 0  ]] && [[ ${#right_separator} -gt 0 ]] ; do
                cursor_dx=$((cursor_dx + 1))
                cursor_x=$((cursor_x - 1))
                right_separator="${right_separator:1}"
                debug_buf < <(apply "$_hy$_b$_i" "<")
                debug_enabled && separator_fmt="$_y$_i"
            done
        fi
    fi
    apply "$separator_fmt" <<< "$right_separator"
    CURRENT_COL_SHIFTS+=([$column_idx]="$cursor_x")
}
_colorize_hex() {
    # args: <hl_format> <lead_zero2x_format>
    sed -E -e "s/^((00)*)(.+)/${2}\1$_f${1}\3$_f/"
}
# -----------------------------------------------------------------------------
declare SELF="${0##*/}"
declare MAX_BYTE=$(printf %d 0x10ffff)
declare CHAR_CODE_DOT=0x2e
declare CHAR_CODE_SPACE=0x20
declare W_CHAR=3
declare -A CURRENT_COL_SHIFTS
declare ENABLE_STABILIZING=true
[[ -n "$NO_STABILIZING" ]] && ENABLE_STABILIZING=""

declare START_BYTE=0x0
declare COUNT=127
declare COLS=6
declare PRINT_EVERY=1
declare VERBOSITY=2
declare PRINT_CONTROL_CHARS=
#declare RAW_MODE= # @es7s-commons
declare ENABLE_TABLE=true

while getopts :as:n:c:e:v:rh-: OPT; do
    if [ "$OPT" = "-" ]; then
        OPT="${OPTARG%%=*}"
        OPTARG="${OPTARG#$OPT}"
        OPTARG="${OPTARG#=}"
    fi
    # shellcheck disable=SC2214
    case "$OPT" in
          a|all) PRINT_CONTROL_CHARS=true ;;
        s|start) _ensure_arg
                 START_BYTE="$OPTARG" ;;
        n|count) _ensure_arg
                 COUNT="$OPTARG" ;;
      c|columns) _ensure_arg
                 COLS="$OPTARG" ;;
        e|every) _ensure_arg
                 PRINT_EVERY="$OPTARG" ;;
      v|verbose) _ensure_arg
                 VERBOSITY=$(( OPTARG )) ;;
          r|raw) RAW_MODE=true
                 COLS=0
                 VERBOSITY=1
                 ;;
         h|help) _print_help
                 exit 0 ;;
          ??*|?) _illegal_opt ;;
    esac
done
# -----------------------------------------------------------------------------
declare PADDING=" "
declare SEPARATOR=" │ "
declare SEPARATOR_FORMAT="$_gy"

if [[ $(( COLS )) -le 0 ]] ; then
    COLS=0
    ENABLE_TABLE=
fi
if [[ $(( COLS )) -lt 2 ]] ; then
    ENABLE_STABILIZING=
    SEPARATOR=""
fi
if [[ $((VERBOSITY)) -eq 1 ]] ; then
    SEPARATOR="  "
fi
if [[ $((VERBOSITY)) -eq 0 ]] ; then
    ENABLE_STABILIZING=
    SEPARATOR=""
    PADDING=""
fi

[[ -n "$NO_SEPARATOR" ]] && SEPARATOR=

if debug_enabled ; then
    PADDING="$(sed -Ee "s/\s/·/g" <<< "$PADDING")"
    SEPARATOR="$(sed -Ee "s/\s/·/g" <<< "$SEPARATOR")"
    SEPARATOR_FORMAT="$_i$_c"
fi

if [[ -n "$ENABLE_STABILIZING" ]] ; then
     # purpose of this thing is to keep program running when stabilizing
     # is active, so no reason to invoke it when it's not
    : #hide-user-input
fi
_print_chars
