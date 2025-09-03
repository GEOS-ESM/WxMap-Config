#!/bin/sh

field=$1
region=$2
region_title=`grep "^$region:" regions.txt | cut -d':' -f2`

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
echo '<font size="+4">'$region_title'</font>'
echo '</th>'
echo '</tr>'

i=1
while [ $i -le 25 ]; do

  member=`expr $i + 1000 | cut -c2-4`
  time_label=`grep "^$member:" times.txt | cut -d':' -f2`

  echo '<tr> <td> <br> </td> </tr>'
  echo '<tr id="'$member'">'
  echo '<td align="center" valign="center">'
  echo '<img src="../../.images/M2NINO.'$field'.'$region'.'$member'.image.png" />'
  echo '</td>'
  echo '<td align="center" valign="center">'
  echo '<font size="+2">'$time_label'</font>'
  echo '</td>'
  echo '</tr>'

  i=`expr $i + 1`

done

echo '</body>'
echo '</html>'

exit 0
