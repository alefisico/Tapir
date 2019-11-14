##################################################################
########   TO RUN THIS: python crab3_QCD.py
########   DO NOT DO: crab submit crab3_QCD.py
##################################################################

from CRABClient.UserUtilities import config
import argparse, sys
from httplib import HTTPException
from CRABAPI.RawCommand import crabCommand
from multiprocessing import Process
import glob

config = config()
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.maxMemoryMB = 3000 # Default is 2500 : Max I have used is 13000

config.Data.splitting = 'FileBased'
config.Data.publication = True
config.Data.unitsPerJob = 1
#config.Data.ignoreLocality = True

config.Site.storageSite = 'T2_CH_CSCS'
config.Data.outLFNDirBase = '/store/user/algomez/ttH/nanoAOD/'

def submit(config):
    try:
        if args.dryrun: crabCommand('submit', '--dryrun', config = config)
        else: crabCommand('submit', config = config)
    except HTTPException, hte:
        print 'Cannot execute commend'
        print hte.headers


#######################################################################################
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sample', action='store', default='all', dest='sample', help='Sample to process. Example: QCD, RPV, TTJets.' )
    parser.add_argument('-v', '--version', action='store', default='v01_20181022', dest='version', help='Version' )
    parser.add_argument('-d', '--dryrun', action='store_true', default=False, help='To run dryrun crab mode.' )

    try: args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    Samples = {}

    #Samples[ 'internal name of sample' ] = [ "DATASET name", job_splitting ]
    #Samples[ '2017_ttHTobb_ttToSemiLep' ] = [ "/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
    Samples[ '2017_TTToSemiLeptonic' ] = [ "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
    Samples[ '2017_TTTo2L2Nu' ] = [ "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
    Samples[ '2017_TTToHadronic' ] = [ "/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM", 1 ]
    Samples[ '2017_TTZToQQ' ] = [ "/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM", 1 ]
    Samples[ '2017_ttHTobb' ] = [ "/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
    Samples[ '2017_ttHNonbb' ] = [ "/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM", 1 ]
    Samples[ '2017_ST_s-channel' ] = [ "/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
    Samples[ '2017_ST_t-channel_top' ] = [ "/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
    Samples[ '2017_ST_t-channel_antitop' ] = [ "/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM", 1 ]
    Samples[ '2017_ST_tW_top' ] = [ "/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
    Samples[ '2017_ST_tW_antitop' ] = [ "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM", 1 ]
    Samples[ '2017_WJetsToLNu' ] = [ "/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM", 1 ]
    Samples[ '2017_WW' ] = [ "/WW_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
    Samples[ '2017_WZ' ] = [ "/WZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
    Samples[ '2017_ZZ' ] = [ "/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM", 1 ]
    Samples[ '2017_QCD' ] = [ "/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
    Samples[ '2017_TTWJetsToQQ' ] = [ "/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM", 1 ]
    Samples[ '2017_TTGJets' ] = [ "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
    Samples[ '2017_THW' ] = [ "/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
    Samples[ '2017_SingleMuonB' ] = [ "/SingleMuon/Run2017B-31Mar2018-v1/MINIAOD", 1 ]
    Samples[ '2017_SingleMuonC' ] = [ "/SingleMuon/Run2017C-31Mar2018-v1/MINIAOD", 1 ]
    Samples[ '2017_SingleMuonD' ] = [ "/SingleMuon/Run2017D-31Mar2018-v1/MINIAOD", 1 ]
    Samples[ '2017_SingleMuonE' ] = [ "/SingleMuon/Run2017E-31Mar2018-v1/MINIAOD", 1 ]
    Samples[ '2017_SingleMuonF' ] = [ "/SingleMuon/Run2017F-31Mar2018-v1/MINIAOD", 1 ]
    Samples[ '2017_SingleElectronB' ] = [ "/SingleElectron/Run2017B-31Mar2018-v1/MINIAOD", 1 ]
    Samples[ '2017_SingleElectronC' ] = [ "/SingleElectron/Run2017C-31Mar2018-v1/MINIAOD", 1 ]
    Samples[ '2017_SingleElectronD' ] = [ "/SingleElectron/Run2017D-31Mar2018-v1/MINIAOD", 1 ]
    Samples[ '2017_SingleElectronE' ] = [ "/SingleElectron/Run2017E-31Mar2018-v1/MINIAOD", 1 ]
    Samples[ '2017_SingleElectronF' ] = [ "/SingleElectron/Run2017F-31Mar2018-v1/MINIAOD", 1 ]
    #Samples[ 'empty' ] = [ "", 1 ]


    processingSamples = {}
    if 'all' in args.sample:
        for sam in Samples: processingSamples[ sam ] = Samples[ sam ]
    else:
        for sam in Samples:
            if sam.startswith( args.sample ): processingSamples[ sam ] = Samples[ sam ]

    if len(processingSamples)==0: print 'No sample found. \n Have a nice day :)'

    for sam in processingSamples:

        dataset = processingSamples[sam][0]
        procName = dataset.split('/')[1].split('-')[0] if dataset.endswith('SIM') else dataset.split('/')[1]+'_'+dataset.split('/')[2]
        config.Data.inputDataset = dataset
        config.Data.unitsPerJob = 1 #processingSamples[sam][1]
        config.Data.outputDatasetTag = 'NANOAOD_'+args.version if dataset.endswith('SIM') else dataset.split('/')[2]+'NANOAOD_'+args.version
        config.JobType.psetName = 'modifiedNanoAOD_MC_2017_cfi.py' if dataset.endswith('SIM') else 'modifiedNanoAOD_DATA_2017_cfi.py'
        config.General.requestName = procName+'_NANOAOD'+args.version
        print config
        print '|--- Submmiting sample: ', procName
        p = Process(target=submit, args=(config,))
        p.start()
        p.join()
