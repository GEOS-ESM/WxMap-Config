#!/bin/sh

field=$1
member=$2

time_label=`grep "^$member:" times.txt | cut -d':' -f2`

URL="MERRA-2/ENSO_Composite/M2NINO/$field"

REGIONS="enso ensoext nam usa midatl conus npac nepacific nps sps australia sevseas natl sam carib camer africa europe eastasia india mideast indonesia global pacific atlantic indian ortho greenland nasia brazil siberia alaska hawaii"
TITLES="ENSO,ENSO Extended,North America,United States,Mid Atlantic,CONUS,North Pacific,Northeast Pacific,N Polar,S Polar,Australia,Seven Seas,North Atlantic,South America,Caribbean,Central America,Africa,Europe,East Asia,India,Middle East,Indonesia,Global,Pacific Ocean,Atlantic Ocean,Indian Ocean,Orthographic East,Greenland,North Asia,Brazil,Siberia,Alaska,Hawaii"

echo '<html>'
echo '<body bgcolor="#000000" text="white">'
echo '<table>'
echo '<tr>'
echo '<th colspan="7" align="center" valign="center">'
echo '<font size="+4">MERRA-2 ENSO Composite for El Nino</font>'
echo '</th>'
echo '</tr>'
echo '<tr>'
echo '<th colspan="7" align="center" valign="center">'
echo '<font size="+4">'$time_label'</font>'
echo '</th>'
echo '</tr>'
echo '<tr> <td> <br> </td> </tr>'

i=0
for region in $REGIONS; do

  url="$URL/regions/$region/index.html"

  n=`expr $i % 7`

  if [ $n -eq 0 ]; then

    echo '<tr>'
    for j in 1 2 3 4 5 6 7; do
      k=`expr $i + $j`
      title=`echo $TITLES | cut -d',' -f$k`
      echo '<th>'$title'</th>'
    done
    echo '</tr><tr>'

  fi

  echo '<td align="center" valign="center">'
# echo '<a href="https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/.internal/'$URL'/M2NINO.'$field'.'$region'.'$member'.image.png"> <img src="M2NINO.'$field'.'$region'.'$member'.icon.png" /> </a>'
  echo '<a href="https://portal.nccs.nasa.gov/datashare/gmao/geos-fp/.internal/'$url'#'$member'"> <img src="../../.thumbnails/M2NINO.'$field'.'$region'.'$member'.icon.png" /> </a>'
  echo '</td>'

  i=`expr $i + 1`
  n=`expr $i % 7`

  if [ $n -eq 0 ]; then
    echo '</tr>'
  fi

done

echo '</tr>'
echo '</body>'
echo '</html>'

exit 0
