#!/bin/sh

if [ $# -ne 1 ]; then
  echo "Usage: $0 [release month as ccyymm]" 2>&1
  exit 1
fi

DATAPATH=$NOBACKUP/FLUID/S2S/%Y%m
OPATH=$NOBACKUP/FLUID/S2S/latest/vertical

release_date=${1}01
year=`echo $release_date | cut -c1-4`
month=`echo $release_date | cut -c5-6`
DATE=${year}-${month}-01

datapath=$(date +"$DATAPATH" -d "$DATE")
opath=$(date +"$OPATH" -d "$DATE")

mkdir -p $opath

for field in SST_anom SSS_anom; do

  for region in glb eqpac; do

    files=$datapath/*.$field.$region.*
    pathname=`/bin/ls $datapath/*.$field.$region.* | tail -1`

    field=`echo $pathname | cut -d'.' -f2`
    var=`echo $field | cut -d'_' -f1`
    region=`echo $pathname | cut -d'.' -f3`
    release_date=`echo $pathname | cut -d'.' -f4`
    target_date=`echo $pathname | cut -d'.' -f5`

    year=`echo $release_date | cut -c1-4`
    month=`echo $release_date | cut -c5-6`
    DATE=${year}-${month}-01
    mmm=`echo $(date +"%b" -d "$DATE") | tr '[A-Z]' '[a-z]'`

    oname=$opath/S2S_2.1_${mmm}_mean_${var}_anom_fcst_${region}.png
    echo $oname

    aggregate_vertical.py -i $files -o $oname

  done

done

exit 0
