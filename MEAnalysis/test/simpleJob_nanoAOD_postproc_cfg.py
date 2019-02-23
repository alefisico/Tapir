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
nanoCFG = NanoConfig( "102Xv1", jec=False, btag=False, pu=False )

p=PostProcessor(
    '.', inputFiles(),
    cut="",
    branchsel="keep_and_drop.txt",
    modules=nanoCFG.modules,
    ##compression="LZMA:9", ## "LZMA:9" is the default
    #friend=args.noFriend,
    postfix="_postprocessed",
    provenance=True, ### copy MetaData and ParametersSets
    haddFileName = "nano_postprocessed.root",
    fwkJobReport=True,
    #jsonInput=None, noOut=False, justcount=False,
    #needs a patch to NanoAODTools
    #treename="nanoAOD/Events", eventRange=eventRange
)
p.run()
