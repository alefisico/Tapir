import FWCore.ParameterSet.Config as cms

process = cms.Process("NANO")

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)

process.source.fileNames = [
        #'root://xrootd-cms.infn.it//store/data/Run2018A/EGamma/NANOAOD/02Apr2020-v1/250000/A84D4B35-BC46-2C40-BB68-1072C82FCE35.root'
        #'root://xrootd-cms.infn.it//store/mc/RunIIFall17NanoAODv7/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/120000/7BDFF01C-6519-5847-B1CF-348604D57531.root'
        'root://xrootd-cms.infn.it//store/mc/RunIIAutumn18NanoAODv7/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/60000/022107FA-F567-1B44-B139-A18ADC996FCF.root'
        #'root://xrootd-cms.infn.it//store/mc/RunIIAutumn18NanoAODv7/THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/260000/DA365B0B-8DC6-B44D-92AA-97E81DD46210.root'
        #'root://xrootd-cms.infn.it//store/mc/RunIIAutumn18NanoAODv7/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/130000/9373FB4D-EE86-DC40-ABF5-00BE8B1C84AF.root'
    #'root://xrootd-cms.infn.it//store/data/Run2017B/SingleMuon/NANOAOD/Nano1June2019-v1/40000/50AE97C4-272A-2B42-88E0-787EE5943156.root'
    #'root://xrootd-cms.infn.it//store/data/Run2017F/SingleMuon/NANOAOD/Nano1June2019-v1/30000/713368EF-14E8-6345-BCFB-8D177C90971A.root',
    #'BDAE7388-AA56-804E-B89F-08919D5ED75D.root'

]

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('nano_postprocessed.root'),
    fakeNameForCrab = cms.untracked.bool(True),
)
process.out = cms.EndPath(process.output)

