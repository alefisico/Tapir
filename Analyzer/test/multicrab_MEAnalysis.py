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

    BASH_SCRIPT = '''
echo "ENV..................................."
env
echo "VOMS"
voms-proxy-info -all
echo "CMSSW BASE, python path, pwd"
echo $CMSSW_BASE
echo $PYTHON_PATH
echo $PWD
cd $CMSSW_BASE/src/TTH/MEAnalysis/test/
eval `scramv1 runtime -sh`

echo Found Proxy in: $X509_USER_PROXY
echo "python simpleJob_MEAnalysis.py ......."
python simpleJob_MEAnalysis.py --sample {datasets}
mv Loop_{datasets}/tree.root tree.root
    '''
    open('runMEAnalysis.sh', 'w').write(BASH_SCRIPT.format(**options.__dict__))

def createPSet():

    PYTHON_SCRIPT = '''import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring([
            'root://cms-xrd-global.cern.ch//store/user/algomez/ttH/nanoAOD_postProc/CRAB_UserFiles/tthbb13_nanoPostProc_nanoAOD_simpleJobs_ttH2018_102X__102X_v00/190224_220957/0000/nano_postprocessed_123.root'
            ]),
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('tree.root'),
    #fakeNameForCrab = cms.untracked.bool(True),
)

process.out = cms.EndPath(process.output)
    '''
    open('PSet.py', 'w').write(PYTHON_SCRIPT)


def submitJobs( job, lnfList, unitJobs ):


    from WMCore.Configuration import Configuration
    config = Configuration()

    from CRABAPI.RawCommand import crabCommand
    from httplib import HTTPException

    config.section_("General")
    config.General.workArea = options.dir
    config.General.transferLogs = True

    config.section_("JobType")
    config.JobType.pluginName = 'Analysis'
    config.JobType.psetName = 'PSet.py'

    config.section_("Data")
    config.Data.ignoreLocality = False
    #config.Data.publication = True
    #config.Data.publishDBS = 'phys03'

    config.section_("Site")
    config.Site.storageSite = options.storageSite
    #config.Site.whitelist = ['T2_US_*']
    #config.Site.whitelist = ['T2_US_Nebraska','T2_CH_CSCS','T3_US_UMD','T2_US_Caltech','T2_US_MIT']
    #config.Site.blacklist = ['T2_US_Florida','T3_TW_*','T2_BR_*','T2_GR_Ioannina','T2_BR_SPRACE','T2_RU_IHEP','T2_PL_Swierk','T2_KR_KNU','T3_TW_NTU_HEP']


    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException, hte:
            print 'Cannot execute command'
            print hte.headers


    requestname = 'tthbb13_MEAnalysis_'+ options.datasets + '_' +options.version
    print requestname
    config.JobType.scriptExe = 'runMEAnalysis.sh'
    config.JobType.inputFiles = [ 'PSet.py','runMEAnalysis.sh', 'simpleJob_MEAnalysis.py', 'simpleJob_config.cfg']
    #config.JobType.sendPythonFolder  = True

    if options.textFile:
        config.Data.userInputFiles = lfnList
        config.Data.splitting = 'FileBased'
        config.Data.outputPrimaryDataset = job
    else:
        config.Data.inputDBS = 'phys03'
        config.Data.inputDataset = lfnList ### it is the dataset name
        config.Data.splitting = 'FileBased'
        config.Data.unitsPerJob = unitJobs

    config.Data.publication = False #True
    config.JobType.outputFiles = [ 'tree.root']
    config.Data.outLFNDirBase = '/store/user/'+os.environ['USER']+'/ttH/MEAnalysis/'

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

    (options, args) = parser.parse_args()

    dictSamples = {}
    if not options.textFile:
        #dictSamples['SingleMuon_Run2018B'] = ['/SingleMuon/algomez-tthbb13_PostProc_SingleMuon_Run2018B_v01-0cddb9e2402d2a936e94a815e9296873/USER', dbsglobal, 1 ]
        dictSamples['EGamma_Run2018B'] = ['/EGamma/algomez-tthbb13_PostProc_EGamma_Run2018B_v01-0cddb9e2402d2a936e94a815e9296873/USER', dbsglobal, 1 ]
        dictSamples['TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8'] = ['/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/algomez-tthbb13_PostProc_TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_v01-0607c559a339ced63de31d38b5efa1f6/USER', dbsglobal, 1 ]
        dictSamples['ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8'] = ['/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/algomez-tthbb13_PostProc_ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8_v01-82f9a1e3d3dcf76bf6a4a44034cf6840/USER', dbsglobal, 1 ]
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

        print ("dataset %s has %d files" % (processingSamples[isam], len(lfnList)))
        submitJobs( isam, lfnList, processingSamples[isam][2] )
