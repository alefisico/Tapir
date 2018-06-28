#!/bin/bash

source common.sh


#go to work directory
cd $GC_SCRATCH

echo "Starting"

echo "using CMSSW946"

python ${CMSSW_BASE}/src/TTH/Plotting/python/maren/BoostedKinematics/CheckUnmatchedObjects.py $FILE_NAMES 

echo "done script"
echo "pwd"
pwd
echo "ls"
ls -lactrh