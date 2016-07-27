from DIRAC.Core.Base import Script
Script.initialize()
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from DIRAC import gLogger

import os.path as path
import sys
from pprint import pprint


fc = FileCatalogClient()

# gridPath = "/ilc/prod/ilc/mc-dbd.generated/500-TDR_ws/4f/temp001/"
gridPath = "/ilc/prod/ilc/mc-dbd.generated/500-TDR_ws/4f/temp004/"

# filepref="E500-TDR_ws.P4f_sznu_l.Gwhizard-1_95.eR.pL.I250056.001"
filepref="E500-TDR_ws.P4f_sze_l.Gwhizard-1_95.eR.pR.I250035.003"
# srcpath="/ilc/prod/ilc/mc-dbd/generated/500-TDR_ws/4f/"+filepref+".stdhep"
srcpath="/ilc/prod/ilc/mc-dbd/generated/500-TDR_ws/4f/E500-TDR_ws.P4f_sze_l.Gwhizard-1_95.eR.pR.I250035.003.stdhep"
print "Original stdhep : "+srcpath
res=fc.getFileUserMetadata(srcpath)
if not res["OK"] : 
  print "Failed to get meta data of "+srcpath
  exit()

srcMeta = res["Value"]
pprint(srcMeta)

nseq_from=int(0)
nseq_to=int( 135)
nevents=int(1000)
last_fileseq=int( 135)
last_file_nevents=int( 76)

for i in range(nseq_from, nseq_to+1) : 
  filename=filepref+"_%3.3d.stdhep"%i
  print filename
  thisMeta=srcMeta
  nevents=nevents
  if i == last_fileseq : 
    nevents = last_file_nevents
  thisMeta["NumberOfEvents"]=nevents
  thisMeta["SerialNumber"]=3 
  thisMeta["SubSerialNumber"]=i
#  meta = fc.getFileUserMetadata(gridPath+filename)
  lfn=gridPath+filename
  res = fc.setMetadata(lfn, thisMeta)
  if not res['OK']:
    gLogger.error("Failed to set meta data %s to %s\n" % (lfn, thisMeta), res['Message'] )
  res = fc.getFileUserMetadata(lfn)
  print "Meta added to "+lfn
  pprint(res)
 
