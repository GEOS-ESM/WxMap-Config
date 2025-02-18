#!/bin/sh

if [ $# -ne 1 ]; then
  echo "Usage: $0 [release month as ccyymm]" 2>&1
  exit 1
fi

DATAPATH=$NOBACKUP/FLUID/S2S/%Y%m
OPATH=$NOBACKUP/FLUID/S2S/latest

release_date=${1}01
year=`echo $release_date | cut -c1-4`
month=`echo $release_date | cut -c5-6`
DATE=${year}-${month}-01
datapath=$(date +"$DATAPATH" -d "$DATE")
opath=$(date +"$OPATH" -d "$DATE")
mmm=`echo $(date +"%b" -d "$DATE") | tr '[A-Z]' '[a-z]'`

echo $datapath
echo $opath
echo $mmm
