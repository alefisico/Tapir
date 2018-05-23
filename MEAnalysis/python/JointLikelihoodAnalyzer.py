import ROOT
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")
from ROOT import MEM

import numpy as np

from TTH.MEAnalysis.MEMUtils import set_integration_vars, add_obj
from TTH.MEAnalysis.MEMConfig import MEMConfig

import logging

LOG_MODULE_NAME = logging.getLogger(__name__)

from TTH.MEAnalysis.Analyzer import FilterAnalyzer

# function to calculate the joint likelihood ratio using the MEM::Integrand::scattering function
class JointLikelihoodAnalyzer(FilterAnalyzer):
    """
    Perfomrs the calculation of the joint likelihood ratio using the MEM::Integrand::scattering function
    in order to follow the approach presented in https://arxiv.org/pdf/1805.00013.pdf

    It stores the output for the parton-level distributions from matrix element for ttH and ttbb.    

    The ME algorithms are run only in case the njet/nlep/Wtag category (event.cat)
    is in the accepted categories specified in the config.
    Additionally, we require the b-tagging category (event.cat_btag) to be "H" (high).

    For each ME configuration on each event, the jets which are counted to be b-tagged
    in event.selected_btagged_jets_high are added as the candidates for t->b (W) or h->bb.
    These jets must be exactly 4, otherwise no permutation is accepted (in case
    using BTagged/QUntagged assumptions).

    Any additional jets are assumed to come from the hadronic W decay. These are
    specified in event.wquark_candidate_jets.

    Based on the event njet/nlep/Wtag category, if a jet fmor the W is counted as missing,
    it is integrated over using additional variables set by self.vars_to_integrate.

    self.vars_to_integrate_any contains the list of particles which are integrated over assuming
    perfect reconstruction efficiency.

    The MEM top pair hypothesis (di-leptonic or single leptonic top pair) is chosen based
    on the reconstructed lepton multiplicity (event.good_leptons).

    The algorithm is shortly as follows:
    1. check if event passes event.cat and event.cat_btag
    2. loop over all MEM configurations i=[0...Nmem)
        2a. add all 4 b-tagged jets to integrator
        2b. add all 0-3 untagged jets to integrator
        2c. add all leptons to integrator
        2d. decide SL/DL top pair hypo based on leptons
        2e. based on event.cat, add additional integration vars
        2f. run ME integrator for both tth and ttbb hypos
        2g. save output in event.mem_output_tth[i] (or ttbb)
        2i. clean up event in integrator

    Relies on:
    event.good_jets, event.good_leptons, event.cat, event.input.met_pt

    Produces:
    mem_results_tth (MEMOutput): probability for the tt+H(bb) hypothesis
    mem_results_ttbb (MEMOutput): probability for the tt+bb hypothesis

    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(FilterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

        self.mem_configs = self.conf.mem_configs

        self.save = True

        cfg = MEMConfig(self.conf)
        self.integrator = MEM.Integrand(
            0,#verbosity (debug code) 1=output,2=input,4=init,8=init_more,16=event,32=integration
            cfg.cfg
        )

        #self.mem_configs = self.conf.mem_configs
        #self.memkeysToRun = self.conf.mem["methodsToRun"]

        #cfg = MEMConfig(self.conf)
        #cfg.configure_transfer_function(self.conf)
        #cfg.cfg.num_jet_variations = len(self.conf.mem["jet_corrections"])
        #self.integrator = MEM.Integrand(
        #    0,#verbosity (debug code) 1=output,2=input,4=init,8=init_more,16=event,32=integration
        #    cfg.cfg
        #)

    def beginLoop(self, setup):
        super(FilterAnalyzer, self).beginLoop(setup)

    def process(self, event):

        if self.cfg_comp.isMC:

            print "Event number:", event.evt

            # get inputs for scattering amplitudes
            #double MEM::Integrand::scattering(const LV &top, const LV &atop, const LV &b1,
            #                      const LV &b2, const LV &additional_jet,
            #                      double &x1, double &x2)



            idx = [(event.GenParticle[p].genPartIdxMother, event.GenParticle[p].pdgId) for p in range(len(event.GenParticle))]
            print idx

            # get inital-state partons
            #IS = [(i, tupl) for i, tupl in enumerate(idx) if tupl[0] == -1]
            #x1 = ROOT.TLorentzVector()
            #x1.SetPtEtaPhiM(event.GenParticle[IS[0][0]].pt, event.GenParticle[IS[0][0]].eta, event.GenParticle[IS[0][0]].phi, event.GenParticle[IS[0][0]].mass)
            #x2 = ROOT.TLorentzVector()
            #x2.SetPtEtaPhiM(event.GenParticle[IS[1][0]].pt, event.GenParticle[IS[1][0]].eta, event.GenParticle[IS[1][0]].phi, event.GenParticle[IS[1][0]].mass)

            # get top/antitop and bottom/anti-bottom LV 
            HS = [(i, tupl) for i, tupl in enumerate(idx) if tupl[0] == 0]
            top = ROOT.TLorentzVector()
            atop = ROOT.TLorentzVector()
            bottom = ROOT.TLorentzVector()
            abottom = ROOT.TLorentzVector()
            add_rad = ROOT.TLorentzVector()

            # !! only implemented so far for ttH(H->bb) sample
            for p in HS:
                
                # top quark
                if p[1][1] == 6:
                    top.SetPtEtaPhiM(event.GenParticle[p[0]].pt, event.GenParticle[p[0]].eta, event.GenParticle[p[0]].phi, event.GenParticle[p[0]].mass)
                # anti-top quark
                elif p[1][1] == -6:
                    atop.SetPtEtaPhiM(event.GenParticle[p[0]].pt, event.GenParticle[p[0]].eta, event.GenParticle[p[0]].phi, event.GenParticle[p[0]].mass)

                # Higgs decay
                elif p[1][1] == 25:
        
                    j = p[0]
                    while j < len(event.GenParticle):
                        decay = [(i,tupl) for i,tupl in enumerate(idx) if tupl[0] == j]
                        print decay
                        if len(decay) == 1:
                            j = decay[0][0]
                        else:
                            break
                    for d in decay:
                        if d[1][1] == 5:
                            bottom.SetPtEtaPhiM(event.GenParticle[d[0]].pt, event.GenParticle[d[0]].eta, event.GenParticle[d[0]].phi, event.GenParticle[d[0]].mass)    
                        if d[1][1] == -5:
                            abottom.SetPtEtaPhiM(event.GenParticle[d[0]].pt, event.GenParticle[d[0]].eta, event.GenParticle[d[0]].phi, event.GenParticle[d[0]].mass)   

                # additional radiation
                #else:
                #    add_rad.SetPtEtaPhiM(event.GenParticle[p[0]].pt, event.GenParticle[p[0]].eta, event.GenParticle[p[0]].phi, event.GenParticle[p[0]].mass)


            # check if enough information to compute joint likelihood, o.w. set all values to -9999
            if bottom == ROOT.TLorentzVector() or abottom == ROOT.TLorentzVector() or top == ROOT.TLorentzVector() or atop == ROOT.TLorentzVector():
    
                event.prob_ttHbb = -9999
                event.prob_ttbb = -9999
                event.jointlikelihood = -9999

            else:

                # call MEM scattering to get the probability for hypo = TTH and hypo = TTBB
                prob = {}
                # TTH
                self.integrator.set_hypo(MEM.Hypothesis.TTH)
                prob["ttHbb"] = self.integrator.scattering(top, atop, bottom, abottom, add_rad, ROOT.Double(0), ROOT.Double(0))
                # TTBB
                self.integrator.set_hypo(MEM.Hypothesis.TTBB)
                prob["ttbb"] = self.integrator.scattering(top, atop, bottom, abottom, add_rad, ROOT.Double(0), ROOT.Double(0))
                print prob

                event.prob_ttHbb = prob["ttHbb"]    
                event.prob_ttbb = prob["ttbb"]

                r = prob["ttbb"]/prob["ttHbb"]
                print r
                event.jointlikelihood = r

            if self.save == True:

                event.jlr_top = top
                event.jlr_atop = atop
                event.jlr_bottom = bottom
                event.jlr_abottom = abottom
                event.jlr_addRad = add_rad

        return True        
