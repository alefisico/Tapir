import subprocess
import copy, os
import unittest
import logging
import ROOT

from TTH.Plotting.joosep.sparsinator import main
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    import argparse
    parser = argparse.ArgumentParser(description='Runs MEAnalysis tests')
    parser.add_argument(
        '--sample',
        action="store",
        help="Sample to process",
        required=True,
    )
    parser.add_argument(
        '--analysis_cfg',
        action="store",
        help="Analysis cfg (eg. MEAnalysis/data/default.cfg)",
        default="simpleJob_config_noME.cfg"
        ##default=os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/test/simpleJob_config.cfg"
    )
    parser.add_argument(
        '--inputDir',
        action="store",
        default='datasets/',
        help="Directory with input files.",
    )
    parser.add_argument(
        '--numEvents',
        action="store",
        type=int,
        default=-1,
        help="Directory with input files.",
    )
    args = parser.parse_args()

    analysis = analysisFromConfig(args.analysis_cfg)
    #file_names = ['root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/algomez/ttH/nanoPostMEAnalysis/EGamma_Run2018A/tthbb13_PostProcMEAnalysis_noME_EGamma_Run2018A_102X_v00/190228_211822/0000/tree_123.root']
    file_names = [ line.rstrip('\n').split(' = ')[0] for line in open(args.inputDir+'/'+args.sample+'.txt') if ('root' in line ) ]
    outputFile = args.sample+"_sparsinator.root"
    if '_Run' in args.sample: args.sample = args.sample.split('_')[0]
    main(analysis, file_names, args.sample, outputFile, 0, args.numEvents, "*")
