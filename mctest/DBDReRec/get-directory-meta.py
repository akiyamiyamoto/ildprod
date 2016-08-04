#!/usr/bin/env python 
from DIRAC.Core.Base import Script
Script.initialize()
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from DIRAC import gLogger

import os.path as path
import sys
from pprint import pprint


fc = FileCatalogClient()

topdir="/ilc/prod/ilc/test/ild-rerec/"
topdir="/ilc/prod/ilc/mc-dbd/"

res=fc.listDirectory(topdir)
pprint(res)

res=fc.getDirectoryMetadata(topdir)
pprint(res)



#res=fc.getFileUserMetadata(topdir)
#if not res["OK"] : 
#  print "Failed to get meta data of "+topdir
#  pprint(res)
#  exit()

#srcMeta = res["Value"]
#pprint(srcMeta)


