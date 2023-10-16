#!/bin/bash
##            es7s/core              ##
 ##      (c) 2023 A. Shavykin         ##
  ##     <0.delameter@gmail.com>       ##
   ## --------------------------------- ##
    [[ $* =~ --help ]]                   &&
     echo "Usage: $(basename "${0%.*}")"  &&
      exit                                  0
       X                                    ()
        {                          echo $PATH \
         |                           tr : '\n' \
          |                                sort \
           |                                uniq \
            | xargs -I{} -n1  find {} -maxdepth 1 \
             -type f -printf $'\t%30h\t\e[1m\t%f\e[m
             '| sed -Ee '/^\s*\/usr/s/\x1b\[/&34;/1'\
              -e '/^\s*\/home/s/\x1b\[/&33;/1'       \
               -e 's|^\s*((/[^/ \t]+){4})/\S+|\1..|1' \
                -e 's|'${HOME//\//\\\/}'|~|1'          \
                 -e 's|(\S+)|\1\/|1'                    \
                   |                         sort -k3,3  \
                    |                          tr -s ' '  \
                     |                     column -ts$'\t' \
                      | sed -Ee 's/(\x1b\[[0-9;]*m)\t/\1/1' \
                      -e 's/^\s*(\S+)(\s+)(\S+)\s+/\2\1 \3/1'|
                        cat                                  -n
                         };                                    X
