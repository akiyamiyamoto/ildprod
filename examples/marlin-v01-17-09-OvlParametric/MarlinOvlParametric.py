from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Marlin, OverlayInput
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC

simdir="LFN:/ilc/prod/ilc/mc-dbd/ild/sim/500-TDR_ws/6f_ttbar/ILD_o1_v05/v01-14-01-p00/"
simlists=[]
for i in range(0,5) :
  iser=i+1
  simlists.append(simdir+"sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I37623.P6f_bbcyyc.eR.pL-%5.5i.slcio"%iser)

energy=500
jobpara={}
jobpara["setting_file"]="LFN:/ilc/user/a/amiyamot/software/Settings/marlinSettings-v01-17-09_500.tar.gz"
jobpara["n_events_per_job"]=100
jobpara["energy"]=500
jobpara["GGToHadInt500"]=1.7
jobpara["BXOverlay"]=1



############################################################
def getJob(jobid, jobpara):
  iser=jobid+1

  outdst = "toto-ovl-%5.5i.dst.slcio"%iser
  outrec = "toto-ovl-%5.5i.rec.slcio"%iser

###In case one wants a loop: comment the folowing.
#for i in range(2):
  j = UserJob()
  j.setJobGroup("Tutorial")
  j.setName("MarlinOverlayParametric%i"%iser)
  j.setInputSandbox(jobpara["setting_file"])

## Define the overlay
  ov = OverlayInput()
  ov.setMachine("ilc_dbd")
  ov.setEnergy(energy)
  ov.setNumberOfSignalEventsPerJob(int(jobpara["n_events_per_job"]))
  ov.setBXOverlay(int(jobpara["BXOverlay"]))
  ov.setGGToHadInt(float(jobpara["GGToHadInt500"]))
  ov.setBkgEvtType("aa_lowpt")
# ov.setBackgroundType("aa_lowpt")
  ov.setDetectorModel("ILD_o1_v05")
  res = j.append(ov)
  if not res['OK']:
    print res['Message']
    exit(1)

## Define Marlin job
  ma = Marlin()
  ma.setDebug()
  ma.setVersion("ILCSoft-01-17-09")
  ma.setSteeringFile("marlin_ovl_stdreco.xml")
  ma.setGearFile("GearOutput.xml")
#   ma.setInputFile(simfile)
  ma.setInputFile(simlists[jobid])
  ma.setOutputDstFile(outdst)
  ma.setOutputRecFile(outrec)
  res = j.append(ma)
  if not res['OK']:
    print res['Message']
    exit(1)
  
  j.setOutputData([outdst,outrec],"myprod2/test","PNNL-SRM")
  j.setOutputSandbox(["*.log","*.xml","*.sh","TaggingEfficiency.root","PfoAnalysis.root"])
  j.setCPUTime(10000)
  j.dontPromptMe()
  return j


if __name__ == '__main__':

  d = DiracILC(True, "parametric.rep")

  for jobid in range(0, len(simlists)) :
    job = getJob(jobid, jobpara)
#     job.setParametricInputData(simlists[jobid])
    res = job.submit(d)
    if not res["OK"] : 
      print "Failed submit job"
      print res

