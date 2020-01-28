#################################################################
## To run:
##  - Input file in PSet.py
##  - Example: python simpleAnalyzer.py --sample ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8  --oFile _TTSemi --local --process boosted --numEvents 1000
#################################################################
import os
from importlib import import_module
import sys
import ROOT
#import logging
#logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.INFO)

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis
### central nanoAOD modules
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsModule
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puAutoWeight_2016, puAutoWeight_2017, puAutoWeight_2018, puWeight_2017
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
### other modules
from TTH.Analyzer.boostedAnalyzer import boostedAnalyzer
from TTH.Analyzer.resolvedAnalyzer import resolvedAnalyzer
#from selection import parameters
import argparse

parser = argparse.ArgumentParser(description='Runs MEAnalysis')
parser.add_argument(
    '--sample',
    action="store",
    help="Sample to process",
    default='ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8'
    #choices=[samp.name for samp in an.samples],
    #required=True
)
parser.add_argument(
    '--numEvents',
    action="store",
    type=int,
    help="Number of events to process",
    default=1000000000000,
)
parser.add_argument(
    '--iFile',
    action="store",
    help="Input file (for condor)",
    default=""
)
parser.add_argument(
    '--oFile',
    action="store",
    help="Output file (for condor)",
    default=""
)
parser.add_argument(
    '--process',
    action="store",
    help="Run boosted, resolved, or both",
    default="boosted"
)
parser.add_argument(
    '--local',
    action="store_true",
    help="Run local or condor/crab"
)
parser.add_argument(
    '--year',
    action="store",
    help="year of data",
    choices=["2016", "2017", "2018"],
    default="2017",
    required=False
)
parser.add_argument(
    '--loglevel',
    action="store",
    help="log level",
    choices=["ERROR", "INFO", "DEBUG"],
    default="INFO",
    required=False
)
args = parser.parse_args(sys.argv[1:])

if args.sample.startswith( ('EGamma', 'Single', 'Double', 'MuonEG') ): isMC = False
else: isMC = True

### General selections:
PV = "(PV_npvsGood>0)"
METFilters = "( (Flag_goodVertices==1) && (Flag_globalSuperTightHalo2016Filter==1) && (Flag_HBHENoiseFilter==1) && (Flag_HBHENoiseIsoFilter==1) && (Flag_EcalDeadCellTriggerPrimitiveFilter==1) && (Flag_BadPFMuonFilter==1) )"
if not isMC: METFilters = METFilters + ' && (Flag_eeBadScFilter==1)'

if args.year.startswith('2016'): Triggers = "( (HLT_Ele27_WPTight_Gsf==1) || (HLT_IsoMu24==1) || (HLT_IsoTkMu24==1) )"
elif args.year.startswith('2017'): Triggers = "( (HLT_Ele35_WPTight_Gsf==1) || (HLT_Ele28_eta2p1_WPTight_Gsf_HT150==1) || (HLT_IsoMu24_eta2p1==1) || (HLT_IsoMu27==1) )"
elif args.year.startswith('2018'): Triggers = "( (HLT_Ele32_WPTight_Gsf==1) || (HLT_Ele28_eta2p1_WPTight_Gsf_HT150==1) || (HLT_IsoMu24==1) )"

cuts = PV + " && " + METFilters + " && " + Triggers
#cuts= precuts+' && ( (event==1550290) || (event==1550342) || (event==1550361) || (event==1550387) || (event==1550467) || (event==1550502) || (event==1550607) || (event==1550660) )'

### lepton scale factors files. This assumes that the files are stored in TTH/Analyzer/data/
LeptonSF = {
    '2016' : {
        'muon' : {
            'Trigger' : [ "EfficienciesAndSF_RunBtoF.root", "IsoMu24_OR_IsoTkMu24_PtEtaBins/pt_abseta_ratio" ],
            'ID' : [ "MuonID_2016_RunBCDEF_SF_ID.root", "NUM_TightID_DEN_genTracks_eta_pt", False ],       ### True: X:pt Y:eta
            'ISO' : [ "MuonID_2016_RunBCDEF_SF_ISO.root", "NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt", True ],
        },
        'electron' : {
            'Trigger' : [ "TriggerSF_Run2016All_v1.root", "Ele27_WPTight_Gsf" ],
            'ID' : [ "2016LegacyReReco_ElectronTight_Fall17V2.root", "EGamma_SF2D", False ],
            'ISO' : [ "EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root", "EGamma_SF2D", False ],
        },
    },
    '2017' : {
        'muon' : {
            'Trigger' : [ "EfficienciesAndSF_RunBtoF_Nov17Nov2017.root", "IsoMu27_PtEtaBins/pt_abseta_ratio" ],
            'ID' : [ "MuonID_2017_RunBCDEF_SF_ID.root", "NUM_TightID_DEN_genTracks_pt_abseta", True ],     ### True: X:pt Y:eta
            'ISO' : [ "MuonID_2017_RunBCDEF_SF_ISO.root", "NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta", True ],
        },
        'electron' : {
            'Trigger' : [ "SingleEG_JetHT_Trigger_Scale_Factors_ttHbb_Data_MC_v5.0.histo.root", "SFs_ele_pt_ele_sceta_ele28_ht150_OR_ele35_2017BCDEF" ],
            'ID' : [ "egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root", "EGamma_SF2D", False ],
            'ISO' : [ "2017_ElectronTight.root", "EGamma_SF2D", False ],
        },
    },
    '2018' : {
        'muon' : {
            'Trigger' : [ "EfficienciesAndSF_2018Data_AfterMuonHLTUpdate.root", "IsoMu24_PtEtaBins/pt_abseta_ratio" ],
            'ID' : [ "MuonID_2018_RunABCD_SF_ID.root", "NUM_TightID_DEN_TrackerMuons_pt_abseta", True ],
            'ISO' : [ "MuonID_2018_RunABCD_SF_ISO.root", "NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta", True ],
        },
        'electron' : {
            'Trigger' : [ "SingleEG_JetHT_Trigger_Scale_Factors_ttHbb_Data_MC_v5.0.root", "SFs_ele_pt_ele_sceta_ele28_ht150_OR_ele35_2017BCDEF" ],
            'ID' : [ "egammaEffi.txt_EGM2D_updatedAll.root", "EGamma_SF2D", False ],
            'ISO' : [ "2018_ElectronTight.root", "EGamma_SF2D", False ],
        },
    },
}

listOfModules = []
listOfModules.append( countHistogramsModule() )
if isMC:
    if args.year.startswith('2016'): listOfModules.append( puAutoWeight_2016() )
    #elif args.year.startswith('2017'): listOfModules.append( puWeight_2017() )
    elif args.year.startswith('2017'): listOfModules.append( puAutoWeight_2017() )
    elif args.year.startswith('2018'): listOfModules.append( puAutoWeight_2018() )
jetmetCorrector = createJMECorrector(isMC=isMC, dataYear=args.year, jesUncert="All", redojec=True)
listOfModules.append( jetmetCorrector() )
if args.process.startswith( ('both', 'resolved') ):
    print "|----------> RUNNING RESOLVED"
    listOfModules.append( resolvedAnalyzer( args.sample ) )
if args.process.startswith( ('both', 'boosted') ):
    print "|----------> RUNNING BOOSTED"
    fatJetCorrector = createJMECorrector(isMC=isMC, dataYear=args.year, jesUncert="All", redojec=True, jetType = "AK8PFPuppi")
    listOfModules.append( fatJetCorrector() )
    listOfModules.append( boostedAnalyzer( args.sample, LeptonSF[args.year], args.year ) )

if args.process.startswith( ('both', 'resolved') ):
    p = PostProcessor(
        '.', (inputFiles() if not args.iFile else [args.iFile]),
        cut=cuts,
        branchsel="keep_and_drop.txt",
        modules=listOfModules,
        provenance=True, ### copy MetaData and ParametersSets
        #haddFileName = "nano_postprocessed"+args.oFile+".root",
        histFileName = "histograms"+args.oFile+".root",
        histDirName = 'tthbb13',
        #fwkJobReport=True,
        maxEntries=args.numEvents,
        prefetch=args.local,
        longTermCache=args.local,
    )
else:
    p = PostProcessor(
        '.', (inputFiles() if not args.iFile else [args.iFile]),
        cut=cuts,
        modules=listOfModules,
        provenance=True, ### copy MetaData and ParametersSets
        histFileName = "histograms"+args.oFile+".root",
        histDirName = 'tthbb13',
        maxEntries=args.numEvents,
        prefetch=args.local,
        longTermCache=args.local,
    )
p.run()
