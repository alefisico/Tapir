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
echo "python runSkimmerTF.py ......."
python runSkimmerTF.py --sample {datasets}
fi
    '''
    open('runPostProcTF.sh', 'w').write(BASH_SCRIPT.format(**options.__dict__))     ### create file and replace arguments with {THIS}


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

    config.JobType.scriptExe = 'runPostProcTF.sh'
    config.JobType.inputFiles = [ 'runSkimmerTF.py', '../haddnano.py', '../keep_and_drop.txt']
    config.JobType.sendPythonFolder  = True

    # following 3 lines are the trick to skip DBS data lookup in CRAB Server
    config.Data.inputDataset = lfnList ### it is the dataset name
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = unitJobs

    #if options.addMEAnalysis: config.JobType.outputFiles = [ 'tree.root' ]
    config.JobType.outputFiles = [ 'nano_postprocessed.root' ]
    config.Data.outLFNDirBase = '/store/user/'+os.environ['USER']+'/ttH/nanoPostTransferFunctions/'

    outputTag = 'TF'
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

    ### dictionary with datasets
    dictSamples = {}
    dictSamples['2016_TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8'] = ['/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', dbsglobal, 1 ]
    dictSamples['2016_ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8'] = ['/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', dbsglobal, 1 ]

    dictSamples['2017_TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8'] = ['/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM', dbsglobal, 1 ]
    dictSamples['2017_ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8'] = ['/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv5-PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/NANOAODSIM', dbsglobal, 1 ]

    dictSamples['2018_TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8'] = ['/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM', dbsglobal, 1 ]
    dictSamples['2018_ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8'] = ['/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv5-Nano1June2019_102X_upgrade2018_realistic_v19-v1/NANOAODSIM', dbsglobal, 1 ]


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

        lfnList = processingSamples[isam][0]

        print ("dataset %s has %d files" % (processingSamples[isam], len(lfnList)))
        submitJobs( isam, lfnList, processingSamples[isam][2] )
