#!/bin/bash

if [[ $# -eq 0 ]] ; then
    echo 'First argument, name of sample, is needed. Have a good day :)'
else

    sample=$1
    process=$2
    version=$3

    if [[ "$sample" == "simple" ]]; then
        listOfSamples="ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8 TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8 TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8"
    elif [[ "$sample" == "MC" ]]; then
        listOfSamples="ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8 TTToHadronic_TuneCP5_13TeV-powheg-pythia8 TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8 ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8 ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8 ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8 ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8 ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8 THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8 TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8 TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8 WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8 WW_TuneCP5_13TeV-pythia8 WZ_TuneCP5_13TeV-pythia8 ZZ_TuneCP5_13TeV-pythia8 QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8"
    elif [[ "$sample" == "Muon" ]]; then
        listOfSamples="SingleMuon_Run2017B SingleMuon_Run2017C SingleMuon_Run2017D SingleMuon_Run2017E SingleMuon_Run2017F"
    elif [[ "$sample" == "Electron" ]]; then
        listOfSamples="SingleElectron_Run2017B SingleElectron_Run2017C SingleElectron_Run2017D SingleElectron_Run2017E SingleElectron_Run2017F"
    else
        listOfSamples="${sample}"
    fi

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
allSamples['SingleMuon_Run2017B'] = ['/SingleMuon/Run2017B-Nano1June2019-v1/NANOAOD' ]
allSamples['SingleMuon_Run2017C'] = ['/SingleMuon/Run2017C-Nano1June2019-v1/NANOAOD' ]
allSamples['SingleMuon_Run2017D'] = ['/SingleMuon/Run2017D-Nano1June2019-v1/NANOAOD' ]
allSamples['SingleMuon_Run2017E'] = ['/SingleMuon/Run2017E-Nano1June2019-v1/NANOAOD' ]
allSamples['SingleMuon_Run2017F'] = ['/SingleMuon/Run2017F-Nano1June2019-v1/NANOAOD' ]
allSamples['SingleElectron_Run2017B'] = ['/SingleElectron/Run2017B-Nano1June2019-v1/NANOAOD' ]
allSamples['SingleElectron_Run2017C'] = ['/SingleElectron/Run2017C-Nano1June2019-v1/NANOAOD' ]
allSamples['SingleElectron_Run2017D'] = ['/SingleElectron/Run2017D-Nano1June2019-v1/NANOAOD' ]
allSamples['SingleElectron_Run2017E'] = ['/SingleElectron/Run2017E-Nano1June2019-v1/NANOAOD' ]
allSamples['SingleElectron_Run2017F'] = ['/SingleElectron/Run2017F-Nano1June2019-v1/NANOAOD' ]
allSamples[ 'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8' ] = [ '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8' ] = [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8' ] = [ '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8' ] = [ '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'TTToHadronic_TuneCP5_13TeV-powheg-pythia8' ] = [ '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8' ] = [ '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8' ] = [ '/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8' ] = [ '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8' ] = [ '/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8' ] = [ '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8' ] = [ '/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8' ] = [ '/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8' ] = [ '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8' ] = [ '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8' ] = [ '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'WW_TuneCP5_13TeV-pythia8' ] = [ '/WW_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'WZ_TuneCP5_13TeV-pythia8' ] = [ '/WZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'ZZ_TuneCP5_13TeV-pythia8' ] = [ '/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
allSamples[ 'QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8' ] = [ '/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]

#allSamples['SingleMuon_Run2017B'] = ['/SingleMuon/algomez-Run2017B-31Mar2018-v1NANOAOD_v02-d53cb735e3282af22af454e27bbb6cf1/USER' ]
#allSamples['SingleMuon_Run2017C'] = [ '/SingleMuon/algomez-Run2017C-31Mar2018-v1NANOAOD_v02-d53cb735e3282af22af454e27bbb6cf1/USER' ]
#allSamples['SingleMuon_Run2017D'] = [ '/SingleMuon/algomez-Run2017D-31Mar2018-v1NANOAOD_v02-d53cb735e3282af22af454e27bbb6cf1/USER' ]
#allSamples['SingleMuon_Run2017E'] = [ '/SingleMuon/algomez-Run2017E-31Mar2018-v1NANOAOD_v02-d53cb735e3282af22af454e27bbb6cf1/USER' ]
#allSamples['SingleMuon_Run2017F'] = [ '/SingleMuon/algomez-Run2017F-31Mar2018-v1NANOAOD_v02-d53cb735e3282af22af454e27bbb6cf1/USER' ]
#allSamples['SingleElectron_Run2017B'] = [ '/SingleElectron/algomez-Run2017B-31Mar2018-v1NANOAOD_v02-d53cb735e3282af22af454e27bbb6cf1/USER' ]
#allSamples['SingleElectron_Run2017C'] = [ '/SingleElectron/algomez-Run2017C-31Mar2018-v1NANOAOD_v02-d53cb735e3282af22af454e27bbb6cf1/USER' ]
#allSamples['SingleElectron_Run2017D'] = [ '/SingleElectron/algomez-Run2017D-31Mar2018-v1NANOAOD_v02-d53cb735e3282af22af454e27bbb6cf1/USER' ]
#allSamples['SingleElectron_Run2017E'] = [ '/SingleElectron/algomez-Run2017E-31Mar2018-v1NANOAOD_v02-d53cb735e3282af22af454e27bbb6cf1/USER' ]
#allSamples['SingleElectron_Run2017F'] = [ '/SingleElectron/algomez-Run2017F-31Mar2018-v1NANOAOD_v02-d53cb735e3282af22af454e27bbb6cf1/USER' ]
#allSamples[ 'ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8' ] = [ '/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/algomez-NANOAOD_v02p1-3ea2ff745e1084ea23260bd2ac726434/USER' ]
#allSamples[ 'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8' ] = [ '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#allSamples[ 'ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8' ] = [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#allSamples[ 'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8' ] = [ '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/algomez-NANOAOD_v02-3ea2ff745e1084ea23260bd2ac726434/USER' ]
#allSamples[ 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8' ] = [ '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/algomez-NANOAOD_v02-3ea2ff745e1084ea23260bd2ac726434/USER' ]
#allSamples[ 'TTToHadronic_TuneCP5_13TeV-powheg-pythia8' ] = [ '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/algomez-NANOAOD_v02-3ea2ff745e1084ea23260bd2ac726434/USER' ]
#allSamples[ 'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8' ] = [ '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/algomez-NANOAOD_v02-3ea2ff745e1084ea23260bd2ac726434/USER' ]
#allSamples[ 'ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8' ] = [ '/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#allSamples[ 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8' ] = [ '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#allSamples[ 'ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8' ] = [ '/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#allSamples[ 'ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8' ] = [ '/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#allSamples[ 'THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8' ] = [ '/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#allSamples[ 'TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8' ] = [ '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#allSamples[ 'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8' ] = [ '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#allSamples[ 'WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8' ] = [ '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#allSamples[ 'WW_TuneCP5_13TeV-pythia8' ] = [ '/WW_TuneCP5_13TeV-pythia8/algomez-NANOAOD_v02-5157e087a222b5255c63dabe0cebaee6/USER' ]
#allSamples[ 'WZ_TuneCP5_13TeV-pythia8' ] = [ '/WZ_TuneCP5_13TeV-pythia8/algomez-NANOAOD_v02-5fb730f1ae83631a3be7a3e2c0ea6b8f/USER' ]
#allSamples[ 'ZZ_TuneCP5_13TeV-pythia8' ] = [ '/ZZ_TuneCP5_13TeV-pythia8/algomez-NANOAOD_v02-5fb730f1ae83631a3be7a3e2c0ea6b8f/USER' ]
#allSamples[ 'QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8' ] = [ '/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/algomez-NANOAOD_v02-5fb730f1ae83631a3be7a3e2c0ea6b8f/USER' ]
#allSamples[ '' ] = [ '' ]


## trick to run only in specific samples
dictSamples = {}
for sam in allSamples:
    if sam.startswith( args.dataset ): dictSamples[ sam ] = allSamples[ sam ]
    #else: dictSamples = allSamples

for sample, jsample in dictSamples.items():

    ##### Create a list from the dataset
    lfnList = []
    for j in jsample:
        fileDictList = ( dbsPhys03 if j.endswith('USER') else dbsglobal).listFiles(dataset=j,validFileOnly=1)
        print "dataset %s has %d files" % (j, len(fileDictList))
        # DBS client returns a list of dictionaries, but we want a list of Logical File Names
        #lfnList = lfnList + [ 'root://cms-xrd-global.cern.ch/'+dic['logical_file_name'] for dic in fileDictList ]
        lfnList = lfnList + [ 'root://xrootd-cms.infn.it/'+dic['logical_file_name'] for dic in fileDictList ]

    textFile = open( 'condorlogs/'+sample+'.txt', 'w')
    textFile.write("\n".join(lfnList))

EOF

    for isample in $listOfSamples; do

        python condorlogs/samples.py -d ${isample}

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
