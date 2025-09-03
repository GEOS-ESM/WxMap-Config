#!/bin/sh

i=1
while [ $i -le 25 ]; do

  member=`expr $i + 1000 | cut -c2-4`
  echo $member
  mkdir -p members/$member
  make_member_html.sh t2m_anom $member > members/$member/index.html

  i=`expr $i + 1`

done

exit 0
