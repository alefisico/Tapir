#!/usr/bin/env python
"""
This is a small script that submits a config over many datasets
"""
import os
from optparse import OptionParser
from dbs.apis.dbsClient import DbsApi  ## talk to DBS to get list of files in this dataset
dbsphys03 = DbsApi('https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader')
dbsglobal = DbsApi('https://cmsweb.cern.ch/dbs/prod/global/DBSReader')

def make_list(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

def createBash():

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
echo "python simpleJob_nanoAODPostproc.py ......."
python simpleJob_nanoAODPostproc.py --sample {datasets}
fi
    '''
    open('runPostProc.sh', 'w').write(BASH_SCRIPT.format(**options.__dict__))

def createPSet():

    PYTHON_SCRIPT = '''import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring([
            "root://cms-xrd-global.cern.ch//store/user/algomez/ttH/nanoAOD/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_simpleJobs_v00/190221_170126/0000/myNanoProdMc_NANO_38.root"
            ]),
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('nano_postprocessed.root'),
    fakeNameForCrab = cms.untracked.bool(True),
)

process.out = cms.EndPath(process.output)
    '''
    open('PSet.py', 'w').write(PYTHON_SCRIPT)

def submitJobs( job, lnfList, unitJobs ):


    from WMCore.Configuration import Configuration
    config = Configuration()

    from CRABAPI.RawCommand import crabCommand
    from httplib import HTTPException


    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.                                                        =
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.section_("General")
    config.General.workArea = options.dir
    config.General.transferLogs = False
    config.General.transferOutputs = True

    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'PSet.py'

    config.section_("Data")
    config.Data.publication = True
    config.Data.publishDBS = 'phys03'
    config.Data.inputDBS = 'phys03'

    config.section_("Site")
    config.Site.storageSite = options.storageSite
    #config.Site.whitelist = ['T2_US_Nebraska','T2_CH_CSCS','T3_US_UMD','T2_US_Caltech','T2_US_MIT']
    #config.Site.blacklist = ['T2_US_Florida','T3_TW_*','T2_BR_*','T2_GR_Ioannina','T2_BR_SPRACE','T2_RU_IHEP','T2_PL_Swierk','T2_KR_KNU','T3_TW_NTU_HEP']


    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException, hte:
            print 'Cannot execute command'
            print hte.headers


    requestname = 'tthbb13_PostProc_'+ job + '_' +options.version
    print requestname
    config.JobType.scriptExe = 'runPostProc.sh'
    config.JobType.inputFiles = [ 'PSet.py','runPostProc.sh', 'simpleJob_nanoAODPostproc.py' ,'../haddnano.py', 'keep_and_drop.txt']
    config.JobType.sendPythonFolder  = True

    # following 3 lines are the trick to skip DBS data lookup in CRAB Server
    if options.textFile:
        config.Data.userInputFiles = lfnList
        config.Data.splitting = 'FileBased'
        config.Data.outputPrimaryDataset = job
    else:
        config.Data.inputDataset = lfnList ### it is the dataset name
        #config.Data.splitting = 'EventAwareLumiBased'
        config.Data.splitting = 'FileBased'
        config.Data.unitsPerJob = unitJobs
        #config.Data.ignoreLocality = True
        #config.Site.whitelist = ['T2_CH_CSCS']
        #config.Data.splitting = 'Automatic'
        #config.Data.unitsPerJob = 480

    # since the input will have no metadata information, output can not be put in DBS
    config.JobType.outputFiles = [ 'nano_postprocessed.root']
    config.Data.outLFNDirBase = '/store/user/'+os.environ['USER']+'/ttH/nanoAODPostproc/'

    if len(requestname) > 100: requestname = (requestname[:95-len(requestname)])
    print 'requestname = ', requestname
    config.General.requestName = requestname
    config.Data.outputDatasetTag = requestname
    print 'Submitting ' + config.General.requestName + ', dataset = ' + job
    print 'Configuration :'
    print config
    try :
        from multiprocessing import Process

        p = Process(target=submit, args=(config,))
        p.start()
        p.join()
        #submit(config)
    except :
        print 'Not submitted.'



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
            dest="storageSite", default="T2_CH_CSCS",
            help=("Storage Site"),
            metavar="SITE")
    parser.add_option(
            "-v", "--version",
            dest="version", default="102X_v00",
            help=("Version of output"),
            metavar="VER")


    (options, args) = parser.parse_args()


    dictSamples = {}
    if not options.textFile:
        #dictSamples['SingleMuon_Run2018A'] = ['/SingleMuon/Run2018A-Nano14Dec2018-v1/NANOAOD', dbsglobal, 7 ]  ###20000 ]
        dictSamples['SingleMuon_Run2018B'] = ['/SingleMuon/Run2018B-Nano14Dec2018-v1/NANOAOD', dbsglobal, 3 ] ## 20000 ]
        #dictSamples['SingleMuon_Run2018C'] = ['/SingleMuon/Run2018C-Nano14Dec2018-v1/NANOAOD', dbsglobal, 3 ]
        #dictSamples['SingleMuon_Run2018D'] = ['/SingleMuon/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD', dbsglobal, 15 ]
        #dictSamples['EGamma_Run2018A'] = ['/EGamma/Run2018A-Nano14Dec2018-v1/NANOAOD', dbsglobal, 7 ]
        dictSamples['EGamma_Run2018B'] = ['/EGamma/Run2018B-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        #dictSamples['EGamma_Run2018C'] = ['/EGamma/Run2018C-Nano14Dec2018-v1/NANOAOD', dbsglobal, 3 ]
        #dictSamples['EGamma_Run2018D'] = ['/EGamma/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD', dbsglobal, 15 ]
        #dictSamples['DoubleMuon_Run2018A'] = ['/DoubleMuon/Run2018A-Nano14Dec2018-v1/NANOAOD', dbsglobal, 7 ]
        dictSamples['DoubleMuon_Run2018B'] = ['/DoubleMuon/Run2018B-Nano14Dec2018-v1/NANOAOD', dbsglobal, 3 ]
        #dictSamples['DoubleMuon_Run2018C'] = ['/DoubleMuon/Run2018C-Nano14Dec2018-v1/NANOAOD', dbsglobal, 3 ]
        #dictSamples['DoubleMuon_Run2018D'] = ['/DoubleMuon/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD', dbsglobal, 15 ]
        #dictSamples['MuonEG_Run2018A'] = ['/MuonEG/Run2018A-Nano14Dec2018-v1/NANOAOD', dbsglobal, 7 ]
        dictSamples['MuonEG_Run2018B'] = ['/MuonEG/Run2018B-Nano14Dec2018-v1/NANOAOD', dbsglobal, 1 ]
        #dictSamples['MuonEG_Run2018C'] = ['/MuonEG/Run2018C-Nano14Dec2018-v1/NANOAOD', dbsglobal, 3 ]
        #dictSamples['MuonEG_Run2018D'] = ['/MuonEG/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD', dbsglobal, 15 ]
        dictSamples['TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8'] = ['/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM', dbsglobal, 1 ] #50000 ]
        #dictSamples['TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8'] = ['/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM', dbsglobal, 2 ]
        dictSamples['TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8'] = ['/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/algomez-TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1-e05f95fef0725c09f3ec1f4a47bebd2d/USER', dbsglobal, 1 ]
        dictSamples['ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8'] = ['/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAOD-102X_upgrade2018_realistic_v15-v3/NANOAODSIM', dbsglobal, 3 ]
        dictSamples['ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8'] = ['/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM', dbsglobal, 2 ]
    else: dictSamples[options.datasets] = [ options.textFile ]

    processingSamples = {}
    if 'all' in options.datasets:
        for sam in dictSamples: processingSamples[ sam ] = dictSamples[ sam ]
    else:
        for sam in dictSamples:
            if sam.startswith( options.datasets ): processingSamples[ sam ] = dictSamples[ sam ]

    if len(processingSamples)==0: print 'No sample found. \n Have a nice day :)'

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

        print ("dataset %s has %d files" % (processingSamples[isam], len(lfnList)))
        submitJobs( isam, lfnList, processingSamples[isam][2] )
