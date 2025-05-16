#!/bin/sh

imonth=1
lmonth=-12
idate=19791201
while [ $idate -le 19811201 ]; do

  IMONTH=`expr $imonth + 1000 | cut -c2-4`

  wxmap.py --config /discover/nobackup/jardizzo/software/GEOS-ESM/WxMap-Config/ENSO_composite --stream M2NINO --time_dt $idate --region greenland --oname $IMONTH/'$field.$stream.'$IMONTH'.png' --lights_off --no_logo --field t2m_anom

  LMONTH=$lmonth
  if [ $LMONTH -ge 0 ]; then LMONTH='+'$LMONTH; fi
  cat index.template | sed s/LMONTH/$LMONTH/ | sed s/IMONTH/$IMONTH/ > $IMONTH/index.html

  idate=`timetag $idate 0 %Y%m%d%+m01`
  imonth=`expr $imonth + 1`
  lmonth=`expr $lmonth + 1`

done

exit 0
