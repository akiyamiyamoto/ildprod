from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import DDSim
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC
from datetime import datetime


localjob=True
localjob=False

if localjob :
  genfile="/gpfs/home/ilc/miyamoto/ILDProd/examples/ddsim-v01-17-10/E0500-TDR_ws.Pea_lvv.Gwhizard-1.95.eL.pB.I37494.01_000.stdhep"

else:
  genfile="LFN:/ilc/prod/ilc/ild/test/temp1/gensplit/500-TDR_ws/3f/run002/E0500-TDR_ws.Pea_lvv.Gwhizard-1.95.eL.pB.I37494.01_000.stdhep"

now = datetime.now()
simfile="ddsim-data-%s.slcio" % now.strftime("%Y%m%d-%H%M%S")
steeringfile="/cvmfs/ilc.desy.de/sw/ILDConfig/v01-17-10-p01/StandardConfig/lcgeo_current/ddsim_steer.py"

d= DiracILC(True,"repo.rep")

###In case one wants a loop: comment the folowing.
#for i in range(2):
j = UserJob()
j.setJobGroup("Tutorial")
j.setName("DDSim-example")  #%i)
# j.setInputSandbox(setting_file)

ddsim = DDSim()
ddsim.setVersion("ILCSoft-01-17-10")
ddsim.setDetectorModel("ILD_o1_v05")
ddsim.setInputFile(genfile)
ddsim.setRandomSeed(12345)
# ddsim.setStartFrom(1)
ddsim.setNumberOfEvents(5)  # Number of events should not exceed number of events in file.
                            # Otherwise, G4exception is thrown
# ddsim.setDebug()
ddsim.setSteeringFile(steeringfile)
ddsim.setOutputFile(simfile)

res = j.append(ddsim)
if not res['OK']:
    print res['Message']
    exit(1)
  
j.setOutputSandbox(["*.log","*.xml","*.sh","*.root"])
j.dontPromptMe()

if localjob :
  j.submit(d, mode="local")

else:
  simdir="testjob"
  j.setOutputData(simfile,simdir,"PNNL-SRM")
  res=j.submit(d)
  if res['OK']:
    print "Dirac job, "+str(res["Value"])+", was submitted."
  else:
    print "Failed to submit dirac job. "
    print res
