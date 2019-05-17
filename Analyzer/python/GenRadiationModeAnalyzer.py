import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TTH.Analyzer.utils import lvec, autolog

class GenRadiationModeAnalyzer(Module):
    """
    Performs B/C counting in order to classify heavy flavour / light flavour events.

    We count the number of reconstructed jets which are matched to b/c quarks by CMSSW (ghost clustering).
    From this, the jets matched to b quarks from tops are subtracted.

    Therefore, nMatchSimB == 2 corresponds to 2 additional gluon radiation b quarks
    which are reconstructed as good jets.
    """
    def __init__(self, cfg_ana, isMC):
        self.conf = cfg_ana
        self.isMC = isMC

    def analyze(self, event):
        if self.isMC:
            for (syst, event_syst) in event.systResults.items():
                if event_syst.passes_jet:
                    res = self._process(event_syst)
                    event.systResults[syst] = res
        return True

    def _process(self, event):

        if "debug" in self.conf.general["verbosity"]:
            autolog("GenRadiationModeAnalyzer started")

        event.nMatchSimB = 0
        event.nMatchSimC = 0
        lv_bs = map(lvec, event.GenBQuarkFromTop)
        for jet in event.good_jets:
            lv_j = lvec(jet)

            if (lv_j.Pt() > 20 and abs(lv_j.Eta()) < 2.5):
                if any([lv_b.DeltaR(lv_j) < 0.5 for lv_b in lv_bs]):
                    continue
                absid = abs(jet.partonFlavour)
                if absid == 5:
                    event.nMatchSimB += 1
                if absid == 4:
                    event.nMatchSimC += 1

        return event
