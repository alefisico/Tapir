import FWCore.ParameterSet.Config as cms

process = cms.Process("FAKE")

#MC

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        "root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAODv2/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/00A03F2A-6042-E811-98BF-0CC47A5FBE31.root"
    ),
    lumisToProcess = cms.untracked.VLuminosityBlockRange(
        "1:5245-1:5247",
        "1:5250-1:5253"
    )
)


##Data
#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring(
#        #'root://cms-xrd-global.cern.ch//store/data/Run2017F/JetHT/MINIAOD/17Nov2017-v1/50000/00280B8B-36E0-E711-A549-02163E01421E.root'
#        #'/store/data/Run2017E/SingleElectron/MINIAOD/17Nov2017-v1/60000/E45D32D2-33F6-E711-9ABA-A0369F836372.root'
#        'root://t3se.psi.ch//store/mc/RunIISummer17MiniAOD/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/92X_upgrade2017_realistic_v10-v2/10000/0C164E52-C692-E711-B1C8-00266CFEFDEC.root'
#        
#    ),
##    lumisToProcess = cms.untracked.VLuminosityBlockRange(
##        "306037:1-306037:1",
##    )
#)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
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
