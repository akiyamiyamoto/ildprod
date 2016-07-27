#!/bin/bash

logfilename=`pwd`/logfilename.list

cat <<EOF > ${logfilename}
sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250033.P4f_sze_l.eL.pL_sim_6834-000.tar.gz
sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250033.P4f_sze_l.eL.pL_sim_6834-000.tar.gz
rv01-16-p05_500.sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250033.P4f_sze_l.eL.pL_rec_6838-000.tar.gz
rv01-16-p05_500.sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250033.P4f_sze_l.eL.pL_rec_6838-001.tar.gz
sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250034.P4f_sze_l.eL.pR_sim_6835-000.tar.gz
sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250034.P4f_sze_l.eL.pR_sim_6835-001.tar.gz
rv01-16-p05_500.sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250034.P4f_sze_l.eL.pR_rec_6839-000.tar.gz
rv01-16-p05_500.sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250034.P4f_sze_l.eL.pR_rec_6839-001.tar.gz
sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250035.P4f_sze_l.eR.pR_sim_6836-000.tar.gz
sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250035.P4f_sze_l.eR.pR_sim_6836-001.tar.gz
rv01-16-p05_500.sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250035.P4f_sze_l.eR.pR_rec_6840-000.tar.gz
rv01-16-p05_500.sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250035.P4f_sze_l.eR.pR_rec_6840-001.tar.gz
sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250036.P4f_sze_l.eR.pL_sim_6837-000.tar.gz
sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250036.P4f_sze_l.eR.pL_sim_6837-001.tar.gz
rv01-16-p05_500.sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250036.P4f_sze_l.eR.pL_rec_6841-000.tar.gz
rv01-16-p05_500.sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I250036.P4f_sze_l.eR.pL_rec_6841-001.tar.gz
EOF



for pr in 6839 6840 6841 ; do 
  ( 
    cd prod${pr}
    for subd in 000 001 ; do
      fn=`grep ${pr}-${subd} ${logfilename} | sed -e "s/.tar.gz//g" `
      mv -v log-${subd} ${fn}
      tar zcf ${fn}.tar.gz ${fn}
    done
   )

done
