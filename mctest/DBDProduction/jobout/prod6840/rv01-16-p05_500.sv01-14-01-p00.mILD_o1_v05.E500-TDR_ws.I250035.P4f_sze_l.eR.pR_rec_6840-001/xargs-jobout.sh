cat xargs.input | xargs -P 10 -I{}  /bin/bash -c {} > getjobout.log 2>&1 
