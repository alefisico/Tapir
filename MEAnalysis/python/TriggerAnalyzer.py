from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
from TTH.MEAnalysis.vhbb_utils import lvec
from TTH.MEAnalysis.Analyzer import FilterAnalyzer

class TriggerAnalyzer(FilterAnalyzer):
    """
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TriggerAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def beginLoop(self, setup):
        super(TriggerAnalyzer, self).beginLoop(setup)

    def process(self, event):

        event.triggerDecision = False
        event.trigvec = []
        if self.cfg_comp.isMC:
            triglist = self.conf.trigger["trigTable"]
        else:
            triglist = self.conf.trigger["trigTableData"]
        triglist = filter(lambda x: "ttH" in x[0], triglist.items())
        triglist = dict(triglist)
        for pathname, trigs in triglist.items():
            pathBit = False
            for name in trigs:
                bit = int(event.input.__getattr__(name, -1))
                setattr(event, name, bit)                
                event.trigvec += [bit == 1]
                pathBit = pathBit or bool(bit)
                #print name, bit
                if "trigger" in self.conf.general["verbosity"]:
                    print "[trigger]", name, bit
                if (bit == 1):
                    event.triggerDecision = True
            setattr(event, "HLT_"+pathname, int(pathBit))
        passes = True
        if self.conf.trigger["filter"] and not event.triggerDecision:
            passes = False
        
        return self.conf.general["passall"] or passes
