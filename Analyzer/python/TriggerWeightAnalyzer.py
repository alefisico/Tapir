import ROOT
import logging
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class TriggerWeightAnalyzer(Module):
    """
    Computes trigger weight from root files containing the SF
    """
    def __init__(self, cfg_ana, isMC):
        self.calcSF = cfg_ana.trigger["calcFHSF"]
        self.isMC = isMC
        if self.calcSF:
            sfFile = ROOT.TFile(cfg_ana._conf.trigger["TriggerSFFile"],"READ")
            self.SF = deepcopy(sfFile.Get(cfg_ana._conf.trigger["TriggerSFHisto"])) #only works with deepcopy

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        #Only process MC
        if not self.isMC:
            return event

        if not self.calcSF:
            event.TriggerFHWeight = 1
            return True
        else:
            SF = 1
            nominalEvent = event.systResults["nominal"]
            #Make the Analyizer save for runnign with pass all!
            hasCSVHTAttr = hasattr(nominalEvent, "nBCSVM") and hasattr(nominalEvent, "ht30")
            hasGoodJets = hasattr(nominalEvent, "good_jets")
            hasSixJets = False
            if hasGoodJets:
                hasSixJets = len(nominalEvent.good_jets) >= 6
            if not (hasCSVHTAttr and hasGoodJets and hasSixJets):
                event.TriggerFHWeight = 1
                return True
            ht, pt, nBSCM = nominalEvent.ht30, getattr(nominalEvent.good_jets[5], "pt"), nominalEvent.nBCSVM
            _bin = self.SF.FindBin(ht, pt, nBSCM)
            SF = self.SF.GetBinContent(_bin)
            #print ht, pt, nBSCM, _bin, SF
            if SF == 0:
                SF = 1

            event.TriggerFHWeight = SF
            return True
