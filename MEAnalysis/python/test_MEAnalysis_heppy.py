import subprocess
import copy, os
import logging
import ROOT
import fnmatch
import sys

from TTH.MEAnalysis.MEAnalysis_heppy import main
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

def launch_test_MEAnalysis(analysis, sample, **kwargs):
    output_name = "Loop_{0}".format(sample.name)
    files = sample.file_names_step1[:sample.debug_max_files]

    #replace local SE access with remote SE access
    files = [fi.replace("t3dcachedb03", "t3se01") for fi in files]
    main(analysis, sample_name=sample.name, firstEvent=0, output_name=output_name, files=files, **kwargs)

    return output_name

def test_MEAnalysis(sample_pattern, analysis_cfg, **kwargs):
    analysis = analysisFromConfig(analysis_cfg)
    if not sample_pattern:
        raise KeyError("Choose sample from {0}".format([s.name for s in analysis.samples]))
    
    for sample in analysis.samples:
        if sample.name == sample_pattern:
            logging.info("Running on sample {0}".format(sample.name))
            out = launch_test_MEAnalysis(analysis, sample, numEvents=analysis.config.getint(sample.name, "test_events"))
            
            tf = ROOT.TFile(out + "/tree.root")
            tt = tf.Get("tree")
            if not tt:
                raise Exception("Could not find tree in output")
            logging.info("produced {0} entries".format(tt.GetEntries()))
            
            tf.Close()
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    import argparse
    parser = argparse.ArgumentParser(description='Runs MEAnalysis tests')
    parser.add_argument(
        '--sample',
        action="store",
        help="Sample to process",
        required=False,
        default=None
    )
    parser.add_argument(
        '--analysis_cfg',
        action="store",
        help="Analysis cfg (eg. MEAnalysis/data/default.cfg)",
        required=False,
        default=os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/default.cfg"
    )
    args = parser.parse_args(sys.argv[1:])
    test_MEAnalysis(args.sample, args.analysis_cfg)
