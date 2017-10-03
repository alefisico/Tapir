from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
from TTH.MEAnalysis.vhbb_utils import lvec, autolog
import resource
import ROOT
from TTH.MEAnalysis.VHbbTree import LHEPdfWeight
import logging

class FilterAnalyzer(Analyzer):
    """
    A generic analyzer that may filter events.
    Counts events the number of processed and passing events.
    """
    def beginLoop(self, setup):
        super(FilterAnalyzer, self).beginLoop(setup)
        self.counters.addCounter("processed")

    def process(self, event):
        self.counters.counter("processed").inc(0)

class MemoryAnalyzer(Analyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(MemoryAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.logger = logging.getLogger("MemoryAnalyzer")
        self.hpy = None
        self.do_heapy = False 
        if self.do_heapy:
            try:
                from guppy import hpy
                self.hpy = hpy()
                self.hpy.setrelheap()
            except Exception as e:
                autolog("Could not import guppy, skipping")

        self.heap_prev = None

    def process(self, event):
        memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if event.iEv % 100 == 0:
            autolog("memory usage at event {0}: {1:.2f} MB".format(event.iEv, memory/1024.0))
 
        if not self.hpy is None:
            heap = self.hpy.heap() 
            if not self.heap_prev is None:
                diff = heap - self.heap_prev
                print diff
            self.heap_prev = heap
        return True

class PrefilterAnalyzer(Analyzer):
    """
    Performs a very basic prefiltering of the event before fully
    loading the event from disk into memory.
    NB: Actually we can't use this, since systematics may migrate the event into a different category
    """
    
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(PrefilterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
    
    def process(self, event):
        njet = event.input.nJet
        #btag_csv = [getattr(event.input, "Jet_btagCSV")[nj] for nj in range(njet)]
        btag_cmva = [getattr(event.input, "Jet_btagCMVA")[nj] for nj in range(njet)]
        #btag_csv_m = filter(lambda x, wp=self.conf.jets["btagWPs"]["CSVM"][1]: x>=wp, btag_csv)
        btag_cmva_m = filter(lambda x, wp=self.conf.jets["btagWPs"]["CMVAM"][1]: x>=wp, btag_cmva)
        #if not njet >= 4:
        #if not (len(btag_csv_m) >= 2 or len(btag_cmva_m) >= 2):
        #    if not self.conf.general["passall"]:
        #        return False
        return True

class CounterAnalyzer(FilterAnalyzer):
    
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.counter_name = cfg_ana.counter_name
        super(CounterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
    
    def beginLoop(self, setup):
        super(CounterAnalyzer, self).beginLoop(setup)
        self.chist = ROOT.TH1F("CounterAnalyzer_count{0}".format(self.counter_name), "count", 1,0,1)
    
    def process(self, event):
        if event.input.nJet >= 0:
            self.chist.Fill(0)
        else:
            raise Exception("Could not read event")
        return True

class EventIDFilterAnalyzer(FilterAnalyzer):
    """
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventIDFilterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.event_whitelist = self.conf.general.get("eventWhitelist", None)

    def beginLoop(self, setup):
        super(EventIDFilterAnalyzer, self).beginLoop(setup)

    def process(self, event):

        passes = True
        if not self.event_whitelist is None:
            passes = False
            if (event.input.run, event.input.luminosityBlock, event.input.evt) in self.event_whitelist:
                print "IDFilter", (event.input.run, event.input.luminosityBlock, event.input.event)
                passes = True

        if passes and (
            "eventboundary" in self.conf.general["verbosity"] or
            "debug" in self.conf.general["verbosity"]
            ):
            print "---starting EVENT r:l:e", event.input.run, event.input.luminosityBlock, event.input.event
        return passes


class EventWeightAnalyzer(FilterAnalyzer):
    """
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventWeightAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.n_gen = cfg_comp.n_gen
        self.xs = cfg_comp.xs

    def beginLoop(self, setup):
        super(EventWeightAnalyzer, self).beginLoop(setup)

    def process(self, event):
        event.weight_xs = self.xs/float(self.n_gen) if self.n_gen > 0 else 1
       

        return True

class PrimaryVertexAnalyzer(FilterAnalyzer):
    """
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(PrimaryVertexAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def beginLoop(self, setup):
        super(PrimaryVertexAnalyzer, self).beginLoop(setup)

    def process(self, event):
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
        return True
