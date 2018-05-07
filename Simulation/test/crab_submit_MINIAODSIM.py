from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'ttbbMC_generation_MINIAODSIM'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step3_MINIAODSIM_crab_cfg.py'

config.Data.inputDataset = '/TTToSemilepton_NLOPS-powheg-pythia8/algomez-NewMCwithNLOPS_AODSIM_v01-b1a4edca9adfa7a2e4059536bf605cd7/USER'
config.Data.inputDBS = 'phys03'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
NJOBS = 2000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'NewMCwithNLOPS_MINIAODSIM_v01'

config.Site.storageSite = 'T2_CH_CSCS'
