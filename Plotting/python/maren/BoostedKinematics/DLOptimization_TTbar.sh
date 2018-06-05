#!/bin/bash

source common.sh


#go to work directory
cd $GC_SCRATCH

echo "Starting"
echo "-------------------------------------------------------"
echo $FILE_NAMES
python ${CMSSW_BASE}/src/TTH/Plotting/python/maren/DLOptimization_TTbar.py $FILE_NAMES 

echo "done script"
echo "pwd"
pwd
echo "ls"
ls -lactrh
