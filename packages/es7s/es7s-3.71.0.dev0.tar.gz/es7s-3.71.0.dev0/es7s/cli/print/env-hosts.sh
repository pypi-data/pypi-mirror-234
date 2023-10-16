#!/bin/bash
# -----------------------------------------------------------------------------
# es7s/core (G2/legacy)
# (C) 2022 A. Shavykin <0.delameter@gmail.com>
# -----------------------------------------------------------------------------

declare SELF=$(basename "${0}")
declare MAX_ENV_NAME_LEN=20
declare MAX_ENV_VALUE_LEN=30
declare MAX_COMMENT_LEN=10
declare _FLOCK_PIPE=/tmp/leo-peh

function _print_help {
    echo "USAGE"
    echo "    $SELF [--remote|--all] [--debug] [--no-trunc] [PATH]"
    echo
    echo "Find all dotenv (\".env\") files in specified PATH (recursively) and search the contents for "
    echo "variables with URLs as values. Be default local host names are filtered out."
    echo
    echo "OPTIONS"
    echo "  -r|-remote   Display only vars that are considered to be a remote host name [this is a default]"
    echo "  -a|-all      Display all variables that look like a hostname"
    echo "  -c|--count   Print amount of matches instead of matches themselves"
    echo "  -d|-debug    Print additional information from different stages of the internal process"
    echo "  --no-trunc   Do not truncate the output"
    echo
    echo "By default environment var name+value is $((MAX_ENV_NAME_LEN + 1 + MAX_ENV_VALUE_LEN)) charcters max, and comment is limited by $MAX_COMMENT_LEN chars."
    echo
}

declare ccs1=$'\x1d' # temp separator for formatting
declare ccs2=$'\x1e' # temp separator for formatting
declare ccs3=$'\x1f' # temp separator for column swapping
declare sgr=$'\e\['
declare esc=$'\e'
declare c_reset="${sgr}m"

declare app_user_repos_path=
declare app_remote_only=true
declare app_debug=
declare app_truncate_output=true
declare app_count=

function _main {
    _arg_parse "$@"
    pushd "$app_user_repos_path" &>/dev/null || {
        echo "Failed to access ${app_user_repos_path@Q} (code $?)"
        exit 127
    }

    if [[ -n "$app_debug" ]]; then
        cat "$_FLOCK_PIPE" &
    fi
    [[ -z $app_count ]] && echo "Searching in ${app_user_repos_path@Q}..."
    find . -name .env -print |
        _read_files |
        _filter_vars |
        _filter_hosts |
        _find_duplicates |
        _filter_remote |
        _format |
        _truncate |
        _align |
        _debug |
        _count

    [[ -z $app_count ]] && echo
    popd &>/dev/null || exit 127
}

function _arg_parse {
    while getopts :racd-: OPT; do
        if [ "$OPT" = "-" ]; then
            OPT="${OPTARG%%=*}"
            OPTARG="${OPTARG#$OPT}"
            OPTARG="${OPTARG#=}"
        fi
        # shellcheck disable=SC2214
        case "$OPT" in
            r | remote) app_remote_only=true ;;
               a | all) app_remote_only= ;;
             c | count) app_count=true ;;
             d | debug) app_debug=true ;;
              no-trunc) app_truncate_output= ;;
                  help) _print_help && exit 0 ;;
               ??* | ?) echo "ERROR: Ilegal option -${OPTARG:-"-"$OPT}"
                        printf "\nShow usage:\n  %s --help\n\n" "$SELF"
                        exit 1
                        ;;
        esac
    done
    shift $((OPTIND - 1))

    app_user_repos_path="${1:-}"
    [[ -z $app_user_repos_path ]] && app_user_repos_path=${ES7S_USER_REPOS_PATH}
    [[ -z $app_user_repos_path ]] && {
        echo "No path specified. Set an ES7S_USER_REPOS_PATH env var or pass a" \
            "path to work with as first argument."
        exit 126
    }
}

function _peek {
    # args: [middleware_cmd [middleware_cmd_args]...]
    # clone stdin -> stdout and redirect it to stderr
    # through "middleware" proxy command
    tee 2> >(${1:-cat} "${@:2}" >&2) /dev/stderr
}

function _print_interm_result {
    local c_val="\x1b[1m"  # no fking idea why ${sgr} (\e) doesn't work here
    local c_reset="\x1b[m"
    if [[ -z $app_count ]] ; then
        printf "%12s: ${c_val}%d${c_reset}" "$1" "$(wc -l)"
        echo
    else
        cat >/dev/null
    fi
}

function _debug {
    if [[ -n "$app_debug" ]]; then
        _peek _debug_format "${FUNCNAME[1]}" "$@"
    else
        cat
    fi
}
function _debug_format {
    local c_header="${sgr}1m"
    local r_header="${sgr}22m"
    local c_msg="${sgr}36m"
    local c_control_char="${sgr}7m"
    local r_control_char="${sgr}27m"

    flock -x "$_FLOCK_PIPE" sed -E --unbuffered \
            -e "s/^.+$/  ${c_msg}&${c_reset}/" \
            -e "1s/^/${c_header}function ${1}${2:+ (${*:2})}:$r_header\n/" \
            -e '$ s/$/\n/' \
            -e "s/$ccs1|$ccs2|$ccs3/${c_control_char}&${r_control_char}/g" \
            -e "s/$ccs1/]/g" \
            -e "s/$ccs2/^/g" \
            -e "s/$ccs3/_/g" > "$_FLOCK_PIPE" &
}

function _read_files {
    _peek _print_interm_result "Files found" |
        _debug 'before' |
        fgrep -v vendor |
        _debug 'filtered' |
        xargs -L10 --no-run-if-empty grep -EHv --line-buffered \
            -e '^#' \
            -e '^$' \
            -e '^[^=]+$'
}

function _filter_vars {
    _peek _print_interm_result "Vars found" |
    grep -Ev --line-buffered -e '=\s*$' |
        _debug 'after'
}
function _filter_hosts {
    grep -E --line-buffered -e 'HOST|http' |
        _debug 'after'
}

function _find_duplicates {
    # `uniq` merges line duplicates into FIRST occurence, but dotenvs are read in a way
    # that only LAST duplicated variable is effective. That's why we reverse the lines
    # with `tac` before invoking `uniq`, and then reverse them back (also with `tac`).

    # Env var should considered a duplicate if its marked with underscore part matches
    # with another line:    ______________________________________
    # (input line format): './event-storage/.env:   MEMCACHED_HOST=127.0.0.1'

    # You cannot define a custom field separator for `uniq` (like for `sort` below),
    # neithter you can set a custom range of fileds to compare the lines on. Solution is
    # to reverse characters in lines, so input lines' format becomes:
    # (part to sort on):              ______________________________________
    # (reversed line fmt): '1.0.0.721=TSOH_DEHCACMEM   :vne./egarots-tneve/.'
    # ... and then reverse them back with `rev`.

    # We also replace '=' with spaces (so that `uniq` is able to sort lines by necessary
    # fields), but before that actual spaces are replaced with 0x1F, control character
    # that is very unlikely to encounter in a filesystem or dotenv contents.

    sort --stable -t '=' -k1,1 |
        rev |
        tac |
        sed -E --unbuffered \
            -e "s/ /${ccs3}/g" \
            -e "s/=/ =/1" |
        uniq -c -f1 |
        sed -E --unbuffered \
            -e "s/^(\s*)([0-9]+)(\s+)(.+)$/\4\3\2\1/" |
        rev |
        tac |
        sed -E --unbuffered \
            -e "s/= /=/1" |
        _debug 'after'
}

function _filter_remote {
    # SHOULD run AFTER _find_duplicates!
    # or else it can miss some duplicates in --remote mode

    if [[ -z "$app_remote_only" ]]; then
        cat
    else
        grep -Ev --line-buffered \
            -e 127\.0\.0\.1 \
            -e 0\.0\.0\.0 \
            -e 192\.168\. \
            -e localhost \
            -e front-main \
            -e smtp\.gmail\.com \
            -e '=\s*\/' \
            -e '=[^.]*$' |
            _debug 'after'
    fi
}

function _format {
    local c_dir=
    local c_var="${sgr}32m"
    local c_eq="${sgr}90m"
    local c_value="${sgr}34m"
    local c_comment="${sgr}90m"
    local fmt_src="^\s+([0-9>x_]+)\s+(.+).env:\s*([^=]{,$MAX_ENV_NAME_LEN})([^=]*)=([^#]{,$MAX_ENV_VALUE_LEN})([^#]*)((#\s*.{,$MAX_COMMENT_LEN})(.*))?$"
    local fmt_dest="\t${ccs3}${c_dir}\2\t${ccs3}\1\t${ccs3}${c_var}\3${ccs1}\4${ccs2}\t${c_eq}=${c_value}\5${ccs1}\6${ccs2}\t${c_comment}\8${ccs1}\9${ccs2}"

    _peek _print_interm_result "Vars matched" |
        sed -E --unbuffered \
            -e "s/^\s(\s*)[0-9]{2,}/\1>9x/g" \
            -e "s/^\s(\s*[0-9])/\1x/g" \
            -e "s/${ccs3}/ /g" \
            -e "s|^(\s+)1x(\s+)|\1__\2|g" \
            -e "s|^(\s+[0-9>x_]+\s+)\./([^:]+)/|\1\2|g" \
            -e "s|$fmt_src|$fmt_dest|" \
            -e "2s///" |
        _debug 'after'
}

function _truncate {
    if [[ -n "$app_truncate_output" ]]; then
        sed -E --unbuffered \
            -e "s/${ccs1}[^$ccs2]+${ccs2}/‥/g" \
            -e "s/${ccs1}|${ccs2}//g"
    else
        sed -E --unbuffered \
            -e "s/${ccs1}|${ccs2}//g"
    fi
}

function _align {
    local c_dupl="${sgr}97;41;1m"

    column -s$'\t' -t |
        _debug 'after columns' |
        sed -E --unbuffered \
            -e "s|^${ccs3}(\S+)\s(\s+)${ccs3}_{2}(\s)\s(\s*)${ccs3}|\1\2  \3\4|" \
            -e "s|^${ccs3}(\S+)\s(\s+)${ccs3}(\S+)(\s)\s(\s*)${ccs3}|\1\2${c_dupl}\3${c_reset}\4\5|" \
            -e '1s/^/\n/' \
            -e "s/$/$c_reset/"
}

function _count {
    if [[ -n "$app_count" ]]; then
        sed '/^$/d' | wc -l
    else
       cat
    fi
}

_main "$@"
