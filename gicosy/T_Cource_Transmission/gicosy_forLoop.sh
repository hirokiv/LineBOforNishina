#!/bin/sh
ln -sf $1 GICOSYIN.DAT
/usr/local/phys/bin/gicosy.x
/usr/local/phys/bin/meta2ps META.DAT
#file=$1
#cp -f GICOSYOUT.DAT ${file%.dat}_out.dat
#mv -f gicoplot.ps gicosyplot.ps
#cp -f gicosyplot.ps ${file%.dat}_tmp.ps
#sed -e 's/%%BoundingBox::/%%BoundingBox:/g'  ${file%.dat}_tmp.ps > ${file%.dat}.ps
#ps2pdf ${file%.dat}.ps

mv *.MAT matrix/
#ps2pdf gicosyplot.ps
#

