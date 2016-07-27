#!/bin/bash
# 
# Merge lcio into single files
# Usage: 
#  lcio_merge.sh list.txt out_file_name


do_merge()
{
  export MARLIN_DLL=
  . /group/ilc/soft/gcc481/gcc481.setup
  . /group/ilc/soft/ilcsoft/x86_64_gcc481/v01-16-02/init_ilcsoft.sh 
  export MARLIN_DLL=${ROOTSYS}/lib/libTreePlayer.so:${ROOTSYS}/lib/libGui.so:${ROOTSYS}/lib/libGed.so:${MARLIN_DLL}

  geardir=/group/ilc/soft/ilcsoft/x86_64_gcc44/ILDConfig/v01-16-p05_500/StandardConfig/current
  configdir=${MCPROD_TOP}/config

  filelist=$1
  outfile=$2
  maxrec=0
  marlinsteer=marlin_merge.xml
  gearfile=GearOutput.xml
  ln -sf ${geardir}/GearOutput.xml .

  cat ${configdir}/marlin_merge.xml.in | \
  sed -e "/%%LIST_MERGE_INPUT_FILES%%/r${filelist}" -e "/%%LIST_MERGE_INPUT_FILES%%/d" \
      -e "s/%%MAX_RECORD_NUMBER%%/${maxrec}/" \
      -e "s/%%GEAR_FILE%%/${gearfile}/" \
      -e "s|%%MERGE_OUTPUT_FILE%%|${outfile}|" > \
          ${marlinsteer}  

  # Marlin ${marlinsteer} > ${marlinlog} 2>&1 
  Marlin ${marlinsteer} 
  ret=$?
  echo "### Marlin completed with ret=$ret : `date` "

}

echo "### lcio_merge.sh started : `date` "
echo "arg1=$1"
echo "arg2=$2"
echo "##################################"

do_merge $1 $2

