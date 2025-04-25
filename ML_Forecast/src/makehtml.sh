#!/bin/sh

while [ $# -gt 0 ]; do

  fname=`basename $1`

  fname=`basename $fname`
  VNODE=`echo $fname | cut -d'.' -f4`
  TAU=`echo $fname | cut -d'.' -f5`

  idate=`echo $VNODE | cut -c1-8`
  itime=`echo $VNODE | cut -c9-10`
  itime=`expr $itime \* 10000`

  VSTRING=`timetag $idate $itime "%Y-%m-%d %HZ"`
  cat impact.tmpl | sed s/VNODE/"$VNODE"/ | sed s/VSTRING/"$VSTRING"/ \
                  | sed s/TAU/"$TAU"/

  shift 1

done

exit 0
