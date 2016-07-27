
subdir="001"
for i in `seq 6834 6837` ; do 
  cat sim-${i}-${subdir}.lfnlist | while read f ; do ( dirac-dms-replicate-lfn $f DESY-SRM ) ; done > sim-${i}-${subdir}-rep.log 2>&1 &
done


subdir="000"
for i in `seq 6835 6837` ; do 
  cat sim-${i}-${subdir}.lfnlist | while read f ; do ( dirac-dms-replicate-lfn $f DESY-SRM ) ; done > sim-${i}-${subdir}-rep.log 2>&1 &
done


