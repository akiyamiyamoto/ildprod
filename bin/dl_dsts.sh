#!/bin/bash

dstlist=$1

if [ "x$dstlist" == "x" ] ; then 
  echo "Function: Download dsts to the current directory"
  echo "Usage:"
  echo "dl_dsts.sh [dst_lfn_list]" 
  exit
fi

cat ${dstlist} | xargs -P 16 -I{} dirac-dms-get-file {} > dst_download.log

