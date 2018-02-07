import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

#MC
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/0C0796F5-CFC6-E611-ADB6-008CFA0A58B4.root'),
    lumisToProcess = cms.untracked.VLuminosityBlockRange(
        "1:883-1:890",
        "1:2205-1:2206"
    )
)

#Data
#process.source = cms.Source("PoolSource",
#        fileNames = cms.untracked.vstring('root://cmsxrootd.hep.wisc.edu//store/data/Run2016H/SingleMuon/MINIAOD/03Feb2017_ver3-v1/80000/F0B09550-7DEA-E611-A445-B8CA3A70A5E8.root'),
#    lumisToProcess = cms.untracked.VLuminosityBlockRange(
#        "284036:1-284036:1",
#    )
#)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.output = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('tree.root'),
    logicalFileName = cms.untracked.string('')
)


process.out = cms.EndPath(process.output)
