import ROOT
import logging
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class PrimaryVertexAnalyzer(Module):
    """
    """
    def __init__(self, cfg_ana):
        self.conf = cfg_ana

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        pvs = event.PV
        if len(pvs) > 0:
            event.primaryVertex = pvs[0]
            event.passPV = (not event.primaryVertex.isFake) and (event.primaryVertex.ndof >= 4 and event.primaryVertex.Rho <= 2)
        else:
            event.passPV = False
            print "PrimaryVertexAnalyzer: number of vertices=", (len(pvs))
            #cannot use passAll here because we want to ntuplize the primary vertex, in case it doesn't exist, the
            #code will fail
            return False
        if not self.conf.general["passall"]:
            return event.passPV
        else:
            return True
