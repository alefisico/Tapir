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
process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v6'

process.TFileService=cms.Service("TFileService", fileName=cms.string('MCValidation_newMC.root'))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'/store/user/algomez/TTToSemilepton_NLOPS-powheg-pythia8/NewMCwithNLOPS_MINIAODSIM_v01/180506_173645/0000/HIG-RunIISummer16MiniAODv2-00059_986.root'
	'/store/mc/RunIISummer16MiniAODv2/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/32702552-3BC2-E611-AE02-001E67F336E0.root'
    )
)

##########################################################
#### MUONS
process.selectedPatMuons = cms.EDFilter("PATMuonSelector",
	src = cms.InputTag("slimmedMuons"),
	cut = cms.string('pt > 15. && abs(eta) < 2.4'),
)
##########################################################

##########################################################
#### ELECTRONS
process.selectedPatElectrons = cms.EDFilter("PATElectronSelector",
	src = cms.InputTag("slimmedElectrons"),
	cut = cms.string('pt > 15. && abs(eta) < 2.4'),
)
##########################################################


##########################################################
#### MET
process.selectedPatMET = cms.EDFilter("PATMETSelector",
	src = cms.InputTag("slimmedMETs"),
	cut = cms.string('pt > 40'),
)
##########################################################


##########################################################
#### JETS
process.selectedPatJetsAK4 = cms.EDFilter("PATJetSelector",
		src = cms.InputTag("slimmedJets"),
		cut = cms.string("pt > 20 && abs(eta) < 2.4") )
		
process.selectedPatJetsAK8 = cms.EDFilter("PATJetSelector",
		src = cms.InputTag("slimmedJetsAK8"),
		cut = cms.string("pt > 200 && abs(eta) < 2.5") )
##########################################################


##########################################################
#### Validator
process.mcValidator = cms.EDAnalyzer('MCValidation',
		Vertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
		#AK8jets = cms.InputTag( "selectedPatJetsAK8" ),
		AK8jets = cms.InputTag( "slimmedJetsAK8" ),
		AK4jets = cms.InputTag( "selectedPatJetsAK4" ),
		Muons = cms.InputTag( "selectedPatMuons" ),
		Electrons = cms.InputTag( "selectedPatElectrons" ),
		MET = cms.InputTag( "selectedPatMET" ),
		genParticles = cms.InputTag( 'prunedGenParticles' ),
		particle1 = cms.int32( 25 ),
		particle2 = cms.int32( 6 ),
		particle3 = cms.int32( 24 ),
		muonIso = cms.double( 0.25 ), 
		eleIso = cms.double( 0.06 ), 
)
##########################################################




##########################################################
#### GENParticles
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleListDrawer",
		maxEventsToPrint = cms.untracked.int32(2),
		printVertex = cms.untracked.bool(False),
		src = cms.InputTag("prunedGenParticles")
		)
##########################################################



process.p = cms.Path(
	process.selectedPatMuons
	* process.selectedPatElectrons
	* process.selectedPatMET
	* process.selectedPatJetsAK4
	#* process.selectedPatJetsAK8
	* process.mcValidator
	* process.printTree
)
#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
