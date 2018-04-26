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

process.TFileService=cms.Service("TFileService", fileName=cms.string('myQuickAnalysis_ttWjetsToQQ.root'))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
	    #### SIGNAL
        #'/store/mc/RunIISummer16MiniAODv2/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/44949CF4-96C6-E611-B9A0-0025905A6122.root' 	#### ttHtobb
	#'/store/mc/RunIISummer16MiniAODv2/ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/00D10AF2-76BE-E611-8EFB-001E67457DFA.root' 	### ttHtoNonbb

	###### BKG
	#'/store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/0693E0E7-97BE-E611-B32F-0CC47A78A3D8.root' 				### pure tt
	#'/store/mc/RunIISummer16MiniAODv2/TTToSemilepton_ttbbFilter_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_TTbbWithttHFGenFilter_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/100000/0C36F638-25D1-E611-B3DA-B083FED18BA0.root'  		#### ttbb with weird filter
	#'/store/mc/RunIISummer16MiniAODv2/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/0023AF2C-D7CD-E611-9247-002590E7D7CE.root' 	### ttbb no filter		
	#'/store/mc/RunIISummer16MiniAODv2/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/100000/0AC42490-2FD3-E611-9800-0025904C7A58.root' 			### ttZJetsToQQ
	'/store/mc/RunIISummer16MiniAODv2/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/60000/3832F2B7-C2BD-E611-A88E-002590DE6E8A.root' 	### ttWJetstoQQ
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

##########################################################
#### MET
process.selectedMET20 = cms.EDFilter("PATMETSelector",
	src = cms.InputTag("slimmedMETs"),
	cut = cms.string('pt > 20'),
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
		cut = cms.string("pt > 300 && abs(eta) < 2.5") )

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
		met = cms.InputTag( "selectedMET20" ),
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
	* process.selectedMET20
	* process.selectedPatJetsAK4
	* process.selectedPatJetsAK8
	#* process.analyzerAK8
	* process.quickAnalyzer
	#* process.printTree
)
#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 2000
