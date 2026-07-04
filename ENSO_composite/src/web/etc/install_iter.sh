#!/bin/sh

stream=$1
stat=$2

while read var; do

    echo ${var}_$stat
    install_var.sh $stream ${var}_$stat

done

exit 0
