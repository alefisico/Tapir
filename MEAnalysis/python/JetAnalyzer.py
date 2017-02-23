from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.VHbbTree import *
from TTH.MEAnalysis.vhbb_utils import *
from copy import deepcopy
import numpy as np
import copy
from collections import OrderedDict

#FIXME: understand the effect of cropping the transfer functions
def attach_jet_transfer_function(jet, conf):
    """
    Attaches transfer functions to the supplied jet based on the jet eta bin.
    """
    jet_eta_bin = 0
    if abs(jet.eta)>1.0:
        jet_eta_bin = 1
    jet.tf_b = conf.tf_formula['b'][jet_eta_bin]
    jet.tf_l = conf.tf_formula['l'][jet_eta_bin]
    jet.tf_b.SetNpx(10000)
    jet.tf_b.SetRange(0, 500)

    jet.tf_l.SetNpx(10000)
    jet.tf_l.SetRange(0, 500)


class JetAnalyzer(FilterAnalyzer):
    """
    Performs jet selection and b-tag counting.
    FIXME: doc
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(JetAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def beginLoop(self, setup):
        super(JetAnalyzer, self).beginLoop(setup)

    def variateJets(self, jets, systematic, sigma):
        newjets = [SystematicObject(jet, {"pt": jet.pt, "mass": jet.mass}) for jet in jets]
        for i in range(len(jets)):
            if sigma > 0:
                sdir = "Up"
                _sigma = sigma
            elif sigma < 0:
                sdir = "Down"
                _sigma = abs(sigma)
            else:
                raise Exception("sigma must be != 0")
            new_corr = getattr(newjets[i], "corr_{0}{1}".format(systematic, sdir))
            old_corr = newjets[i].corr

            #for JER need to uncorrect by a different factor
            if systematic == "JER":
                old_corr = newjets[i].corr_JER

            if new_corr > 0:
                cf =  _sigma * new_corr / old_corr
            else:
                cf = 0.0

            newjets[i].pt *= cf
            newjets[i].mass *= cf
        return newjets

    def process(self, event):
        event.MET = MET(pt=event.met.pt, phi=event.met.phi)
        event.MET_gen = MET(pt=event.MET.genPt, phi=event.MET.genPhi)
        event.MET_tt = MET(px=0, py=0)
       
        evdict = OrderedDict()
        
        #We create a wrapper around the base event with nominal quantities
        if "nominal" in self.conf.general["systematics"]:
            evdict["nominal"] = SystematicObject(event, {"systematic": "nominal"})

        #add events with variated jets
        if self.cfg_comp.isMC:
            jets_variated = {}
            for fjc in self.conf.mem["factorized_sources"] + ["JER"]:
                for sdir, sigma in [("Up", 1.0), ("Down", -1.0)]:
                    jet_var = self.variateJets(event.Jet, fjc, sigma)
                    jets_variated[fjc+sdir] = jet_var
            for name, jets in jets_variated.items():
                #skip processing of systematics that are not enabled
                if not name in self.conf.general["systematics"]:
                    continue

                ev = SystematicObject(event, {"Jet": jets, "systematic": name})
                evdict[name] = ev

        for syst, event_syst in evdict.items():
            event_syst.systematic = syst 
            res = self._process(event_syst, evdict)
            if syst != "nominal":
                res.nominal_event = evdict["nominal"]
            evdict[syst] = res
        event.systResults = evdict
        
        event.systResults["nominal"].changes_jet_category = False
        event.systResults["nominal"].nominal_event = event.systResults["nominal"]
        nj_nominal = event.systResults["nominal"].numJets
        nt_nominal = event.systResults["nominal"].nBCSVM
        for syst in evdict.keys():
            nj = evdict[syst].numJets
            nt = evdict[syst].nBCSVM
            evdict[syst].changes_jet_category = False
            if nj != nj_nominal or nt != nt_nominal:
                evdict[syst].changes_jet_category = True
        return self.conf.general["passall"] or np.any([v.passes_jet for v in event.systResults.values()])

    def _process(self, event, evdict):
        
        #FIXME: why discarded jets no longer in vhbb?
        #injets = event.Jet+event.DiscardedJet
        event.injets = event.Jet
        #pt-descending input jets
        if "input" in self.conf.general["verbosity"]:
            autolog("jets input") 
            for ij, j in enumerate(event.injets):
                autolog("InJetReco", ij, j.pt, j.eta, j.phi, j.mass, j.btagCSV, j.mcFlavour)
                autolog("InJetGen", ij, j.mcPt, j.mcEta, j.mcPhi, j.mcM)

        #choose pt cut key based on lepton channel
        pt_cut  = "pt"
        eta_cut = "eta"
        if event.is_sl:
            pt_cut  = "pt_sl"
            eta_cut = "eta_sl"
        elif event.is_dl:
            pt_cut  = "pt_dl"
            eta_cut = "eta_dl"
        
        #define lepton-channel specific selection function
        jetsel = lambda x, self=self: (
            x.pt > self.conf.jets[pt_cut]
            and abs(x.eta) < self.conf.jets[eta_cut]
            and self.conf.jets["selection"](x)
        )
        
        jetsel_loose_pt = lambda x, self=self: (
            x.pt > 20
            and abs(x.eta) < self.conf.jets[eta_cut]
            and self.conf.jets["selection"](x)
        )

        #Identify loose jets by (pt, eta)
        loose_jets = sorted(filter(
            jetsel_loose_pt, event.injets 
            ), key=lambda x: x.pt, reverse=True
        )

        #Take care of overlaps between jets and veto leptons
        jets_to_remove = []
        for lep in event.veto_leptons:
            #overlaps removed by delta R
            for jet in loose_jets:
                lv1 = lvec(jet)
                lv2 = lvec(lep)
                dr = lv1.DeltaR(lv2)
                if dr < 0.4:
                    if "jets" in self.conf.general["verbosity"] or "debug" in self.conf.general["verbosity"]:
                        autolog("[jet lepton cleaning] deltaR", dr, lep.pt, lep.eta, lep.phi, jet.pt, jet.eta, jet.phi)
                    jets_to_remove += [jet]

        #Now actually remove the overlapping jets
        for jet in jets_to_remove:
            if "jets" in self.conf.general["verbosity"] or "debug" in self.conf.general["verbosity"]:
                autolog("removing jet", jet.pt, jet.eta)
            if jet in loose_jets:
                loose_jets.remove(jet)
        
        #in DL apply two-stage pt cuts
        #Since this relies on jet counting, needs to be done **after** any other jet filtering
        if event.is_dl:
            good_jets_dl = []
            for jet in loose_jets:
                if len(good_jets_dl) < 2:
                    ptcut = self.conf.jets["pt_sl"]
                else:
                    ptcut = self.conf.jets["pt_dl"]
                if jet.pt > ptcut:
                    good_jets_dl += [jet]
            loose_jets = good_jets_dl

        #Now apply true pt cuts to identify analysis jets
        event.good_jets = filter(jetsel, loose_jets)
        event.loose_jets = filter(lambda x, event=event: x not in event.good_jets, loose_jets) 

        if "debug" in self.conf.general["verbosity"]:
            autolog("All jets: ", len(event.injets))
            for x in event.injets:
                autolog(str(x))
            autolog("Loose jets: ", len(event.loose_jets))
            for x in event.loose_jets:
                autolog(str(x))
            autolog("Good jets: ", len(event.good_jets))
            for x in event.good_jets:
                autolog(str(x))

        #Assing jet transfer functions
        for jet in event.loose_jets + event.good_jets:
            attach_jet_transfer_function(jet, self.conf)

        event.numJets = len(event.good_jets)

        event.btagged_jets_bdisc = {}
        event.buntagged_jets_bdisc = {}
        for (btag_wp_name, btag_wp) in self.conf.jets["btagWPs"].items():
            algo, wp = btag_wp
            event.btagged_jets_bdisc[btag_wp_name] = filter(
                lambda x, algo=algo, wp=wp: getattr(x, algo) > wp,
                event.good_jets
            )
            event.buntagged_jets_bdisc[btag_wp_name] = filter(
                lambda x, algo=algo, wp=wp: getattr(x, algo) <= wp,
                event.good_jets
            )
            if "jets" in self.conf.general["verbosity"] or "debug" in self.conf.general["verbosity"]:
                autolog("btagged jets", btag_wp_name, btag_wp, len(event.btagged_jets_bdisc[btag_wp_name]))
            setattr(event, "nB"+btag_wp_name, len(event.btagged_jets_bdisc[btag_wp_name]))

        #Find jets that pass/fail the specified default b-tagging algo/working point
        event.buntagged_jets_bdisc = event.buntagged_jets_bdisc[self.conf.jets["btagWP"]]
        event.btagged_jets_bdisc = event.btagged_jets_bdisc[self.conf.jets["btagWP"]]

        #Find how many of these tagged jets are actually true b jets
        if self.cfg_comp.isMC:
            event.n_tagwp_tagged_true_bjets = 0
            for j in event.btagged_jets_bdisc:
                if abs(j.mcFlavour) == 5:
                    event.n_tagwp_tagged_true_bjets += 1

        #Require at least 2 good resolved jets to continue analysis
        passes = True
        if event.systematic == "nominal":
            event_proxy = event
        else:
            event_proxy = evdict["nominal"]
        if event.is_sl and not (len(event_proxy.good_jets) >= 4 and event_proxy.nBCSVM>=3):
            if "debug" in self.conf.general["verbosity"]:
                autolog("fails because SL NJ<3")
            passes = False
        elif event.is_dl:
            if not (len(event_proxy.good_jets) >= 4 and event_proxy.nBCSVM>=3):
                if "debug" in self.conf.general["verbosity"]:
                    autolog("fails because DL NJ<2")
                passes = False
        elif event.is_fh:
            if len(event.good_jets) < self.conf.jets["minjets_fh"]: #DS
                passes = False        
            if len(event.good_jets) >= self.conf.jets["minjets_fh"]:
                if event.good_jets[ self.conf.jets["nhard_fh"]-1 ].pt<self.conf.jets["pt_fh"]:
                    passes = False


        #Calculate jet corrections to MET
        corrMet_px = event.MET.px
        corrMet_py = event.MET.py
        sum_dEx = 0
        sum_dEy = 0
        if self.cfg_comp.isMC:
            for jet in event.good_jets:
                Prec = lvec(jet)
                Pgen = lvec(jet)
                Pgen.SetPtEtaPhiM(jet.mcPt, jet.mcEta, jet.mcPhi, jet.mcM)
                Erec = Prec.E()
                Egen = Pgen.E()
                dEx = (Erec-Egen) * Prec.Px()/Prec.P()
                dEy = (Erec-Egen) * Prec.Py()/Prec.P()
                sum_dEx += dEx
                sum_dEy += dEy
        corrMet_px += sum_dEx
        corrMet_py += sum_dEy
        event.MET_jetcorr = MET(px=corrMet_px, py=corrMet_py)
        event.passes_jet = passes
        
        #Do gen-jet analysis
        if self.cfg_comp.isMC:
            genjets = event.GenJet
            for jet in event.good_jets:
                pt1 = jet.mcPt
                eta1 = jet.mcEta
                phi1 = jet.mcPhi
                mass1 = jet.mcM
                lv1 = ROOT.TLorentzVector()
                lv1.SetPtEtaPhiM(pt1, eta1, phi1, mass1)
                for gj in genjets:
                    lv2 = lvec(gj)
                    if lv1.DeltaR(lv2) < 0.01:
                        jet.genjet = gj
                        genjets.remove(gj)
                        break
        event.ht = sum(map(lambda x: x.pt, event.good_jets))
        return event
