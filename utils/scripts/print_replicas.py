#!/usr/bin/env python
########################################################################
# $HeadURL$
# File :    print_replicas.py
# Author :  Akiya Miyamoto
########################################################################
"""
  Print number of replicas and replicas' names for LFN.
  [Usage]
    python print_replicas.py [lfn_list_file]

    [lfn_list_file] is a file containing LFN
    Result is writeen to std.out
    
"""

import DIRAC
from DIRAC.Core.Base import Script
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from DIRAC.Core.Base import Script


import os,sys
import pprint

Script.initialize()
fileCatalog = FileCatalogClient()
lfns=["lfns.list"]
exitCode = 0

def getSEInfo(lfns) :

  result = fileCatalog.getReplicas( lfns )
  if not result['OK']:
    print 'ERROR: ', result['Message']
    exitCode = 2
    DIRAC.exit( exitCode )

  replicas=result['Value']['Successful'][lfns]
  nreplicas = len(replicas)

  ralsrm=''
  selist=''
  for se in replicas.keys() :
    selist=selist+se+','
#    if se == target :
#      ralsrm=replicas[se]

  print str(nreplicas)+' '+lfns+' '+selist[:-1]



if __name__ == '__main__':

  filelist=sys.argv[1]
  print "filelist is "+filelist

  f = open(filelist, 'r')
  for fn in f.readlines() :
    getSEInfo(fn[:-1])


