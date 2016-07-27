
for pr in 6838 6839 6840 ; do 
  (
    cd prod${pr}
    for subd in 000 001 ; do 
      ( 
        pwd
        cd log-${subd} 
        . xargs-jobout.sh 
      )
    done
  )

done

