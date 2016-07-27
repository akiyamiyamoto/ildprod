#!/bin/bash

hostname
ls /cvmfs/ilc.cern.ch
df
pwd
date

cat /proc/cpuinfo > cpuinfo.log

printenv 2>&1 > env.dat

