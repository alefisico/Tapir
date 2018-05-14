from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.vhbb_utils import *
import numpy as np


class BtagWeightAnalyzer(FilterAnalyzer):

    def beginLoop(self, setup):
        super(FilterAnalyzer, self).beginLoop(setup)

    def btagWeight(self, jets_btagSF):
        if len(jets_btagSF) == 0:
            return 1.0
        return reduce(lambda x,y : x*y, jets_btagSF)
            
    def process(self, event):

        jets = event.systResults["nominal"].good_jets

        if self.cfg_comp.isMC:

            syst = ["jes", "lf", "hf", "hfstats1", "hfstats2", "lfstats1", "lfstats2", "cferr1", "cferr2"]

            btagSF = ["btagSF", "btagSF_up", "btagSF_down", "btagSF_shape"]
            for s in syst:
                for i in ["up", "down"]:

                    btagSF.append("btagSF_shape_" + i + "_" + s)

            for b in btagSF:
                numJet = len(jets)
                jetsbtagSF = [getattr(jets[i], b) for i in range(numJet)]
                setattr(event, b, self.btagWeight(jetsbtagSF))

        return True
