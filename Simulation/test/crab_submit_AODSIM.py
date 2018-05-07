from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'ttbbMC_generation_AODSIM'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step2_AODSIM_crab_cfg.py'
#config.JobType.numCores = 4
#config.JobType.maxMemoryMB = 3000

config.Data.inputDataset = '/TTToSemilepton_NLOPS-powheg-pythia8/algomez-NewMCwithNLOPS_RAWSIM-16ca0fac1b892ff3c3d45d801745cbbf/USER'
config.Data.inputDBS = 'phys03'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
NJOBS = 2000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'NewMCwithNLOPS_AODSIM_v01'

config.Site.storageSite = 'T2_CH_CSCS'
