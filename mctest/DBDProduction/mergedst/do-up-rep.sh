#!/bin/bash

DESTSE="KEK-SRM"
REPSE="DESY-SRM"

do_up_rep()
{
  prodid=$1
  destdir=$2
  subdir=$3
  echo "Uploading dst-merged of prod=$prodid to $destdir"
  ( 
    cd $prodid
    for d in merge-${subdir}-* ; do 
      (
        cd $d 
        pwd
        infile=`/bin/ls r*.slcio`
        dirac-dms-add-file ${destdir}/${infile} ${infile} ${DESTSE}
        dirac-dms-replicate-lfn ${destdir}/${infile} ${REPSE}
      )
    done
  )
}


ddir=/ilc/prod/ilc/mc-dbd/ild/dst-merged/500-TDR_ws/4f_singleZee_leptonic/ILD_o1_v05/v01-16-p05_500

date

subdir=001
# do_up_rep 6839 ${ddir}
for pr in 6838 6839 6840 6841 ; do
  do_up_rep ${pr} ${ddir} ${subdir}
done

date
echo "All completed."

