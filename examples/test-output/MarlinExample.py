from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Marlin
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC


basedir="/cvmfs/ilc.desy.de/sw/ILDConfig/v01-16-p05_500/StandardConfig/current/"
pandoraLikelihoodData=basedir+"PandoraLikelihoodData9EBin.xml"
bg_aver=basedir+"bg_aver.sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.PBeamstr-pairs.I230000.root"

simfile="LFN:/ilc/prod/ilc/mc-dbd/ild/sim/500-TDR_ws/6f_ttbar/ILD_o1_v05/v01-14-01-p00/sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I37623.P6f_bbcyyc.eR.pL-00001.slcio"
gearfile=basedir+"GearOutput.xml"
outdst = "toto.dst.slcio" #% i
outrec = "toto.rec.slcio" #% i

d= DiracILC(True,"repo.rep")

###In case one wants a loop: comment the folowing.
#for i in range(2):
j = UserJob()
j.setJobGroup("Tutorial")
j.setName("MarlinExample")#%i)



ma = Marlin()
ma.setDebug()
# ma.setLogLevel("verbose")
# ma.setILDConfig("v01-16-p05_500") 

ma.setVersion("v01-16-02")
ma.setSteeringFile("marlin_stdreco.xml")
ma.setGearFile(gearfile)
ma.setInputFile([simfile, pandoraLikelihoodData, bg_aver])
ma.setOutputDstFile(outdst)
ma.setOutputRecFile(outrec)


res = j.append(ma)
if not res['OK']:
    print res['Message']
    exit(1)
  
j.setOutputData(["myprod2/test/dst/"+outdst,"myprod2/test/rec/"+outrec],OutputSE="PNNL-SRM")
j.setOutputSandbox(["*.log","*.xml","*.sh"])
j.dontPromptMe()
j.submit(d)
