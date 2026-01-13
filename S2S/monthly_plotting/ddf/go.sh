#!/bin/sh

COLLECTIONS="ocn_tavg_1mo_glo_L720x361_z50 sfc_tavg_3hr_glo_L720x361_sfc"

for collection in $COLLECTIONS; do

  ONAME=%Y/^%b/^%b.$collection.monthly.%%Y%%m.ddf

  idate=20250901
  while [ $idate -le 20261201 ]; do

    tdate=$idate
    edate=`timetag $idate 0 %Y%m%d%+m08`

    while [ $tdate -le $edate ]; do

      oname=`timetag $idate 0 $ONAME`
      oname=`timetag $tdate 0 $oname`

      echo $oname
      mkdir -p `dirname $oname`

      cat template.fcst | timetag $idate 0 | timetag $tdate 0 | \
          sed s/COLLECTION/$collection/ > $oname

      tdate=`timetag $tdate 0 %Y%m%d%+m01`

    done

  idate=`timetag $idate 0 %Y%m%d%+m01`

  done

done

exit 0

  
