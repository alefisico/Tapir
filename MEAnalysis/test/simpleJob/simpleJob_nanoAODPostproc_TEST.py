#################################################################
## Based on PhysicsTools/NanoAODTools/scripts/nano_postproc.py
## To run:
##  - Input file in PSet.py
##  - python simpleJob_nanoAODPostproc_cfg.py
##  /store/mc/RunIIAutumn18NanoAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/102X_upgrade2018_realistic_v15-v1/40000/A6521C51-AC51-DD43-9E43-5B06B630B635.root
#################################################################
import os
from importlib import import_module
import sys
import ROOT
import logging
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis
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
    help="Number of events to process",
    default=-1,
)
parser.add_argument(
    '--loglevel',
    action="store",
    help="log level",
    choices=["ERROR", "INFO", "DEBUG"],
    default="INFO",
    required=False
)
parser.add_argument(
    '--config',
    action="store",
    help="Config file",
    default='simpleJob_config.cfg',
)
args = parser.parse_args(sys.argv[1:])

if 'pythia' in args.sample: isMC = True
else: isMC = False

### Adding modules for JEC, Btag SF and PU reweighting
### AND TEST includes MEAnalysis
from TTH.MEAnalysis.simpleNano.nano_config import ModulesConfig
nanoCFG = ModulesConfig( "102Xv1", isMC, args.sample, jec=isMC, btag=isMC, pu=isMC )


### Preliminary selection to speed up postProcessing
if args.sample in [ 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8' ]:
    cuts='( nJet>1 ) && ( Jet_pt>20 ) && ( abs(Jet_eta)<2.4 ) && ( (nElectron>0) || (nMuon>0) ) && ( abs(Muon_eta)<2.4 ) && ( abs(Electron_eta)<2.4 )'
else:
    cuts='( nJet>3 ) && ( Jet_pt>30 ) && ( abs(Jet_eta)<2.4 ) && ( (nElectron>0) || (nMuon>0) ) && ( abs(Electron_eta)<2.4 )'

p=PostProcessor(
    '.', inputFiles(),
    cut=cuts,
    branchsel="keep_and_drop.txt",
    modules=nanoCFG.modules,
    ##compression="LZMA:9", ## "LZMA:9" is the default
    #friend=args.noFriend,
    #postfix="_postprocessed",
    provenance=True, ### copy MetaData and ParametersSets
    haddFileName = "nano_postprocessed.root",
    jsonInput=runsAndLumis(),
    #fwkJobReport=True,
    #noOut=False, justcount=False,
)
p.run()
