#!/bin/bash

topdir=/hsm/ilc/grid/storm/prod/ilc/mc-dbd/ild/dst-merged
topdir=/hsm/ilc/grid/storm/prod/ilc/mc-dbd/generated
ftype=slcio
ftype=stdhep

hostname 
date

for ene in 250 350 500 ; do 
  machine="TDR_ws"
  echo "###################################################"
  echo "## `hostname` #####################################"
  echo "## `date` #########################################"
  echo "###################################################"

  find ${topdir}/${ene}-TDR_ws -name *.${ftype} -exec ./dood.sh {} \;

  echo "###################################################"
  echo "## od done ... host=`hostname` ####################"
  echo "## `date` #########################################"
  echo "###################################################"
done


