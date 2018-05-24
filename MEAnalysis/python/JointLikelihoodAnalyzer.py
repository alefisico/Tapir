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
