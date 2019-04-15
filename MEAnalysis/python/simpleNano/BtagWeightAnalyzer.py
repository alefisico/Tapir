import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

import logging
LOG_MODULE_NAME = logging.getLogger(__name__)

class BtagWeightAnalyzer(Module):

    def __init__(self, isMC):
        self.isMC = isMC
        pass

    def btagWeight(self, jets_btagSF):
        if len(jets_btagSF) == 0:
            return 1.0
        return reduce(lambda x,y : x*y, jets_btagSF)

    def analyze(self, event):

        jets = event.systResults["nominal"].good_jets

        if self.isMC:

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
