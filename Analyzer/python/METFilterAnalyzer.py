import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import logging
LOG_MODULE_NAME = logging.getLogger(__name__)

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class METFilterAnalyzer(Module):
    """
    Creates combination flag of MET data quality filters defiend in config.
    """
    def __init__(self, cfg_ana, isMC):
        self.conf = cfg_ana
        if isMC:
            self.METFilterList = self.conf.general["METFilterMC"]
            LOG_MODULE_NAME.debug("Loading MC METFilters")
        else:
            self.METFilterList = self.conf.general["METFilterData"]
            LOG_MODULE_NAME.debug("Loading Data METFilters")
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("passMETFilters",  "F");
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        flags = Object(event, "Flag")
        passesFilter = False
        for ifilter, _filter in enumerate(self.METFilterList):
            filterVal = getattr(flags,  _filter.split("_")[1])
            if ifilter == 0:
                passesFilter = filterVal
            else:
                passesFilter = passesFilter and filterVal

        self.out.fillBranch("passMETFilters", passesFilter)

        return True
