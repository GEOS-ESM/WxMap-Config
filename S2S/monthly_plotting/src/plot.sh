#!/bin/sh

if [ $# -ne 1 ]; then
  echo "Usage: $0 [release date as ccyymm]" 2>&1
  exit 1
fi

release_date=${1}01
year=`echo $release_date | cut -c1-4`
month=`echo $release_date | cut -c5-6`
DATE=${year}-${month}-01
ONAME=$NOBACKUP'/FLUID/S2S/%%Y%%m/s2s.$field.$region.%%Y%%m%%d.%Y%m%d.png'

app=`realpath $0`
app_path=`dirname $app`
config_path=`dirname $app_path`

export PATH=${PATH}:$app_path

for lead in 1 2 3 4 5 6 7 8 9; do

  incmon=`expr $lead - 1`
  target_date=$(date +%Y%m%d -d "$DATE + $incmon month")

  echo $release_date $target_date

  for field in SST_anom SSS_anom t2m_anom Precip_anom; do

    wxmap.py --config $config_path --stream S2SENS --fcst_dt $release_date --time_dt $target_date --field $field --no_title --tight --no_logo --oname $ONAME

  done

done

# Aggregate the plots onto a single canvas.

aggregate.sh $1
aggregate_vertical.sh $1

exit 0
