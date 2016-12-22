#!/bin/bash

if [ "x$1" == "x" ] ; then 
  echo "This command download production job logs."
  echo "Usage: postprod.sh [prodid]"
  exit
fi

prodid=$1

mkdir prod${prodid}
cd prod${prodid}

# /ilc/prod/ilc/mc-dbd/ild/rec/500-TDR_ws/4f_singleZee_leptonic/ILD_o1_v05/v01-16-p05_500/00006838/LOG/001

echo "### Executing dirac-ilc-get-info -p ${prodid} ##########"
dirac-ilc-get-info -p $prodid 2>&1 | tee prodinfo-${prodid}.log
echo "### Executing dirac-ilc-get-prod-log -P ${prodid} ######"
dirac-ilc-get-prod-log -P ${prodid} 
mv -v 000 tgz
mkdir -v log
cd log 
  pwd
  xargsinput="xargs.input"
  joboutcmd="jobout.sh"
  getjobout="xargs-jobout.sh"
  for f in ../tgz/*.gz ; do 
    fdir=`basename $f | sed -e "s/.tar.gz//"`
    (
      mkdir -v $fdir
      cd ${fdir}
      tar zxf ../$f 
    )
  done

  echo "### Picking up jobid at `pwd` ####################"
  for d in 0* ; do 
    jobid=`grep DIRACJOBID $d/localEnv.log | cut -d"=" -f2`
    echo "cd $d && dirac-wms-job-get-output ${jobid} " > $d/${joboutcmd}
    chmod +x $d/${joboutcmd}
    echo "${d}/${joboutcmd}" >> ${xargsinput}
  done

  echo "cat ${xargsinput} | xargs -P 10 -I{}  /bin/bash -c {} > getjobout.log 2>&1 " > ${getjobout}
  echo "jobout command was created at ${getjobout}"





