#!/bin/bash 
# Run hepsplit and create splitted hepstd files.
. /group/ilc/soft/gcc481/gcc481.setup
/home/ilc/miyamoto/bin/hepsplit --infile ../4f/E500-TDR_ws.P4f_sze_l.Gwhizard-1_95.eR.pR.I250035.003.stdhep \
 --outpref E500-TDR_ws.P4f_sze_l.Gwhizard-1_95.eR.pR.I250035.003 \
 --nw_per_file 1000 \
 > hepsplit-250035.003.log 2>&1 
# make a list of splitted stdhep file.
/bin/ls E500-TDR_ws.P4f_sze_l.Gwhizard-1_95.eR.pR.I250035.003*.stdhep > stdhep.list