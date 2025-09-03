#!/bin/sh

cat regions.txt | while read line; do

  region=`echo $line | cut -d':' -f1`
  echo $region
  mkdir -p regions/$region
  make_region_html.sh t2m_anom $region > regions/$region/index.html

done

exit 0
