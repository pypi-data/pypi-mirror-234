#!/usr/bin/env bash
# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
# shellcheck disable=SC2119,SC2016
# shellcheck source=../../data/es7s-shell-commons.sh
__E7SL() { local c="$(realpath "$(dirname "$(readlink -f "$0")")")" ; local l=\
"es7s-shell-commons.sh" ; local p=( "$ES7S_SHELL_COMMONS" "$HOME/.es7s/data/$l"
"$c/../$l" ); while [[ ! $(type -t __es7s_com) =~ ^fu ]];do [[ -f "${p[0]}" ]]\
&& source "${p[0]}"; p=("${p[@]:1}"); [[ "${#p[@]}" -gt 0 ]] && continue; echo\
'ERROR: es7s/commons is missing (ES7S_SHELL_COMMONS)'; exit 57; done } ; __E7SL
# ------------------------------------------------------------- loader v.3B ---
[[ $* =~ --help ]] && echo "Usage: $(basename "${0%.*}") [FILE...]" && exit 0

_main() {
  (
    set -o pipefail
    maxw=$(( $(tput cols) - 2 ))
    N=$(($(bat --list-themes|wc -l)))
    idx=1
    IFS=$'\n'
    lines=$(( ($(tput lines) - 3)/N ))
    for t in $(bat --list-themes | sort); do
      maxh=$(( $(tput lines) - lines * (idx-1) - 3 ))
      row=$(( lines * (idx-1) + 2 ))
      [[ $maxh -le 0 ]] && echo "Unable to continue, terminal height is too small" && break
      printf "\e[$row;1H\e[34;48;5;17;53m\e[2K%${maxw}s\e[55m\e8"
      printf "\e[$row;1H\e[34;7;1m %3d \e7" $idx
      printf "\e[34;2m %s  \e[m\n\e[0J"   "${t}"
      if ! bat "$1" --theme=$t  --decorations=never -r 1:$maxh --no-pager --color=always |  sed --unbuffered -zEe '$s/\n$//' ; then
        break
      fi
      read -n1 -sr
      {
        printf "\e[$row;1H\e[0K\e[m[%3d] %-20.20s \e[0K\e[m" $idx "$t"
        bat "$1" -r1:$N --no-pager --decorations=never --theme="$t" --color=always | cat |  sed -zEe "s/\n/ /g; s/\s+/ /g"
      } |  es7s e wrap -W $maxw -c | head -$lines  | sed -Ee 's/$/\x1b[m/'
      ((idx++))
    done
  )
  printf "\e[0J"
}

fidx=0
#printf "\e[?1049h"
hide-user-input
[[ $# -eq 0 ]] && set - $0
for file in "$@" ; do
  ((fidx++))
  [[ fidx -gt 1 ]] && read -n1 -srp "(NEXT?)"
  printf "\e[2J\e[H\e[48;5;12;38;5;16;1m\e[0K $(printf %3d $fidx)/$# \e[48;5;24;97m $file \e[K"
  [[ -r "$file" ]] || { echo "File not found or not readable" && continue ; }
  [[ -s "$file" ]] || { echo "File is empty" && continue ; }
  grep -Iq . "$file" || { echo "File is binary" && continue ; }
  _main "$file"
done
#printf "\e[?1049l"
