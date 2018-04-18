import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.TFileService=cms.Service("TFileService", fileName=cms.string('myQuickAnalysis.root'))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/mc/RunIIFall17MiniAOD/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/CC0FCC49-B50A-E811-9694-02163E0144C8.root'
    )
)

process.selectedPatJetsAK4 = cms.EDFilter("PATJetSelector",
		src = cms.InputTag("slimmedJets"),
		cut = cms.string("pt > 30 && abs(eta) < 2.5") )
		
process.selectedPatJetsAK8 = cms.EDFilter("PATJetSelector",
		src = cms.InputTag("slimmedJetsAK8"),
		cut = cms.string("pt > 200 && abs(eta) < 2.5") )

process.analyzer = cms.EDAnalyzer('myQuickAnalyzer',
		AK8jets = cms.InputTag( "selectedPatJetsAK8" ),
		AK4jets = cms.InputTag( "selectedPatJetsAK4" ),
		genParticles = cms.InputTag( 'prunedGenParticles' ),
		particle1 = cms.int32( 25 ),
		particle2 = cms.int32( 6 ),
)

#from JMEAnalysis.JetToolbox.jetToolbox_cff import jetToolbox
#jetToolbox( process, 'ak8', 'jetSequence', 'out', PUMethod='CHS', miniAOD=True, addPruning=True )


process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleListDrawer",
		maxEventsToPrint = cms.untracked.int32(1),
		printVertex = cms.untracked.bool(False),
		src = cms.InputTag("prunedGenParticles")
		)



process.p = cms.Path(
	process.selectedPatJetsAK4
	* process.selectedPatJetsAK8
	* process.analyzer
	* process.printTree
)
#############   Format MessageLogger #################
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
