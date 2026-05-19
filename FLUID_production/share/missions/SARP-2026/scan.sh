#!/bin/sh

while read line; do

  var=`echo $line | cut -d'.' -f1`
  collection=`echo $line | cut -d'.' -f2 | cut -d'(' -f1`

  result=`getvar.sh $var cf2fc | grep $collection`

  if [ -z "$result" ]; then
    echo $var $collection
  fi

done

exit 0
  
