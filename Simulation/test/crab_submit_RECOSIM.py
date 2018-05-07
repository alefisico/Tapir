from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'ttbbMC_generation_RAWSIM_1'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step1_RAWSIM_crab_cfg.py'
#config.JobType.numCores = 4
#config.JobType.maxMemoryMB = 3000

#config.Data.inputDataset = '/TTToSemilepton_NLOPS-powheg-pythia8/algomez-NewMCwithNLOPS-618ef6768e8b1a248ec0286524609aae/USER'
config.Data.inputDataset = '/TTToSemilepton_NLOPS-powheg-pythia8/algomez-NewMCwithNLOPS_LHESIM-618ef6768e8b1a248ec0286524609aae/USER'
config.Data.inputDBS = 'phys03'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
NJOBS = 4000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'NewMCwithNLOPS_RAWSIM_v0p1'

config.Site.storageSite = 'T2_CH_CSCS'
