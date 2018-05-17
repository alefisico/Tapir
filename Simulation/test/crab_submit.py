from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'semileptonicttbbMC_generation_LHE'

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'step0_LHESIM_crab_cfg.py'
config.JobType.inputFiles = [ 'file:/scratch/algomez/Archive/ttH/NLOPS_ttb/semiLeptonicttbar_sample0005/semileptonicttbar_NLOPS.lhe', ]

config.Data.outputPrimaryDataset = 'TTTo2L2Nu_NLOPS-powheg-pythia8'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 500
NJOBS = 1000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True
config.Data.outputDatasetTag = 'NewMCwithNLOPS_LHESIM'

config.Site.storageSite = 'T2_CH_CSCS'
