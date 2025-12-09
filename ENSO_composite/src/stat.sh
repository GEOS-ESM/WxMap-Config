#!/bin/sh

if [ $# -ne 1 ]; then
  echo "Usage: $0 [field]" 2>&1
  exit 1
fi

field=$1

imonth=1
idate=19791201
while [ $idate -le 19811201 ]; do

  IMONTH=`expr $imonth + 1000 | cut -c2-4`
  echo $IMONTH $idate

  wxmap.py --config /discover/nobackup/jardizzo/software/GEOS-ESM/WxMap-Config/ENSO_composite --stream M2NEUT --time_dt $idate --oname stats/'$field.$region.stat' --field $field

  idate=`timetag $idate 0 %Y%m%d%+m01`
  imonth=`expr $imonth + 1`

done

exit 0
