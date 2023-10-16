#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------

USAGE=$(cat <<-EOL
	Parse RSS from specified sourceforge URL and download all files found.

	Usage:
	    $(basename "$0") https://sourceforge.net/projects/gimp-tools/rss?path=/
	EOL
)

[[ $# -lt 1 ]] || [[ $* =~ (--)?help ]] && { echo "$USAGE" ; exit ; }

curl "${1:?"URL to RSS feed required.$USAGE"}" |
    sed -nEe 's:<link>(.+)/download</link>:\1:g;T;p' |
    xargs -t -n1 wget

# curl "<URL>" | grep "<link>.*</link>" | sed 's|<link>||;s|</link>||' | while read url; do url=`echo $url | sed 's|/download$||'`; wget $url ; done
# https://stackoverflow.com/questions/39668291
