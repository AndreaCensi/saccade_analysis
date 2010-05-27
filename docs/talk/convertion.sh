#!/bin/bash
set -e
b=`dirname $1`/`basename $1 .eps`
pstopnm --stdout $b.eps  > $b.pnm
convert $b.pnm -rotate 90 $b.png
echo "Written $b.png "
# rr-fedora