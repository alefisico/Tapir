#!/usr/bin/env python
"""
Multicrab script to submit several datasets at the time, for postProcessing with/wo MEAnalysis
"""
import os
from optparse import OptionParser
from dbs.apis.dbsClient import DbsApi  ## talk to DBS to get list of files in this dataset
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
echo "python simpleJob_nanoAODPostproc_MEAnalysis.py ......."
python simpleJob_nanoAODPostproc_MEAnalysis.py --sample {datasets} --config {config} --addMEAnalysis
mv Loop_*/tree.root tree.root
fi
    '''
    open('runPostProcMEAnalysis.sh', 'w').write(BASH_SCRIPT.format(**options.__dict__))     ### create file and replace arguments with {THIS}

##########################################
def createPSet():
    """docstring for createPSet: create the PSet.py file needed for postprocessing"""

    PYTHON_SCRIPT = '''import FWCore.ParameterSet.Config as cms

process = cms.Process("NANO")

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)

process.source.fileNames = [
            "root://cms-xrd-global.cern.ch//store/user/algomez/ttH/nanoAOD/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_simpleJobs_v00/190221_170126/0000/myNanoProdMc_NANO_38.root"
]

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('nano_postprocessed.root'),
    #fakeNameForCrab = cms.untracked.bool(True),
)
process.out = cms.EndPath(process.output)
    '''
    open('PSet.py', 'w').write(PYTHON_SCRIPT)


##########################################
def submitJobs( job, lnfList, unitJobs ):
    """docstring for submitJobs: create the crab python config file"""


    from WMCore.Configuration import Configuration
    config = Configuration()

    from CRABAPI.RawCommand import crabCommand
    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.section_("General")
    config.General.workArea = options.dir
    #config.General.transferLogs = True
    config.General.transferOutputs = True

    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'PSet.py'
    config.JobType.maxJobRuntimeMin = 2750

    config.section_("Data")
    #config.Data.ignoreLocality = False
    #config.Data.publication = True
    #config.Data.publishDBS = 'phys03'

    config.section_("Site")
    config.Site.storageSite = options.storageSite
    #config.Site.whitelist = ['T2_US_Nebraska','T2_CH_CSCS','T3_US_UMD','T2_US_Caltech','T2_US_MIT']
    #config.Site.blacklist = ['T2_US_Florida','T3_TW_*','T2_BR_*','T2_GR_Ioannina','T2_BR_SPRACE','T2_RU_IHEP','T2_PL_Swierk','T2_KR_KNU','T3_TW_NTU_HEP']

    config.JobType.scriptExe = 'runPostProcMEAnalysis.sh'
    config.JobType.inputFiles = [ 'simpleJob_nanoAODPostproc_MEAnalysis.py', options.config, 'haddnano.py', 'keep_and_drop.txt']
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

    if options.addMEAnalysis: config.JobType.outputFiles = [ 'tree.root' ]
    config.Data.outLFNDirBase = '/store/user/'+os.environ['USER']+'/ttH/nanoPostMEAnalysis/' if options.addMEAnalysis else '/store/user/'+os.environ['USER']+'/ttH/nanoAODPostproc/'

    outputTag = 'tthbb13_PostProcMEAnalysis_withME' if options.addMEAnalysis else 'tthbb13_PostProc'
    requestname = job + '_' +outputTag + '_' + options.version
    print requestname
    if len(requestname) > 100: requestname = (requestname[:95-len(requestname)])
    print 'requestname = ', requestname
    config.General.requestName = requestname
    config.Data.outputDatasetTag = requestname
    #config.Data.outputDatasetTag = outputTag + "_" + options.version
    print 'Submitting ' + config.General.requestName + ', dataset = ' + job
    print 'Configuration :'
    print config
    try :
        crabCommand('submit', config = config)
        #crabCommand('submit', "--dryrun", config = config)
    except :
        print 'Not submitted.'


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
            '-c', '--config',
            dest="config", default='simpleJob_config.cfg',
            help=("Config file "),
            metavar="CONFIG")
    parser.add_option(
            '-a', '--addMEAnalysis',
            dest="addMEAnalysis", default=False,
            help=("Including MEAnalysis"),
            metavar="ADDMEANALYSIS")

    (options, args) = parser.parse_args()

    ### dictionary with datasets
    dictSamples = {}
    if not options.textFile:
        dictSamples['SingleMuon_Run2018A'] = ['/SingleMuon/Run2018A-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['SingleMuon_Run2018B'] = ['/SingleMuon/Run2018B-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['SingleMuon_Run2018C'] = ['/SingleMuon/Run2018C-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['SingleMuon_Run2018D'] = ['/SingleMuon/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['EGamma_Run2018A'] = ['/EGamma/Run2018A-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['EGamma_Run2018B'] = ['/EGamma/Run2018B-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['EGamma_Run2018C'] = ['/EGamma/Run2018C-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['EGamma_Run2018D'] = ['/EGamma/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['DoubleMuon_Run2018A'] = ['/DoubleMuon/Run2018A-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['DoubleMuon_Run2018B'] = ['/DoubleMuon/Run2018B-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['DoubleMuon_Run2018C'] = ['/DoubleMuon/Run2018C-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['DoubleMuon_Run2018D'] = ['/DoubleMuon/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['MuonEG_Run2018A'] = ['/MuonEG/Run2018A-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['MuonEG_Run2018B'] = ['/MuonEG/Run2018B-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['MuonEG_Run2018C'] = ['/MuonEG/Run2018C-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['MuonEG_Run2018D'] = ['/MuonEG/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD', dbsglobal, 1 ]
        dictSamples['TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8'] = ['/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAOD-102X_upgrade2018_realistic_v15-v1/NANOAODSIM', dbsglobal, 1 ]
        dictSamples['TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8'] = ['/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM', dbsglobal, 1 ]
        dictSamples['ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8'] = ['/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAOD-102X_upgrade2018_realistic_v15-v3/NANOAODSIM', dbsglobal, 1 ]

    else: dictSamples[options.datasets] = [ options.textFile ]

    ### Trick to copy only datasets specified
    processingSamples = {}
    if 'all' in options.datasets:
        for sam in dictSamples: processingSamples[ sam ] = dictSamples[ sam ]
    else:
        for sam in dictSamples:
            if sam.startswith( options.datasets ): processingSamples[ sam ] = dictSamples[ sam ]
    if len(processingSamples)==0: print 'No sample found. \n Have a nice day :)'

    ### Creating files needed and running submitJobs
    for isam in processingSamples:

        options.datasets = isam
        createBash()
        print('Creating bash file...')
        createPSet()
        print('Creating PSet file...')

        if options.textFile:
            rootLines = open( processingSamples[isam][0] ).readlines()
            lfnList = [ lfnList.append( str(iroot[:-1] ) ) for iroot in rootLines ]
        else:
            lfnList = processingSamples[isam][0]
        #    # DBS client returns a list of dictionaries, but we want a list of Logical File Names
        #    fileDictList = processingSamples[isam][1].listFiles( dataset=processingSamples[isam][0], validFileOnly=1 )
        #    lfnList = [ 'root://cms-xrd-global.cern.ch/'+dic['logical_file_name'] for dic in fileDictList ]

        print ("dataset %s has %d files" % (processingSamples[isam], len(lfnList)))
        submitJobs( isam, lfnList, processingSamples[isam][2] )
