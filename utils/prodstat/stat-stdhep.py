#!/usr/bin/env python 

import sys, os
from pprint import pprint

dbs={}
genid0='Index'
dbs[genid0]={'filename':'filename','nfiles':'nfiles'}
nread=0
maxread=1000000000

############################################################################
def scanfile(stdhep_list) :
  fr=open(stdhep_list,'r')
  nread=0
  for line in fr:
    nread=nread+1
#    print str(nread)+", "+str(maxread)
    if ( nread > maxread ) : 
       break
    files=line[:-1].split('/')
    if len(files) > 3 : 
      continue

    filename=files[2]
    filename=filename.replace('Gwhizard-1.95','Gwhizard-1_95')
    for n in range(0,10) :
      filename=filename.replace('.'+str(n),'.N'+str(n))

    fkeys=filename.split('.')
#     print files[2]
    genid='undef'
    for lk in fkeys:
#      print lk[0]
      if lk[0] == 'I' : 
         genid=lk[1:]

    if dbs.has_key(genid) :
      dbs[genid]['nfiles']=dbs[genid]['nfiles']+1
      dbs[genid]['filename']=files[2]
    else :
      dbs[genid]={}
      dbs[genid]['nfiles']=1
      dbs[genid]['filename']=files[2]

    for lk in fkeys:
      if not dbs[genid0].has_key(lk[0]) : 
        dbs[genid0][lk[0]]=lk[0]
      if lk != genid :
        value=lk[1:]
        if value == 'tdhep' :
          value = 'stdhep'
        dbs[genid][lk[0]]=value
   
  fr.close()  


# ============ Main routine =============================    
scanfile('stdheps/250-TDR_ws.list')
scanfile('stdheps/350-TDR_ws.list')
scanfile('stdheps/500-TDR_ws.list')
scanfile('stdheps/1000-B1b_ws.list')


print 'dbs length='+str(len(dbs))
print 'genid ',
for row in dbs[genid0].keys() :
  print str(row),
print ' '

for col in sorted(dbs.keys()) :
  if col == 'Index' : 
    continue
  print str(col),
  for row in dbs[genid0].keys() :
    if dbs[col].has_key(row) :
      print str(dbs[col][row]),
    else :
      print '*',
  print ' '

# pprint(dbs)

