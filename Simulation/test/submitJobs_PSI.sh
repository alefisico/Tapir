#!/bin/bash

#######
#Set up environment
#######
#set +e
source /cvmfs/cms.cern.ch/cmsset_default.sh
#export SCRAM_ARCH=slc6_amd64_gcc530
#env

#######
#Set up CMSSW
#######
cd /shome/algomez/work/ttH/CMSSW_7_1_25/src/Tapir/Simulation/test/ #$PWD #this is the TMPDIR assigned by grid-control, lives in the right place on /scratch, auto-cleaned
#scramv1 project CMSSW CMSSW_8_0_5
#cd CMSSW_8_0_5/
eval `scramv1 runtime -sh`

#######
#Now run our code
#######


echo $FILE_NAMES, $MAX_EVENTS
edmConfigDump step0_LHESIM_cfg.py
cp step0_LHESIM_cfg.py $GC_SCRATCH 

cd $GC_SCRATCH
cmsRun step0_LHESIM_cfg.py
