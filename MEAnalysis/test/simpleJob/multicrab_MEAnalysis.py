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
#rm -rf $CMSSW_BASE/lib/
#rm -rf $CMSSW_BASE/src/
#rm -rf $CMSSW_BASE/module/
#rm -rf $CMSSW_BASE/python/
#mv lib $CMSSW_BASE/lib
#mv src $CMSSW_BASE/src
#echo "000000000000000000000000000000000000"
#ls $CMSSW_BASE/python
#mv python $CMSSW_BASE/python
cd $CMSSW_BASE/src/TTH/MEAnalysis/test/
eval `scramv1 runtime -sh`

echo Found Proxy in: $X509_USER_PROXY
echo "python simpleJob_MEAnalysis_heppy.py ......."
python simpleJob_MEAnalysis_heppy.py --sample {datasets}
mv Loop_{datasets}/tree.root tree.root
fi
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
    fakeNameForCrab = cms.untracked.bool(True),
)

process.out = cms.EndPath(process.output)
    '''
    open('PSet.py', 'w').write(PYTHON_SCRIPT)


def submitJobs( job, lnfList ):


    from WMCore.Configuration import Configuration
    config = Configuration()

    from CRABAPI.RawCommand import crabCommand
    from httplib import HTTPException


    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.                                                        =
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
    #config.Site.whitelist = ['T2_US_*']
    #config.Site.whitelist = ['T2_US_Nebraska','T2_CH_CSCS','T3_US_UMD','T2_US_Caltech','T2_US_MIT']
    #config.Site.blacklist = ['T2_US_Florida','T3_TW_*','T2_BR_*','T2_GR_Ioannina','T2_BR_SPRACE','T2_RU_IHEP','T2_PL_Swierk','T2_KR_KNU','T3_TW_NTU_HEP']


    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException, hte:
            print 'Cannot execute command'
            print hte.headers


    requestname = 'tthbb13_MEAnalysis_noME_'+ options.datasets + '_' +options.version
    print requestname
    config.JobType.scriptExe = 'runMEAnalysis.sh'
    config.JobType.inputFiles = [ 'PSet.py','runMEAnalysis.sh', 'simpleJob_MEAnalysis_heppy.py', 'simpleJob_config.cfg']
    config.JobType.sendPythonFolder  = True

    # following 3 lines are the trick to skip DBS data lookup in CRAB Server
    config.Data.userInputFiles = lfnList
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = 1

    #config.Data.inputDataset = job
    #config.Data.inputDBS = 'phys03'
    #config.Data.splitting = 'FileBased'
    #config.Data.unitsPerJob = 1
    #config.Data.splitting = 'Automatic'#'EventAwareLumiBased'
    #config.Data.unitsPerJob = 100
    #config.Data.totalUnits = 2000
    # since the input will have no metadata information, output can not be put in DBS
    config.Data.publication = False #True
    config.JobType.outputFiles = [ 'tree.root']
    config.Data.outLFNDirBase = '/store/user/algomez/ttH/MEAnalysis/'

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
    parser.add_option("-D", "--dir", dest="dir", default="crab_projects",
        help=("The crab directory you want to use "),
        metavar="DIR")
    parser.add_option("-d", "--datasets", dest="datasets", default='all',
        help=("File listing datasets to run over"),
        metavar="FILE")
    parser.add_option("-t", "--textFile", dest="textFile", default='nanoAOD_simpleJobs_ttH2018.txt',
        help=("Text file containing root files"),
        metavar="TEXT")
    parser.add_option("-s", "--storageSite", dest="storageSite", default="T3_CH_PSI",
        help=("Site"),
        metavar="SITE")
    parser.add_option("-v", "--version", dest="version", default="102X_v00",
        help=("Version of output"),
        metavar="VER")


    (options, args) = parser.parse_args()


    dictSamples = {}
    #dictSamples['SingleMuon2018'] = ['/SingleMuon/Run2018A-14Sep2018_ver3-v1/NANOAOD', dbsglobal]
    #dictSamples['TTSL'] = ['/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAOD-102X_upgrade2018_realistic_v15-v1/NANOAODSIM', dbsglobal]
    #dictSamples['ttHbb'] = ['/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAOD-102X_upgrade2018_realistic_v15-v3/NANOAODSIM', dbsglobal]
    dictSamples[options.datasets] = [ options.textFile ]

    processingSamples = {}
    if 'all' in options.datasets:
        for sam in dictSamples: processingSamples[ sam ] = dictSamples[ sam ]
    else:
        for sam in dictSamples:
            if sam.startswith( options.datasets ): processingSamples[ sam ] = dictSamples[ sam ]

    if len(processingSamples)==0: print 'No sample found. \n Have a nice day :)'

    createBash()
    print('Creating bash file...')
    createPSet()
    print('Creating PSet file...')

    for isam in processingSamples:

        #if 'text' in isam:
        rootLines = open( processingSamples[isam][0] ).readlines()
        lfnList = []
        for iroot in rootLines: lfnList.append( str(iroot[:-1] ) )
        processingSamples[isam][0] = processingSamples[isam][0].split(".txt")[0]
        #else:
        #    # DBS client returns a list of dictionaries, but we want a list of Logical File Names
        #    fileDictList = processingSamples[isam][1].listFiles( dataset=processingSamples[isam][0], validFileOnly=1 )
        #    lfnList = [ 'root://cms-xrd-global.cern.ch/'+dic['logical_file_name'] for dic in fileDictList ]

        #print ("dataset %s has %d files" % (processingSamples[isam][0], len(lfnList)))
        #submitJobs( processingSamples[isam][0], lfnList )
        print ("dataset %s has %d files" % (processingSamples[isam], len(lfnList)))
        submitJobs( isam, lfnList )