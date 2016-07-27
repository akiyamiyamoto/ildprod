#!/bin/bash

if [ "x$1" == "x" ] ; then 
  echo "Usage: ./mk_outcmd.sh.sh [subdir]"
  ech "[subdir]=000, 001, ..."
  exit
fi

subdir=$1

mkdir log-${subdir}
cd log-${subdir}

  pwd
  xargsinput="xargs.input"
  joboutcmd="jobout.sh"
  getjobout="xargs-jobout.sh"
  for f in ../${subdir}/*.gz ; do 
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


cd ..


