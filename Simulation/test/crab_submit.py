from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'ttbbMC_generation_LHE'

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'step0_LHESIM_crab_cfg.py'
config.JobType.inputFiles = [
		'file:sample001.lhe',
		]

config.Data.outputPrimaryDataset = 'TTToSemilepton_NLOPS-powheg-pythia8'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 200
NJOBS = 1000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'NewMCwithNLOPS'

config.Site.storageSite = 'T2_CH_CSCS'
