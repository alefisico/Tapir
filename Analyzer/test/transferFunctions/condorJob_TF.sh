#!/bin/bash
export SCRAM_ARCH=slc6_amd64_gcc700
export X509_USER_PROXY=/afs/cern.ch/user/a/algomez/x509up_u15148

cd /afs/cern.ch/work/a/algomez/ttH/CMSSW_10_2_12/src/TTH/Analyzer/test/transferFunctions/
eval `scramv1 runtime -sh`
echo ${PWD}
time python /afs/cern.ch/user/a/algomez/workingArea/ttH/CMSSW_10_2_12/src/TTH/Analyzer/test/transferFunctions/config.py -d ${1}

time python /afs/cern.ch/user/a/algomez/workingArea/ttH/CMSSW_10_2_12/src/TTH/Analyzer/test/transferFunctions/TFmain.py ${1}
