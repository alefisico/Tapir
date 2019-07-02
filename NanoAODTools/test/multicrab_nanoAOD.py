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
config.General.requestName = ''
config.General.workArea = 'crab_projects'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'modifiedNanoAOD_MC_2017_cfi.py'

config.Data.inputDataset = ''
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
	Samples[ '2017_ttHTobb_ttToSemiLep' ] = [ "/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
	Samples[ '2017_TTToSemiLeptonic' ] = [ "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", 1 ]
	#Samples[ '' ] = [ "", 1 ]
	#Samples[ '' ] = [ "", 1 ]
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
		procName = dataset.split('/')[1].split('-')[0]
		config.Data.inputDataset = dataset
		config.Data.unitsPerJob = processingSamples[sam][1]
        config.Data.outputDatasetTag = 'NANOAOD_'+args.version
        config.General.requestName = procName+'_NANOAODSIM'+args.version
        print config
        print '|--- Submmiting sample: ', procName
        p = Process(target=submit, args=(config,))
        p.start()
        p.join()
