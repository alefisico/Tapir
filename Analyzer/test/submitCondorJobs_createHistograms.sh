#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'First argument, name of sample, is needed. Have a good day :)'
else

    sample=$1

    condorFile=${sample}_condorJob
    echo '''universe    =  vanilla
arguments   =  '${sample}' $(ProcId)_v01 $(myfile)
executable  =  '${PWD}'/'${condorFile}'.sh
log         =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId).log
error       =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId)-$(ProcId).err
output      =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId)-$(ProcId).out
initialdir  =  '${PWD}'/Rootfiles/
getenv      =  True
requirements = (OpSysAndVer =?= "SLCern6")
+JobFlavour = "workday"
queue myfile from '${PWD}'/samples/'${sample}'.txt


    ''' > ${condorFile}.sub


    echo '''#!/bin/bash
export SCRAM_ARCH=slc6_amd64_gcc700
export X509_USER_PROXY=/afs/cern.ch/user/a/algomez/x509up_u15148

cd '${CMSSW_BASE}'/src
eval `scramv1 runtime -sh`
env
cd -
echo ${PWD}
ls
echo "Running: python '${PWD}'/createHistograms.py -d ${1} -v ${2} -s -i ${3}"
time python '${PWD}'/createHistograms.py -d ${1} -v ${2} -s -i ${3}
ls
    ''' > ${condorFile}.sh

    condor_submit ${condorFile}.sub

fi
