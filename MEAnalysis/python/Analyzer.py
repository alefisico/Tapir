from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
from TTH.MEAnalysis.vhbb_utils import lvec
import ROOT
from TTH.MEAnalysis.VHbbTree import LHE_weights_pdf

class FilterAnalyzer(Analyzer):
    """
    A generic analyzer that may filter events.
    Counts events the number of processed and passing events.
    """
    def beginLoop(self, setup):
        super(FilterAnalyzer, self).beginLoop(setup)


class PrefilterAnalyzer(Analyzer):
    """
    Performs a very basic prefiltering of the event before fully
    loading the event from disk into memory.
    """
    
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(PrefilterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
    
    def process(self, event):
        njet = event.input.nJet
        btag_csv = [getattr(event.input, "Jet_btagCSV")[nj] for nj in range(njet)]
        btag_cmva = [getattr(event.input, "Jet_btagCMVA")[nj] for nj in range(njet)]
        btag_csv_m = filter(lambda x, wp=self.conf.jets["btagWPs"]["CSVM"][1]: x>=wp, btag_csv)
        btag_cmva_m = filter(lambda x, wp=self.conf.jets["btagWPs"]["CMVAM"][1]: x>=wp, btag_cmva)
        if not (len(btag_csv_m) >= 3 or len(btag_cmva_m) >= 3):
            return False
        return True

class CounterAnalyzer(FilterAnalyzer):
    
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(CounterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
    
    def beginLoop(self, setup):
        super(CounterAnalyzer, self).beginLoop(setup)
        self.chist = ROOT.TH1F("CounterAnalyzer_count", "count", 1,0,1)
    
    def process(self, event):
        #super(CounterAnalyzer, self).process(event)
        passes = False
        try:
            if( LHE_weights_pdf.make_array(event.input) ):
                self.chist.Fill(0)
                passes = True
        except:
            print "event in tree not accessible"
        return passes

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
            if (event.input.run, event.input.lumi, event.input.evt) in self.event_whitelist:
                print "IDFilter", (event.input.run, event.input.lumi, event.input.evt)
                passes = True

        if passes and (
            "eventboundary" in self.conf.general["verbosity"] or
            "debug" in self.conf.general["verbosity"]
            ):
            print "---starting EVENT r:l:e", event.input.run, event.input.lumi, event.input.evt
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
        pvs = event.primaryVertices
        if len(pvs) > 0:
            event.primaryVertex = pvs[0]
            event.passPV = (not event.primaryVertex.isFake) and (event.primaryVertex.ndof >= 4 and event.primaryVertex.Rho <= 2)
        else:
            event.passPV = False
            print "PrimaryVertexAnalyzer: number of vertices=", (len(pvs))
            return False
        return True
