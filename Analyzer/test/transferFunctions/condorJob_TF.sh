#!/bin/bash
export SCRAM_ARCH=slc6_amd64_gcc700
export X509_USER_PROXY=/afs/cern.ch/user/a/algomez/x509up_u15148

cd ${CMSSW_BASE}/src/TTH/Analyzer/test/transferFunctions/
eval `scramv1 runtime -sh`
echo ${PWD}
time python ${CMSSW_BASE}/src/TTH/Analyzer/test/transferFunctions/config.py -d ${1}

time python ${CMSSW_BASE}/src/TTH/Analyzer/test/transferFunctions/TFmain.py ${1}
