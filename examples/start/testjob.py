#!/usr/bin/env python


import sys

from DIRAC.Core.Base import Script
Script.parseCommandLine()

from ILCDIRAC.Interfaces.API.NewInterface.UserJob import *
from ILCDIRAC.Interfaces.API.NewInterface.Applications import *
from ILCDIRAC.Interfaces.API.DiracILC import *

argvs=sys.argv
argc=len(argvs)
print argvs

param={"KEK":{"dest":"LCG.KEK.jp","name":"testkek"},
       "DESY":{"dest":"LCG.DESY-HH.de","name":"testdesy"},
       "PNNL":{"dest":"OSG.PNNL.us","name":"testpnnl"},
       "CERN":{"dest":"LCG.CERN.ch","name":"testcern"}}

site="KEK"
opt=""
if (argc > 1) :
  site = argvs[1]

if (argc > 2 ) :
  opt = argvs[2]

jobname=param[site]["name"]
dest=param[site]["dest"]

print "Test getfile to "+site+"( jobname="+jobname+" dest="+dest+" opt="+opt+")"

job = UserJob()
job.setCPUTime(500)  # time in sec
job.setExecutable('/bin/ls -l ')
job.setExecutable('/bin/bash test.sh')

job.setName("test1")

job.setInputSandbox(["test.sh"])
job.setOutputSandbox(["*.log","*.dat"])
# job.setDestination(dest)
job.dontPromptMe()

dirac = DiracILC(True,jobname+".rep")
jobID = job.submit(dirac)
print jobname+" submitted. JobID=",jobID



