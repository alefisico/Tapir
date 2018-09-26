from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powhel_NLOPS-pythia8_RAWSIM'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step1_RAWSIM_crab_cfg.py'
#config.JobType.numCores = 8
config.JobType.maxMemoryMB = 2500

config.Data.inputDataset = '/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powhel_NLOPS-pythia8/algomez-RunIIFall17wmLHEGS-93X_mc2017_realistic_v3-v1_privateGENSIM-cefcf785733ecf53c923c454a98ea705/USER'
config.Data.inputDBS = 'phys03'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1000
#config.Data.unitsPerJob = 1
NJOBS = 5000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'RunIIFall17wmLHEGS-93X_mc2017_realistic_v3-v1_privateRAWSIM'

config.Site.storageSite = 'T2_CH_CSCS'
config.Site.whitelist = ['T2_CH_CSCS', 'T2_US_Purdue', 'T2_CH_CERN', 'T2_US_Nebraska']
