#!/bin/bash
##
##
## a script to upload file
##
/bin/ls -l 
dirac-dms-add-file -ddd /ilc/user/a/amiyamot/myprod2/test/dst/toto-25.dst.slcio toto-25.dst.slcio CERN-SRM
dirac-dms-add-file -ddd /ilc/user/a/amiyamot/myprod2/test/rec/toto-25.rec.slcio toto-25.rec.slcio CERN-SRM
