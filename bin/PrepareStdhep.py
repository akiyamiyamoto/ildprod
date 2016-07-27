from subprocess import call, check_call
import sys, os

# mokkacfg=topdir+"/mokka-production.cfg.in"
# setmeta_py="setMetaData.py" # actual setMetaData.py, which is created in each directory




class PrepareStdhep :
  def __init__(self):
    self._confdir="/home/ilc/miyamoto/DiracProd/config/"
    self._setmeta_temp=self._confdir+"setMetaData.py.in"
    self._setup_gcc_cmd=". /group/ilc/soft/gcc481/gcc481.setup"
    self._hepsplit_exe="/home/ilc/miyamoto/bin/hepsplit"

    self.settings={}
    self.settings["src_lfn_dir"]="/ilc/prod/ilc/mc-dbd/generated/500-TDR_ws/4f/"
    self.settings["src_local_dir"]="../4f/"
    self.settings["upload_dir"]="/ilc/prod/ilc/mc-dbd.generated/500-TDR_ws/4f/temp003/"
    self.settings["upload_se"]="PNNL-SRM"
    self.settings["fnkeys"]={"E":"500-TDR_ws","P":"4f_szeorsw_l","G":"whizard-1_95"}
    self.settings["nw_per_file"]="1000"

  def setSettings(self, settings):
    # Set settings
    self.settings=settings

  def makeFileName(self, fnkeys, keyorder) :
    # Construct a file name from file name key list.
    fn=""
    for k in keyorder.split(" "):
      if len(fn) > 0 :
        fn+="."
      fn+=k+fnkeys[k]
    return fn

  def makeSplitScripts(self, jobkey, jobvalues):
    # Produce scripts for stdhep split
    # jobkey : GenProcessID.FileSeqNumber, 250001.001 for example.
    # jobvalues : array containing information for stdhep split, for example, 
    #             {"pol":"eL.pR","nseq_from":237,"skip_nevents":47100}
    (processid, serial_number_s)=jobkey.split(".")
    serial_number=int(serial_number_s)
    workdir="stdhep-"+jobkey
    hepsplitlog="hepsplit-"+jobkey+".log"
    src_stdhep_pref=self.makeFileName(self.settings["fnkeys"], "E P G")+"."+jobvalues["pol"]+".I"+jobkey
    ret=call("mkdir -p "+workdir, shell=True)
    os.chdir(workdir)

#   Step1: a script for hepsplit and create a list of splitted files
    fcmd=open("step1-splitcmd.sh","w")
    fcmd.write("#!/bin/bash \n")
    fcmd.write("# Run hepsplit and create splitted hepstd files.\n")
    fcmd.write(self._setup_gcc_cmd+"\n")
    fcmd.write(self._hepsplit_exe+" --infile "+self.settings["src_local_dir"]+src_stdhep_pref+".stdhep \\\n")
    fcmd.write(" --outpref "+src_stdhep_pref+" \\\n")
    if jobvalues["skip_nevents"] != 0 :
      fcmd.write(" --nseq_from "+str(jobvalues["nseq_from"]) )
      fcmd.write(" --skip_nevents "+str(jobvalues["skip_nevents"])+" \\\n")
    fcmd.write(" --nw_per_file "+str(self.settings["nw_per_file"])+" \\\n")
    fcmd.write(" > "+hepsplitlog+" 2>&1 \n")
    fcmd.write("# make a list of splitted stdhep file.\n")
    fcmd.write("/bin/ls "+src_stdhep_pref+"*.stdhep > stdhep.list")
    fcmd.close()

#2  Step2: Create a script to upload splitted stdhep files.
    fcmd2=open("step2-upload.sh","w")
    fcmd2.write("#!/bin/bash \n")
    fcmd2.write("cat stdhep.list | xargs -P 15 -I{} dirac-dms-add-file "+self.settings["upload_dir"]+"{} {} "+self.settings["upload_se"] + "> upload.log 2>&1 " )
    fcmd2.close()

#   Step3: Create a script to setMeta to the uploaded files.
    fcmd3=open("step3-makeSetMeta.sh","w")
    fcmd3.write("#!/bin/bash \n")
    fcmd3.write("# Create a script to set meta data.\n")
    fcmd3.write("nseq_to=`grep -a \"  File number of the last file :\" "+hepsplitlog+" | cut -d\":\" -f2 `\n")
    fcmd3.write("last_fileseq=${nseq_to}\n")
    fcmd3.write("last_file_nevents=`grep -a \" Record written = \" "+hepsplitlog+" | tail -1 | cut -d\"=\" -f2 `\n")
    fcmd3.write("echo \"Last file number is ${last_fileseq}\" \n")
    fcmd3.write("echo \"Event number of last file is ${last_file_nevents}\" \n")

    fcmd3.write("cat "+self._setmeta_temp+" | sed \\\n")
    fcmd3.write(" -e \"s|%%GRID_PATH%%|"+self.settings["upload_dir"]+"|g\" \\\n")
    fcmd3.write(" -e \"s|%%FILE_PREFIX%%|"+src_stdhep_pref+"|g\" \\\n")
    fcmd3.write(" -e \"s|%%SRC_PATH%%|"+self.settings["src_lfn_dir"]+src_stdhep_pref+".stdhep|g\" \\\n")
    fcmd3.write(" -e \"s|%%NSEQ_FROM%%|"+str(jobvalues["nseq_from"])+"|g\" \\\n")
    fcmd3.write(" -e \"s|%%NSEQ_TO%%|${nseq_to}|g\" \\\n")
    fcmd3.write(" -e \"s|%%NEVENTS%%|"+self.settings["nw_per_file"]+"|g\" \\\n")
    fcmd3.write(" -e \"s|%%LAST_FILENO%%|${last_fileseq}|g\" \\\n")
    fcmd3.write(" -e \"s|%%SERIAL_NUMBER%%|"+str(serial_number)+"|g\" \\\n")
    fcmd3.write(" -e \"s|%%LAST_FILE_NEVENTS%%|${last_file_nevents}|g\" \\\n")
    fcmd3.write(" > setMetaData.py \n")
    fcmd3.write("echo \" a script to write Metadata, setMetaData.py was created.\"\n")
    fcmd3.close()

#  Step4: Create a script to execute setMetaData.py
    fcmd4=open("step4-runsetMeta.sh","w")
    fcmd4.write("# Run setMetaData.py\n")
    fcmd4.write("python setMetaData.py > setMetaData.log 2>&1  \n")
    fcmd4.close()

#  Step-all
    fcmdall=open("allstep.sh","w")
    fcmdall.write("#!/bin/bash\n")
    fcmdall.write("( export LC_ALL=C && date )\n")
    fcmdall.write("hostname \n")
    fcmdall.write("./step1-splitcmd.sh \n")
    fcmdall.write("echo \"step1-splitcmd.sh completed.\" \n")
    fcmdall.write("./step2-upload.sh\n")
    fcmdall.write("echo \"upload completed.\"\n")
    fcmdall.write("./step3-makeSetMeta.sh\n")
    fcmdall.write("./step4-runsetMeta.sh\n")
    fcmdall.write("echo \"runSetMeta completed.\"\n")
    fcmdall.write("( export LC_ALL=C && date )\n")
    fcmdall.close()

    ret=call("chmod +x *.sh",shell=True)
    print "Scripts were created in "+workdir
    os.chdir("..")


#if __name__ == "__main__" :
#
#  jobparam={"250049.001":{"pol":"eL.pL","nseq_from":24,"skip_nevents":4500},
#            "250050.001":{"pol":"eL.pR","nseq_from":237,"skip_nevents":47100},
#            "250050.002":{"pol":"eL.pR","nseq_from":0,"skip_nevents":0},
#            "250050.003":{"pol":"eL.pR","nseq_from":0,"skip_nevents":0},
#            "250050.004":{"pol":"eL.pR","nseq_from":0,"skip_nevents":0},
#            "250051.001":{"pol":"eR.pR","nseq_from":3,"skip_nevents":4500}}


#  prod=PrepareStdhep()

##   prod.makeSplitScripts("250052.001",{"pol":"eR.pL","nseq_from":3,"skip_nevents":1400})
##   prod.makeSplitScripts("250051.001",{"pol":"eR.pR","nseq_from":3,"skip_nevents":4500})
##  prod.makeSplitScripts("250050.001",{"pol":"eL.pR","nseq_from":237,"skip_nevents":47100})
##  prod.makeSplitScripts("250049.001",{"pol":"eL.pL","nseq_from":24,"skip_nevents":4500})
##  prod.makeSplitScripts("250050.002",{"pol":"eL.pR","nseq_from":0,"skip_nevents":0})
#  prod.makeSplitScripts("250050.003",{"pol":"eL.pR","nseq_from":0,"skip_nevents":0})
#  prod.makeSplitScripts("250050.004",{"pol":"eL.pR","nseq_from":0,"skip_nevents":0})



