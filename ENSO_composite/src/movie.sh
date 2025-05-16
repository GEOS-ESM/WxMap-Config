#!/bin/sh

tmpdir=$TMPDIR/`basename $0`.$$
mkdir -p $tmpdir

TYPES=`find 0* -name "*.png" -exec basename {} \; | cut -d'.' -f1-2 | sort -u`

for type in $TYPES; do
  find 0* -name "$type.*.png" -exec cp -p {} $tmpdir \;
  mp4_encode -o $type.mp4 $tmpdir/$type'.*.png'
  /bin/rm $tmpdir/*.png
done

rmdir $tmpdir

exit 0
