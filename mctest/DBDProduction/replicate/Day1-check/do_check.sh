#!/bin/bash

NPROC=5

prepare_check()
{
  prodid=$1
  dtype=$2
  seq_from=$3
  seq_to=$4
  basedir="/ilc/prod/ilc/mc-dbd/ild/"
  echo "Making lfnlist file for dtype=${dtype} prodid=${prodid}" 
  dirac-dms-find-lfns Path=${basedir}${dtype}/ "ProdID=${prodid}" | grep -v "ProdID" > ${dtype}-${prodid}.list
  for subdir in `seq ${seq_from} ${seq_to}` ; do 
    subdirstr=`printf "%3.3d" ${subdir}`
    grep "/${subdirstr}/" ${dtype}-${prodid}.list > ${dtype}-${prodid}-${subdirstr}.lfnlist
  done
}

do_listrep()
{
  lfnlist=$1
#  destse=$2
  dtype=`echo $lfnlist | cut -d"-" -f1`
  prodid=`echo $lfnlist | cut -d"-" -f2`
  subdir=`echo $lfnlist | cut -d"-" -f3 | cut -d"." -f1`
  date 
  echo "### Listing replicate ${dtype} ProdID=${prodid}"
#  ffile=`head -1 ${lfnlist}`
#  adir=`dirname ${ffile}`
#  afn=`basename ${ffile}`
#  dirac-dms-replicate-lfn ${ffile} ${destse}

  cat ${lfnlist} | while read f ; do \
   ( dirac-dms-lfn-replicas ${f} ) ; done 


  date
  echo "### Listing replica of ${lfnlist} completed."

}

# Step1
# for id in `seq 6834 6837` ; do 
#   prepare_check ${id} sim 0 1
# done

# Step2
lfnlist=$1
if [ "x${lfnlist}" == "x" ] ; then 
   echo "lfnlist is not given."
   exit
fi
do_listrep ${lfnlist} 

