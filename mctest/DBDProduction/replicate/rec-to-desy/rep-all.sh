
destse="DESY-SRM"
dt="rec"
subdir="001"
seqfrom=6838
seqto=6841

for i in `seq ${seqfrom} 6840` ; do 
  cat ${dt}-${i}-${subdir}.lfnlist | while read f ; do ( dirac-dms-replicate-lfn $f ${destse} ) ; done > ${dt}-${i}-${subdir}-rep.log 2>&1 &
done


subdir="000"
for i in `seq ${seqfrom} ${seqto}` ; do 
  cat ${dt}-${i}-${subdir}.lfnlist | while read f ; do ( dirac-dms-replicate-lfn $f ${destse} ) ; done > ${dt}-${i}-${subdir}-rep.log 2>&1 &
done


