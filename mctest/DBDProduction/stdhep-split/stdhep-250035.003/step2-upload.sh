#!/bin/bash 
cat stdhep.list | xargs -P 15 -I{} dirac-dms-add-file /ilc/prod/ilc/mc-dbd.generated/500-TDR_ws/4f/temp004/{} {} PNNL-SRM> upload.log 2>&1 