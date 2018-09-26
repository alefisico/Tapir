from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powhel_NLOPS-pythia8_MINIAODSIM'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
#config.JobType.psetName = 'step3_MINIAODSIM_crab_cfg.py'
config.JobType.psetName = 'step23_MINIAODSIM_crab_cfg.py'
config.JobType.maxMemoryMB = 2500

config.Data.inputDataset = '/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powhel_NLOPS-pythia8/algomez-RunIIFall17wmLHEGS-93X_mc2017_realistic_v3-v1_privateRAWSIM-5b9cd2c7eef36524de7af1c8e43b0ebc/USER'
config.Data.inputDBS = 'phys03'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
NJOBS = 4000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'RunIIFall17wmLHEGS-93X_mc2017_realistic_v3-v1_privateMINIAODSIM'

config.Site.storageSite = 'T2_CH_CSCS'
