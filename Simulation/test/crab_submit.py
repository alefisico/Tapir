from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powhel_NLOPS-pythia8'

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'step0_LHESIM_crab_cfg.py'
#config.JobType.inputFiles = [ 'file:/scratch/algomez/Archive/ttH/NLOPS_ttb/semiLeptonicttbar_sample0005/semileptonicttbar_NLOPS.lhe', ]

config.Data.outputPrimaryDataset = 'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powhel_NLOPS-pythia8'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1000
NJOBS = 2980
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'RunIIFall17wmLHEGS-93X_mc2017_realistic_v3-v1_privateGENSIM'
#config.JobType.numCores = 8

config.Site.storageSite = 'T2_CH_CSCS'
config.Site.whitelist = ['T2_CH_CSCS']
