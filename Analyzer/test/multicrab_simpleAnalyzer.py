#!/usr/bin/env python
"""
Multicrab script to submit several datasets at the time, for postProcessing with/wo MEAnalysis
"""
import os
from os import listdir
from os.path import isfile, join
from optparse import OptionParser
from dbs.apis.dbsClient import DbsApi  ## talk to DBS to get list of files in this dataset
from datasets import dictSamples, checkDict
dbsphys03 = DbsApi('https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader')
dbsglobal = DbsApi('https://cmsweb.cern.ch/dbs/prod/global/DBSReader')


##########################################
def createBash():
    """docstring for createBash: create the sh file for crab"""

    BASH_SCRIPT = '''#this is not mean to be run locally
#
echo Check if TTY
if [ "`tty`" != "not a tty" ]; then
  echo "YOU SHOULD NOT RUN THIS IN INTERACTIVE, IT DELETES YOUR LOCAL FILES"
else

###ls -lR .
echo "ENV..................................."
env
echo "VOMS"
voms-proxy-info -all
echo "CMSSW BASE, python path, pwd"
echo $CMSSW_BASE
echo $PYTHON_PATH
echo $PWD
rm -rf $CMSSW_BASE/lib/
rm -rf $CMSSW_BASE/src/
rm -rf $CMSSW_BASE/module/
rm -rf $CMSSW_BASE/python/
mv lib $CMSSW_BASE/lib
mv src $CMSSW_BASE/src
mv python $CMSSW_BASE/python

echo Found Proxy in: $X509_USER_PROXY
echo "Running: python simpleAnalyzer.py --sample {datasets} --process boosted"
python simpleAnalyzer.py --sample {datasets} --process boosted --year {year}
fi
    '''
    open('runPostProcSimplerJob_'+options.datasets+'.sh', 'w').write(BASH_SCRIPT.format(**options.__dict__))     ### create file and replace arguments with {THIS}

##########################################
def createPSet():
    """docstring for createPSet: create the PSet.py file needed for postprocessing"""

    PYTHON_SCRIPT = '''import FWCore.ParameterSet.Config as cms

process = cms.Process("NANO")

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)

process.source.fileNames = [
            "root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/102X_upgrade2018_realistic_v15-v1/40000/6801F357-BF95-2E41-BA2D-ABD083577275.root"
]

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('nano_postprocessed.root'),
    fakeNameForCrab = cms.untracked.bool(True),
)
process.out = cms.EndPath(process.output)
    '''
    open('PSet.py', 'w').write(PYTHON_SCRIPT)


##########################################
def submitJobs( job, lnfList, unitJobs ):
    """docstring for submitJobs: create the crab python config file"""

    from CRABAPI.RawCommand import crabCommand
    from WMCore.Configuration import Configuration
    config = Configuration()
    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.section_("General")
    config.General.workArea = options.dir
    #config.General.transferLogs = True
    #config.General.transferOutputs = True

    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'PSet.py'
    config.JobType.maxMemoryMB = 5000
    #config.JobType.maxJobRuntimeMin = 2750

    config.section_("Data")
    #config.Data.ignoreLocality = True
    #config.Data.publication = True
    #config.Data.publishDBS = 'phys03'

    config.section_("Site")
    config.Site.storageSite = options.storageSite
    #config.Site.storageSite = 'T2_CH_CERNBOX'
    #config.Site.whitelist = [ 'T2_CH_CSCS' ]
    #config.Site.blacklist = ['T2_US_Florida','T3_TW_*','T2_BR_*','T2_GR_Ioannina','T2_BR_SPRACE','T2_RU_IHEP','T2_PL_Swierk','T2_KR_KNU','T3_TW_NTU_HEP']

    config.JobType.scriptExe = 'runPostProcSimplerJob_'+options.datasets+'.sh'
    #rootfiles = ['../data/'+f for f in listdir('../data/') if isfile(join('../data/', f))]
    config.JobType.inputFiles = [ 'simpleAnalyzer.py', 'keep_and_drop.txt', 'haddnano.py'] #+ rootfiles
    config.JobType.sendPythonFolder  = True

    # following 3 lines are the trick to skip DBS data lookup in CRAB Server
    if options.textFile:
        config.Data.userInputFiles = lfnList
        config.Data.splitting = 'FileBased'
        config.Data.outputPrimaryDataset = job
    else:
        config.Data.inputDataset = lfnList ### it is the dataset name
        config.Data.splitting = 'FileBased'
        config.Data.unitsPerJob = unitJobs

    config.JobType.outputFiles = [ 'nano_postprocessed.root' ]#, 'histograms.root' ]
    config.Data.outLFNDirBase = '/store/user/'+os.environ['USER']+'/tmpFiles/ttH/'
    ##config.Data.inputDBS = 'phys03'

    outputTag = 'nanoAODPostProcessor'
    requestname = job + '_' +outputTag + '_' + options.year + '_' + options.version
    print requestname
    if len(requestname) > 100: requestname = (requestname[:95-len(requestname)])
    print 'requestname = ', requestname
    config.General.requestName = requestname
    config.Data.outputDatasetTag = requestname  #outputTag + '_' + options.version
    print 'Submitting ' + config.General.requestName + ', dataset = ' + job
    print 'Configuration :'
    print config
    crabCommand('submit', config = config)
#    try :
#        crabCommand('submit', config = config)
#        #crabCommand('submit', "--dryrun", config = config)
#    except :
#        print 'Not submitted.'


##########################################
if __name__ == '__main__':

    usage = ('usage: python submit_all.py -c CONFIG -d DIR -f DATASETS_FILE')

    parser = OptionParser(usage=usage)
    parser.add_option(
            "-D", "--dir",
            dest="dir", default="crab_projects",
            help=("The crab directory you want to use "),
            metavar="DIR" )
    parser.add_option(
            "-d", "--datasets",
            dest="datasets", default='all',
            help=("File listing datasets to run over"),
            metavar="FILE" )
    parser.add_option(
            "-t", "--textFile",
            dest="textFile", default='',
            help=("Text file containing root files"),
            metavar="TEXT")
    parser.add_option(
            "-s", "--storageSite",
            dest="storageSite", default="T3_CH_PSI",
            help=("Storage Site"),
            metavar="SITE")
    parser.add_option(
            "-v", "--version",
            dest="version", default="102X_v00",
            help=("Version of output"),
            metavar="VER")
    parser.add_option(
            "-y", "--year",
            dest="year", default="2016",
            help=("Year of dataset"),
            metavar="YEAR")

    (options, args) = parser.parse_args()

    ### dictionary with datasets
    processingSamples = {}
    if not options.textFile:
        allSamples = {}
        allSamples['SingleMuon_Run2016Bv1']  = '/SingleMuon/Run2016B_ver1-Nano25Oct2019_ver1-v1/NANOAOD'
        allSamples['SingleMuon_Run2016Bv2']  = '/SingleMuon/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD'
        allSamples['SingleMuon_Run2016C']  = '/SingleMuon/Run2016C-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2016D']  = '/SingleMuon/Run2016D-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2016E']  = '/SingleMuon/Run2016E-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2016F']  = '/SingleMuon/Run2016F-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2016G']  = '/SingleMuon/Run2016G-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2016H']  = '/SingleMuon/Run2016H-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2017B']  = '/SingleMuon/Run2017B-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2017C']  = '/SingleMuon/Run2017C-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2017D']  = '/SingleMuon/Run2017D-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2017E']  = '/SingleMuon/Run2017E-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2017F']  = '/SingleMuon/Run2017F-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2018A']  = '/SingleMuon/Run2018A-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2018B']  = '/SingleMuon/Run2018B-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2018C']  = '/SingleMuon/Run2018C-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleMuon_Run2018D']  = '/SingleMuon/Run2018D-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2016Bv1']  = '/SingleElectron/Run2016B_ver1-Nano25Oct2019_ver1-v1/NANOAOD'
        allSamples['SingleElectron_Run2016Bv2']  = '/SingleElectron/Run2016B_ver2-Nano25Oct2019_ver2-v1/NANOAOD'
        allSamples['SingleElectron_Run2016C']  = '/SingleElectron/Run2016C-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2016D']  = '/SingleElectron/Run2016D-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2016E']  = '/SingleElectron/Run2016E-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2016F']  = '/SingleElectron/Run2016F-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2016G']  = '/SingleElectron/Run2016G-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2016H']  = '/SingleElectron/Run2016H-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2017B']  = '/SingleElectron/Run2017B-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2017C']  = '/SingleElectron/Run2017C-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2017D']  = '/SingleElectron/Run2017D-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2017E']  = '/SingleElectron/Run2017E-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2017F']  = '/SingleElectron/Run2017F-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2018A']  = '/EGamma/Run2018A-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2018B']  = '/EGamma/Run2018B-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2018C']  = '/EGamma/Run2018C-Nano25Oct2019-v1/NANOAOD'
        allSamples['SingleElectron_Run2018D']  = '/EGamma/Run2018D-Nano25Oct2019-v1/NANOAOD'


        ## trick to run only in specific samples
        if options.datasets.startswith('Single'):
            for sam in allSamples:
                if sam.startswith( options.datasets ) and sam.startswith('Single') and sam.split('Run')[1].startswith(options.year): processingSamples[ sam ] = allSamples[ sam ]
        else:
            for sam in dictSamples:
                if 'all' in options.datasets:
                    for sam in dictSamples: processingSamples[ sam ] = checkDict( sam, dictSamples )[options.year][0]
                else:
                    for sam in dictSamples:
                        if sam.startswith( options.datasets ): processingSamples[ sam ] = checkDict( sam, dictSamples )[options.year][0]
                if len(processingSamples)==0: print 'No sample found. \n Have a nice day :)'

#        #dictSamples[ 'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8' ] = [ '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/NANOAODSIM' ]
#	dictSamples[ 'ttHTobb2016' ] =  [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM' ]
#	dictSamples[ 'ttHTobb2017' ] =  [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM' ]
#	dictSamples[ 'ttHTobb2018' ] =  ['/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM' ]
#	dictSamples[ 'ttHTobb2018ext' ] =  [ '/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_EXT_102X_upgrade2018_realistic_v21-v1/NANOAODSIM' ]
#	dictSamples[ 'THW2016' ] =  [ '/THW_ctcvcp_HIncl_M125_TuneCP5_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM'  ]
#	dictSamples[ 'THW2017' ] =  [ '/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM' ]
#	dictSamples[ 'THW2018' ] =  [ '/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM' ]

    else: processingSamples[options.datasets] = [ options.textFile ]


    ### Creating files needed and running submitJobs
    for isam in processingSamples:

        options.datasets = isam
        createBash()
        #print('Creating bash file...')
        #createPSet()
        print('Creating PSet file...')

        if options.textFile:
            rootLines = open( processingSamples[isam][0] ).readlines()
            lfnList = [ lfnList.append( str(iroot[:-1] ) ) for iroot in rootLines ]
        else:
            lfnList = processingSamples[isam]
        #    # DBS client returns a list of dictionaries, but we want a list of Logical File Names
        #    fileDictList = processingSamples[isam][1].listFiles( dataset=processingSamples[isam][0], validFileOnly=1 )
        #    lfnList = [ 'root://cms-xrd-global.cern.ch/'+dic['logical_file_name'] for dic in fileDictList ]

        print ("dataset %s has %d files" % (processingSamples[isam], len(lfnList)))
        submitJobs( isam, lfnList, 1  )
