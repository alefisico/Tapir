from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powhel_NLOPS-pythia8_NANOAODSIM'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step4_NANOAOD_cfg.py'
#config.JobType.maxMemoryMB = 2500

config.Data.inputDataset = '/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powhel_NLOPS-pythia8/algomez-RunIIFall17wmLHEGS-93X_mc2017_realistic_v3-v1_privateMINIAODSIM-57e6cb033643cfa6c372ff41c8f6b812/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
NJOBS = 4000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'RunIIFall17wmLHEGS-93X_mc2017_realistic_v3-v1_privateNANOAODSIM'

config.Site.storageSite = 'T3_CH_PSI'
