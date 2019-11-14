import FWCore.ParameterSet.Config as cms

process = cms.Process("NANO")

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)

process.source.fileNames = [
            #"root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/102X_upgrade2018_realistic_v15-v1/40000/6801F357-BF95-2E41-BA2D-ABD083577275.root"
            #'root://xrootd-cms.infn.it//store/mc/RunIIFall17NanoAODv5/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/110000/4C93C46E-A48C-3344-BA8F-48D92CE4BAB3.root'
            #'root://xrootd-cms.infn.it//store/mc/RunIIFall17NanoAODv5/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_new_pmx_102X_mc2017_realistic_v7-v1/110000/F6A79C6E-E63D-4A4E-A611-473C6C5A99B8.root'
            #'root://xrootd-cms.infn.it//store/mc/RunIIFall17NanoAODv5/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano1June2019_102X_mc2017_realistic_v7-v1/120000/EB7998BC-1D8B-4545-BF96-857741C0B086.root',

#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02/190720_142525/0000/modifiedNanoAOD_MC_2017_115.root',

#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02p1/190723_080112/0000/modifiedNanoAOD_MC_2017_174.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02p1/190723_080112/0000/modifiedNanoAOD_MC_2017_112.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02p1/190723_080112/0000/modifiedNanoAOD_MC_2017_152.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02p1/190723_080112/0000/modifiedNanoAOD_MC_2017_35.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02p1/190723_080112/0000/modifiedNanoAOD_MC_2017_102.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02p1/190723_080112/0000/modifiedNanoAOD_MC_2017_142.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02p1/190723_080112/0000/modifiedNanoAOD_MC_2017_60.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02p1/190723_080112/0000/modifiedNanoAOD_MC_2017_45.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02p1/190723_080112/0000/modifiedNanoAOD_MC_2017_136.root',
            #'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02p1/190723_080112/0000/modifiedNanoAOD_MC_2017_61.root',
            #'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02p1/190723_080112/0000/modifiedNanoAOD_MC_2017_24.root',
            #'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02p1/190723_080112/0000/modifiedNanoAOD_MC_2017_123.root',

#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02/190720_142525/0000/modifiedNanoAOD_MC_2017_487.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02/190720_142525/0000/modifiedNanoAOD_MC_2017_4.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02/190720_142525/0000/modifiedNanoAOD_MC_2017_816.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02/190720_142525/0000/modifiedNanoAOD_MC_2017_501.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02/190720_142525/0000/modifiedNanoAOD_MC_2017_162.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02/190720_142525/0000/modifiedNanoAOD_MC_2017_156.root',
#            'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02/190720_142525/0000/modifiedNanoAOD_MC_2017_703.root',

	'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02/190901_212040/0000/modifiedNanoAOD_MC_2017_88.root',
	'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02/190901_212040/0000/modifiedNanoAOD_MC_2017_68.root',
	#'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02/190901_212040/0000/modifiedNanoAOD_MC_2017_59.root',
	#'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_v02/190901_212040/0000/modifiedNanoAOD_MC_2017_108.root',

#        'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/SingleMuon/Run2017B-31Mar2018-v1NANOAOD_v02/191010_145729/0000/modifiedNanoAOD_DATA_2017_177.root',
#        'root://xrootd-cms.infn.it//store/user/algomez/ttH/nanoAOD/SingleMuon/Run2017B-31Mar2018-v1NANOAOD_v02/191010_145729/0000/modifiedNanoAOD_DATA_2017_181.root'
]

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('nano_postprocessed.root'),
    #fakeNameForCrab = cms.untracked.bool(True),
)
process.out = cms.EndPath(process.output)

