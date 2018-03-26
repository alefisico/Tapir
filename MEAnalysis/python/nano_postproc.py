import os
from importlib import import_module
import sys

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from TTH.MEAnalysis.samples_base import getSitePrefix

from TTH.MEAnalysis.nano_config import NanoConfig

def main(infiles, outdir):
    nano_cfg = NanoConfig("94X", btag=True, pu=True)
    p=PostProcessor(
        outdir, infiles,
        cut=nano_cfg.cuts, branchsel=nano_cfg.branchsel, modules=nano_cfg.modules,
        compression="LZMA:9", friend=True, postfix="_postprocessed",
        jsonInput=nano_cfg.json, noOut=False, justcount=False
    )
    p.run()

if __name__ == "__main__":
    outdir = "./"
    infiles = map(getSitePrefix, os.environ["FILE_NAMES"].split())
    main(infiles, outdir)
