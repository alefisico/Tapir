#################################################################
## Based on PhysicsTools/NanoAODTools/scripts/nano_postproc.py
#################################################################
import os
from importlib import import_module
import sys
import ROOT

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

import argparse
#################################
# Argument parser definitions:
argumentparser = argparse.ArgumentParser()
argumentparser.add_argument(
    "--input",
    action = "store",
    help = "Inputfiles for postprocessing (separated by whitespace). Default: Get names for environment - FILE_NAMES",
    nargs='+',
    type=str,
    default = None
)
argumentparser.add_argument(
    "--outputdir",
    action = "store",
    help = "Ouput dir of the postprocessed file. Default: ./",
    type = str,
    default = "./",
)
argumentparser.add_argument(
    "--skipEvents",
    action = "store",
    help = "Number of events to skip",
    type = int,
    default = 0,
)
argumentparser.add_argument(
    "--maxEvents",
    action = "store",
    help = "Number of events to process",
    type = int,
    default = -1,
)

argumentparser.add_argument(
    "--era",
    action = "store",
    help = "Era. Defailt: 94Xv1",
    choices = ["80X", "92X", "94Xv1", "94Xv2"],
    type = str,
    default = "94Xv2",
)

argumentparser.add_argument(
    "--noFriend",
    action = "store_false",
    default = False,
    help = "Disables friend option in nanoAOD postprocessor",
)
argumentparser.add_argument(
    "--isMC",
    action = "store_false",
    default = True,
    help = "Disables all postprocessor modules",
)
argumentparser.add_argument(
    "--subfolderClone",
    action = "store_false",
    default = False,
    help = "Create clone of Events tree in subfolder",
)
argumentparser.add_argument(
    "--cuts",
    action = "store",
    help = "Cuts",
    type=str,
    default = None
)
argumentparser.add_argument(
    "--unc",
    action = "store",
    help = "Uncertainties: jec, btag, pu, all",
    choices = ["jec", "btag", "pu", "all"],
    type = str,
    default = "all",
)


args = argumentparser.parse_args()

if '80X' in args.era:
    eraBtagSF = "2016"
    algoBtag = "csvv2"
    print "Using CMSSW 80X"
elif '92X' in args.era:
    eraBtagSF = "2017"
    algoBtag = "csvv2"
    print "Using CMSSW 92X"
elif '94Xv1' in args.era:
    eraBtagSF = "2017"
    algoBtag = "deepcsv"
    print "Using CMSSW 94X with v1 era"
elif '94Xv2' in args.era:
    eraBtagSF = "2017"
    algoBtag = "deepcsv"
    print "Using CMSSW 94X with v2 era"

imports = []
if args.isMC:
    if ('jec' in args.unc) or ('all' in args.unc): imports += [ ('PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties', 'jetmetUncertainties2017All') ]
    if ('btag' in args.unc) or ('all' in args.unc): imports += [ ('PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer','btagSFProducer') ]
    if ('pu' in args.unc) or ('all' in args.unc): imports += [ ('PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer','puAutoWeight') ]

#Imports the various nanoAOD postprocessor modules
modules = []
for mod, names in imports:
    import_module(mod)
    obj = sys.modules[mod]
    selnames = names.split(",")
    for name in dir(obj):
        if name[0] == "_": continue
        if name in selnames:
            print "Loading %s from %s " % (name, mod)
            if name == "btagSFProducer":
                modules.append(getattr(obj,name)(eraBtagSF, algoBtag))
            else:
                modules.append(getattr(obj,name)())

p=PostProcessor(
    args.outputdir, args.input,
    cut=args.cuts, branchsel=None, modules=modules,
    compression="LZMA:9", friend=args.noFriend, postfix="_postprocessed",
    jsonInput=None, noOut=False, justcount=False,
    #needs a patch to NanoAODTools
    #treename="nanoAOD/Events", eventRange=eventRange
)
#for module in p.modules:
#    module.treename = "nanoAOD/Events"
p.run()
