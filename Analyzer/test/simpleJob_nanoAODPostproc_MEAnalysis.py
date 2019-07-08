#################################################################
## Based on PhysicsTools/NanoAODTools/scripts/nano_postproc.py
## To run:
##  - Input file in PSet.py
##  - python simpleJob_nanoAODPostproc_MEAnalysis_cfg.py
#################################################################
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

### Adding modules for JEC, Btag SF and PU reweighting
from TTH.MEAnalysis.nano_config import NanoConfig

### Adding MEAnalysis
from TTH.MEAnalysis.MEAnalysis_heppy import main
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
import argparse


parser = argparse.ArgumentParser(description='Runs MEAnalysis')
parser.add_argument(
    '--config',
    action="store",
    help="Config file",
    default='simpleJob_config.cfg',
)
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
    help="Number of events to process",
    default=-1,
)
parser.add_argument(
    '--addMEAnalysis',
    action="store_true",
    help="Run Post processing and MEAnalysis (true) or postProcessing only (false)",
    default=False,
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

if 'pythia' in args.sample: isMC = True
else: isMC = False

### Preliminary selection to speed up postProcessing
### General selections:
PV = "(PV_npvsGood>0)"
METFilters = "( (Flag_goodVertices==1) && (Flag_globalSuperTightHalo2016Filter==1) && (Flag_HBHENoiseFilter==1) && (Flag_HBHENoiseIsoFilter==1) && (Flag_EcalDeadCellTriggerPrimitiveFilter==1) && (Flag_BadPFMuonFilter==1) && (Flag_eeBadScFilter==1) )"

Triggers = "( (HLT_Ele35_WPTight_Gsf==1) || (HLT_Ele28_eta2p1_WPTight_Gsf_HT150==1) || (HLT_IsoMu24_eta2p1==1) || (HLT_IsoMu27==1) || (HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL==1) || (HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ==1) || (HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL==1) || (HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ==1) || (HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ==1) || (HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ==1) || (HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ==1) || (HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8==1) || (HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8==1) )"

precuts = PV + " && " + METFilters + " && " + Triggers

### Preliminary selection to speed up postProcessing
cuts= precuts + " && ( ( nJet>1 ) && ( Jet_pt>15 ) && ( abs(Jet_eta)<2.4 ) && ( (nElectron>0) || (nMuon>0) ) && ( abs(Muon_eta)<2.4 ) && ( abs(Electron_eta)<2.4 ) )"

###### Running nanoAOD postprocessing
nanoCFG = NanoConfig( "102Xv1", jec=isMC, btag=False, pu=isMC )

### Rerunning JECs for data
if not isMC:
    runEra = args.sample.split('2018')[1]
    from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import jetRecalib
    nanoCFG.modules.append(jetRecalib("Autumn18_Run"+runEra+"_V8_DATA"))
    print "Loading ", jetRecalib, "Autumn18_Run"+runEra+"_V8_DATA"

p=PostProcessor(
    '.', inputFiles(),
    cut=cuts,
    branchsel="keep_and_drop.txt",
    modules=nanoCFG.modules,
    provenance=True, ### copy MetaData and ParametersSets
    haddFileName = "nano_postprocessed.root",
    jsonInput=(None if isMC else runsAndLumis()),
    fwkJobReport=True,
)
p.run()

##### Running MEAnalysis
if args.addMEAnalysis:
    an = analysisFromConfig(args.config)
    looper_dir, files = main( an,
                            sample_name= args.sample if isMC else args.sample.split('_')[0],
                            ##numEvents=args.numEvents,
                            files=["nano_postprocessed.root"],
                            loglevel = args.loglevel
                            )