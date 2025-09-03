#!/bin/sh

imonth=1
lmonth=-12
idate=19791201
while [ $idate -le 19811201 ]; do

  IMONTH=`expr $imonth + 1000 | cut -c2-4`
  echo $IMONTH $idate

  wxmap.py --config /discover/nobackup/jardizzo/software/GEOS-ESM/WxMap-Config/ENSO_composite --stream $1 --time_dt $idate --oname $IMONTH/'$stream.$field.$region.'$IMONTH'.image.png' --field $2 --lights_off
  wxmap.py --config /discover/nobackup/jardizzo/software/GEOS-ESM/WxMap-Config/ENSO_composite --stream $1 --time_dt $idate --oname $IMONTH/'$stream.$field.$region.'$IMONTH'.icon.png' --field $2 --geometry 200x150 --fullframe --lights_off --plot_only

  LMONTH=$lmonth
  if [ $LMONTH -ge 0 ]; then LMONTH='+'$LMONTH; fi
  cat index.template | sed s/LMONTH/$LMONTH/ | sed s/IMONTH/$IMONTH/ > $IMONTH/index.html

  idate=`timetag $idate 0 %Y%m%d%+m01`
  imonth=`expr $imonth + 1`
  lmonth=`expr $lmonth + 1`

done

exit 0
