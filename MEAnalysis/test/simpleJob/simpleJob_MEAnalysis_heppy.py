import os
import sys

from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
from TTH.MEAnalysis.MEAnalysis_heppy import main
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

an = analysisFromConfig(args.config)

print an

for ifile in inputFiles():
    print ifile
    looper_dir, files = main( an,
                                sample_name=args.sample,
                                files=[ifile],
                                loglevel = args.loglevel
                                )

#    import TTH.MEAnalysis.counts as counts
#    counts.main(files, "{0}/tree.root".format(looper_dir))
