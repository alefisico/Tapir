from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.vhbb_utils import autolog

class TreeVarAnalyzer(FilterAnalyzer):
    """
    Flattens the systematic dictionary into the event.
    {"JESUp": res} => event.res_JESUp
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TreeVarAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def process(self, event):
        if "debug" in self.conf.general["verbosity"]:
            autolog("TreeVarAnalyzer started")
        #Need to create empty lists for objects that may not be produced in case the analyzer is skipped
        setattr( event, 'boosted_bjets', [] )
        setattr( event, 'boosted_ljets', [] )
        setattr( event, 'topCandidate', [] )
        setattr( event, 'othertopCandidate', [])
        setattr( event, 'topCandidatesSync', [])    
        setattr( event, 'higgsCandidate', [] )
        event.b_quarks_h_nominal = []
        event.b_quarks_t_nominal = []
        event.l_quarks_w_nominal = []
        
        #FIXME: currently, gen-level analysis is redone for systematic variations
        #in order to correctly ntuplize, we need to define event.genTopLep = event.systResults["nominal"].genTopLep etc
        event.genTopLep = getattr(event.systResults["nominal"], "genTopLep", [])
        event.genTopHad = getattr(event.systResults["nominal"], "genTopHad", [])
       
        orig_items = event.systResults["nominal"].__dict__.items() + event.__dict__.items()
        for k, v in orig_items:
            event.__dict__[k + "_nominal"] = v

        for syst, event_syst in event.systResults.items():
            all_items = event_syst.__dict__.items()
            #add all variated quantities to event with a suffix
            for k, v in all_items:
                event.__dict__[k + "_" + syst] = v
                
        #for br in ["boosted_bjets", "boosted_ljets", "topCandidate", "othertopCandidate", "topCandidatesSync", "higgsCandidate"]:
        #    if not hasattr(event, br+"_nominal"):
        #        setattr(event, br + "_nominal", [])
        if "debug" in self.conf.general["verbosity"]:
            autolog("TreeVarAnalyzer ended")
        return True
