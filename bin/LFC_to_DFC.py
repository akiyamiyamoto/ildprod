#!/usr/bin/env python

#########################################################################################
#
# Script to populate the DIRAC FileCatalog with the information from the LFC
# FileCatalog
#
# Author: A.Tsaregorodtsev
# Last Modified: 4.01.2012 
#
#########################################################################################

from DIRAC.Core.Base import Script
Script.parseCommandLine()

import DIRAC.Resources.Catalog.LcgFileCatalogClient as LcgFileCatalogClient
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from DIRAC.ConfigurationSystem.Client.Helpers.Registry import getUsernameForDN, getGroupsWithVOMSAttribute, getDNForUsername
from DIRAC.Core.Utilities.ThreadPool import ThreadPool, ThreadedJob
from DIRAC.Core.Utilities.ProcessPool import ProcessPool
from DIRAC.Core.Utilities.File import makeGuid
from DIRAC import gConfig, S_OK, S_ERROR

import time, sys, random
import os,  commands
from pprint import pprint

dirCount = 0
fileCount = 0
globalStart = time.time()

dnCache = {}
roleCache = {}

def getDNandRole(info):
  global dnCache, roleCache

  owner = {}
  username = dnCache.get(info['Owner'])
  if username:
    result = getDNForUsername(info['Owner'])
    if not result['OK']:
      print "Cannot find DN"
      return S_ERROR()
    owner['OwnerDN']=result['Value']
    owner['OwnerRole'] = 'ilc/Role=production'
  else:
    print "no username"
  return owner

def getUserNameAndGroup(info):
  """ Get the user name and group from the DN and VOMS role
  """

  global dnCache, roleCache

  owner = {}
  username = dnCache.get(info['OwnerDN'])
  if not username:
    result = getUsernameForDN(info['OwnerDN'])
    if result['OK']:
      username = result['Value']
      dnCache[info['OwnerDN']] = username
    elif "No username" in result['Message']:
      username = 'Unknown'
      dnCache[info['OwnerDN']] = username

  if username and username != 'Unknown':
    groups = roleCache.get('/'+info['OwnerRole'])
    if not groups:
      groups = getGroupsWithVOMSAttribute('/'+info['OwnerRole'])
      roleCache['/'+info['OwnerRole']] = groups
    if groups:
      owner['username'] = username
      owner['group'] = groups[0]

  return owner

def processDir(initPath,recursive=False,host=None,fcInit=None,dfcInit=None):
  """ Process one directory,  possibly recursively 
  """

  global dirCount, fileCount, globalStart, dnCache, roleCache, outputFile

  fc = fcInit
  if not fc:
    fc = LcgFileCatalogClient.LcgFileCatalogClient( host=host )
    #fc = FileCatalogClient()
  dfc = dfcInit
  if not dfc:
    #dfc = LcgFileCatalogClient.LcgFileCatalogClient( host=host )
    dfc = FileCatalogClient()
  start = time.time()
  initPath = initPath.rstrip("/")
  resultList = fc.listDirectory(initPath,True)
  #print resultList
  #return S_OK()

  lfc_time = (time.time() - start)

  s = time.time()
  print resultList
  if resultList['OK']:
  # Add directories

    if resultList['Value']['Failed']:
      return S_ERROR("Path %s failed: %s" % (initPath,resultList['Value']['Failed'][initPath]))

    dirDict = resultList['Value']['Successful'][initPath]['SubDirs']
    paths = {}
    for path,info in dirDict.items():
      print info
      paths[path] = {}
      paths[path]['Mode'] = info['Mode']
      owner = getUserNameAndGroup( info )
      #owner = getDNandRole( info )
      if owner:
        paths[path]['Owner'] = owner
    #return S_OK()
    p_dirs = time.time() - s
    s = time.time()
    nDir = len(paths)
    if nDir:
      print "Adding %d directories in %s" % (nDir,initPath)
      result = dfc.createDirectory(paths)
      if not result['OK']:
        print "Error adding directories:",result['Message']

      dirCount += nDir
      print "Total directories added", dirCount

    e_dirs = time.time() - s

    # Add files

    s = time.time()

    fileDict = resultList['Value']['Successful'][initPath]['Files']
    lfns = {}
    for lfn,info in fileDict.items():


      lfns[lfn] = {}
      lfns[lfn]['Size'] = info['MetaData']['Size']
      lfns[lfn]['Checksum'] = info['MetaData']['Checksum']
      if 'GUID' in info['MetaData']:
        lfns[lfn]['GUID'] = info['MetaData']['GUID']
      else:
        lfns[lfn]['GUID'] = makeGuid()
      lfns[lfn]['Mode'] = info['MetaData']['Mode']
      lfns[lfn]['PFN'] = ''
      owner = getUserNameAndGroup( info['MetaData'] )
      if owner:
        lfns[lfn]['Owner'] = owner

      if info['Replicas']:
        seList = info['Replicas'].keys()
        lfns[lfn]['SE'] = seList

    p_files = time.time() - s
    s = time.time()
    
    nFile = len(lfns)
    nRep = 0
    if nFile:

      for lfn in lfns:
        if 'SE' in lfns[lfn]:
          nRep += len(lfns[lfn]['SE'])

      print "Adding %d files in %s" % (nFile,initPath)
      #print lfns
      
      done = False
      count = 0
      error = False
      while not done:
        count += 1
        result = dfc.addFile(lfns)
        #print result
        if not result['OK']:
          print "Error adding files %d:" % count,result['Message']
          if count > 10:
            print "Completely failed path", initPath
            break
          error = True
          time.sleep(2)
        elif error:
          print "Successfully added files on retry %d" % count
          done = True
        else:
          done = True
        

      fileCount += nFile
      print "Total files added", fileCount


    e_files = time.time() - s

    dfc_time = time.time() - start - lfc_time
    total_time = time.time() - globalStart

    format = "== %s: time lfc/dfc %.2f/%.2f, files %d/%d, dirs %d/%d, time: %.2f/%.2f/%.2f/%.2f %.2f \n"
    outputFile = open('lfc_dfc.out','a')
    outputFile.write( format % (initPath,lfc_time,dfc_time,nFile,fileCount,nDir,dirCount,p_dirs,e_dirs,p_files,e_files,total_time) )
    outputFile.close()

#    print format % (initPath,lfc_time,dfc_time,nFile,fileCount,nDir,dirCount,p_dirs,e_dirs,p_files,e_files,total_time)

    # Go into directories
    if recursive:
      for path in paths:
        result = processDir(path,True,host=host,fcInit=fc,dfcInit=dfc)
        if result['OK']:
          nFile += result['Value'].get('NumberOfFiles',0)
          nDir += result['Value'].get('NumberOfDirectories',0)
          nRep += result['Value'].get('NumberOfReplicas',0)

    resultDict = {}
    resultDict['NumberOfFiles'] = nFile
    resultDict['NumberOfDirectories'] = nDir
    resultDict['NumberOfReplicas'] = nRep
    resultDict['Path'] = initPath
    return S_OK(resultDict)

def finalizeDirectory(task,result):

  if result['OK']:
    print "Finished directory %(Path)s, dirs: %(NumberOfDirectories)s, files: %(NumberOfFiles)s, replicas: %(NumberOfReplicas)s" % result['Value']
  else:
    print "Task failed: %s" % result['Message'] 

#########################################################################

argvs = sys.argv
if len(argvs) != 2 :
   print 'Usage: LFC_to_DFC.py [dirlist_file]'
   print '[dirlist_file] should contain the directory list.'
   quit()

dirlist_file=argvs[1]
if ( not os.path.exists(dirlist_file) ) :
  print dirlist_file+" does not exist"
  quit()

execfile(dirlist_file)

pPool = ProcessPool(10,50,50)
pPool.daemonize()

# dirlist = ['prod/ilc/mc-dbd/generated','prod/ilc/mc-dbd/ild']
# dirlist= ['prod/ilc/mc-dbd/generated/500-TDR_ws/higgs']
# dirlist= ['prod/ilc/mc-dbd/generated/250-TDR_ws/higgs','prod/ilc/mc-dbd/generated/350-TDR_ws/higgs']
#dirlist= ['prod/ilc/mc-dbd/generated/250-TDR_ws']
#dirlist= ['prod/ilc/mc-dbd/generated/250-TDR_ws/1f',
#          'prod/ilc/mc-dbd/generated/250-TDR_ws/3f',
#          'prod/ilc/mc-dbd/generated/250-TDR_ws/aa_lowpt',
#          'prod/ilc/mc-dbd/generated/250-TDR_ws/aa_minijet']
#dirlist= ['prod/ilc/mc-dbd/generated/250-TDR_ws/aa_2f',
#          'prod/ilc/mc-dbd/generated/350-TDR_ws/3f',
#          'prod/ilc/mc-dbd/generated/350-TDR_ws/1f',
#          'prod/ilc/mc-dbd/generated/350-TDR_ws/aa_minijet']

lfcHosts = ['grid-lfc.desy.de']

for dir in dirlist:
  path = "/ilc/%s" % (dir)
  print "Queueing user", dir, pPool.getFreeSlots(),pPool.getNumWorkingProcesses(),pPool.hasPendingTasks(),pPool.getNumIdleProcesses(), lfcHosts[0]
  result = pPool.createAndQueueTask( processDir,[path,True,lfcHosts[0]],callback=finalizeDirectory ) 
  if not result['OK']:
    print "Failed queueing", path

pPool.processAllResults()

print "LFC_to_DFC completed."


