#!/bin/sh

if [ $# -ne 1 ]; then
  echo "Usage: $0 [release month as ccyymm]" 2>&1
  exit 1
fi

DATAPATH=$NOBACKUP/FLUID/S2S/%Y%m
OPATH=$NOBACKUP/FLUID/S2S/latest

idate=${1}01
datapath=`timetag $idate 0 $DATAPATH`
opath=`timetag $idate 0 $OPATH`
mkdir -p $opath

for field in t2m_anom Precip_anom SSS_anom SST_anom; do

  for region in glb eqpac NA SA AUS SEASIA EUR; do

    files=$datapath/*.$field.$region.*
    pathname=`/bin/ls $datapath/*.$field.$region.* | tail -1`

    field=`echo $pathname | cut -d'.' -f2`
    var=`echo $field | cut -d'_' -f1`
    region=`echo $pathname | cut -d'.' -f3`
    release_date=`echo $pathname | cut -d'.' -f4`
    target_date=`echo $pathname | cut -d'.' -f5`

    mmm=`timetag $release_date 0 "^%b"`

    oname=$opath/S2S_2.1_${mmm}_mean_${var}_anom_fcst_${region}.png
    echo $oname

    aggregate.py -i $files -o $oname

  done

done

exit 0
