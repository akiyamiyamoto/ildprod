#!/usr/bin/env python 


'''
Created on Mar 26, 2012

@author: Stephane Poss

Modified to perform ILD reconstruction.

C. Calancha
'''

from DIRAC.Core.Base import Script
Script.parseCommandLine()

from ILCDIRAC.Interfaces.API.NewInterface.ILDProductionJob import ILDProductionJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications     import Mokka, Marlin, OverlayInput
from ILCDIRAC.Interfaces.API.NewInterface.Applications     import SLCIOSplit, StdHepSplit
from decimal import Decimal

import os, sys, commands
from pprint import pprint

## Get config file name from the command line

argvs = sys.argv 
if len(argvs) !=3 :
  print 'Usage: python ILDProductionChain.py [dry or nodry] config_file'

  quit()

dryrun = True
if argvs[1] == "nodry" : 
  dryrun = False
  print "dryrun was set to False by a command line option"

config_file=argvs[2]
if ( not os.path.exists(config_file) ) :
  print config_file + " does not exist."
  quit()

print "Reading config file, "+config_file
execfile( config_file)



###### Whatever is below is not to be touched... Or at least only when something changes

overlay = OverlayInput()
overlay.setMachine("ilc_dbd")             #Don't touch, this is how the system knows what files to get
overlay.setEnergy(energy)                 #Don't touch, this is how the system knows what files to get
overlay.setDetectorModel(detectorModel) #Don't touch, this is how the system knows what files to get
overlay.setBkgEvtType("aa_lowpt")
if energy==500.: #here you chose the overlay parameters as this determines how many files you need
  #it does NOT affect the content of the marlin steering file whatsoever, you need to make sure the values
  #there are correct. Only the file names are handled properly so that you don't need to care
  overlay.setBXOverlay(BXOverlay)
  overlay.setGGToHadInt(GGToHadInt500)
elif energy == 1000.:
  overlay.setBXOverlay(BXOverlay)
  overlay.setGGToHadInt(GGToHadInt1000)
elif energy == 350.:
  overlay.setBXOverlay(BXOverlay)
  overlay.setGGToHadInt(GGToHadInt350)
elif energy == 250.:
  overlay.setBXOverlay(BXOverlay)
  overlay.setGGToHadInt(GGToHadInt250)
else:
  print "Overlay ILD: No overlay parameters defined for this energy"

##Reconstruction ILD with overlay
mao = Marlin()
mao.setDebug()
mao.setVersion(MarlinVer) ##PUT HERE YOUR MARLIN VERSION
if ild_rec_ov:
  if energy in [250.0, 350.0, 500.0, 1000.0]:
    mao.setSteeringFile("bbudsc_3evt_stdreco.xml")
    mao.setGearFile("GearOutput.xml")
  else:
    print "Marlin: No reconstruction suitable for this energy"


print "Applications defined."
print ild_rec_ov
print meta

###################################################################################
if ild_rec_ov and meta:
  #######################
  print "Goding to define production job"
  #Define the reconstruction prod
  pmao = ILDProductionJob()
  pmao.matchToInput = matchToInput_marlin
  pmao.setDryRun(dryrun)
  pmao.setILDConfig(ILDConfig)
  # pmao.setEvtClass(my_evtclass)
  ## # pmao.setUseSoftTagInPath(False)
  # pmao.setEvtType(my_evttype)
  pmao.setLogLevel("verbose")
  pmao.setProdType('MCReconstruction_Overlay')
  pmao.setBannedSites(banned_sites)
  pmao.setOutputSandbox(["*.log","*.sh","*.xml"])
  pmao.setInputSandbox( input_sand_box )
  pmao.setGenProcName(genprocessname)
  res = pmao.setInputDataQuery(meta)
  if not res['OK']:
    print res['Message']
    exit(1)

  pmao.setOutputSE(SE)
#   wname = process+"_"+str(energy)+"_ild_rec_overlay"
#   wname += additional_name
  pmao.setWorkflowName(wname)
  pmao.setProdGroup(prodgroup)


  #Add the application
  res = pmao.append(overlay)
  if not res['OK']:
    print res['Message']
    exit(1)
  #Add the application
  res = pmao.append(mao)
  if not res['OK']:
    print res['Message']
    exit(1)
  pmao.addFinalization(True,True,True,True)
  descrp = "%s, Overlay" % detectorModel

  if additional_name:
    descrp += ", %s"%additional_name
  pmao.setDescription(descrp)
  res = pmao.createProduction()
  if not res['OK']:
    print res['Message']

  res = pmao.setProcessIDInFinalPath()
  if not res['OK']:
    print res['Message']

  res = pmao.finalizeProd()
  if not res['OK']:
    print res['Message']
    exit(1)
