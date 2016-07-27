
import sys, os
from PrepareStdhep import PrepareStdhep

settings={}
settings["src_lfn_dir"]="/ilc/prod/ilc/mc-dbd/generated/500-TDR_ws/4f/"
settings["src_local_dir"]="../4f/"
settings["upload_dir"]="/ilc/prod/ilc/mc-dbd.generated/500-TDR_ws/4f/temp004/"
settings["upload_se"]="PNNL-SRM"
settings["fnkeys"]={"E":"500-TDR_ws","P":"4f_sze_l","G":"whizard-1_95"}
settings["nw_per_file"]="1000"

prep=PrepareStdhep()
prep.setSettings(settings)

# prep.makeSplitScripts("250033.002",{"pol":"eL.pL","nseq_from":898,"skip_nevents":64211})
# prep.makeSplitScripts("250034.003",{"pol":"eL.pR","nseq_from":0,"skip_nevents":67016})
# prep.makeSplitScripts("250035.002",{"pol":"eR.pR","nseq_from":0,"skip_nevents":64083})
# prep.makeSplitScripts("250036.003",{"pol":"eR.pL","nseq_from":0,"skip_nevents":60437})

# for ser in range(4, 11) : 
#  key="250034.%3.3d"%ser
#  prep.makeSplitScripts(key,{"pol":"eL.pR","nseq_from":0,"skip_nevents":0})

# for ser in range(3, 11) :
#   key="250033.%3.3d"%ser
#   prep.makeSplitScripts(key,{"pol":"eL.pL","nseq_from":0,"skip_nevents":0})

for ser in range(3, 11) :
   key="250035.%3.3d"%ser
   prep.makeSplitScripts(key,{"pol":"eR.pR","nseq_from":0,"skip_nevents":0})

for ser in range(4, 11) :
   key="250036.%3.3d"%ser
   prep.makeSplitScripts(key,{"pol":"eR.pL","nseq_from":0,"skip_nevents":0})

