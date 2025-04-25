#!/bin/sh

STREAMS="GEOSFP GenCast Pangu Aifs Prithvi"

OPTIONS1="--lights_off --no_logo --no_title --tight --geometry 800x600"
OPTIONS2="--lights_off --plot_only --geometry 800x600"

for stream in $STREAMS; do

  wxmap.py --config /gpfsm/dnb34/jardizzo/software/GEOS-ESM/WxMap-Config/ML_Forecast --stream $stream --fcst_dt 20241231 --time_dt 20250101 --end_dt 20250105 --t_deltat 24  --field slp --region nam --oname 'images/$stream.$field.%%Y%%m%%d_%%Hz.%Y%m%d%H.$tau.png' $OPTIONS2

done

exit 0
