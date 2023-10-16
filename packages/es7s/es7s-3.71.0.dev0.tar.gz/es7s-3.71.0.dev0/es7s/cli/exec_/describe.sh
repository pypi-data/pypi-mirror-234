#!/bin/bash
# -----------------------------------------------------------------------------
# es7s/core
# (C) 2022 A. Shavykin <0.delameter@gmail.com>
# -----------------------------------------------------------------------------
# shellcheck disable=SC2120
# shellcheck source=../es7s-shell-commons.sh
__E7SL() { local c="$(realpath "$(dirname "$(readlink -f "$0")")")" ; local l=\
"es7s-shell-commons.sh" ; local p=( "$ES7S_SHELL_COMMONS" "$HOME/.es7s/data/$l"
"$c/../$l" ); while [[ ! $(type -t __es7s_com) =~ ^fu ]];do [[ -f "${p[0]}" ]]\
&& source "${p[0]}"; p=("${p[@]:1}"); [[ "${#p[@]}" -gt 0 ]] && continue; echo\
'ERROR: es7s/commons is missing (ES7S_SHELL_COMMONS)'; exit 57; done } ; __E7SL
# ------------------------------------------------------------- loader v.3B ---

describe() {
    [[ $1 =~ ^--?h(elp)? ]] && printf "%s\n" \
"Usage:" \
"  ${FUNCNAME[0]} <command>" "" \
"  <command> can be anything that bash interprets. If it is:" \
"       executable file     display source code or open $(_u man) page for it" \
"     alias or function     display source code" \
"    builtin or keyword     run '$(_u help) <command>'" "" \
"  If source code is available, $(_u pygmentize) is invoked for syntax highlighting. Source language is guessed " \
"by library itself for executables and set up explicitly as \"shell\" in case of aliases and functions. Pager " \
"is invoked next if neccessary." "" \
"  Can be used for user scripts too, as long as they are located in \$PATH." "" \
"Examples:" \
"  ${FUNCNAME[0]} sed" \
"  ${FUNCNAME[0]} print-env python" \
| sed -Ee "s/executables?|alias(es)?|functions?|builtins?|keywords?/$_be&$_f/g" && return

    local arg="${1:?Subject required. Usage: 'describe --help'}"
    __describe_entrypoint "$@" | less --quit-if-one-screen -+c  # clear-screen
}
function __mafn {  # @TODO
    #if command -v maf &>/dev/null ; then
    #    maf "$@"
    #el
    if [[ $# -gt 0 ]] ; then
        man "$@"
    else
        echo "$@"
        cat
    fi
}
function vp { _vp "$@" | less ; }
function _vp { [[ -n "$*" ]] && __vp "$@" || cat - | __vp ; }
function __vp { pygmentize -g -f terminal "$@" ; }
function __vpa { cat - | pygmentize -l "${1:-text}" -f terminal | less -+S ; }
function __describe_sep { printf '%40s\n' "" | tr ' ' - ; }
function __invoke_bash { bash --norc -ilc "$*" | sed --unbuffered -Ee 's/\x1b]0;\a//;' ; }
function __describe_entrypoint {
    local p
    local t='' m=''

    t=$(__invoke_bash type -t "$arg")
    if [[ $? -gt 0 ]] || [[ -z $t ]] ; then
        error "Failed to resolve type of ${arg@Q}"
        return 1
    fi
    notice "Type: $_b$t$_f"

    if [[ $t == file ]] ; then
        p=$(command -v "$arg") || { error "Failed to find path of ${arg@Q}" ; return 1 ; }
        notice "Path: $p"
        if f=$(file --dereference "$p") && head -1 <<< "$f" | grep -q text ; then
            __describe_sep
            vp <"$p" 2>/dev/null
        else
            notice "No source is available as executable is binary"
            if m=$(man --where "$arg" 2>/dev/null) ; then
                verbose "Man page: $m"
                __describe_sep
                __mafn "$arg"
            else
                notice "No man page found for ${arg@Q}"
                __describe_sep
                echo "${f/$p: /}"
            fi
        fi
    elif [[ $t == function ]] ; then
        __describe_sep
        __invoke_bash command -V "$arg" | sed 1d | __vpa shell
    elif [[ $t == alias ]] ; then
        __describe_sep
        __invoke_bash command -v "$arg" | __vpa shell
    elif [[ $t == builtin ]] || [[ $t == keyword ]] ; then
        __describe_sep
        help "$arg" | ES7S_MAF_FORMAT=help __mafn
    else
        warn "Unknown response from type: $t"
        return 1
    fi
    #echo
}

#set -x
set -o pipefail
describe "$@"
