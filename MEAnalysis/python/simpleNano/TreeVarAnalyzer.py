import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import logging
LOG_MODULE_NAME = logging.getLogger(__name__)

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class TreeVarAnalyzer(Module):
    """
    Flattens the systematic dictionary into the event.
    {"JESUp": res} => event.res_JESUp
    """

    def __init__(self):
        pass

    def analyze(self, event):
        #Need to create empty lists for objects that may not be produced in case the analyzer is skipped
        setattr( event, 'boosted_bjets', [] )
        setattr( event, 'boosted_ljets', [] )
        setattr( event, 'topCandidate', [] )
        setattr( event, 'higgsCandidate', [] )
        setattr( event, 'higgsCandidateAK8', [] )
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

        return True
