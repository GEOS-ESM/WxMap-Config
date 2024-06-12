#!/bin/sh

FILE=https://www.spc.noaa.gov/climo/reports/%y%m%d_rpts_filtered_torn.csv

idate=20240501
while [ $idate -le 20240531 ]; do

  file=`timetag $idate 0 $FILE`
  echo $file
  wget $file

  idate=`timetag $idate 0 %Y%m%d%+d01`

done

exit 0
