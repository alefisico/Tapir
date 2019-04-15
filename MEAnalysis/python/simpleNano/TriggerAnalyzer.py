from TTH.MEAnalysis.vhbb_utils import lvec

import ROOT
import logging
LOG_MODULE_NAME = logging.getLogger(__name__)
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class TriggerAnalyzer(Module):
    """
    """
    def __init__(self, cfg_ana, isMC, sample):
        self.conf = cfg_ana
        self.isMC = isMC
        self.sample = sample
        self.setOnce = False


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        event.triggerDecision = False
        event.trigvec = []
        removedTriggers = []
        if self.isMC:
            triglist = self.conf.trigger["trigTable"]
        else:
            triglist = self.conf.trigger["trigTableData"]
        triglist_all = filter(lambda x: "ttH" in x[0], triglist.items())
        triglist = filter(lambda x: "ttH" in x[0] and not ":" in x[0], triglist.items())
        dsSensitivetrigs = filter(lambda x: len(x[0].split(":"))>1, triglist_all)
        triglist = dict(triglist)
        #Replace dataset specific configurations
        for targetDS, trigConf in dsSensitivetrigs:
            targetTrigger, dataset = targetDS.split(":")[0], targetDS.split(":")[1]
            if dataset in self.sample:
                removedTriggers = set(triglist[targetTrigger]).difference(trigConf)#Get triggers from default conf that are not in specific conf to put them in the event later
                if not self.setOnce:
                    LOG_MODULE_NAME.info("Found dataset specific trigger configuration for current dataset: {0}".format(self.sample))
                    LOG_MODULE_NAME.debug("Replacing configuration: {0}".format(triglist[targetTrigger]))
                    LOG_MODULE_NAME.debug("Replacement: {0}".format(trigConf))
                triglist[targetTrigger] = trigConf

        paths = []
        for pathname, trigs in triglist.items():
            pathBit = False
            paths.append(pathname)
            for name in trigs:
                if isinstance(name, tuple):
                    if not self.setOnce:
                        LOG_MODULE_NAME.info("Found trigger with alternate logic expression")
                    logicexp, name = name
                else:
                    logicexp = None
                #NB: bool(-1) -> True, therefore, we should NOT use -1 for a missing trigger
                ################## Check this logic
                bit = bool(event.__getattr__(name))
                setattr(event, name, bit)
                event.trigvec += [bit == 1]
                if logicexp is None:
                    pathBit = pathBit or bool(bit)
                elif logicexp == "and":
                    if not self.setOnce:
                        LOG_MODULE_NAME.debug("Found alternate logic expression: AND")
                    pathBit = pathBit and bool(bit)
                elif logicexp == "and not":
                    if not self.setOnce:
                        LOG_MODULE_NAME.debug("Found alternate logic expression: AND NOT")
                    pathBit = pathBit and not bool(bit)
                else:
                    if not self.setOnce:
                        LOG_MODULE_NAME.warning("Unsupported alternate logic expression. Falling back to OR!")
                    pathBit = pathBit or bool(bit)
                if "trigger" in self.conf.general["verbosity"]:
                    print "[trigger]", name, bit
                if (bit == 1):
                    event.triggerDecision = True
            setattr(event, "HLT_"+pathname, int(pathBit))
        for name in removedTriggers:
            #bit = int(event.__getattr__(name, -1))
            bit = int(event.__getattr__(name))
            setattr(event, name, bit)
            event.trigvec += [bit == 1]

        """
        Merge paths as specified in the MergePaths variable in the Trigger config

        The code will look for path that start with **ttH_** plus the string defined
        in the variable. All these path will be merged into a path called ttH_variable
        """
        for toMerge in self.conf.trigger["MergePaths"]:
            if "ttH_"+toMerge in paths:
                if not self.setOnce:
                    LOG_MODULE_NAME.warning("Path ttH_%s aleady defined in TriggerTable!", toMerge)
                continue
            pathbit = False
            for path in paths:
                if toMerge in path:
                    #print path, getattr(event, "HLT_"+path)
                    pathbit = pathbit or bool(getattr(event, "HLT_"+path))
            setattr(event, "HLT_ttH_"+str(toMerge), int(pathbit))
            #print  "HLT_ttH_"+str(toMerge), getattr(event, "HLT_ttH_"+str(toMerge))
        """ Add all trigger bits that are specified in paths that are not starting with ttH_* """
        variousTrigList = filter(lambda x: "ttH" not in x[0], self.conf.trigger["trigTable"].items())
        for pathname, trigs in variousTrigList:
            for name in trigs:
                #bit = bool(event.__getattr__(name, 0))
                bit = bool(event.__getattr__(name))
                setattr(event, name, bit)
                event.trigvec += [bit == 1]
        passes = True
        if self.conf.trigger["filter"] and not event.triggerDecision:
            passes = False
        if not self.setOnce:
            self.setOnce = True
            LOG_MODULE_NAME.debug("Will not show dataset specific trigger logs again")
        return self.conf.general["passall"] or passes
