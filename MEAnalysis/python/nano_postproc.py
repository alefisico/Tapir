import os
from importlib import import_module
import sys

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from TTH.MEAnalysis.samples_base import getSitePrefix

from TTH.MEAnalysis.nano_config import NanoConfig


def main(outdir = "./", _input = None, asFriend = True, _era = "94Xv1", runAll = False):
    if _input is None:
        infiles = map(getSitePrefix, os.environ["FILE_NAMES"].split())
    else:
        infiles = map(getSitePrefix, _input)

    if runAll:
        nano_cfg = NanoConfig(_era, jec = True, btag=True, pu=True)
    else:
        nano_cfg = NanoConfig(_era, btag=True, pu=True)
    print nano_cfg.modules
    p=PostProcessor(
        outdir, infiles,
        cut=nano_cfg.cuts, branchsel=nano_cfg.branchsel, modules=nano_cfg.modules,
        compression="LZMA:9", friend=asFriend, postfix="_postprocessed",
        jsonInput=None, noOut=False, justcount=False
    )
    p.run()

if __name__ == "__main__":
    import argparse
    ##############################################################################################################
    # Argument parser definitions:
    argumentparser = argparse.ArgumentParser(
        description='Wrapper for running the nanoAOD postprocessor with the tthbb definition for CRAB'
    )
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
        "--era",
        action = "store",
        help = "Era. Defailt: 94Xv1",
        choices = ["80X", "92X", "94Xv1", "94Xv2"],
        type = str,
        default = "94Xv1",
    )
    
    argumentparser.add_argument(
        "--noFriend",
        action = "store_false",
        help = "Disables friend option in nanoAOD postprocessor",
    )
    argumentparser.add_argument(
        "--runAllModules",
        action = "store_true",
        help = "Disables friend option in nanoAOD postprocessor",
    )
    



    args = argumentparser.parse_args()
    #
    ##############################################################################################################
    main(args.outputdir, args.input, args.noFriend, args.era, args.runAllModules)
