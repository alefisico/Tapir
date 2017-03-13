import subprocess
import copy, os
import unittest
import logging
import ROOT

from TTH.MEAnalysis.MEAnalysis_heppy import main
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

class MEAnalysisTestCase(unittest.TestCase):
    testfiles = [
        ("/store/user/jpata/tth/tth_Jul31_V24_v1/ttHTobb_M125_13TeV_powheg_pythia8/tth_Jul31_V24_v1/160731_130548/0000/tree_1.root", "tth"),
        ("/store/user/jpata/tth/Aug11_leptonic_nome_v1/TT_TuneCUETP8M1_13TeV-powheg-pythia8/Aug11_leptonic_nome_v1/160811_212409/0000/tree_1.root", "ttjets")
    ]
    
    def launch_test_MEAnalysis(self, analysis, sample):
        main(analysis, sample_name=sample, firstEvent=0, numEvents=1000, output_name="Loop_{0}".format(sample))
        return True
    
    def test_MEAnalysis(self):
        analysis = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/default.cfg")
        for sample in analysis.samples:
            logging.info("Running on sample {0}".format(sample.name))
            self.launch_test_MEAnalysis(analysis, sample.name)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
