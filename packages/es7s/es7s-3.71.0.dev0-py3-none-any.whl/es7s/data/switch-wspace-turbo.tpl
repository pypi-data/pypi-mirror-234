#!/bin/bash
#################################/\\ ,#####,######'###### *'; ###,##################|||||||####
#  STATIC ACCELERATOR TEMPLATE  |>@}}>>>>>>>>>>>>>>>>>>>>>>>>>>>!>>>>>>>>>>>.  #####|||| ||####
####==@@=========================\// repeats logic of `exec switch-wspace`, |\  ####|||||||####
######|| but for hardcoded configuraion instead of a general case (so it is ||\   ##|+|||||####
#######\\     consistent only if config values didn't change; when they do, ||/   ##||||||^####
#######//  `exec switch-wspace -S` should be invoked to rewrite the script. |/  ####||| |||####
######//___-------+---------------------------------------------------------'  #####|||||||####
##__SUBSTITUTES___|################################################################/////-/#####
##- filter_name --|###############################################################/// ///#####
#-- filter_regex -|##############################################################///////#####
#-- selector_name |#############################################################/// ///####
#-- wmctrl_path  -|############################################################/+/// /###
#-----------------'########################################
#######################################

switch-wspace.main() {
    local active_idx=$(( "$(%(wmctrl_path)s -d | grep -Ee '^[0-9]+\s*\*' --only-matching | cut -d' ' -f1)" ))
    echo "Active idx: $active_idx" >&2
    local first_select=
    local select=

    for allowed_idx in $(%(wmctrl_path)s -d | grep -Ee '^[0-9]+\s*\-' --only-matching | cut -d' ' -f1 | sed -Ee "$(switch-wspace.allowed-by-filter)") ; do
        echo "Allowed: $allowed_idx" >&2
        [[ -z "$first_select" ]] && first_select=$allowed_idx
        select="$(switch-wspace.select "$allowed_idx" "$active_idx" "$select")"
    done
    [[ -z "$select" ]] && [[ -n "$first_select" ]] && select=$first_select
    [[ -z "$select" ]] && [[ -z "$first_select" ]] && echo "No suitable targets" && exit 0
    %(wmctrl_path)s -s$select
}

switch-wspace.allowed-by-filter() {
    switch-wspace.filter-%(filter_name)s "$@"
}
switch-wspace.filter-off() {
    echo ""
}
switch-wspace.filter-blacklist() {
    echo "/%(filter_regex)s/d"
    # "1", "1|2|3", "^$"
}
switch-wspace.filter-whitelist() {
    echo "/%(filter_regex)s/!d"
    # "1", "1|2|3", "^$"
}

switch-wspace.select() {
    switch-wspace.selector_%(selector_name)s "$@"
}
switch-wspace.selector_first() {
    local allowed_idx="$1" active_idx="$2" select="$3"
    [[ -z "$select" ]] && echo $allowed_idx
}
switch-wspace.selector_cycle() {
    local allowed_idx="$1" active_idx="$2" select="$3"
    [[ -z "$select" ]] && [[ $allowed_idx -gt $active_idx ]] && echo $allowed_idx
}


switch-wspace.main "$@"
