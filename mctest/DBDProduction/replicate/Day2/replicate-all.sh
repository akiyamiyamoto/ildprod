#!/bin/bash

NPROC=5

do_replicate()
{
  prodid=$1
  dtype=$2
  destse=$3
  date
  echo "Replicate ${dtype} ProdID=${prodid} to ${destse}" 
  dirac-dms-find-lfns Path=/ilc/prod/ilc/mc-dbd/ild/${dtype}/ "ProdID=${prodid}" | grep -v ProdID > ${dtype}-${prodid}.list 

#  ffile=`head -1 ${dtype}-${prodid}.list`
#  hdir=`dirname ${ffile}`
#  fn=`basename ${ffile}`
#  echo $hdir
#  echo $fn  
  echo "none" > last_hdir.txt
  rm -f ${dtype}-${prodid}-fn.list

  cat ${dtype}-${prodid}.list | while read f  ; do 
    adir=`dirname ${f}`
    afn=`basename ${f}`
    hdir=`cat last_hdir.txt`
    if [ "x${adir}" != "x${hdir}" ] ; then 
      if [ -e ${dtype}-${prodid}-fn.list ] ; then 
        cat ${dtype}-${prodid}-fn.list | xargs -P ${NPROC} -I{} dirac-dms-replicate-lfn ${hdir}/{} ${destse} >> ${dtype}-${prodid}-rep.log 2>&1 
        rm -f ${dtype}-${prodid}-fn.list
      fi
      dirac-dms-replicate-lfn ${adir}/${afn} ${destse} >> ${dtype}-${prodid}-rep.log 2>&1
      hdir=${adir}
      echo ${adir} > last_hdir.txt
    else 
      echo `basename ${f}` >> ${dtype}-${prodid}-fn.list
      echo ${adir} > last_hdir.txt
    fi  
  done

  if [ -e ${dtype}-${prodid}-fn.list ] ; then 
    hdir=`cat last_hdit.txt`
    echo "last hdir is $hdir"
    cat ${dtype}-${prodid}-fn.list | xargs -P ${NPROC} -I{} dirac-dms-replicate-lfn ${hdir}/{} ${destse} >> ${dtype}-${prodid}-rep.log 2>&1 
    rm -f ${dtype}-${prodid}-fn.list
  fi

}


# for id in 6837 ; do 
#   do_replicate ${id} sim KEK-SRM
# done

for id in `seq 6838 6841` ; do
  do_replicate ${id} rec KEK-SRM
done

