from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Marlin
from ILCDIRAC.Interfaces.API.NewInterface.Applications import GenericApplication
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC

simfile="LFN:/ilc/prod/ilc/mc-dbd/ild/sim/500-TDR_ws/6f_ttbar/ILD_o1_v05/v01-14-01-p00/sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I37623.P6f_bbcyyc.eR.pL-00001.slcio"
setting_file="LFN:/ilc/user/a/amiyamot/software/Settings/marlinSettings-v01-17-09_500.tar.gz"


outdst = "toto-7.dst.slcio" #% i
outrec = "toto-7.rec.slcio" #% i

d= DiracILC(True,"repo.rep")

###In case one wants a loop: comment the folowing.
#for i in range(2):
j = UserJob()
j.setJobGroup("Tutorial")
j.setName("MarlinExample")#%i)
j.setInputSandbox([setting_file,"mypre.sh", "mypost.sh"])

################################################
appre = GenericApplication()
appre.setScript("mypre.sh")
appre.setArguments("This is input")
res=j.append(appre)
if not res['OK']:
  print res['Message']
  exit(1)

################################################
ma = Marlin()
ma.setDebug()
ma.setVersion("ILCSoft-01-17-09")
ma.setSteeringFile("marlin_stdreco.xml")
ma.setGearFile("GearOutput.xml")
ma.setInputFile(simfile)
ma.setOutputDstFile(outdst)
ma.setOutputRecFile(outrec)

res = j.append(ma)
if not res['OK']:
    print res['Message']
    exit(1)
  
################################################
appost = GenericApplication()
appost.setScript("mypost.sh")
appost.setArguments("This is at the end of job")
res=j.append(appost)
if not res['OK']:
  print res['Message']
  exit(1)


# j.setOutputData([outdst,outrec],"myprod2/test","PNNL-SRM")
j.setOutputSandbox(["*.log","*.xml","*.sh","TaggingEfficiency.root","PfoAnalysis.root"])
j.dontPromptMe()
# j.submit(d, mode="local")
j.submit(d)

