import FWCore.ParameterSet.Config as cms

process = cms.Process("NANO")

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)

process.source.fileNames = [
        #"root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv4/ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/120000/896CF8F1-9D1F-5845-9764-83F22A13145A.root"
        "root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv4/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6-v1/10000/725BCC68-FAEC-6D41-879E-3C1158D9E311.root"
]

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('nano_postprocessed.root'),
    #fakeNameForCrab = cms.untracked.bool(True),
)
process.out = cms.EndPath(process.output)
