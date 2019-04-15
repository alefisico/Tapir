import ROOT
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")
from ROOT import MEM
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

import numpy as np

import logging
LOG_MODULE_NAME = logging.getLogger(__name__)


class MECategoryAnalyzer(Module):
    """
    Performs ME categorization
    FIXME: doc
    """
    def __init__(self, cfg_ana):
        self.conf = cfg_ana
        self.cat_map = {"NOCAT":-1, "cat1": 1, "cat2": 2, "cat3": 3, "cat6":6, "cat7":7, "cat8":8, "cat9":9, "cat10":10, "cat11":11, "cat12":12 }
        self.btag_cat_map = {"NOCAT":-1, "L": 0, "H": 1}

    def analyze(self, event):
        if event.catChange: #DS
            if "systematics" in self.conf.general["verbosity"]:
                autolog("MECatAna: processing catChange")
            res = self._process(event.catChange)
            event.catChange = res #DS

        for (syst, event_syst) in event.systResults.items():
            if event_syst.passes_wtag:
                #print syst, event_syst, event_syst.__dict__
                res = self._process(event_syst)
                event.systResults[syst] = res
            else:
                event.systResults[syst].passes_mecat = False
        return self.conf.general["passall"] or np.any([v.passes_mecat for v in event.systResults.values()])

    def _process(self, event):

        eventstr = "{0}:{1}:{2}".format(event.run, event.luminosityBlock, event.event)
        LOG_MODULE_NAME.debug("MECategoryAnalyzer started {0}".format(eventstr))

        cat = "NOCAT"

        pass_btag_csv = (self.conf.jets["untaggedSelection"] == "btagCSV" and
            len(event.selected_btagged_jets_high) >= 4
        )

        # printouts by DS
        if "debug" in self.conf.general["verbosity"]:
            if (self.conf.jets["untaggedSelection"] == "btagLR") and event.is_fh and event.systematic == "nominal": #DS
                if (event.btag_LR_4b_2b > self.conf.mem["FH_bLR_4b_SR"]):
                    print "4b_SR",
                if (event.btag_LR_4b_2b < self.conf.mem["FH_bLR_4b_excl"] and
                    event.btag_LR_3b_2b > self.conf.mem["FH_bLR_3b_SR"]):
                    print "3b_SR",
                if (event.btag_LR_3b_2b < self.conf.mem["FH_bLR_3b_excl"] and
                    event.btag_LR_4b_2b > self.conf.mem["FH_bLR_4b_CR_lo"] and
                    event.btag_LR_4b_2b < self.conf.mem["FH_bLR_4b_CR_hi"]):
                    print "4b_CR",
                if (event.btag_LR_3b_2b > self.conf.mem["FH_bLR_3b_CR_lo"] and
                    event.btag_LR_3b_2b < self.conf.mem["FH_bLR_3b_CR_hi"]):
                    print "3b_CR",
                if (len(event.selected_btagged_jets_high)<3):
                    print "2b_event"

            elif event.is_fh and event.systematic == "nominal": #DS
                print "event considered:",
                if len(event.btagged_jets_bdisc) >= 4:
                    print "4b_SR",
                if len(event.btagged_jets_bdisc) == 3:
                    print "3b_SR",
                if len(event.btagged_jets_bdisc)==2 and len(event.loosebtag_jets_bdisc)>=4:
                    print "4b_CR",
                if len(event.btagged_jets_bdisc)==2 and len(event.loosebtag_jets_bdisc)==3:
                    print "3b_CR",
                if (len(event.btagged_jets_bdisc)==2 and len(event.loosebtag_jets_bdisc)==2) or len(event.btagged_jets_bdisc)<=1:
                    print "2b_event",
                print "{0}j,{1}b,{2}lb".format(len(event.good_jets),len(event.btagged_jets_bdisc),len(event.loosebtag_jets_bdisc))
            print "{0}j".format(len(event.good_jets))
        #Here we define if an event was of high-btag multiplicity
        cat_btag = "NOCAT"
        if event.pass_category_blr or pass_btag_csv:
            cat_btag = "H"
        else:
            cat_btag = "L"

        if event.is_sl:
            #at least 6 jets, if 6, Wtag in [60,100], if more Wtag in [72,94]
            if ((len(event.good_jets) == 6 and event.Wmass >= 60 and event.Wmass < 100) or
               (len(event.good_jets) > 6 and event.Wmass >= 72 and event.Wmass < 94)):
               cat = "cat1"
               #W-tagger fills wquark_candidate_jets
            #at least 6 jets, no W-tag
            elif len(event.good_jets) >= 6:
                cat = "cat2"
            #one W daughter missing
            elif len(event.good_jets) == 5:
                event.wquark_candidate_jets = event.buntagged_jets
                cat = "cat3"
        elif event.is_dl and len(event.good_jets)>=4:
            #event.wquark_candidate_jets = []
            event.wquark_candidate_jets = event.buntagged_jets
            cat = "cat6"
        elif event.is_fh:
            #exactly 8 jets, Wtag in [60,100]
            if (len(event.good_jets) == 8 and event.Wmass >= 60 and event.Wmass < 100):
                #event.wquark_candidate_jets = event.buntagged_jets + event.selected_btagged_jets_low #DS adds 5th,6th,... btags
                if(len(event.selected_btagged_jets_high) == 4):
                    cat = "cat8"
                elif(len(event.selected_btagged_jets_high) == 3):
                    cat = "cat10"
            #exactly 7 jets, Wtag in [60,100]
            if (len(event.good_jets) == 7 and event.Wmass >= 60 and event.Wmass < 100):
                #event.wquark_candidate_jets = event.buntagged_jets + event.selected_btagged_jets_low
                if(len(event.selected_btagged_jets_high) == 4):
                    cat = "cat7"
                elif(len(event.selected_btagged_jets_high) == 3):
                    cat = "cat11"
            #exactly 9 jets, Wtag in [70,92] - new allow more than 9 jets, just drop the 10th...
            if (len(event.good_jets) >= 9 and event.Wmass >= 70 and event.Wmass < 92):
                #event.wquark_candidate_jets = event.buntagged_jets + event.selected_btagged_jets_low
                if(len(event.selected_btagged_jets_high) == 4):
                    cat = "cat9"
                elif(len(event.selected_btagged_jets_high) == 3):
                    cat = "cat12"

        event.cat = cat
        event.cat_btag = cat_btag
        event.catn = self.cat_map.get(cat, -1)
        event.cat_btag_n = self.btag_cat_map.get(cat_btag, -1)

        #always pass ME category analyzer
        event.passes_mecat = True

        return event
