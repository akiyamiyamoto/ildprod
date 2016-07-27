#!/bin/bash 
# Create a script to set meta data.
nseq_to=`grep -a "  File number of the last file :" hepsplit-250035.003.log | cut -d":" -f2 `
last_fileseq=${nseq_to}
last_file_nevents=`grep -a " Record written = " hepsplit-250035.003.log | tail -1 | cut -d"=" -f2 `
echo "Last file number is ${last_fileseq}" 
echo "Event number of last file is ${last_file_nevents}" 
cat /home/ilc/miyamoto/DiracProd/config/setMetaData.py.in | sed \
 -e "s|%%GRID_PATH%%|/ilc/prod/ilc/mc-dbd.generated/500-TDR_ws/4f/temp004/|g" \
 -e "s|%%FILE_PREFIX%%|E500-TDR_ws.P4f_sze_l.Gwhizard-1_95.eR.pR.I250035.003|g" \
 -e "s|%%SRC_PATH%%|/ilc/prod/ilc/mc-dbd/generated/500-TDR_ws/4f/E500-TDR_ws.P4f_sze_l.Gwhizard-1_95.eR.pR.I250035.003.stdhep|g" \
 -e "s|%%NSEQ_FROM%%|0|g" \
 -e "s|%%NSEQ_TO%%|${nseq_to}|g" \
 -e "s|%%NEVENTS%%|1000|g" \
 -e "s|%%LAST_FILENO%%|${last_fileseq}|g" \
 -e "s|%%SERIAL_NUMBER%%|3|g" \
 -e "s|%%LAST_FILE_NEVENTS%%|${last_file_nevents}|g" \
 > setMetaData.py 
echo " a script to write Metadata, setMetaData.py was created."
