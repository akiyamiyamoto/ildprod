#!/bin/bash
( export LC_ALL=C && date )
hostname 
./step1-splitcmd.sh 
echo "step1-splitcmd.sh completed." 
./step2-upload.sh
echo "upload completed."
./step3-makeSetMeta.sh
./step4-runsetMeta.sh
echo "runSetMeta completed."
( export LC_ALL=C && date )
