#!/bin/sh

if [ $# -ne 2 ]; then
  echo "Usage: $0 [stream] [application]" 2>&1
  exit 1
fi

stream=$1
app=$2

while read line; do

  var=`echo $line | cut -d',' -f1`
  title=`echo $line | cut -d',' -f2`
  units=`echo $line | cut -d',' -f3`

  $app $stream $var "$title" "$units"

done

exit 0
