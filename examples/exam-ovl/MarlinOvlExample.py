from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Marlin, OverlayInput
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC


basedir="/cvmfs/ilc.desy.de/sw/ILDConfig/v01-16-p05_500/StandardConfig/current/"
pandoraLikelihoodData=basedir+"PandoraLikelihoodData9EBin.xml"
bg_aver=basedir+"bg_aver.sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.PBeamstr-pairs.I230000.root"
simdir="/ilc/prod/ilc/mc-dbd/ild/sim/500-TDR_ws/higgs/ILD_o1_v05/v01-14-01-p00/00006762/000/"
simfile="LFN:"+simdir+"sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I108161.Pffh.eL.pL_sim_6762_1.slcio"

gearfile=basedir+"GearOutput.xml"
outdst = "toto.dst.slcio" #% i
outrec = "toto.rec.slcio" #% i

n_events_per_job=50000
energy=500
GGToHadInt500=1.7
BXOverlay=1

d= DiracILC(True,"repo.rep")

###In case one wants a loop: comment the folowing.
#for i in range(2):
j = UserJob()
j.setJobGroup("Tutorial")
j.setName("MarlinExample")#%i)
j.setInputSandbox([pandoraLikelihoodData, bg_aver])

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

ma = Marlin()
ma.setDebug()
# ma.setLogLevel("verbose")
# ma.setILDConfig("v01-16-p05_500") 

ma.setVersion("v01-16-02")
ma.setSteeringFile("marlin_stdreco.xml")
ma.setGearFile(gearfile)
ma.setInputFile(simfile)
ma.setOutputDstFile(outdst)
ma.setOutputRecFile(outrec)


res = j.append(ma)
if not res['OK']:
    print res['Message']
    exit(1)
  
# j.setOutputData([outdst,outrec],"myprod2/test","PNNL-SRM")
j.setOutputSandbox(["*.log","*.xml","*.sh"])
j.dontPromptMe()
j.submit(d, mode="local")
