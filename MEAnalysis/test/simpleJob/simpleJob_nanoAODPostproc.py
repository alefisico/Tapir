#################################################################
## Based on PhysicsTools/NanoAODTools/scripts/nano_postproc.py
## To run:
##  - Input file in PSet.py
##  - python simpleJob_nanoAODPostproc.py
##  /store/mc/RunIIAutumn18NanoAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/102X_upgrade2018_realistic_v15-v1/40000/A6521C51-AC51-DD43-9E43-5B06B630B635.root
#################################################################
import os
from importlib import import_module
import sys
import ROOT

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
args = parser.parse_args(sys.argv[1:])

if 'pythia' in args.sample: isMC = True
else: isMC = False

### Adding modules for JEC, Btag SF and PU reweighting
from TTH.MEAnalysis.nano_config import NanoConfig
nanoCFG = NanoConfig( "102Xv1", jec=isMC, btag=isMC, pu=isMC )

### Rerunning JECs for data
if not isMC:
    runEra = args.sample.split('2018')[1]
    from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import jetRecalib
    nanoCFG.modules.append(jetRecalib("Autumn18_Run"+runEra+"_V8_DATA"))

p=PostProcessor(
    '.', inputFiles(),
    cut="",
    branchsel="keep_and_drop.txt",
    modules=nanoCFG.modules,
    provenance=True, ### copy MetaData and ParametersSets
    haddFileName = "nano_postprocessed.root",
    jsonInput=runsAndLumis(),
    fwkJobReport=True,
    #noOut=False, justcount=False,
    #friend=args.noFriend,
    #postfix="_postprocessed",
    ##compression="LZMA:9", ## "LZMA:9" is the default
)
p.run()
