#!/bin/bash

source common.sh


#go to work directory
cd $GC_SCRATCH

echo "Starting"

python ${CMSSW_BASE}/src/TTH/Plotting/python/maren/BasicTaggerStudies.py $FILE_NAMES 

echo "done script"
echo "pwd"
pwd
echo "ls"
ls -lactrh