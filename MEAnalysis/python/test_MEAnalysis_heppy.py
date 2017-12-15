import subprocess
import copy, os
import logging
import ROOT
import fnmatch
import sys

from TTH.MEAnalysis.MEAnalysis_heppy import main
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

test_files = {
        "TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8": "root://t3se01.psi.ch//store/user/jpata/tth/Oct16_puid_LHE_v3/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Oct16_puid_LHE_v3/171017_052828/0000/tree_1.root",
        "ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8": "root://t3se01.psi.ch//store/user/jpata/tth/Oct16_puid_LHE_v3/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Oct16_puid_LHE_v3/171017_053022/0000/tree_1.root",
        "DoubleMuon": "root://t3se01.psi.ch//store/user/jpata/tth/Oct27_data/DoubleMuon/Oct27_data/171027_095929/0000/tree_100.root",
}

def launch_test_MEAnalysis(analysis, sample, filename, **kwargs):
    output_name = "Loop_{0}".format(sample)
    main(analysis, sample_name=sample, firstEvent=0, output_name = output_name, files=[filename], **kwargs)
    return output_name

def test_MEAnalysis(analysis_cfg, sample_pattern, **kwargs):
    analysis = analysisFromConfig(analysis_cfg)
    for sample in analysis.samples:
        if fnmatch.fnmatch(sample.name, sample_pattern):
            logging.info("Running on sample {0}".format(sample.name))
            out = launch_test_MEAnalysis(
                analysis,
                sample.name,
                numEvents=analysis.config.getint(sample.name, "test_events"),
                filename=test_files[sample.name]
            )
            
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
        '--sample_pattern',
        action="store",
        help="Samples to process, glob pattern",
        required=False,
        default="*"
    )
    parser.add_argument(
        '--analysis_cfg',
        action="store",
        help="Analysis cfg (eg. MEAnalysis/data/default.cfg)",
        required=False,
        default=os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/default.cfg"
    )
    args = parser.parse_args(sys.argv[1:])
    test_MEAnalysis(args.analysis_cfg, args.sample_pattern)
