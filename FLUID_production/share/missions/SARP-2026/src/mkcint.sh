#!/bin/sh

fname=$1

id=`head -1 $fname`
cat $fname | cut -d',' -f1 | cut -d':' -f2 > tt1
cat $fname | cut -d',' -f4 | cut -d':' -f2 | cut -d'}' -f1 > tt2

paste -d' ' tt1 tt2 > tt3

echo "$id" | sed -n s/cdict/cint/p
cat tt3 | while read line; do
  level=`echo $line | cut -d' ' -f1`
  cint=`echo $line | cut -d' ' -f2`
  echo "      $level: $cint"
done

exit 0
