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

usage = 'usage: %prog [options]'

parser = argparse.ArgumentParser()
parser.add_argument( '-d', '--dataset', action='store', dest='dataset', default='ttHTobb', help='Type of sample' )
try: args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

##### Samples
allSamples = {}
allSamples[ 'DoubleMuon' ] = [ '/DoubleMuon/algomez-DoubleMuon_Run2018A_tthbb13_PostProcMEAnalysis_withME_v03-0cddb9e2402d2a936e94a815e9296873/USER', '/DoubleMuon/algomez-DoubleMuon_Run2018B_tthbb13_PostProcMEAnalysis_withME_v03-0cddb9e2402d2a936e94a815e9296873/USER', '/DoubleMuon/algomez-DoubleMuon_Run2018C_tthbb13_PostProcMEAnalysis_withME_v03-0cddb9e2402d2a936e94a815e9296873/USER', '/DoubleMuon/algomez-DoubleMuon_Run2018D_tthbb13_PostProcMEAnalysis_withME_v03-8f87a7a44696406b0351f755f100b05c/USER' ]
allSamples[ 'EGamma' ] = [ '/EGamma/algomez-EGamma_Run2018A_tthbb13_PostProcMEAnalysis_withME_v03-0cddb9e2402d2a936e94a815e9296873/USER', '/EGamma/algomez-EGamma_Run2018B_tthbb13_PostProcMEAnalysis_withME_v03-0cddb9e2402d2a936e94a815e9296873/USER', '/EGamma/algomez-EGamma_Run2018C_tthbb13_PostProcMEAnalysis_withME_v03-0cddb9e2402d2a936e94a815e9296873/USER', '/EGamma/algomez-EGamma_Run2018D_tthbb13_PostProcMEAnalysis_withME_v03-8f87a7a44696406b0351f755f100b05c/USER' ]
allSamples[ 'MuonEG' ] = [ '/MuonEG/algomez-MuonEG_Run2018A_tthbb13_PostProcMEAnalysis_withME_v03-0cddb9e2402d2a936e94a815e9296873/USER', '/MuonEG/algomez-MuonEG_Run2018B_tthbb13_PostProcMEAnalysis_withME_v03-0cddb9e2402d2a936e94a815e9296873/USER', '/MuonEG/algomez-MuonEG_Run2018C_tthbb13_PostProcMEAnalysis_withME_v03-0cddb9e2402d2a936e94a815e9296873/USER','/MuonEG/algomez-MuonEG_Run2018D_tthbb13_PostProcMEAnalysis_withME_v03-8f87a7a44696406b0351f755f100b05c/USER' ]
allSamples[ 'SingleMuon' ] = [ '/SingleMuon/algomez-SingleMuon_Run2018A_tthbb13_PostProcMEAnalysis_withME_v03-0cddb9e2402d2a936e94a815e9296873/USER', '/SingleMuon/algomez-SingleMuon_Run2018B_tthbb13_PostProcMEAnalysis_withME_v03-0cddb9e2402d2a936e94a815e9296873/USER', '/SingleMuon/algomez-SingleMuon_Run2018C_tthbb13_PostProcMEAnalysis_withME_v03-0cddb9e2402d2a936e94a815e9296873/USER', '/SingleMuon/algomez-SingleMuon_Run2018D_tthbb13_PostProcMEAnalysis_withME_v03-8f87a7a44696406b0351f755f100b05c/USER' ]
allSamples[ 'TTTo2L2Nu' ] = [ '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/algomez-TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_tthbb13_PostProcMEAnalysis_withME_v03-1c5958aa15d63140fc83aaccef484714/USER' ]
allSamples[ 'TTToSemiLeptonic' ] = [ '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/algomez-TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_tthbb13_PostProcMEAnalysis_withME_v03-0607c559a339ced63de31d38b5efa1f6/USER' ]
allSamples[ 'ttHTobb_ttTo2L2Nu' ] = [ '/ttHTobb_ttTo2L2Nu_M125_TuneCP5_13TeV-powheg-pythia8/algomez-ttHTobb_ttTo2L2Nu_M125_TuneCP5_13TeV-powheg-pythia8_tthbb13_PostProcMEAnalysis_withME_v03-ddbc6e4800ee377f7f90aa90b506845b/USER' ]
allSamples[ 'ttHTobb_ttToSemiLep' ] = [ '/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/algomez-ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8_tthbb13_PostProcMEAnalysis_withME_v03-ddbc6e4800ee377f7f90aa90b506845b/USER' ]


## trick to run only in specific samples
dictSamples = {}
for sam in allSamples:
    if sam.startswith( args.dataset ): dictSamples[ sam ] = allSamples[ sam ]
    #else: dictSamples = allSamples

for sample, jsample in dictSamples.items():

    ##### Create a list from the dataset
    lfnList = []
    for j in jsample:
        fileDictList = dbsPhys03.listFiles(dataset=j,validFileOnly=1)
        print "dataset %s has %d files" % (j, len(fileDictList))
        # DBS client returns a list of dictionaries, but we want a list of Logical File Names
        lfnList = lfnList + [ 'root://cms-xrd-global.cern.ch/'+dic['logical_file_name'] for dic in fileDictList ]

    textFile = open( 'condorlogs/'+sample+'.txt', 'w')
    textFile.write("\n".join(lfnList))

EOF

    python condorlogs/samples.py -d ${sample}

    condorFile=${sample}_condorJob
    echo '''universe    =  vanilla
arguments   =  '${sample}' $(ProcId)_v02 $(myfile)
executable  =  '${PWD}'/condorlogs/'${condorFile}'.sh
log         =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId).log
error       =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId)-$(ProcId).err
output      =  '${PWD}'/condorlogs/log_'${condorFile}'_$(ClusterId)-$(ProcId).out
initialdir  =  '${PWD}'/Rootfiles/
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
echo "Running: python '${PWD}'/createHistograms.py -d ${1} -v ${2} -s -i ${3}"
time python '${PWD}'/evenSimpler_createHistograms.py -d ${1} -v ${2} -s -i ${3}
ls
    ''' > condorlogs/${condorFile}.sh

    condor_submit condorlogs/${condorFile}.sub

fi
