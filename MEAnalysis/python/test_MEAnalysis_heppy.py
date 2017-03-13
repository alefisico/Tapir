import subprocess
import copy, os
import unittest
import logging
import ROOT

from TTH.MEAnalysis.MEAnalysis_heppy import main
from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

class MEAnalysisTestCase(unittest.TestCase):
    testfiles = [
        ("/store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_10.root", "tth"),
        #("/store/user/jpata/tth/Feb6_leptonic_nome/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/Feb6_leptonic_nome/170206_161748/0000/tree_10.root", "ttjets")
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
