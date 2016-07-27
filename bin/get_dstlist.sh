#!/bin/bash

prodid=$1

if [ "x$prodid" == "x" ] ; then 
  echo "Function: Get LFN list of given prodID"
  echo "Usage:"
  echo "get_dstlist.sh [prodid]" 
  exit
fi

dirac-dms-find-lfns Path=/ilc/prod/ilc/mc-dbd/ild/dst/500-TDR_ws/ "ProdID=${prodid}" | tee dst${prodid}.list
sed -i -e "/^{/d" dst${prodid}.list

