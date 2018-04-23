import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = '94X_mc2017_realistic_v10'

process.TFileService=cms.Service("TFileService", fileName=cms.string('myQuickAnalysis.root'))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/mc/RunIIFall17MiniAOD/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/CC0FCC49-B50A-E811-9694-02163E0144C8.root'
    )
)


##########################################################
#### MUONS
process.selectedMuonsPt25 = cms.EDFilter("PATMuonSelector",
	src = cms.InputTag("slimmedMuons"),
	cut = cms.string('pt > 25. && abs(eta) < 2.1 && isGlobalMuon()'),
)
muonFilter = cms.EDFilter("CandCountFilter",
	src = cms.InputTag("selectedMuonsPt25"),
	minNumber = cms.uint32(2),
  )
##########################################################

##########################################################
#### ELECTRONS
process.selectedElectronsPt30 = cms.EDFilter("PATElectronSelector",
	src = cms.InputTag("slimmedElectrons"),
	cut = cms.string('pt > 30. && abs(eta) < 2.1'),
)
##########################################################

#from JMEAnalysis.JetToolbox.jetToolbox_cff import jetToolbox
#jetToolbox( process, 'ca15', 'jetSequence', 'out', PUMethod='CHS', JETCorrPayload="AK8PFchs", miniAOD=True, addPruning=True, Cut="pt > 150 && abs(eta) < 2.5" )
#
#
process.selectedPatJetsAK4 = cms.EDFilter("PATJetSelector",
		src = cms.InputTag("slimmedJets"),
		cut = cms.string("pt > 30 && abs(eta) < 2.5") )
		
process.selectedPatJetsAK8 = cms.EDFilter("PATJetSelector",
		src = cms.InputTag("slimmedJetsAK8"),
		cut = cms.string("pt > 200 && abs(eta) < 2.5") )

#process.analyzerAK8 = cms.EDAnalyzer('matchingAnalyzer',
#		AK8jets = cms.InputTag( "selectedPatJetsAK8" ),
#		AK4jets = cms.InputTag( "selectedPatJetsAK4" ),
#		genParticles = cms.InputTag( 'prunedGenParticles' ),
#		particle1 = cms.int32( 25 ),
#		particle2 = cms.int32( 6 ),
#		boostedDistance = cms.double( 0.6 ), 
#		groomedMass = cms.string( 'ak8PFJetsCHSValueMap:ak8PFJetsCHSPrunedMass' ),
#)

process.quickAnalyzer = cms.EDAnalyzer('quickAnalyzer',
		AK8jets = cms.InputTag( "selectedPatJetsAK8" ),
		AK4jets = cms.InputTag( "selectedPatJetsAK4" ),
		electrons = cms.InputTag( "selectedElectronsPt30" ),
		muons = cms.InputTag( "selectedMuonsPt25" ),
)


######## GenInfo
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleListDrawer",
		maxEventsToPrint = cms.untracked.int32(1),
		printVertex = cms.untracked.bool(False),
		src = cms.InputTag("prunedGenParticles")
		)



process.p = cms.Path(
	process.selectedMuonsPt25
	* process.selectedElectronsPt30
	* process.selectedPatJetsAK4
	* process.selectedPatJetsAK8
	#* process.analyzerAK8
	* process.quickAnalyzer
	#* process.printTree
)
#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
