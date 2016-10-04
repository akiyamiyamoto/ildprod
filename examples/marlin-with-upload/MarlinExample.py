'''
Example to run Marlin and write dst and rec files to different directories.

'''


import os

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Marlin
from ILCDIRAC.Interfaces.API.NewInterface.Applications import GenericApplication
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC

simfile="LFN:/ilc/prod/ilc/mc-dbd/ild/sim/500-TDR_ws/6f_ttbar/ILD_o1_v05/v01-14-01-p00/sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I37623.P6f_bbcyyc.eR.pL-00001.slcio"
setting_file="LFN:/ilc/user/a/amiyamot/software/Settings/marlinSettings-v01-17-09_500.tar.gz"

outdir="/ilc/user/a/amiyamot/myprod2/test/"
outdst = "toto-25.dst.slcio" #% i
outrec = "toto-25.rec.slcio" #% i


d= DiracILC(True,"repo.rep")

###In case one wants a loop: comment the folowing.
#for i in range(2):
j = UserJob()
j.setJobGroup("Tutorial")
j.setName("MarlinExample")#%i)

ma = Marlin()
ma.setDebug()
ma.setVersion("ILCSoft-01-17-10")
ma.setSteeringFile("marlin_stdreco.xml")
ma.setGearFile("GearOutput.xml")
ma.setInputFile(simfile)
ma.setOutputDstFile(outdst)
ma.setOutputRecFile(outrec)

res = j.append(ma)
if not res['OK']:
    print res['Message']
    exit(1)
  
# Upload files to different directories
upload_script="upload.sh"
upload = GenericApplication()
# Create a script to upload files.
shfile = open(upload_script,"w")
shfile.write("#!/bin/bash\n")
shfile.write("/bin/ls -l \n")
shfile.write("dirac-dms-add-file -ddd "+outdir+"dst/"+outdst+" "+outdst+" CERN-SRM\n")
shfile.write("dirac-dms-add-file -ddd "+outdir+"rec/"+outrec+" "+outrec+" CERN-SRM\n")
shfile.close()
os.chmod(upload_script,0755)
upload.setScript(upload_script)

res = j.append(upload)
if not res['OK'] :
  print res['Message']
  exit(1)

j.setInputSandbox([ setting_file, upload_script ] )

j.setOutputSandbox(["*.log","*.xml","*.sh","TaggingEfficiency.root","PfoAnalysis.root"])
j.dontPromptMe()
j.submit(d)
