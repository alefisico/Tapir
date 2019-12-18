#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'First argument, name of sample, is needed. Have a good day :)'
else

    sample=$1
    process=$2
    version=$3
    year=$4

    if [[ "$sample" == "simple" ]]; then
        listOfSamples="ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8 TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8 TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8"
    elif [[ "$sample" == "MC" ]]; then
        listOfSamples="ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8 TTToHadronic_TuneCP5_13TeV-powheg-pythia8 TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8 ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8 ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8 ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8 ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8 ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8 THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8 TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8 TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8 WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8 WW_TuneCP5_13TeV-pythia8 WZ_TuneCP5_13TeV-pythia8 ZZ_TuneCP5_13TeV-pythia8 QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8"
    elif [[ "$sample" == "Muon" ]]; then
        if [[ "$year" == "2017" ]]; then
            listOfSamples="SingleMuon_Run2017B SingleMuon_Run2017C SingleMuon_Run2017D SingleMuon_Run2017E SingleMuon_Run2017F"
        elif [[ "$year" == "2016" ]]; then
            listOfSamples="SingleMuon_Run2016Bv1 SingleMuon_Run2016Bv2 SingleMuon_Run2016C SingleMuon_Run2016D SingleMuon_Run2016E SingleMuon_Run2016F SingleMuon_Run2016G SingleMuon_Run2016H"
        else
            listOfSamples="SingleMuon_Run2018A SingleMuon_Run2018B SingleMuon_Run2018C SingleMuon_Run2018D"
        fi
    elif [[ "$sample" == "Electron" ]]; then
        if [[ "$year" == "2017" ]]; then
            listOfSamples="SingleElectron_Run2017B SingleElectron_Run2017C SingleElectron_Run2017D SingleElectron_Run2017E SingleElectron_Run2017F"
        elif [[ "$year" == "2016" ]]; then
            listOfSamples="SingleElectron_Run2016Bv1 SingleElectron_Run2016Bv2 SingleElectron_Run2016C SingleElectron_Run2016D SingleElectron_Run2016E SingleElectron_Run2016F SingleElectron_Run2016G SingleElectron_Run2016H"
        else
            listOfSamples="SingleElectron_Run2018A SingleElectron_Run2018B SingleElectron_Run2018C SingleElectron_Run2018D"
        fi
    else
        listOfSamples="${sample}"
    fi

    cat << EOF > condorlogs/samples.py
#!/usr/bin/python
import sys,os,time
import argparse, shutil
from dbs.apis.dbsClient import DbsApi
from computeGenWeights import dictSamples as allSamples
dbsPhys03 = DbsApi('https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader')
dbsglobal = DbsApi('https://cmsweb.cern.ch/dbs/prod/global/DBSReader')

usage = 'usage: %prog [options]'

parser = argparse.ArgumentParser()
parser.add_argument( '-d', '--dataset', action='store', dest='dataset', default='ttHTobb', help='Type of sample' )
parser.add_argument("-y", "--year", action='store', choices=[ '2016', '2017', '2018' ],  default="2017", help="Version" )
try: args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

##### Samples
allSamples['SingleMuon_Run2016Bv1']  = '/SingleMuon/Run2016B_ver1-Nano1June2019_ver1-v1/NANOAOD'
allSamples['SingleMuon_Run2016Bv2']  = '/SingleMuon/Run2016B_ver2-Nano1June2019_ver2-v1/NANOAOD'
allSamples['SingleMuon_Run2016C']  = '/SingleMuon/Run2016C-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2016D']  = '/SingleMuon/Run2016D-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2016E']  = '/SingleMuon/Run2016E-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2016F']  = '/SingleMuon/Run2016F-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2016G']  = '/SingleMuon/Run2016G-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2016H']  = '/SingleMuon/Run2016H-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2017B']  = '/SingleMuon/Run2017B-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2017C']  = '/SingleMuon/Run2017C-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2017D']  = '/SingleMuon/Run2017D-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2017E']  = '/SingleMuon/Run2017E-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2017F']  = '/SingleMuon/Run2017F-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2018A']  = '/SingleMuon/Run2018A-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2018B']  = '/SingleMuon/Run2018B-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2018C']  = '/SingleMuon/Run2018C-Nano1June2019-v1/NANOAOD'
allSamples['SingleMuon_Run2018D']  = '/SingleMuon/Run2018D-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2016Bv1']  = '/SingleElectron/Run2016B_ver1-Nano1June2019_ver1-v1/NANOAOD'
allSamples['SingleElectron_Run2016Bv2']  = '/SingleElectron/Run2016B_ver2-Nano1June2019_ver2-v1/NANOAOD'
allSamples['SingleElectron_Run2016C']  = '/SingleElectron/Run2016C-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2016D']  = '/SingleElectron/Run2016D-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2016E']  = '/SingleElectron/Run2016E-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2016F']  = '/SingleElectron/Run2016F-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2016G']  = '/SingleElectron/Run2016G-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2016H']  = '/SingleElectron/Run2016H-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2017B']  = '/SingleElectron/Run2017B-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2017C']  = '/SingleElectron/Run2017C-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2017D']  = '/SingleElectron/Run2017D-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2017E']  = '/SingleElectron/Run2017E-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2017F']  = '/SingleElectron/Run2017F-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2018A']  = '/EGamma/Run2018A-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2018B']  = '/EGamma/Run2018B-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2018C']  = '/EGamma/Run2018C-Nano1June2019-v1/NANOAOD'
allSamples['SingleElectron_Run2018D']  = '/EGamma/Run2018D-Nano1June2019-v1/NANOAOD'


## trick to run only in specific samples
dictSamples = {}
for sam in allSamples:
    if sam.startswith( args.dataset ) and sam.startswith('Single') and sam.split('Run')[1].startswith(args.year): dictSamples[ sam ] = allSamples[ sam ]
    elif sam.startswith( args.dataset ): dictSamples[ sam ] = allSamples[ sam ][ 0 if args.year.startswith('2016') else ( 1 if args.year.startswith('2017') else 2 ) ]
    #else: dictSamples = allSamples

print dictSamples
for sample, jsample in dictSamples.items():

    ##### Create a list from the dataset
    lfnList = []
    #for j in jsample:
    fileDictList = ( dbsPhys03 if jsample.endswith('USER') else dbsglobal).listFiles(dataset=jsample,validFileOnly=1)
    print "dataset %s has %d files" % (jsample, len(fileDictList))
    # DBS client returns a list of dictionaries, but we want a list of Logical File Names
    #lfnList = lfnList + [ 'root://cms-xrd-global.cern.ch/'+dic['logical_file_name'] for dic in fileDictList ]
    lfnList = lfnList + [ 'root://xrootd-cms.infn.it/'+dic['logical_file_name'] for dic in fileDictList ]

    textFile = open( 'condorlogs/'+sample+'.txt', 'w')
    textFile.write("\n".join(lfnList))

EOF

    for isample in $listOfSamples; do

        python condorlogs/samples.py -d ${isample} -y ${year}
        version=${version}_${year}

        condorFile=${isample}_${process}_${version}_condorJob
        echo '''myWD = '${PWD}'/condorlogs/
##logDir = /afs/cern.ch/user/a/algomez/work/tmp/
universe    =  vanilla
arguments   =  '${isample}' $(myfile) _$(ProcId)_'${version}'_'${process}'
executable  =  $(myWD)'${condorFile}'.sh
log         =  $(myWD)log_'${condorFile}'_$(ClusterId).log
error       =  $(myWD)log_'${condorFile}'_$(ClusterId)-$(ProcId).err
output      =  $(myWD)log_'${condorFile}'_$(ClusterId)-$(ProcId).out
initialdir  = $(myWD)
transfer_output_files = ""
###initialdir  = /eos/home-a/algomez/tmpFiles/'${isample}'/
getenv      =  True
###requirements = (OpSysAndVer =?= "SLCern6")
+JobFlavour = "testmatch"
queue myfile from $(myWD)'${isample}'.txt
''' > condorlogs/${condorFile}.sub
        ##cat condorlogs/${condorFile}.sub

        mkdir /eos/home-a/algomez/tmpFiles/${isample}/

        echo '''#!/bin/bash
export SCRAM_ARCH=slc6_amd64_gcc700
export X509_USER_PROXY=/afs/cern.ch/user/a/algomez/x509up_u15148
export EOS_MGM_URL=root://eosuser.cern.ch

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd '${CMSSW_BASE}'/src
eval `scramv1 runtime -sh`
env
cd -
echo ${PWD}
cp '${PWD}'/keep_and_drop.txt .
ls
echo "Running: python '${PWD}'/simpleAnalyzer.py --sample ${1} --iFile ${2} --oFile ${3} --process '${process}'"
python '${PWD}'/simpleAnalyzer.py --sample ${1} --iFile ${2} --oFile ${3} --process '${process}'
ls
cp histograms${3}.root /eos/home-a/algomez/tmpFiles/'${isample}'/
ls /eos/home-a/algomez/tmpFiles/'${isample}'/histograms${3}.root
xrdcopy -f histograms${3}.root root://eosuser.cern.ch//eos/user/a/algomez/tmpFiles/'${isample}'/histograms${3}.root
''' > condorlogs/${condorFile}.sh

        condor_submit condorlogs/${condorFile}.sub

    done

fi
