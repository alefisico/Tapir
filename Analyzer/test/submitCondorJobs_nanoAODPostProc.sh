#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'First argument, name of sample, is needed. Have a good day :)'
else

    sample=$1

    cat << EOF > condorlogs/samples.py
#!/usr/bin/python
import sys,os,time
import argparse, shutil
from dbs.apis.dbsClient import DbsApi
dbsPhys03 = DbsApi('https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader')
dbsglobal = DbsApi('https://cmsweb.cern.ch/dbs/prod/global/DBSReader')

usage = 'usage: %prog [options]'

parser = argparse.ArgumentParser()
parser.add_argument( '-d', '--dataset', action='store', dest='dataset', default='ttHTobb', help='Type of sample' )
try: args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

##### Samples
allSamples = {}
allSamples['SingleMuon_Run2018A'] = ['/SingleMuon/Run2018A-Nano14Dec2018-v1/NANOAOD' ]
allSamples['SingleMuon_Run2018B'] = ['/SingleMuon/Run2018B-Nano14Dec2018-v1/NANOAOD' ]
allSamples['SingleMuon_Run2018C'] = ['/SingleMuon/Run2018C-Nano14Dec2018-v1/NANOAOD' ]
allSamples['SingleMuon_Run2018D'] = ['/SingleMuon/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD' ]
allSamples[ 'TTToSemiLeptonic' ] = [ '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM' ]


## trick to run only in specific samples
dictSamples = {}
for sam in allSamples:
    if sam.startswith( args.dataset ): dictSamples[ sam ] = allSamples[ sam ]
    #else: dictSamples = allSamples

for sample, jsample in dictSamples.items():

    ##### Create a list from the dataset
    lfnList = []
    for j in jsample:
        fileDictList = dbsglobal.listFiles(dataset=j,validFileOnly=1)
        print "dataset %s has %d files" % (j, len(fileDictList))
        # DBS client returns a list of dictionaries, but we want a list of Logical File Names
        lfnList = lfnList + [ 'root://cms-xrd-global.cern.ch/'+dic['logical_file_name'] for dic in fileDictList ]

    textFile = open( 'condorlogs/'+sample+'.txt', 'w')
    textFile.write("\n".join(lfnList))

EOF

    python condorlogs/samples.py -d ${sample}

    condorFile=${sample}_condorJob
    echo '''universe    =  vanilla
arguments   =  '${sample}' $(myfile) _$(ProcId)
executable  =  '${PWD}'/condorlogs/'${condorFile}'.sh
log         =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId).log
error       =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId)-$(ProcId).err
output      =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId)-$(ProcId).out
initialdir  = /eos/home-a/algomez/tmpFiles/
getenv      =  True
requirements = (OpSysAndVer =?= "SLCern6")
+JobFlavour = "workday"
queue myfile from '${PWD}'/condorlogs/'${sample}'.txt


    ''' > condorlogs/${condorFile}.sub


    echo '''#!/bin/bash
export SCRAM_ARCH=slc6_amd64_gcc700
export X509_USER_PROXY=/afs/cern.ch/user/a/algomez/x509up_u15148

cd '${CMSSW_BASE}'/src
eval `scramv1 runtime -sh`
env
cd -
echo ${PWD}
ls
echo "Running: python '${PWD}'/evenSimplerJob_nanoAODPostproc_TEST.py --sample ${1} --iFile ${2} --oFile ${3}"
python '${PWD}'/evenSimplerJob_nanoAODPostproc_TEST.py --sample ${1} --iFile ${2} --oFile ${3}
    ''' > condorlogs/${condorFile}.sh

    condor_submit condorlogs/${condorFile}.sub

fi
