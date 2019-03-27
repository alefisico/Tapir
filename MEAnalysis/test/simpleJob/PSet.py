import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring([
            "root://cms-xrd-global.cern.ch//store/user/algomez/ttH/nanoAOD/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAOD_simpleJobs_v00/190221_170126/0000/myNanoProdMc_NANO_38.root"
            ]),
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('tree.root'),
    fakeNameForCrab = cms.untracked.bool(True),
)

process.out = cms.EndPath(process.output)
    