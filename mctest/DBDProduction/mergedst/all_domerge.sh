#!/bin/bash

prodid=$1 
trgdir=$2
if [ "x${prodid}" == "x" -o "x${trgdir}" == "x" ] ; then 
  echo "[Function] Do all merge dst process."
  echo "[Usage]" 
  echo "do_allmerge.sh [prodid] [tdir]"
  echo "  [tdir] = 000, 001, 002, ..."
  exit
fi

get_dstlist.sh ${prodid}

echo "get_dstlist completed.  Will download all DSTs"

grep "/${trgdir}/" dst${prodid}.list > dst${prodid}-${trgdir}.list

(
mkdir ${trgdir}
cd ${trgdir}
dl_dsts.sh ../dst${prodid}-${trgdir}.list
)

echo "Download DSTs completed."

mkmerge.sh ${trgdir}

echo "Merge file job was created."
echo "do . bsub.sh to submit job."


