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

echo Found Proxy in: $X509_USER_PROXY
echo "python simpleJob_nanoAOD_postproc_withME_cfg.py ......."
python simpleJob_nanoAOD_postproc_withME_cfg.py --sample {datasets} --config {config}
mv Loop_{datasets}/tree.root tree.root
fi
    '''
    open('runPostProcMEAnalysis.sh', 'w').write(BASH_SCRIPT.format(**options.__dict__))

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
    fileName = cms.untracked.string('tree.root'),
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

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.section_("General")
    config.General.workArea = options.dir
    config.General.transferLogs = True

    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'PSet.py'

    config.section_("Data")
    config.Data.inputDataset = None
    config.Data.splitting = ''
    config.Data.unitsPerJob = 1
    config.Data.ignoreLocality = False
    config.Data.publication = True
    config.Data.publishDBS = 'phys03'

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


    requestname = 'tthbb13_PostProcMEAnalysis_withME_'+ job + '_' +options.version
    print requestname
    config.JobType.scriptExe = 'runPostProcMEAnalysis.sh'
    config.JobType.inputFiles = [ 'PSet.py','runPostProcMEAnalysis.sh', 'simpleJob_nanoAOD_postproc_withME_cfg.py', options.config,'./haddnano.py', 'keep_and_drop.txt']
    config.JobType.sendPythonFolder  = True

    # following 3 lines are the trick to skip DBS data lookup in CRAB Server
    if options.textFile:
        config.Data.userInputFiles = lfnList
        config.Data.splitting = 'FileBased'
        config.Data.outputPrimaryDataset = job
    else:
        config.Data.inputDataset = lfnList ### it is the dataset name
        config.Data.splitting = 'EventAwareLumiBased'
        config.Data.unitsPerJob = unitJobs

    # since the input will have no metadata information, output can not be put in DBS
    config.Data.publication = True
    config.JobType.outputFiles = [ 'tree.root' ]
    config.Data.outLFNDirBase = '/store/user/'+os.environ['USER']+'/ttH/nanoPostMEAnalysis/'

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

    (options, args) = parser.parse_args()

    dictSamples = {}
    if not options.textFile:
        #dictSamples['SingleMuon_Run2018A'] = ['/SingleMuon/Run2018A-Nano14Dec2018-v1/NANOAOD', dbsglobal, 20000 ]
        dictSamples['SingleMuon_Run2018B'] = ['/SingleMuon/Run2018B-Nano14Dec2018-v1/NANOAOD', dbsglobal, 20000 ]
        #dictSamples['SingleMuon_Run2018C'] = ['/SingleMuon/Run2018C-Nano14Dec2018-v1/NANOAOD', dbsglobal, 20000 ]
        #dictSamples['SingleMuon_Run2018D'] = ['/SingleMuon/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD', dbsglobal, 20000 ]
        #dictSamples['EGamma_Run2018A'] = ['/EGamma/Run2018A-Nano14Dec2018-v1/NANOAOD', dbsglobal, 20000 ]
        dictSamples['EGamma_Run2018B'] = ['/EGamma/Run2018B-Nano14Dec2018-v1/NANOAOD', dbsglobal, 20000 ]
        #dictSamples['EGamma_Run2018C'] = ['/EGamma/Run2018C-Nano14Dec2018-v1/NANOAOD', dbsglobal, 20000 ]
        #dictSamples['EGamma_Run2018D'] = ['/EGamma/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD', dbsglobal, 20000 ]
        #dictSamples['DoubleMuon_Run2018A'] = ['/DoubleMuon/Run2018A-Nano14Dec2018-v1/NANOAOD', dbsglobal, 20000 ]
        #dictSamples['DoubleMuon_Run2018B'] = ['/DoubleMuon/Run2018B-Nano14Dec2018-v1/NANOAOD', dbsglobal, 20000 ]
        #dictSamples['DoubleMuon_Run2018C'] = ['/DoubleMuon/Run2018C-Nano14Dec2018-v1/NANOAOD', dbsglobal, 20000 ]
        #dictSamples['DoubleMuon_Run2018D'] = ['/DoubleMuon/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD', dbsglobal, 20000 ]
        #dictSamples['MuonEG_Run2018A'] = ['/MuonEG/Run2018A-Nano14Dec2018-v1/NANOAOD', dbsglobal, 20000 ]
        #dictSamples['MuonEG_Run2018B'] = ['/MuonEG/Run2018B-Nano14Dec2018-v1/NANOAOD', dbsglobal, 20000 ]
        #dictSamples['MuonEG_Run2018C'] = ['/MuonEG/Run2018C-Nano14Dec2018-v1/NANOAOD', dbsglobal, 20000 ]
        #dictSamples['MuonEG_Run2018D'] = ['/MuonEG/Run2018D-Nano14Dec2018_ver2-v1/NANOAOD', dbsglobal, 20000 ]
        dictSamples['TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8'] = ['/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAOD-102X_upgrade2018_realistic_v15-v1/NANOAODSIM', dbsglobal, 20000 ]
        dictSamples['ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8'] = ['/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAOD-102X_upgrade2018_realistic_v15-v3/NANOAODSIM', dbsglobal, 2000 ]

    else: dictSamples[options.datasets] = [ options.textFile ]

    processingSamples = {}
    if 'all' in options.datasets:
        for sam in dictSamples: processingSamples[ sam ] = dictSamples[ sam ]
    else:
        for sam in dictSamples:
            if sam.startswith( options.datasets ): processingSamples[ sam ] = dictSamples[ sam ]

    if len(processingSamples)==0: print 'No sample found. \n Have a nice day :)'

    for isam in processingSamples:

        if 'Run2018' in isam:
            options.datasets = isam.split('_')[0]
            isData = True
        else:
            options.datasets = isam
            isData = False
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
