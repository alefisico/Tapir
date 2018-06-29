#!/bin/bash

source common.sh


#go to work directory
cd $GC_SCRATCH

echo "Starting"

echo "using CMSSW946"

python ${CMSSW_BASE}/src/TTH/Plotting/python/maren/BoostedKinematics/Higgs_CheckTaggerAK8.py $FILE_NAMES 

echo "done script"
echo "pwd"
pwd
echo "ls"
ls -lactrh