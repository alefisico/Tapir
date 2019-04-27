#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'First argument, name of sample, is needed. Have a good day :)'
else

    sample=$1

    condorFile=${sample}_condorJob
    echo '''
universe    =  vanilla
arguments   = '${sample}' $(myfile) $(ProcId)
executable  =  '${PWD}'/'${condorFile}'.sh
log         =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId).log
error       =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId)-$(ProcId).err
output      =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId)-$(ProcId).out
initialdir  =  '${PWD}'/
getenv      =  True
requirements = (OpSysAndVer =?= "SLCern6")
+JobFlavour = "tomorrow"
queue myfile from '${sample}'.txt

    ''' > ${condorFile}.sub

    echo '''#!/bin/bash
export SCRAM_ARCH=slc6_amd64_gcc700
export X509_USER_PROXY=/afs/cern.ch/user/a/algomez/x509up_u15148

cd '${CMSSW_BASE}'/src
eval `scramv1 runtime -sh`

echo ${1} ${2} ${3}
cd -
echo "Running: python '${PWD}'/makeNumpyarrays.py -s -d ${1} -i ${2} -o ${3}"
python '${PWD}'/makeNumpyarrays.py -s -d ${1} -i ${2} -o ${3}

ls -l

gfal-copy -E /afs/cern.ch/user/a/algomez/x509up_u15148 --parent '${sample}'_${3}.npy gsiftp://t3se01.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/algomez/ttH/training/'${sample}'/
#for ifile in `ls *npy`; do
#    gfal-copy -E /afs/cern.ch/user/a/algomez/x509up_u15148 --parent --force ${ifile} gsiftp://t3se01.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/algomez/ttH/training/'${sample}'/
#done
#rm *npy
    ''' > ${condorFile}.sh

    condor_submit ${condorFile}.sub

fi
