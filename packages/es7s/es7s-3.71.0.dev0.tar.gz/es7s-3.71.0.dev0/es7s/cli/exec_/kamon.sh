#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------

kamon.main() {
    kamon.reset hard
    kamon.render_status
    printf "\e[34m Queues    \e[m"
    printf "\e[1;94m%s\e[m\n" "$(sed <<< "$queues" -Ee 'y/,/ /;s/kafka://g')"

    while sleep 1.0 ; do
        kamon.reset
        kamon.render_status
        if ! docker exec -t "$cnt" sh -c '
            printf "\e[1;10H\e[34m·\n\e[2;1H\e[K" && \
            php artisan --ansi queue:monitor "'$queues'" 2>/dev/null
        ' | sed -Ee 's/\r/ /g' -e '/^\s*$/d' ; then
            _exit 1
        fi
        kamon.render_status 1

    done
}
kamon.reset() {
    printf "\e[H"
    [[ -n "$1" ]] && printf "\e[J"
    printf "\e[34m[KAMON]\e[31m"
}
kamon.render_status() {
    printf "\e[1;10H\e[K\e[32m  \e[1;34m${cnt}\e[m   "
    date $'+\e[34m%0H:%0M:\e['${1:-34}$'m%0S\e[m\e[34m / %0e %b\e[m'
}

USAGE="$(cat <<-EOL
Usage:
    $(basename "$0") CONTAINER_NAME
EOL
)"
[[ $* =~ (--)?help ]] && { echo "$USAGE" ; exit ; }

cnt="${1:?Container name required}"
shift
queues="database:,$(docker exec -t $cnt sh -c 'fgrep KAFKA_CONSUMER_QUEUES .env' | sed -Ee 's/.+=//;s/,|^/&kafka:/g')"

kamon.main "$cnt" "$queues"
