#!/bin/bash


do_download()
{
  prodid=$1
  tdir=$2
  mkdir -p ${prodid}/${tdir}
  ( 
    cd ${prodid}
    pwd
    get_dstlist.sh ${prodid}
    echo "get_dstlist ${prodid} completed."
    grep "/${tdir}/" dst${prodid}.list > dst${prodid}-${tdir}.list 
    (
      cd ${tdir}
      cat ../dst${prodid}-${tdir}.list | xargs -P 6 -I {} dirac-dms-get-file {} > ../dst_download-${prodid}-${tdir}.log 2>&1     
    )
    echo "File down load completed. for ${prodid} ${tid} "
  )
}


td="000"
for pid in 6840 6841 ; do
  do_download ${pid} ${td}
done

td="001"
for pid in 6838 6839 6840 6841 ; do
  do_download ${pid} ${td}
done
