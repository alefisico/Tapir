#################################################################
## Based on PhysicsTools/NanoAODTools/scripts/nano_postproc.py
#################################################################
import os
from importlib import import_module
import sys
import ROOT

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

###### Running nanoAOD postprocessing
nanoCFG = NanoConfig( "102Xv1", jec=isMC, btag=isMC, pu=isMC )

p=PostProcessor(
    '.', inputFiles(),
    cut="",
    branchsel="keep_and_drop.txt",
    modules=nanoCFG.modules,
    ##compression="LZMA:9", ## "LZMA:9" is the default
    #friend=args.noFriend,
    #postfix="_postprocessed",
    provenance=True, ### copy MetaData and ParametersSets
    haddFileName = "nano_postprocessed.root",
    fwkJobReport=True,
    #jsonInput=None, noOut=False, justcount=False,
    #needs a patch to NanoAODTools
    #treename="nanoAOD/Events", eventRange=eventRange
)
p.run()

##### Running MEAnalysis
an = analysisFromConfig(args.config)
looper_dir, files = main( an,
                            sample_name=args.sample,
                            ##numEvents=args.numEvents,
                            numEvents=1000,
                            files=["nano_postprocessed.root"],
                            loglevel = args.loglevel
                            )
