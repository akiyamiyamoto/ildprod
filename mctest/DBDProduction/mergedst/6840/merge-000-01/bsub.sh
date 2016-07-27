#!/bin/bash 
export MCPROD_TOP=/home/ilc/miyamoto/DiracProd
bsub -o merge-01.log -J merge6840  -q s "( /home/ilc/miyamoto/DiracProd/bin/lcio_merge.sh xaaa rv01-16-p05_500.sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250035.P4f_sze_l.eR.pR_dst_6840_01-DST.slcio > merge-01.log 2>&1 )" 
