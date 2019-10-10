#################################################################
## To run:
##  - Input file in PSet.py
##  - python evenSimplerJob_nanoAODPostproc_TEST.py
##  /store/mc/RunIIAutumn18NanoAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/102X_upgrade2018_realistic_v15-v1/40000/A6521C51-AC51-DD43-9E43-5B06B630B635.root
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
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puAutoWeight_2018
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import jetmetUncertainties2017, jetmetUncertainties2017All
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
METFilters = "( (Flag_goodVertices==1) && (Flag_globalSuperTightHalo2016Filter==1) && (Flag_HBHENoiseFilter==1) && (Flag_HBHENoiseIsoFilter==1) && (Flag_EcalDeadCellTriggerPrimitiveFilter==1) && (Flag_BadPFMuonFilter==1) && (Flag_eeBadScFilter==1) )"

Triggers = "( (HLT_Ele35_WPTight_Gsf==1) || (HLT_Ele28_eta2p1_WPTight_Gsf_HT150==1) || (HLT_IsoMu24_eta2p1==1) || (HLT_IsoMu27==1) || (HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL==1) || (HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ==1) || (HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL==1) || (HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ==1) || (HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ==1) || (HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ==1) || (HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ==1) || (HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8==1) || (HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8==1) )"

precuts = PV + " && " + METFilters + " && " + Triggers

### Preliminary selection to speed up postProcessing
cuts= precuts + " && ( ( nJet>1 ) && ( Jet_pt>15 ) && ( abs(Jet_eta)<2.4 ) && ( (nElectron>0) || (nMuon>0) ) && ( abs(Muon_eta)<2.4 ) && ( abs(Electron_eta)<2.4 ) )"

listOfModules = []
#listOfModules.append( countHistogramsModule() )
if isMC:
    listOfModules.append( puAutoWeight_2018() )
if args.process.startswith( ('both', 'resolved') ):
    print "|----------> RUNNING RESOLVED"
    listOfModules.append( jetmetUncertainties2017All() )
    listOfModules.append( resolvedAnalyzer( args.sample ) )
if args.process.startswith( ('both', 'boosted') ):
    print "|----------> RUNNING BOOSTED"
    listOfModules.append( jetmetUncertainties2017() )
    listOfModules.append( boostedAnalyzer( args.sample ) )

if args.process.startswith( ('both', 'resolved') ):
    p = PostProcessor(
        '.', (inputFiles() if not args.iFile else [args.iFile]),
        cut=cuts,
        branchsel="keep_and_drop.txt",
        modules=listOfModules,
        provenance=True, ### copy MetaData and ParametersSets
        haddFileName = "nano_postprocessed"+args.oFile+".root",
        histFileName = "histograms"+args.oFile+".root",
        histDirName = 'tthbb13',
        fwkJobReport=True,
        maxEntries=args.numEvents,
        prefetch=args.local,
        longTermCache=args.local,
    )
else:
    p = PostProcessor(
        '.', (inputFiles() if not args.iFile else [args.iFile]),
        cut=cuts,
        branchsel="keep_and_drop.txt",
        modules=listOfModules,
        provenance=True, ### copy MetaData and ParametersSets
        histFileName = "histograms"+args.oFile+".root",
        histDirName = 'tthbb13',
        maxEntries=args.numEvents,
        prefetch=args.local,
        longTermCache=args.local,
    )
p.run()
