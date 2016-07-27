#!/bin/bash


mcprod_top=${MCPROD_TOP}
bindir=${mcprod_top}/bin
confdir=${mcprod_top}/config

tdir=$1
seq_begin=$2
if [ "x${tdir}" == "x" -o "x$2" == "x" ] ; then 
   echo "Usage:"
   echo "mkmerge.sh [tdir] [seq_begin]"
   echo " [tdir]=DST, 000, 001, ..."
   echo " [seq_begin]=seq. number of the first dst-merged file."
   exit
fi

set -eu

subsh="bsub.sh"
stdreco="marlin_merge.xml"
dstmergelist="dstmerge-${tdir}.list"

/bin/ls ${tdir}/*.slcio > ${dstmergelist}
fnpick=`head -1 ${dstmergelist} | sed -e "s|DST/||" -e "s/_dst_/ /" `
fpref=`echo $fnpick | cut -d" " -f1 `
prodid=`echo $fnpick | cut -d" " -f2 | cut -d"_" -f1`

filesize_default=500
totdstsize=`du -bsm ${tdir} | cut -f1`
nfile=`echo "print ${totdstsize}/${filesize_default}+1" | python`
wc_list=`wc -l ${dstmergelist} | cut -d" " -f1`
lines_per_file=`echo "print ${wc_list}/${nfile}+1" | python `

split -l ${lines_per_file} -a 3 ${dstmergelist}
iser=$[$seq_begin-1]


for f in xa[a-z][a-z] ; do 
  iser=$[$iser+1]
  seqstr=`printf "%2.2d" ${iser}`
  mergedir="merge-${tdir}-${seqstr}"
  mkdir ${mergedir}
  ( 
    cd ${mergedir}
    echo "#!/bin/bash " > ${subsh}
    echo "export MCPROD_TOP=${mcprod_top}" >> ${subsh}
    outdst=`basename ${fpref}_dst_${prodid}_${seqstr}-DST.slcio`
    jobname="merge${prodid}"
    logfile="merge-${seqstr}.log"
    ln -s ../${tdir} .
    mv -v ../$f . 
    echo "bsub -o ${logfile} -J ${jobname}  -q s \"( ${bindir}/lcio_merge.sh ${f} ${outdst} > ${logfile} 2>&1 )\" " >> ${subsh}
  )

done

