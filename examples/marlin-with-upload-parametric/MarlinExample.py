'''
Example to run Marlin and write dst and rec files to different directories.
Parametirc job and with overlay

'''


import os

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Marlin, OverlayInput
from ILCDIRAC.Interfaces.API.NewInterface.Applications import GenericApplication
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC

simfile="LFN:/ilc/prod/ilc/mc-dbd/ild/sim/500-TDR_ws/6f_ttbar/ILD_o1_v05/v01-14-01-p00/sv01-14-01-p00.mILD_o1_v05.E500-TDR_ws.I37623.P6f_bbcyyc.eR.pL-00001.slcio"
setting_file="LFN:/ilc/user/a/amiyamot/software/Settings/marlinSettings-v01-17-09_500.tar.gz"

outdir="/ilc/user/a/amiyamot/myprod2/test/"
outdst = "toto-25.dst.slcio" #% i
outrec = "toto-25.rec.slcio" #% i


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
def getJob(dirac, jobid, jobpara):
  iser=jobid+100

  outdir = "/ilc/user/a/amiyamoto/myprod2/test/"
  outdst = "toto-ovl-%5.5i.dst.slcio"%iser
  outrec = "toto-ovl-%5.5i.rec.slcio"%iser
  dstlfn = outdir+"dst/"+outdst
  reclfn = outdir+"rec/"+outrec
  outsrm = "CERN-SRM"

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
  ma.setSteeringFile("marlin_stdreco.xml")
  ma.setGearFile("GearOutput.xml")
#   ma.setInputFile(simfile)
  ma.setInputFile(simlists[jobid])
  ma.setOutputDstFile(outdst)
  ma.setOutputRecFile(outrec)
  res = j.append(ma)
  if not res['OK']:
    print res['Message']
    exit(1)

# Upload files to different directories
  upload_script="upload%i.sh"%iser
  upload = GenericApplication()
# Create a script to upload files.
  shfile = open(upload_script,"w")
  shfile.write("#!/bin/bash\n")
  shfile.write("/bin/ls -l \n")
  shfile.write("dirac-dms-add-file -ddd "+dstlfn+" "+outdst+" "+outsrm+" \n")
  shfile.write("dirac-dms-add-file -ddd "+reclfn+" "+outrec+" "+outsrm+" \n")
  shfile.close()
  os.chmod(upload_script,0755)
  upload.setScript(upload_script)

  res = j.append(upload)
  if not res['OK'] :
    print res['Message']
    exit(1)

#   j.setOutputData([outdst,outrec],"myprod2/test","PNNL-SRM")
  j.setInputSandbox([ setting_file, upload_script ] )
  j.setOutputSandbox(["*.log","*.xml","*.sh","TaggingEfficiency.root","PfoAnalysis.root"])
  j.setCPUTime(10000)
  j.dontPromptMe()

  res = j.submit(dirac)
  if not res["OK"] :
    print "Failed submit job, jobid=%s" %jobid
    print res


  os.remove(upload_script)

  return j

# ##############################################################
# Main part
# ##############################################################


if __name__ == '__main__':

  d = DiracILC(True, "parametric.rep")

  for jobid in range(0, len(simlists)) :
    job = getJob(d, jobid, jobpara)




