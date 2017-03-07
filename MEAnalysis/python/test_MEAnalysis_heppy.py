import subprocess
import copy, os
import unittest
import logging
import ROOT

class MEAnalysisTestCase(unittest.TestCase):
    testfiles = [
        ("/store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_10.root", "tth"),
        #("/store/user/jpata/tth/Feb6_leptonic_nome/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/Feb6_leptonic_nome/170206_161748/0000/tree_10.root", "ttjets")
    ]
    
    def launch_test_MEAnalysis(self, infile, sample):
        env = copy.copy(os.environ)
        CMSSW_BASE = os.environ["CMSSW_BASE"]
        env["ME_CONF"] = os.path.join(CMSSW_BASE, "src/TTH/MEAnalysis/python/cfg_local.py")
        env["INPUT_FILE"] = infile
        env["TTH_SAMPLE"] = sample
        outdir = "Loop_2_{0}".format(sample) #if this is anything but Loop_{0} the looper will number them Loop_sample_X, otherwise it requires no existing directory
        if os.path.isdir(outdir):
            raise Exception("output directory exists: {0}".format(outdir))

        import TTH.MEAnalysis.MEAnalysis_heppy as MEAnalysis_heppy
        import cProfile, time
        p = cProfile.Profile(time.clock)
        p.runcall(MEAnalysis_heppy.main)
        p.print_stats()
        return True
    
    def test_MEAnalysis(self):
        for infile, sample in self.testfiles:
            self.launch_test_MEAnalysis(infile, sample)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
