from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Marlin, OverlayInput
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC

simfile="LFN:/ilc/prod/ilc/mc-dbd/ild/sim/500-TDR_ws/6f_ttbar/ILD_o1_v05/v01-14-01-p00/sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I37623.P6f_bbcyyc.eR.pL-00001.slcio"
setting_file="LFN:/ilc/user/a/amiyamot/software/Settings/marlinSettings-v01-17-09_500.tar.gz"

n_events_per_job=100
energy=500
GGToHadInt500=1.7
BXOverlay=1

outdst = "toto-ovl.dst.slcio" #% i
outrec = "toto-ovl.rec.slcio" #% i

d= DiracILC(True,"repo.rep")

###In case one wants a loop: comment the folowing.
#for i in range(2):
j = UserJob()
j.setJobGroup("Tutorial")
j.setName("MarlinOverlayExample")#%i)
j.setInputSandbox([setting_file])

## Define the overlay
ov = OverlayInput()
ov.setMachine("ilc_dbd")
ov.setEnergy(energy)
ov.setNumberOfSignalEventsPerJob(n_events_per_job)
ov.setBXOverlay(BXOverlay)
ov.setGGToHadInt(GGToHadInt500)
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
ma.setInputFile(simfile)
ma.setOutputDstFile(outdst)
ma.setOutputRecFile(outrec)
res = j.append(ma)
if not res['OK']:
    print res['Message']
    exit(1)
  

j.setOutputData([outdst,outrec],"myprod2/test","PNNL-SRM")
j.setOutputSandbox(["*.log","*.xml","*.sh","TaggingEfficiency.root","PfoAnalysis.root"])
j.dontPromptMe()
j.submit(d)
