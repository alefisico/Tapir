#!/usr/bin/env python
import os, sys
from collections import OrderedDict
from itertools import permutations
import numpy as np
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

### ttbar classification
#ttCls = OrderedDict()
#ttCls['ttll'] = '(event.genTtbarId<1)'
#ttCls['ttcc'] = '(event.genTtbarId>40) && (event.genTtbarId<50)'
#ttCls['ttb'] = '(event.genTtbarId==51)'
#ttCls['tt2b'] = '(event.genTtbarId==52)'
#ttCls['ttbb'] = '(event.genTtbarId>52) && (event.genTtbarId<57)'

rhalPtList = [ 250, 300, 350, 400, 450, 500, 550, 600, 700, 800, 1000, 10000 ]

class boostedAnalyzer(Module):
    def __init__(self, sample="None", leptonSFhelper={}, year='2017'):
	self.writeHistFile=True
        self.sample = sample
        self.leptonSFhelper = leptonSFhelper
        self.year = year

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

        self.addObject( ROOT.TH1F('nEvents',   ';number of events in category',   10, 0, 10) )
        self.addObject( ROOT.TH1F('cutFlow',   ';number of events in selection',   10, 0, 10) )
        self.addObject( ROOT.TH1F('cutFlow_weight',   ';number of events in selection',   10, 0, 10) )
        self.addObject( ROOT.TH1F('cutFlow_genWeight',   ';number of events in selection',   10, 0, 10) )
        self.addObject( ROOT.TH1F('muon_pt',  ';p_{T} (GeV)',   200, 0, 2000) )
        self.addObject( ROOT.TH1F('muon_eta', ';#eta', 100, -4.0, 4.0 ) )
        self.addObject( ROOT.TH1F('ele_pt',  ';p_{T} (GeV)',   200, 0, 2000) )
        self.addObject( ROOT.TH1F('ele_eta', ';#eta', 100, -4.0, 4.0 ) )
        self.addObject( ROOT.TH1F('nleps_2J2WNoWeight',   ';number of leptons',   20, 0, 20) )
        self.addObject( ROOT.TH1F('leadAK8JetPt_2J2WNoWeight',   ';Leading AK8 jet mass', 150, 0, 1500) )
        #### general selection
        for isel in [ '', '_noWeight', '_2J', '_2JNoWeight', '_2JMuon', '_2JElectron', '_2J2W', '_2J2WdeltaR', '_2J2WdeltaRTau21' ]:
            self.addObject( ROOT.TH1F('nPVs'+isel,   ';number of PVs',   100, 0, 100) )
            self.addObject( ROOT.TH1F('nleps'+isel,   ';number of leptons',   20, 0, 20) )
            self.addP4Hists( 'lepton', isel )
            self.addObject( ROOT.TH1F('njets'+isel,   ';number of AK4 jets',   20, 0, 20) )
            self.addP4Hists( 'jets', isel )
            self.addObject( ROOT.TH1F('nBjets'+isel,   ';number of AK4 b jets',   20, 0, 20) )
            self.addObject( ROOT.TH1F('nAK8jets'+isel,   ';number of AK8 jets',   20, 0, 20) )
            self.addObject( ROOT.TH1F('METPt'+isel,   ';MET (GeV)',   200, 0, 2000) )

            self.addObject( ROOT.TH1F('lepWMass'+isel,   ';Leptonic W candidate mass', 60, 0, 300) )
            self.addObject( ROOT.TH1F('lepWPt'+isel,   ';Leptonic W candidate pt ', 60, 0, 300) )
            self.addObject( ROOT.TH1F('leadAK8JetMass'+isel,   ';Leading AK8 jet mass', 60, 0, 300) )
            self.addObject( ROOT.TH1F('leadAK8JetPt'+isel,   ';Leading AK8 jet mass', 150, 0, 1500) )
            self.addObject( ROOT.TH1F('leadAK8JetRho'+isel,   ';#rho', 40, -10, 10) )
            self.addObject( ROOT.TH1F('leadAK8JetTau21'+isel,   ';#tau_{21}', 40, 0, 1) )
            self.addObject( ROOT.TH1F('leadAK8JetHbb'+isel,   ';Hbb discriminator', 40, 0, 1) )
            self.addObject( ROOT.TH1F('resolvedWCandMass'+isel,   ';W candidate mass', 60, 0, 300) )
            self.addObject( ROOT.TH1F('resolvedWCandPt'+isel,   ';W candidate pt', 60, 0, 300) )
            #self.addObject( ROOT.TH1F('boostedWCandMass'+isel,   ';W candidate mass', 60, 0, 300) )
            #self.addObject( ROOT.TH1F('boostedWCandPt'+isel,   ';W candidate pt', 60, 0, 300) )
            self.addObject( ROOT.TH1F('noHiggsCandMass'+isel,   ';Leading AK8 jet mass', 60, 0, 300) )
            self.addObject( ROOT.TH3F('leadAK8JetRhoPtHbb'+isel,   ';Leading AK8 jet rho; Leading AK8 jet pt; Hbb discriminator', 40, -10, 10, 150, 0, 1500, 40, 0, 1) )

            #### For ABCD
            #for side in [ 'A', 'B', 'C', 'D' ]:
            #    self.addObject( ROOT.TH2F('HbbvsTau21_'+side+isel,   ';', 20, 0, 1, 20, 0, 1) )
            #    self.addObject( ROOT.TH1F('leadAK8JetMass_'+side+isel,   ';Leading AK8 jet mass', 60, 0, 300) )

        #### For rhalphabet
        for isel in [ '2J2WdeltaRTau21_', '2J2WdeltaR_' ]:
            for ipass in [ 'Pass', 'Fail' ]:
                self.addObject( ROOT.TH1F('leadAK8JetMass_'+isel+ipass,   ';Leading AK8 jet mass', 60, 0, 300) )
                self.addObject( ROOT.TH1F('resolvedWCandMass_'+isel+ipass,   ';W candidate mass', 60, 0, 300) )
                self.addObject( ROOT.TH1F('leadAK8JetRho_'+isel+ipass,   ';Leading AK8 jet #rho', 40, -10, 10) )
                self.addObject( ROOT.TH1F('leadAK8JetTau21_'+isel+ipass,   ';#Leading AK8 jet tau_{21}', 40, 0, 1) )
                self.addObject( ROOT.TH1F('leadAK8JetHbb_'+isel+ipass,   ';Leading AK8 jet Hbb discriminator', 40, 0, 1) )
                self.addObject( ROOT.TH2F('leadAK8JetMassPt_'+isel+ipass,   ';Leading AK8 jet mass;Leading AK8 jet pt', 60, 0, 300,  1500, 0, 1500) )
                self.addObject( ROOT.TH2F('leadAK8JetRhoPt_'+isel+ipass,   ';Leading AK8 jet #rho;Leading AK8 jet pt', 40, -10, 10,  1500, 0, 1500) )
                self.addObject( ROOT.TH3F('leadAK8JetRhoPtMass_'+isel+ipass,   ';Leading AK8 jet #rho;Leading AK8 jet pt;Leading AK8 jet mass', 60, 0, 300,  1500, 0, 1500, 60, 0, 300) )


        ### additional single plots
        self.addObject( ROOT.TH1F('Trigger',   ';Trigger',   10, 0, 10) )
        self.addObject( ROOT.TH1F('PUweight',   ';PUWeight',   20, 0, 2) )
        self.addObject( ROOT.TH1F('Lepweight',   ';LepWeight',   20, 0, 2) )
        self.addObject( ROOT.TH1F('Totalweight',   ';TotalWeight',   20, 0, 2) )
        self.addObject( ROOT.TH1F('Lepweight_2JMuon',   ';Lepweight_2JMuon',   20, 0, 2) )
        self.addObject( ROOT.TH1F('Lepweight_Trigger_2JMuon',   ';Lepweight_Trigger_2JMuon',   20, 0, 2) )
        self.addObject( ROOT.TH1F('Lepweight_ID_2JMuon',   ';Lepweight_ID_2JMuon',   20, 0, 2) )
        self.addObject( ROOT.TH1F('Lepweight_ISO_2JMuon',   ';Lepweight_ISO_2JMuon',   20, 0, 2) )
        self.addObject( ROOT.TH1F('Lepweight_2JElectron',   ';Lepweight_2JElectron',   20, 0, 2) )
        self.addObject( ROOT.TH1F('Lepweight_Trigger_2JElectron',   ';Lepweight_Trigger_2JElectron',   20, 0, 2) )
        self.addObject( ROOT.TH1F('Lepweight_ID_2JElectron',   ';Lepweight_ID_2JElectron',   20, 0, 2) )
        self.addObject( ROOT.TH1F('Lepweight_ISO_2JElectron',   ';Lepweight_ISO_2JElectron',   20, 0, 2) )
        self.addObject( ROOT.TH1F('leadAK8JetN2',   ';#rho', 40, 0, 1) )
        self.addObject( ROOT.TH1F('leadAK8JetTau21DDT',   ';#tau_{21}^{DDT}', 40, 0, 1) )
        self.addObject( ROOT.TH2F('leadAK8JetdeepAK8HbbMDTop',   '', 40, 0, 1, 40, 0, 1) )
        self.addObject( ROOT.TH2F('leadAK8JetdeepAK8HbbMDDDB',   '', 40, 0, 1, 40, 0, 1) )
        self.addObject( ROOT.TH2F('resolvedWCandHiggsCandMass_2J',   ';W candidate mass', 60, 0, 300, 60, 0, 300) )
        self.addObject( ROOT.TH1F('deltaRJJ_2J',   ';deltaR( J, J )', 50, 0, 5 ) )
        self.addObject( ROOT.TH1F('deltaRhadWHiggs_2J',   ';deltaR( hadW, Higgs )', 50, 0, 5 ) )
        self.addObject( ROOT.TH2F('deltaRhadWHiggsMass_2J',   ';deltaR( hadW, Higgs );Leading jet msd', 50, 0, 5, 60, 0, 300 ) )
        self.addObject( ROOT.TH1F('deltaRlepWHiggs_2J',   ';deltaR( lepW, Higgs )', 50, 0, 5 ) )
        self.addObject( ROOT.TH2F('deltaRlepWHiggsMass_2J',   ';deltaR( lepW, Higgs );Leading jet msd', 50, 0, 5, 60, 0, 300 ) )
        self.addObject( ROOT.TH2F('deltaRlepWHiggsdeltaRhadWHiggs_2J',   ';deltaR( lepW, Higgs );deltaR( hadW, Higgs )', 50, 0, 5, 50, 0, 5 ) )
        self.addObject( ROOT.TH1F('deltaRlepWhadW_2J',   ';deltaR( lepW, hadW )', 50, 0, 5 ) )
        self.addObject( ROOT.TH2F('deltaRlepWhadWHiggsMass_2J',   ';deltaR( lepW, hadW );Leading jet msd', 50, 0, 5, 60, 0, 300 ) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_2J2W1B',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetPt_2J2W1B',   ';Leading AK8 jet mass', 150, 0, 1500) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_2J2W2B',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetPt_2J2W2B',   ';Leading AK8 jet mass', 150, 0, 1500) )
        self.addObject( ROOT.TH2F('leadAK8JetRhoTau21_2J2W',   ';#rho', 40, -10, 10, 40, 0, 1) )
        self.addObject( ROOT.TH3F('leadAK8JetPtMassHbb_2J2W',   ';#rho', 50, 100, 600, 30, 0, 300, 40, 0, 1) )
        self.addObject( ROOT.TH2F('resolvedWCandHiggsCandMass_2J2W',   ';W candidate mass', 60, 0, 300, 60, 0, 300) )
        self.addObject( ROOT.TH1F('minDiffLepHadW',   ';min difference between lep and had W',   100, 0, 100) )
        self.addObject( ROOT.TH1F('deltaRJJ_2J2W',   ';deltaR( J, J )', 50, 0, 5 ) )
        self.addObject( ROOT.TH1F('deltaRhadWHiggs_2J2W',   ';deltaR( hadW, Higgs )', 50, 0, 5 ) )
        self.addObject( ROOT.TH2F('deltaRhadWHiggsMass_2J2W',   ';deltaR( hadW, Higgs );Leading jet msd', 50, 0, 5, 60, 0, 300 ) )
        self.addObject( ROOT.TH1F('deltaRlepWHiggs_2J2W',   ';deltaR( lepW, Higgs )', 50, 0, 5 ) )
        self.addObject( ROOT.TH2F('deltaRlepWHiggsMass_2J2W',   ';deltaR( lepW, Higgs );Leading jet msd', 50, 0, 5, 60, 0, 300 ) )
        self.addObject( ROOT.TH2F('deltaRlepWHiggsdeltaRhadWHiggs_2J2W',   ';deltaR( lepW, Higgs );deltaR( hadW, Higgs )', 50, 0, 5, 50, 0, 5 ) )
        self.addObject( ROOT.TH1F('deltaRlepWhadW_2J2W',   ';deltaR( lepW, hadW )', 50, 0, 5 ) )
        self.addObject( ROOT.TH2F('deltaRlepWhadWHiggsMass_2J2W',   ';deltaR( lepW, hadW );Leading jet msd', 50, 0, 5, 60, 0, 300 ) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_2J1B',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('deltaR1BHiggs_2J1B',   ';deltaR( 1b, Higgs )', 50, 0, 5 ) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_2J2B',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_1B',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('deltaR1BHiggs_1B',   ';deltaR( 1b, Higgs )', 50, 0, 5 ) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_2B',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_2J2WdeltaR1B',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('resolvedWCandMass_2J2WdeltaR1B',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetRho_2J2WdeltaR1B',   ';#rho', 40, -10, 10) )
        self.addObject( ROOT.TH1F('leadAK8JetTau21_2J2WdeltaR1B',   ';#tau_{21}', 40, 0, 1) )
        self.addObject( ROOT.TH1F('leadAK8JetHbb_2J2WdeltaR1B',   ';Hbb discriminator', 40, 0, 1) )
        self.addObject( ROOT.TH1F('noHiggsCandMass_2J2WdeltaR1B',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_2J2WdeltaR2B',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('resolvedWCandMass_2J2WdeltaR2B',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetRho_2J2WdeltaR2B',   ';#rho', 40, -10, 10) )
        self.addObject( ROOT.TH1F('leadAK8JetTau21_2J2WdeltaR2B',   ';#tau_{21}', 40, 0, 1) )
        self.addObject( ROOT.TH1F('leadAK8JetHbb_2J2WdeltaR2B',   ';Hbb discriminator', 40, 0, 1) )
        self.addObject( ROOT.TH1F('noHiggsCandMass_2J2WdeltaR2B',   ';Leading AK8 jet mass', 60, 0, 300) )


        ###### OLD plots, just for archive
        self.addObject( ROOT.TH1F('nbadFatJets',   ';number of bad fatjets',   10, 0, 10) )
        self.addObject( ROOT.TH1F('ngoodEvents',   ';Good Events',   10, 0, 10) )
        self.addObject( ROOT.TH1F('TopCandMass',   ';Top candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('WCandMass',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('TopCandMass_TopHiggs',   ';Top candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('WCandMass_TopHiggs',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_TopHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('TopCandMass_WHiggs',   ';Top candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('WCandMass_WHiggs',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_WHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('TopCandMass_WTop',   ';Top candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('WCandMass_WTop',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_WTop',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('TopCandMass_Top',   ';Top candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('WCandMass_W',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_Higgs',   ';Leading AK8 jet mass', 60, 0, 300) )

        #self.addObject( ROOT.TH1F('nGoodPuppiJets_boostedW',   ';number of good puppi jets',   10, 0, 10) )
        #self.addObject( ROOT.TH1F('nGoodPuppiBjets_boostedW',   ';number of good puppi bjets',   10, 0, 10) )
        #self.addObject( ROOT.TH1F('WCandMass_boostedW',   ';W candidate mass', 60, 0, 300) )
        #self.addObject( ROOT.TH1F('boostedHiggsCandMass_boostedW',   ';boosted Leading AK8 jet mass', 60, 0, 300) )
        #self.addObject( ROOT.TH1F('minDiffLepHadTop',   ';min difference between lep and had Top',   100, 0, 100) )
        #self.addObject( ROOT.TH1F('lepTopCandMass_2B_boostedW',   ';leptonic Top candidate masses', 60, 0, 300) )
        #self.addObject( ROOT.TH1F('hadTopCandMass_2B_boostedW',   ';hadronic Top candidate masses', 60, 0, 300) )
        #self.addObject( ROOT.TH1F('boostedHiggsCandPt_2B_boostedW',   ';boosted Leading AK8 jet pt', 1000, 0, 1000) )
        #self.addObject( ROOT.TH1F('boostedHiggsCandMass_2B_boostedW',   ';boosted Leading AK8 jet mass', 60, 0, 300) )
        #self.addObject( ROOT.TH1F('resolvedHiggsCandPt_2B_boostedW',   ';resolved Leading AK8 jet pt', 1000, 0, 1000) )
        #self.addObject( ROOT.TH1F('resolvedHiggsCandMass_2B_boostedW',   ';resolved Leading AK8 jet mass', 60, 0, 300) )
        #self.addObject( ROOT.TH1F('resolvedHiggsCandMass_2Bpt_boostedW',   ';resolved Leading AK8 jet mass', 60, 0, 300) )
        #self.addObject( ROOT.TH1F('resolvedHiggsCandMass_2BdeltaR_boostedW',   ';resolved Leading AK8 jet mass', 60, 0, 300) )
        #self.addObject( ROOT.TH1F('resolvedHiggsCandMass_2BSmallR_boostedW',   ';resolved Leading AK8 jet mass', 60, 0, 300) )
        #self.addObject( ROOT.TH1F('noResolvedHiggsCandMass_2BSmallR_boostedW',   ';resolved Leading AK8 jet mass', 60, 0, 300) )
        #self.addObject( ROOT.TH1F('simplejjMass_2J_boostedW',   ';resolved dijet mass', 60, 0, 300) )
        #self.addObject( ROOT.TH1F('simplejjMass_2JSmallR_boostedW',   ';resolved dijet mass', 60, 0, 300) )
        #self.addObject( ROOT.TH1F('allResolvedHiggsCandPt_2B_boostedW',   ';resolved Leading AK8 jet pt', 1000, 0, 1000) )
        #self.addObject( ROOT.TH1F('allResolvedHiggsCandMass_2B_boostedW',   ';resolved Leading AK8 jet mass', 60, 0, 300) )
        #self.addObject( ROOT.TH2F('allResolvedHiggsCandMassPt_2B_boostedW',   ';resolved Leading AK8 jet mass', 60, 0, 300, 100, 0, 1000) )
        #self.addObject( ROOT.TH1F('deltaR2B_2B_boostedW',   ';deltaR( b, b )', 50, 0, 5 ) )
        #self.addObject( ROOT.TH2F('deltaResHiggs_2B_boostedW',   ';', 500, -500, 500, 60, 0, 300) )
        #self.addObject( ROOT.TH2F('ptMassResHiggs_2B_boostedW',   ';', 500, -500, 500, 60, 0, 300) )

        #self.addObject( ROOT.TH1F('leadingBjetPt_2B_boostedW',   ';leading Bjet p_{T} (GeV)',   500, 0, 5000) )
        #self.addObject( ROOT.TH1F('leadingBjetEta_2B_boostedW',  ';leading Bjet #eta', 100, -4.0, 4.0 ) )
        #self.addObject( ROOT.TH1F('leadingBjetBdisc_2B_boostedW', ';leading Bjet Discriminator', 40, -1, 1) )
        #self.addObject( ROOT.TH1F('subleadingBjetPt_2B_boostedW',   ';subleading Bjet p_{T} (GeV)',   500, 0, 5000) )
        #self.addObject( ROOT.TH1F('subleadingBjetEta_2B_boostedW',  ';subleading Bjet #eta', 100, -4.0, 4.0 ) )
        #self.addObject( ROOT.TH1F('subleadingBjetBdisc_2B_boostedW', ';subleading Bjet Discriminator', 40, -1, 1) )
        #self.addObject( ROOT.TH2F('nJetsvsTau21_boostedW',   ';', 10, 0, 10, 20, 0, 1) )

        '''
        for icut in ['presel', 'preselWeighted',  'lep', 'lepWeighted', 'met', 'metWeighted', 'jet', 'jetWeighted', 'bDeepCSV', 'bDeepCSVWeighted', 'bDeepFlav', 'bDeepFlavWeighted' ]:
            #if self.sample.startswith('TTTo'):
            #    for ttXX, ttXXcond in ttCls.items():
            #        self.listOfHistos( '_'+ttXX+'_'+icut )
            #else:
                self.listOfHistos( '_'+icut )
        '''

    def addP4Hists(self, s, t ):
        self.addObject( ROOT.TH1F(s+'_pt'+t,  s+';p_{T} (GeV)',   200, 0, 2000) )
        self.addObject( ROOT.TH1F(s+'_eta'+t, s+';#eta', 100, -4.0, 4.0 ) )
        self.addObject( ROOT.TH1F(s+'_phi'+t, s+';#phi', 100, -3.14259, 3.14159) )
        self.addObject( ROOT.TH1F(s+'_mass'+t,s+';mass (GeV)', 100, 0, 1000) )
        if s.startswith('jet'):
            self.addObject( ROOT.TH1F(s+'_bDeepFlav'+t, s+';b Discriminator', 40, 0, 1) )

    def leptonSF(self, lepton, leptonP4 ):

        if lepton.startswith("muon"): leptonP4eta = abs(leptonP4.eta)
        else: leptonP4eta = leptonP4.eta

        SFFileTrigger = ROOT.TFile( os.environ['CMSSW_BASE']+"/src/TTH/Analyzer/data/"+self.leptonSFhelper[lepton]['Trigger'][0] )
        histoSFTrigger = SFFileTrigger.Get( self.leptonSFhelper[lepton]['Trigger'][1] )
        SFTrigger = histoSFTrigger.GetBinContent( histoSFTrigger.GetXaxis().FindBin( leptonP4.pt ), histoSFTrigger.GetYaxis().FindBin( leptonP4eta ) )

        SFFileID = ROOT.TFile( os.environ['CMSSW_BASE']+"/src/TTH/Analyzer/data/"+self.leptonSFhelper[lepton]['ID'][0] )
        histoSFID = SFFileID.Get( self.leptonSFhelper[lepton]['ID'][1] )
        histoSFID_X = histoSFID.GetXaxis().FindBin( leptonP4.pt if self.leptonSFhelper[lepton]['ID'][2] else leptonP4eta )
        histoSFID_Y = histoSFID.GetYaxis().FindBin( leptonP4eta if self.leptonSFhelper[lepton]['ID'][2] else leptonP4.pt )
        SFID = histoSFID.GetBinContent( histoSFID_X, histoSFID_Y )
        SFID = SFID if SFID>0 else 1

        if self.year.startswith('2016') and lepton.startswith("muon"): leptonP4eta = leptonP4.eta    #### stupid fix for the stupid SF file
        SFFileISO = ROOT.TFile( os.environ['CMSSW_BASE']+"/src/TTH/Analyzer/data/"+self.leptonSFhelper[lepton]['ISO'][0] )
        histoSFISO = SFFileISO.Get( self.leptonSFhelper[lepton]['ISO'][1] )
        histoSFISO_X = histoSFISO.GetXaxis().FindBin( leptonP4.pt if self.leptonSFhelper[lepton]['ISO'][2] else leptonP4eta )
        histoSFISO_Y = histoSFISO.GetYaxis().FindBin( leptonP4eta if self.leptonSFhelper[lepton]['ISO'][2] else leptonP4.pt )
        SFISO = histoSFISO.GetBinContent( histoSFISO_X, histoSFISO_Y )
        SFISO = SFISO if SFISO>0 else 1

        #print (SFTrigger * SFID * SFISO), SFTrigger , SFID , SFISO, leptonP4.pt, leptonP4.eta
        return [SFTrigger , SFID , SFISO]

    def METzCalculator( self, lepton, MET ):
        '''Based on https://github.com/VPlusJetsAnalyzers/VPlusJets/blob/master/src/METzCalculator.cc'''
        M_W = 80.4
        M_mu = .1056  ## lepton mass
        emu = lepton.E()
        pxmu = lepton.Px()
        pymu = lepton.Py()
        pzmu = lepton.Pz()
        pxnu = MET.Px()
        pynu = MET.Py()
        pznu = 0

        a = M_W*M_W - M_mu*M_mu + 2.0*pxmu*pxnu + 2.0*pymu*pynu
        A = 4.0*(emu*emu - pzmu*pzmu)
        B = -4.0*a*pzmu
        C = 4.0*emu*emu*(pxnu*pxnu + pynu*pynu) - a*a
        #print(a, A, B, C)
        tmproot = B*B - 4.0*A*C

        if tmproot<0: pznu = - B/(2*A)
        else:
            tmpsol1 = (-B + ROOT.TMath.Sqrt(tmproot))/(2.0*A)
            tmpsol2 = (-B - ROOT.TMath.Sqrt(tmproot))/(2.0*A)
            if (abs(tmpsol2-pzmu) < abs(tmpsol1-pzmu)):
                pznu = tmpsol2
                #otherSol_ = tmpsol1
            else:
                pznu = tmpsol1
                #otherSol_ = tmpsol2
                #### if pznu is > 300 pick the most central root
                if ( pznu > 300. ):
                    if (abs(tmpsol1)<abs(tmpsol2) ):
                        pznu = tmpsol1
                        #otherSol_ = tmpsol2
                    else:
                        pznu = tmpsol2
                        #otherSol_ = tmpsol1

        return pznu

    def ABCDRegions(self, mass, var1, var2, cutA, cutB, cutC, cutD, histoVar1vsVar2, histoMass ):
        """docstring for ABCDRegions. Not used, just for archive"""

        getattr( self, histoVar1vsVar2.replace('__', '_') ).Fill(  var1, var2 )
        if cutA:
            getattr( self, histoVar1vsVar2.replace('__', '_A_') ).Fill(  var1, var2 )
            getattr( self, histoMass.replace('__', '_A_') ).Fill( mass )
        if cutB:
            getattr( self, histoVar1vsVar2.replace('__', '_B_') ).Fill(  var1, var2 )
            getattr( self, histoMass.replace('__', '_B_') ).Fill( mass )
        if cutC:
            getattr( self, histoVar1vsVar2.replace('__', '_C_') ).Fill(  var1, var2 )
            getattr( self, histoMass.replace('__', '_C_') ).Fill( mass )
        if cutD:
            getattr( self, histoVar1vsVar2.replace('__', '_D_') ).Fill(  var1, var2 )
            getattr( self, histoMass.replace('__', '_D_') ).Fill( mass )


#    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
#        self.out = wrappedOutputTree
#        self.out.branch("totalWeight",  "F");
#        self.out.branch("LeptonSFTrigger",  "F");
#        self.out.branch("LeptonSFISO",  "F");
#        self.out.branch("LeptonSFID",  "F");
#        self.out.branch("nGoodLep",  "I");
#        self.out.branch("GoodLep_pt",  "F", lenVar="nGoodLep");
#        self.out.branch("GoodLep_eta",  "F", lenVar="nGoodLep");
#        self.out.branch("GoodLep_phi",  "F", lenVar="nGoodLep");
#        self.out.branch("GoodLep_mass",  "F", lenVar="nGoodLep");
#        self.out.branch("nGoodJet",  "I");
#        self.out.branch("GoodJet_pt",  "F", lenVar="nGoodJet");
#        self.out.branch("GoodJet_eta",  "F", lenVar="nGoodJet");
#        self.out.branch("GoodJet_phi",  "F", lenVar="nGoodJet");
#        self.out.branch("GoodJet_mass",  "F", lenVar="nGoodJet");
#        self.out.branch("GoodJet_btagDeepCSV",  "F", lenVar="nGoodJet");
#        self.out.branch("GoodJet_btagDeepFlav",  "F", lenVar="nGoodJet");

    def analyze(self, event):

        isMC = event.run == 1

        isSLmu = False
        isDLmumu = False
        trigger = False
        if self.year.startswith('2016'):
            if (event.HLT_IsoMu24==1) or (event.HLT_IsoTkMu24==1):
                getattr( self, 'Trigger' ).Fill( 1 )
                isSLmu = True
                trigger = True
                if (event.HLT_IsoMu24==1): getattr( self, 'Trigger' ).Fill( 2 )
                else: getattr( self, 'Trigger' ).Fill( 3 )
            elif (event.HLT_Ele27_WPTight_Gsf==1):
                getattr( self, 'Trigger' ).Fill( 5 )
                isSLmu = False
                trigger = True
        elif self.year.startswith('2017'):
            if (event.HLT_IsoMu24_eta2p1==1) or (event.HLT_IsoMu27==1):
                getattr( self, 'Trigger' ).Fill( 1 )
                isSLmu = True
                trigger = True
                if (event.HLT_IsoMu24_eta2p1==1): getattr( self, 'Trigger' ).Fill( 2 )
                else: getattr( self, 'Trigger' ).Fill( 3 )
            elif (event.HLT_Ele35_WPTight_Gsf==1) or (event.HLT_Ele28_eta2p1_WPTight_Gsf_HT150==1):
                getattr( self, 'Trigger' ).Fill( 5 )
                isSLmu = False
                trigger = True
                if (event.HLT_Ele35_WPTight_Gsf==1): getattr( self, 'Trigger' ).Fill( 6 )
                else: getattr( self, 'Trigger' ).Fill( 7 )
        elif self.year.startswith('2018'):
            if (event.HLT_IsoMu24==1):
                getattr( self, 'Trigger' ).Fill( 1 )
                isSLmu = True
                trigger = True
            elif (event.HLT_Ele32_WPTight_Gsf==1) or (event.HLT_Ele28_eta2p1_WPTight_Gsf_HT150==1):
                getattr( self, 'Trigger' ).Fill( 3 )
                isSLmu = False
                trigger = True
                if (event.HLT_Ele32_WPTight_Gsf==1): getattr( self, 'Trigger' ).Fill( 4 )
                else: getattr( self, 'Trigger' ).Fill( 5 )
        else:
            getattr( self, 'Trigger' ).Fill( 10 )
            isDLmumu = False

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        fatjets = Collection(event, "FatJet")
        PV = Object(event, 'PV')
        MET = Object(event, 'MET')

        ### Muons
        vetoMuons = [ m for m in muons if (abs(m.eta)<2.4) and (m.pt>15) and (m.pfRelIso04_all<0.25) and (m.tightId==1) ]
        goodMuons = [ m for m in vetoMuons if (m.pt>29) and (m.pfRelIso04_all<0.15) ]
        for gm in goodMuons:
            getattr( self, 'muon_pt' ).Fill( gm.pt )
            getattr( self, 'muon_eta' ).Fill( gm.eta )


        ### Electrons
        vetoElectrons = [ e for e in electrons if (abs(e.eta)<2.4) and (e.pt>15) and not ( abs(e.deltaEtaSC+e.eta)>=1.4442 and abs(e.deltaEtaSC+e.eta)<=1.5660) and (e.cutBased>=4) ]
        goodElectrons = [ e for e in vetoElectrons if e.pt>30 ]
        for ge in goodElectrons:
            getattr( self, 'ele_pt' ).Fill( ge.pt )
            getattr( self, 'ele_eta' ).Fill( ge.eta )

        goodLeptons = goodMuons + goodElectrons
        goodLeptons.sort(key=lambda x:x.pt, reverse=True)

        if isMC:
            print(self.leptonSFhelper)
            if len(goodMuons)>0 and len(goodElectrons)==0 and isSLmu: leptonWeights= self.leptonSF( "muon", goodMuons[0] )
            elif len(goodMuons)==0 and len(goodElectrons)>0 and not isSLmu: leptonWeights = self.leptonSF( "electron", goodElectrons[0] )
            else: leptonWeights = [0, 0, 0]
        else: leptonWeights = [1, 1, 1]

        ### Jets
        looseJets = [ j for j in jets if (abs(j.eta)<2.4) and (j.pt>30) and (j.jetId>=2) and ( (j.puId>=4) if (j.pt<50) else True ) ]
        goodJets = looseJets if (len(looseJets)>0) and (looseJets[0].pt>30) else []
        goodJetsNoLep = [ j for j in goodJets for l in goodLeptons if j.p4().DeltaR(l.p4())>=0.4  ]

        ### Bjets
        goodBjetsDeepCSV = [ b for b in goodJetsNoLep if b.btagDeepB>0.4941 ]
        goodBjetsDeepFlav = [ b for b in goodJetsNoLep if b.btagDeepFlavB>0.3033 ]

        ### Fatjets
        looseFatJets = [ j for j in fatjets if (abs(j.eta)<2.4) and (j.pt>200) ]
        ## clones for further studies
        badFatJets = [ j for j in fatjets if (abs(j.eta)<2.4) and (j.pt>200) ]
        allFatJets = [ j for j in fatjets if (abs(j.eta)<2.4) and (j.pt>250) and (j.jetId>=2) ]
        goodFatJets = [ j for j in allFatJets for l in goodLeptons if j.p4().DeltaR(l.p4())>=0.8  ]
        #badFatJets_boostedW = [ j for j in fatjets if (abs(j.eta<2.4)) and (j.pt>200) ]

        ### Selection
        metcut = (MET.pt>20)
        nlepcut = (len(goodLeptons)==1)
        njetscut = (len(goodJetsNoLep)>3)
        nbjetscut = (len(goodBjetsDeepFlav)>1)

        #### Weight
        #if isMC: weight = event.puWeight * np.sign(event.genWeight) * np.prod(leptonWeights)
        if isMC: weight = event.puWeight * np.prod(leptonWeights) ## no genWeight, it is taken into account in the normalization after
        else: weight = 1
        #self.out.fillBranch('totalWeight', weight)

        getattr( self, 'cutFlow' ).Fill( 1 )
        getattr( self, 'cutFlow_weight' ).Fill( 1, weight )
        if isMC: getattr( self, 'cutFlow_genWeight' ).Fill( 1, event.genWeight )

        getattr( self, 'nEvents' ).Fill( 0 )
        if ( metcut and nlepcut ): getattr( self, 'nEvents' ).Fill( 1 )
        if ( metcut and nlepcut and (njetscut and nbjetscut) ) : getattr( self, 'nEvents' ).Fill( 2 )
        if ( metcut and nlepcut and not (njetscut and nbjetscut) ) : getattr( self, 'nEvents' ).Fill( 3 )
        if ( metcut and nlepcut and not (njetscut or nbjetscut) ) : getattr( self, 'nEvents' ).Fill( 4 )

        #################################### Boosted
        if trigger and metcut and nlepcut and (len(goodFatJets)>0):

            #print( 'basic', event.run, event.luminosityBlock, int(event.event) )
            getattr( self, 'cutFlow' ).Fill( 2 )
            getattr( self, 'cutFlow_weight' ).Fill( 2, weight )
            if isMC: getattr( self, 'cutFlow_genWeight' ).Fill( 2, event.genWeight )

            ### General
            if isMC:
                getattr( self, 'PUweight' ).Fill( event.puWeight )
                getattr( self, 'Lepweight' ).Fill( np.prod(leptonWeights) )
            getattr( self, 'Totalweight' ).Fill( weight )
            getattr( self, 'nPVs' ).Fill( PV.npvsGood, weight )
            getattr( self, 'nleps' ).Fill( len(goodLeptons), weight )
            getattr( self, 'lepton_pt' ).Fill( goodLeptons[0].pt, weight )
            getattr( self, 'lepton_eta' ).Fill( goodLeptons[0].eta, weight )
            getattr( self, 'lepton_phi' ).Fill( goodLeptons[0].phi, weight )
            getattr( self, 'njets' ).Fill( len(goodJetsNoLep), weight )
            for ijet in goodJetsNoLep:
                getattr( self, 'jets_pt' ).Fill( ijet.pt, weight )
                getattr( self, 'jets_eta' ).Fill( ijet.eta, weight )
                getattr( self, 'jets_phi' ).Fill( ijet.phi, weight )
                getattr( self, 'jets_bDeepFlav' ).Fill( ijet.btagDeepFlavB, weight )
            getattr( self, 'nBjets' ).Fill( len(goodBjetsDeepFlav), weight )
            getattr( self, 'nAK8jets' ).Fill( len(goodFatJets), weight )
            getattr( self, 'METPt' ).Fill( MET.pt, weight )

            ### Leptonic W
            METp4 = ROOT.TLorentzVector()
            METp4.SetPtEtaPhiM( MET.pt, 0, MET.phi, 0 )#MET.pt )
            neuPz = self.METzCalculator( goodLeptons[0].p4(), METp4 )
            neutrinoP4 = ROOT.TLorentzVector()
            neutrinoP4.SetPxPyPzE( METp4.Px(), METp4.Py(), neuPz, ROOT.TMath.Sqrt( METp4.Px()*METp4.Px() + METp4.Py()*METp4.Py() + neuPz*neuPz )  )
            lepW = goodLeptons[0].p4() + neutrinoP4
            getattr( self, 'lepWMass' ).Fill( lepW.M(), weight )
            getattr( self, 'lepWPt' ).Fill( lepW.Pt(), weight )

            ### Leading AK8 jet (higgs candidate) without Higgs conditions yet
            Hbbcut = 0.8945 ## L: 0.6795 M: 0.8945 T: 0.9805
            tau21cut = 0.35 ## L: 0.55 M: 0.45 T: 0.35
            tau21DDTcut = 0.43
            FatJet_msoftdrop = goodFatJets[0].msoftdrop
            FatJet_pt = goodFatJets[0].pt
            #FatJet_Hbb = goodFatJets[0].btagDDBvL
            #FatJet_Hbb = goodFatJets[0].deepTag_H
            FatJet_Hbb = goodFatJets[0].deepTagMD_ZHbbvsQCD
            FatJet_Top = goodFatJets[0].deepTagMD_TvsQCD
            FatJet_tau21 = goodFatJets[0].tau2/goodFatJets[0].tau1 if goodFatJets[0].tau1>0 else -9999
            FatJet_rho = ROOT.TMath.Log( FatJet_msoftdrop*FatJet_msoftdrop/(FatJet_pt*FatJet_pt) )
            FatJet_tau21DDT = FatJet_tau21 + 0.08 * ROOT.TMath.Log( FatJet_msoftdrop*FatJet_msoftdrop/(FatJet_pt) )
            getattr( self, 'leadAK8JetMass' ).Fill( FatJet_msoftdrop, weight )
            getattr( self, 'leadAK8JetPt' ).Fill( FatJet_pt, weight )
            getattr( self, 'leadAK8JetRho' ).Fill( FatJet_rho, weight )
            getattr( self, 'leadAK8JetTau21' ).Fill( FatJet_tau21, weight )
            getattr( self, 'leadAK8JetTau21DDT' ).Fill( FatJet_tau21DDT, weight )
            getattr( self, 'leadAK8JetN2' ).Fill( goodFatJets[0].n2b1, weight )
            getattr( self, 'leadAK8JetHbb' ).Fill( FatJet_Hbb, weight )
            getattr( self, 'leadAK8JetdeepAK8HbbMDTop' ).Fill( FatJet_Hbb, goodFatJets[0].deepTagMD_TvsQCD, weight )
            getattr( self, 'leadAK8JetdeepAK8HbbMDDDB' ).Fill( FatJet_Hbb, goodFatJets[0].btagDDBvL, weight )

            #### test NO weight
            getattr( self, 'nPVs_noWeight' ).Fill( PV.npvsGood )
            getattr( self, 'nleps_noWeight' ).Fill( len(goodLeptons) )
            getattr( self, 'lepton_pt_noWeight' ).Fill( goodLeptons[0].pt )
            getattr( self, 'lepton_eta_noWeight' ).Fill( goodLeptons[0].eta )
            getattr( self, 'lepton_phi_noWeight' ).Fill( goodLeptons[0].phi )
            getattr( self, 'njets_noWeight' ).Fill( len(goodJetsNoLep) )
            for ijet in goodJetsNoLep:
                getattr( self, 'jets_pt_noWeight' ).Fill( ijet.pt )
                getattr( self, 'jets_eta_noWeight' ).Fill( ijet.eta )
                getattr( self, 'jets_phi_noWeight' ).Fill( ijet.phi )
                getattr( self, 'jets_bDeepFlav_noWeight' ).Fill( ijet.btagDeepFlavB )
            getattr( self, 'nBjets_noWeight' ).Fill( len(goodBjetsDeepFlav) )
            getattr( self, 'nAK8jets_noWeight' ).Fill( len(goodFatJets) )
            getattr( self, 'METPt_noWeight' ).Fill( MET.pt )
            getattr( self, 'leadAK8JetMass_noWeight' ).Fill( FatJet_msoftdrop )
            getattr( self, 'leadAK8JetPt_noWeight' ).Fill( FatJet_pt )
            getattr( self, 'leadAK8JetRho_noWeight' ).Fill( FatJet_rho )
            getattr( self, 'leadAK8JetTau21_noWeight' ).Fill( FatJet_tau21 )
            getattr( self, 'leadAK8JetHbb_noWeight' ).Fill( FatJet_Hbb )

            ### AK4 jets without overlap of leading AK8 jet
            cleanJets_Hcand = [ j for j in goodJetsNoLep if (j.p4().DeltaR(goodFatJets[0].p4())>=1.2)  ]
            goodBjets_Hcand = [ j for j in goodBjetsDeepFlav if (j.p4().DeltaR(goodFatJets[0].p4())>=1.2)  ]
            goodJets_Hcand = [ q for q in cleanJets_Hcand if q not in goodBjets_Hcand ]

            #### At least 2 jets for hadronic W
            if len(goodJets_Hcand)>1:
                #print event.event, ( 'Muon' if isSLmu else 'Ele'), 'nleptons ', len(goodLeptons), ' nAK4jets ', len(goodJetsNoLep), ' nAK8jets ', len(goodFatJets), '  good nAK4jets ', len(goodJets_Hcand), ' pt/mass/msoftdrop/eta AK8jet ', goodFatJets[0].pt, goodFatJets[0].mass, goodFatJets[0].msoftdrop, goodFatJets[0].eta,' pt/eta lepton ', goodLeptons[0].pt, goodLeptons[0].eta, ' MET ', MET.pt, ' weights ', event.puWeight, np.prod(leptonWeights), leptonWeights, weight
                #print( '2J', event.run, event.luminosityBlock, int(event.event) )
                getattr( self, 'cutFlow' ).Fill( 3 )
                getattr( self, 'cutFlow_weight' ).Fill( 3, weight )
                if isMC: getattr( self, 'cutFlow_genWeight' ).Fill( 3, event.genWeight )

                getattr( self, 'nEvents' ).Fill( 7 )
                if not (njetscut and nbjetscut): getattr( self, 'nEvents' ).Fill( 8 )
                getattr( self, 'nPVs_2J').Fill( PV.npvsGood, weight )
                getattr( self, 'nleps_2J').Fill( len(goodLeptons), weight )
                getattr( self, 'lepton_pt_2J').Fill( goodLeptons[0].pt, weight )
                getattr( self, 'lepton_eta_2J').Fill( goodLeptons[0].eta, weight )
                getattr( self, 'lepton_phi_2J').Fill( goodLeptons[0].phi, weight )
                getattr( self, 'njets_2J').Fill( len(goodJets_Hcand), weight )
                for ijet in goodJets_Hcand:
                    getattr( self, 'jets_pt_2J').Fill( ijet.pt, weight )
                    getattr( self, 'jets_eta_2J').Fill( ijet.eta, weight )
                    getattr( self, 'jets_phi_2J').Fill( ijet.phi, weight )
                    getattr( self, 'jets_bDeepFlav_2J' ).Fill( ijet.btagDeepFlavB, weight )
                getattr( self, 'nBjets_2J').Fill( len(goodBjets_Hcand), weight )
                getattr( self, 'nAK8jets_2J' ).Fill( len(goodFatJets), weight )
                getattr( self, 'METPt_2J').Fill( MET.pt, weight )
                getattr( self, 'lepWMass_2J').Fill( lepW.M(), weight )
                getattr( self, 'lepWPt_2J').Fill( lepW.Pt(), weight )
                getattr( self, 'leadAK8JetMass_2J').Fill( FatJet_msoftdrop, weight )
                getattr( self, 'leadAK8JetPt_2J').Fill( FatJet_pt, weight )
                getattr( self, 'leadAK8JetRho_2J').Fill( FatJet_rho, weight )
                getattr( self, 'leadAK8JetTau21_2J').Fill( FatJet_tau21, weight )
                getattr( self, 'leadAK8JetHbb_2J').Fill( FatJet_Hbb, weight )

                #### test only Muons
                if isSLmu:
                    if isMC:
                        getattr( self, 'Lepweight_2JMuon' ).Fill( np.prod(leptonWeights) )
                        getattr( self, 'Lepweight_Trigger_2JMuon' ).Fill( leptonWeights[0] )
                        getattr( self, 'Lepweight_ID_2JMuon' ).Fill( leptonWeights[1] )
                        getattr( self, 'Lepweight_ISO_2JMuon' ).Fill( leptonWeights[2] )
                    getattr( self, 'nPVs_2JMuon').Fill( PV.npvsGood, weight )
                    getattr( self, 'nleps_2JMuon').Fill( len(goodLeptons), weight )
                    getattr( self, 'lepton_pt_2JMuon').Fill( goodLeptons[0].pt, weight )
                    getattr( self, 'lepton_eta_2JMuon').Fill( goodLeptons[0].eta, weight )
                    getattr( self, 'lepton_phi_2JMuon').Fill( goodLeptons[0].phi, weight )
                    getattr( self, 'njets_2JMuon').Fill( len(goodJets_Hcand), weight )
                    for ijet in goodJets_Hcand:
                        getattr( self, 'jets_pt_2JMuon').Fill( ijet.pt, weight )
                        getattr( self, 'jets_eta_2JMuon').Fill( ijet.eta, weight )
                        getattr( self, 'jets_phi_2JMuon').Fill( ijet.phi, weight )
                        getattr( self, 'jets_bDeepFlav_2JMuon' ).Fill( ijet.btagDeepFlavB, weight )
                    getattr( self, 'nBjets_2JMuon').Fill( len(goodBjets_Hcand), weight )
                    getattr( self, 'nAK8jets_2JMuon' ).Fill( len(goodFatJets), weight )
                    getattr( self, 'METPt_2JMuon').Fill( MET.pt, weight )
                    getattr( self, 'lepWMass_2JMuon').Fill( lepW.M(), weight )
                    getattr( self, 'lepWPt_2JMuon').Fill( lepW.Pt(), weight )
                    getattr( self, 'leadAK8JetMass_2JMuon').Fill( FatJet_msoftdrop, weight )
                    getattr( self, 'leadAK8JetPt_2JMuon').Fill( FatJet_pt, weight )
                    getattr( self, 'leadAK8JetRho_2JMuon').Fill( FatJet_rho, weight )
                    getattr( self, 'leadAK8JetTau21_2JMuon').Fill( FatJet_tau21, weight )
                    getattr( self, 'leadAK8JetHbb_2JMuon').Fill( FatJet_Hbb, weight )
                #### test only electrons
                else:
                    if isMC:
                        getattr( self, 'Lepweight_2JElectron' ).Fill( np.prod(leptonWeights) )
                        getattr( self, 'Lepweight_Trigger_2JElectron' ).Fill( leptonWeights[0] )
                        getattr( self, 'Lepweight_ID_2JElectron' ).Fill( leptonWeights[1] )
                        getattr( self, 'Lepweight_ISO_2JElectron' ).Fill( leptonWeights[2] )
                    getattr( self, 'nPVs_2JElectron').Fill( PV.npvsGood, weight )
                    getattr( self, 'nleps_2JElectron').Fill( len(goodLeptons), weight )
                    getattr( self, 'lepton_pt_2JElectron').Fill( goodLeptons[0].pt, weight )
                    getattr( self, 'lepton_eta_2JElectron').Fill( goodLeptons[0].eta, weight )
                    getattr( self, 'lepton_phi_2JElectron').Fill( goodLeptons[0].phi, weight )
                    getattr( self, 'njets_2JElectron').Fill( len(goodJets_Hcand), weight )
                    for ijet in goodJets_Hcand:
                        getattr( self, 'jets_pt_2JElectron').Fill( ijet.pt, weight )
                        getattr( self, 'jets_eta_2JElectron').Fill( ijet.eta, weight )
                        getattr( self, 'jets_phi_2JElectron').Fill( ijet.phi, weight )
                        getattr( self, 'jets_bDeepFlav_2JElectron' ).Fill( ijet.btagDeepFlavB, weight )
                    getattr( self, 'nBjets_2JElectron').Fill( len(goodBjets_Hcand), weight )
                    getattr( self, 'nAK8jets_2JElectron' ).Fill( len(goodFatJets), weight )
                    getattr( self, 'METPt_2JElectron').Fill( MET.pt, weight )
                    getattr( self, 'lepWMass_2JElectron').Fill( lepW.M(), weight )
                    getattr( self, 'lepWPt_2JElectron').Fill( lepW.Pt(), weight )
                    getattr( self, 'leadAK8JetMass_2JElectron').Fill( FatJet_msoftdrop, weight )
                    getattr( self, 'leadAK8JetPt_2JElectron').Fill( FatJet_pt, weight )
                    getattr( self, 'leadAK8JetRho_2JElectron').Fill( FatJet_rho, weight )
                    getattr( self, 'leadAK8JetTau21_2JElectron').Fill( FatJet_tau21, weight )
                    getattr( self, 'leadAK8JetHbb_2JElectron').Fill( FatJet_Hbb, weight )
                #### test without weights
                getattr( self, 'nPVs_2JNoWeight').Fill( PV.npvsGood )
                getattr( self, 'nleps_2JNoWeight').Fill( len(goodLeptons) )
                getattr( self, 'lepton_pt_2JNoWeight').Fill( goodLeptons[0].pt )
                getattr( self, 'lepton_eta_2JNoWeight').Fill( goodLeptons[0].eta )
                getattr( self, 'lepton_phi_2JNoWeight').Fill( goodLeptons[0].phi )
                getattr( self, 'njets_2JNoWeight').Fill( len(goodJets_Hcand) )
                for ijet in goodJets_Hcand:
                    getattr( self, 'jets_pt_2JNoWeight').Fill( ijet.pt )
                    getattr( self, 'jets_eta_2JNoWeight').Fill( ijet.eta )
                    getattr( self, 'jets_phi_2JNoWeight').Fill( ijet.phi )
                    getattr( self, 'jets_bDeepFlav_2JNoWeight' ).Fill( ijet.btagDeepFlavB )
                getattr( self, 'nBjets_2JNoWeight').Fill( len(goodBjets_Hcand) )
                getattr( self, 'nAK8jets_2JNoWeight' ).Fill( len(goodFatJets) )
                getattr( self, 'METPt_2JNoWeight').Fill( MET.pt )
                getattr( self, 'lepWMass_2JNoWeight').Fill( lepW.M() )
                getattr( self, 'lepWPt_2JNoWeight').Fill( lepW.Pt() )
                getattr( self, 'leadAK8JetMass_2JNoWeight').Fill( FatJet_msoftdrop )
                getattr( self, 'leadAK8JetPt_2JNoWeight').Fill( FatJet_pt )
                getattr( self, 'leadAK8JetRho_2JNoWeight').Fill( FatJet_rho )
                getattr( self, 'leadAK8JetTau21_2JNoWeight').Fill( FatJet_tau21 )
                getattr( self, 'leadAK8JetHbb_2JNoWeight').Fill( FatJet_Hbb )

                ##### reconstructing WW
                smallestDiffW = 9999
                jFromW = []
                jjCandidates = []
                for jpair in permutations(goodJets_Hcand, 2):
                    jjCandidates.append( jpair[0].p4()+jpair[1].p4() )
                    tmphadW = jpair[0].p4()+jpair[1].p4()
                    tmpDiff = abs(lepW.M() - tmphadW.M())
                    if tmpDiff < smallestDiffW:
                        smallestDiffW = tmpDiff
                        jFromW = [ jpair[0], jpair[1] ]
                getattr( self, 'minDiffLepHadW' ).Fill( smallestDiffW, weight )
                hadW = jFromW[0].p4() + jFromW[1].p4()
                getattr( self, 'resolvedWCandMass_2J' ).Fill( hadW.M(), weight )
                getattr( self, 'resolvedWCandHiggsCandMass_2J' ).Fill( hadW.M(), FatJet_msoftdrop, weight )
                deltaRWHiggs = hadW.DeltaR( goodFatJets[0].p4() )
                getattr( self, 'deltaRhadWHiggs_2J' ).Fill( deltaRWHiggs, weight )
                getattr( self, 'deltaRhadWHiggsMass_2J' ).Fill( deltaRWHiggs, FatJet_msoftdrop, weight )
                deltaRJJ = jFromW[0].p4().DeltaR( jFromW[1].p4() )
                getattr( self, 'deltaRJJ_2J' ).Fill( deltaRJJ, weight )
                deltaRlepWHiggs = lepW.DeltaR( goodFatJets[0].p4() )
                getattr( self, 'deltaRlepWHiggs_2J' ).Fill( deltaRlepWHiggs, weight )
                getattr( self, 'deltaRlepWHiggsMass_2J' ).Fill( deltaRlepWHiggs, FatJet_msoftdrop, weight )
                getattr( self, 'deltaRlepWHiggsdeltaRhadWHiggs_2J' ).Fill( deltaRlepWHiggs, deltaRWHiggs, weight )
                deltaRlepWhadW = lepW.DeltaR( hadW )
                getattr( self, 'deltaRlepWhadW_2J' ).Fill( deltaRlepWhadW, weight )
                getattr( self, 'deltaRlepWhadWHiggsMass_2J' ).Fill( deltaRlepWhadW, FatJet_msoftdrop, weight )


                #### "Good hadronic W candidate"
                if (hadW.M()>65 and hadW.M()<105) and (lepW.M()>65 and lepW.M()<105):
                    getattr( self, 'cutFlow' ).Fill( 4 )
                    getattr( self, 'cutFlow_weight' ).Fill( 4, weight )
                    if isMC: getattr( self, 'cutFlow_genWeight' ).Fill( 4, event.genWeight )

                    getattr( self, 'nPVs_2J2W').Fill( PV.npvsGood, weight )
                    getattr( self, 'nleps_2J2W').Fill( len(goodLeptons), weight )
                    getattr( self, 'nleps_2J2WNoWeight').Fill( len(goodLeptons) )
                    getattr( self, 'lepton_pt_2J2W').Fill( goodLeptons[0].pt, weight )
                    getattr( self, 'lepton_eta_2J2W').Fill( goodLeptons[0].eta, weight )
                    getattr( self, 'lepton_phi_2J2W').Fill( goodLeptons[0].phi, weight )
                    getattr( self, 'njets_2J2W').Fill( len(goodJets_Hcand), weight )
                    for ijet in goodJets_Hcand:
                        getattr( self, 'jets_pt_2J2W').Fill( ijet.pt, weight )
                        getattr( self, 'jets_eta_2J2W').Fill( ijet.eta, weight )
                        getattr( self, 'jets_phi_2J2W').Fill( ijet.phi, weight )
                        getattr( self, 'jets_bDeepFlav_2J2W' ).Fill( ijet.btagDeepFlavB, weight )
                    getattr( self, 'nBjets_2J2W').Fill( len(goodBjets_Hcand), weight )
                    getattr( self, 'nAK8jets_2J2W' ).Fill( len(goodFatJets), weight )
                    getattr( self, 'METPt_2J2W').Fill( MET.pt, weight )
                    getattr( self, 'lepWMass_2J2W').Fill( lepW.M(), weight )
                    getattr( self, 'lepWPt_2J2W').Fill( lepW.Pt(), weight )
                    getattr( self, 'leadAK8JetMass_2J2W').Fill( FatJet_msoftdrop, weight )
                    getattr( self, 'leadAK8JetPt_2J2W').Fill( FatJet_pt, weight )
                    getattr( self, 'leadAK8JetPt_2J2WNoWeight').Fill( FatJet_pt )
                    getattr( self, 'leadAK8JetRho_2J2W').Fill( FatJet_rho, weight )
                    getattr( self, 'leadAK8JetTau21_2J2W').Fill( FatJet_tau21, weight )
                    getattr( self, 'leadAK8JetHbb_2J2W').Fill( FatJet_Hbb, weight )
                    getattr( self, 'resolvedWCandMass_2J2W' ).Fill( hadW.M(), weight )
                    getattr( self, 'resolvedWCandPt_2J2W' ).Fill( hadW.Pt(), weight )
                    getattr( self, 'resolvedWCandHiggsCandMass_2J2W' ).Fill( hadW.M(), FatJet_msoftdrop, weight )
                    getattr( self, 'deltaRhadWHiggs_2J2W' ).Fill( deltaRWHiggs, weight )
                    getattr( self, 'deltaRhadWHiggsMass_2J2W' ).Fill( deltaRWHiggs, FatJet_msoftdrop, weight )
                    getattr( self, 'deltaRJJ_2J2W' ).Fill( deltaRJJ, weight )
                    getattr( self, 'deltaRlepWHiggs_2J2W' ).Fill( deltaRlepWHiggs, weight )
                    getattr( self, 'deltaRlepWHiggsMass_2J2W' ).Fill( deltaRlepWHiggs, FatJet_msoftdrop, weight )
                    getattr( self, 'deltaRlepWHiggsdeltaRhadWHiggs_2J2W' ).Fill( deltaRlepWHiggs, deltaRWHiggs, weight )
                    getattr( self, 'deltaRlepWhadW_2J2W' ).Fill( deltaRlepWhadW, weight )
                    getattr( self, 'deltaRlepWhadWHiggsMass_2J2W' ).Fill( deltaRlepWhadW, FatJet_msoftdrop, weight )

                    getattr( self, 'leadAK8JetRhoTau21_2J2W' ).Fill( FatJet_rho, FatJet_tau21, weight )
                    getattr( self, 'leadAK8JetRhoPtHbb_2J2W' ).Fill( FatJet_rho, FatJet_pt, FatJet_Hbb, weight )

                    #### just checking how does it look with additional btagging
                    if len(goodBjets_Hcand)>0:
                        getattr( self, 'leadAK8JetMass_2J2W1B' ).Fill( FatJet_msoftdrop, weight )
                        getattr( self, 'leadAK8JetPt_2J2W1B' ).Fill( FatJet_pt, weight )
                    if len(goodBjets_Hcand)>1:
                        getattr( self, 'leadAK8JetMass_2J2W2B' ).Fill( FatJet_msoftdrop, weight )
                        getattr( self, 'leadAK8JetPt_2J2W2B' ).Fill( FatJet_pt, weight )

                    ############ THIS IS THE "FINAL" SELECTION
                    #### Asking for Ws and Higgs to be apart
                    if (deltaRlepWHiggs>1) and (deltaRWHiggs>1):
                        getattr( self, 'cutFlow' ).Fill( 5 )
                        getattr( self, 'cutFlow_weight' ).Fill( 5, weight )
                        if isMC: getattr( self, 'cutFlow_genWeight' ).Fill( 5, event.genWeight )

                        getattr( self, 'nPVs_2J2WdeltaR').Fill( PV.npvsGood, weight )
                        getattr( self, 'nleps_2J2WdeltaR').Fill( len(goodLeptons), weight )
                        getattr( self, 'lepton_pt_2J2WdeltaR').Fill( goodLeptons[0].pt, weight )
                        getattr( self, 'lepton_eta_2J2WdeltaR').Fill( goodLeptons[0].eta, weight )
                        getattr( self, 'lepton_phi_2J2WdeltaR').Fill( goodLeptons[0].phi, weight )
                        getattr( self, 'njets_2J2WdeltaR').Fill( len(goodJets_Hcand), weight )
                        for ijet in goodJets_Hcand:
                            getattr( self, 'jets_pt_2J2WdeltaR').Fill( ijet.pt, weight )
                            getattr( self, 'jets_eta_2J2WdeltaR').Fill( ijet.eta, weight )
                            getattr( self, 'jets_phi_2J2WdeltaR').Fill( ijet.phi, weight )
                            getattr( self, 'jets_bDeepFlav_2J2WdeltaR' ).Fill( ijet.btagDeepFlavB, weight )
                        getattr( self, 'nBjets_2J2WdeltaR').Fill( len(goodBjets_Hcand), weight )
                        getattr( self, 'nAK8jets_2J2WdeltaR' ).Fill( len(goodFatJets), weight )
                        getattr( self, 'METPt_2J2WdeltaR').Fill( MET.pt, weight )
                        getattr( self, 'lepWMass_2J2WdeltaR').Fill( lepW.M(), weight )
                        getattr( self, 'lepWPt_2J2WdeltaR').Fill( lepW.Pt(), weight )
                        getattr( self, 'leadAK8JetMass_2J2WdeltaR').Fill( FatJet_msoftdrop, weight )
                        getattr( self, 'leadAK8JetPt_2J2WdeltaR').Fill( FatJet_pt, weight )
                        getattr( self, 'leadAK8JetRho_2J2WdeltaR').Fill( FatJet_rho, weight )
                        getattr( self, 'leadAK8JetTau21_2J2WdeltaR').Fill( FatJet_tau21, weight )
                        getattr( self, 'leadAK8JetHbb_2J2WdeltaR').Fill( FatJet_Hbb, weight )
                        getattr( self, 'resolvedWCandMass_2J2WdeltaR' ).Fill( hadW.M(), weight )
                        getattr( self, 'resolvedWCandPt_2J2WdeltaR' ).Fill( hadW.Pt(), weight )
                        getattr( self, 'leadAK8JetRhoPtHbb_2J2WdeltaR' ).Fill( FatJet_rho, FatJet_pt, FatJet_Hbb, weight )

                        ##### Start asking for boosted Higgs
                        if (FatJet_tau21<tau21cut):
                            getattr( self, 'cutFlow' ).Fill( 6 )
                            getattr( self, 'cutFlow_weight' ).Fill( 6, weight )
                            if isMC: getattr( self, 'cutFlow_genWeight' ).Fill( 6, event.genWeight )

                            getattr( self, 'nPVs_2J2WdeltaRTau21').Fill( PV.npvsGood, weight )
                            getattr( self, 'nleps_2J2WdeltaRTau21').Fill( len(goodLeptons), weight )
                            getattr( self, 'lepton_pt_2J2WdeltaRTau21').Fill( goodLeptons[0].pt, weight )
                            getattr( self, 'lepton_eta_2J2WdeltaRTau21').Fill( goodLeptons[0].eta, weight )
                            getattr( self, 'lepton_phi_2J2WdeltaRTau21').Fill( goodLeptons[0].phi, weight )
                            getattr( self, 'njets_2J2WdeltaRTau21').Fill( len(goodJets_Hcand), weight )
                            for ijet in goodJets_Hcand:
                                getattr( self, 'jets_pt_2J2WdeltaRTau21').Fill( ijet.pt, weight )
                                getattr( self, 'jets_eta_2J2WdeltaRTau21').Fill( ijet.eta, weight )
                                getattr( self, 'jets_phi_2J2WdeltaRTau21').Fill( ijet.phi, weight )
                                getattr( self, 'jets_bDeepFlav_2J2WdeltaRTau21' ).Fill( ijet.btagDeepFlavB, weight )
                            getattr( self, 'nBjets_2J2WdeltaRTau21').Fill( len(goodBjets_Hcand), weight )
                            getattr( self, 'nAK8jets_2J2WdeltaRTau21' ).Fill( len(goodFatJets), weight )
                            getattr( self, 'METPt_2J2WdeltaRTau21').Fill( MET.pt, weight )
                            getattr( self, 'lepWMass_2J2WdeltaRTau21').Fill( lepW.M(), weight )
                            getattr( self, 'lepWPt_2J2WdeltaRTau21').Fill( lepW.Pt(), weight )
                            getattr( self, 'leadAK8JetMass_2J2WdeltaRTau21').Fill( FatJet_msoftdrop, weight )
                            getattr( self, 'leadAK8JetPt_2J2WdeltaRTau21').Fill( FatJet_pt, weight )
                            getattr( self, 'leadAK8JetRho_2J2WdeltaRTau21').Fill( FatJet_rho, weight )
                            getattr( self, 'leadAK8JetTau21_2J2WdeltaRTau21').Fill( FatJet_tau21, weight )
                            getattr( self, 'leadAK8JetHbb_2J2WdeltaRTau21').Fill( FatJet_Hbb, weight )
                            getattr( self, 'resolvedWCandMass_2J2WdeltaRTau21' ).Fill( hadW.M(), weight )
                            getattr( self, 'resolvedWCandPt_2J2WdeltaRTau21' ).Fill( hadW.Pt(), weight )
                            getattr( self, 'leadAK8JetRhoPtHbb_2J2WdeltaRTau21' ).Fill( FatJet_rho, FatJet_pt, FatJet_Hbb, weight )

                            if (FatJet_Hbb>Hbbcut):
                                getattr( self, 'cutFlow' ).Fill( 7 )
                                getattr( self, 'cutFlow_weight' ).Fill( 7, weight )
                                if isMC: getattr( self, 'cutFlow_genWeight' ).Fill( 7, event.genWeight )

                                getattr( self, 'leadAK8JetMass_2J2WdeltaRTau21_Pass' ).Fill( FatJet_msoftdrop, weight )
                                getattr( self, 'resolvedWCandMass_2J2WdeltaRTau21_Pass' ).Fill( hadW.M(), weight )
                                getattr( self, 'leadAK8JetRho_2J2WdeltaRTau21_Pass' ).Fill( FatJet_rho, weight )
                                getattr( self, 'leadAK8JetTau21_2J2WdeltaRTau21_Pass' ).Fill( FatJet_tau21, weight )
                                getattr( self, 'leadAK8JetHbb_2J2WdeltaRTau21_Pass' ).Fill( FatJet_Hbb, weight )
                                getattr( self, 'leadAK8JetMassPt_2J2WdeltaRTau21_Pass' ).Fill( FatJet_msoftdrop, FatJet_pt, weight )
                                getattr( self, 'leadAK8JetRhoPt_2J2WdeltaRTau21_Pass' ).Fill( FatJet_rho, FatJet_pt, weight )
                                getattr( self, 'leadAK8JetRhoPtMass_2J2WdeltaRTau21_Pass' ).Fill( FatJet_rho, FatJet_pt, FatJet_msoftdrop, weight )

                            else:
                                getattr( self, 'leadAK8JetMass_2J2WdeltaRTau21_Fail' ).Fill( FatJet_msoftdrop, weight )
                                getattr( self, 'resolvedWCandMass_2J2WdeltaRTau21_Fail' ).Fill( hadW.M(), weight )
                                getattr( self, 'leadAK8JetRho_2J2WdeltaRTau21_Fail' ).Fill( FatJet_rho, weight )
                                getattr( self, 'leadAK8JetTau21_2J2WdeltaRTau21_Fail' ).Fill( FatJet_tau21, weight )
                                getattr( self, 'leadAK8JetHbb_2J2WdeltaRTau21_Fail' ).Fill( FatJet_Hbb, weight )
                                getattr( self, 'leadAK8JetMassPt_2J2WdeltaRTau21_Fail' ).Fill( FatJet_msoftdrop, FatJet_pt, weight )
                                getattr( self, 'leadAK8JetRhoPt_2J2WdeltaRTau21_Fail' ).Fill( FatJet_rho, FatJet_pt, weight )
                                getattr( self, 'leadAK8JetRhoPtMass_2J2WdeltaRTau21_Fail' ).Fill( FatJet_rho, FatJet_pt, FatJet_msoftdrop, weight )


                        #### Just testing without Tau21
                        if (FatJet_Hbb>Hbbcut):
                            getattr( self, 'cutFlow' ).Fill( 9 )
                            getattr( self, 'cutFlow_weight' ).Fill( 9, weight )
                            if isMC: getattr( self, 'cutFlow_genWeight' ).Fill( 9, event.genWeight )

                            getattr( self, 'leadAK8JetMass_2J2WdeltaR_Pass' ).Fill( FatJet_msoftdrop, weight )
                            getattr( self, 'resolvedWCandMass_2J2WdeltaR_Pass' ).Fill( hadW.M(), weight )
                            getattr( self, 'leadAK8JetRho_2J2WdeltaR_Pass' ).Fill( FatJet_rho, weight )
                            getattr( self, 'leadAK8JetTau21_2J2WdeltaR_Pass' ).Fill( FatJet_tau21, weight )
                            getattr( self, 'leadAK8JetHbb_2J2WdeltaR_Pass' ).Fill( FatJet_Hbb, weight )
                            getattr( self, 'leadAK8JetMassPt_2J2WdeltaR_Pass' ).Fill( FatJet_msoftdrop, FatJet_pt, weight )
                            getattr( self, 'leadAK8JetRhoPt_2J2WdeltaR_Pass' ).Fill( FatJet_rho, FatJet_pt, weight )
                            getattr( self, 'leadAK8JetRhoPtMass_2J2WdeltaR_Pass' ).Fill( FatJet_rho, FatJet_pt, FatJet_msoftdrop, weight )

                        else:
                            getattr( self, 'leadAK8JetMass_2J2WdeltaR_Fail' ).Fill( FatJet_msoftdrop, weight )
                            getattr( self, 'resolvedWCandMass_2J2WdeltaR_Fail' ).Fill( hadW.M(), weight )
                            getattr( self, 'leadAK8JetRho_2J2WdeltaR_Fail' ).Fill( FatJet_rho, weight )
                            getattr( self, 'leadAK8JetTau21_2J2WdeltaR_Fail' ).Fill( FatJet_tau21, weight )
                            getattr( self, 'leadAK8JetHbb_2J2WdeltaR_Fail' ).Fill( FatJet_Hbb, weight )
                            getattr( self, 'leadAK8JetMassPt_2J2WdeltaR_Fail' ).Fill( FatJet_msoftdrop, FatJet_pt, weight )
                            getattr( self, 'leadAK8JetRhoPt_2J2WdeltaR_Fail' ).Fill( FatJet_rho, FatJet_pt, weight )
                            getattr( self, 'leadAK8JetRhoPtMass_2J2WdeltaR_Fail' ).Fill( FatJet_rho, FatJet_pt, FatJet_msoftdrop, weight )

                        ###### Checking if extra bjets help
                        if len(goodBjets_Hcand)>0:
                            getattr( self, 'leadAK8JetMass_2J2WdeltaR1B' ).Fill( FatJet_msoftdrop, weight )
                            getattr( self, 'resolvedWCandMass_2J2WdeltaR1B' ).Fill( hadW.M(), weight )
                            getattr( self, 'leadAK8JetRho_2J2WdeltaR1B' ).Fill( FatJet_rho, weight )
                            getattr( self, 'leadAK8JetTau21_2J2WdeltaR1B' ).Fill( FatJet_tau21, weight )
                            getattr( self, 'leadAK8JetHbb_2J2WdeltaR1B' ).Fill( FatJet_Hbb, weight )
                        else:
                            getattr( self, 'noHiggsCandMass_2J2WdeltaR1B' ).Fill( FatJet_msoftdrop, weight )

                        if len(goodBjets_Hcand)>1:
                            getattr( self, 'leadAK8JetMass_2J2WdeltaR2B' ).Fill( FatJet_msoftdrop, weight )
                            getattr( self, 'resolvedWCandMass_2J2WdeltaR2B' ).Fill( hadW.M(), weight )
                            getattr( self, 'leadAK8JetRho_2J2WdeltaR2B' ).Fill( FatJet_rho, weight )
                            getattr( self, 'leadAK8JetTau21_2J2WdeltaR2B' ).Fill( FatJet_tau21, weight )
                            getattr( self, 'leadAK8JetHbb_2J2WdeltaR2B' ).Fill( FatJet_Hbb, weight )
                        else:
                            getattr( self, 'noHiggsCandMass_2J2WdeltaR2B' ).Fill( FatJet_msoftdrop, weight )
                    else:
                        getattr( self, 'noHiggsCandMass_2J2WdeltaR' ).Fill( FatJet_msoftdrop, weight )



                if len(goodBjets_Hcand)>0:
                    getattr( self, 'leadAK8JetMass_2J1B' ).Fill( FatJet_msoftdrop, weight )
                    deltaR1BHiggs = goodBjets_Hcand[0].p4().DeltaR( goodFatJets[0].p4() )
                    getattr( self, 'deltaR1BHiggs_2J1B' ).Fill( deltaR1BHiggs, weight )
                if len(goodBjets_Hcand)>1:
                    getattr( self, 'leadAK8JetMass_2J2B' ).Fill( FatJet_msoftdrop, weight )



            #### check if has only bjets
            if len(goodBjets_Hcand)>0:
                getattr( self, 'leadAK8JetMass_1B' ).Fill( FatJet_msoftdrop, weight )
                deltaR1BHiggs = goodBjets_Hcand[0].p4().DeltaR( goodFatJets[0].p4() )
                getattr( self, 'deltaR1BHiggs_1B' ).Fill( deltaR1BHiggs, weight )
            if len(goodBjets_Hcand)>1:
                getattr( self, 'leadAK8JetMass_2B' ).Fill( FatJet_msoftdrop, weight )

            ### For boosted W: good idea, it didn't work
            '''
            if len(looseFatJets)>0: looseFatJets.remove(goodFatJets[0])
            goodWCandidate = looseFatJets[0] if (len(looseFatJets)>0) and ((looseFatJets[0].tau2/looseFatJets[0].tau1)<tau21cut) else None
            if goodWCandidate:
                getattr( self, 'leadAK8JetMass_W' ).Fill( FatJet_msoftdrop )
                getattr( self, 'boostedWCandMass_W' ).Fill( goodWCandidate.msoftdrop )
                if len(goodPuppiBjets_Hcand)>0:
                    getattr( self, 'leadAK8JetMass_W1B' ).Fill( FatJet_msoftdrop )
                    getattr( self, 'boostedWCandMass_W1B' ).Fill( goodWCandidate.msoftdrop )
            '''
            ######################################################################

            ######################################################################
            ######################################################################
            ### only boosted W

            '''
            ### W candidate
            wCandidates_boostedW = [ j for j in looseFatJets if ((j.tau2/j.tau1 < tau21cut) and (j.deepTagMD_ZHbbvsQCD<Hbbcut))  ]
            goodWCandidate_boostedW = min(wCandidates_boostedW, key=lambda j: j.tau2/j.tau1 ) if len(wCandidates_boostedW)>0 else None
            if goodWCandidate_boostedW: badFatJets_boostedW.remove(goodWCandidate_boostedW)

            ##### FOR ABCD
            for ifj in badFatJets_boostedW:
                getattr( self, 'nJetsvsTau21_boostedW' ).Fill( len(badFatJets_boostedW), ifj.tau2/ifj.tau1 )

            if goodWCandidate_boostedW:
                isolatedPuppiJets_boostedW = [ j for j in goodPuppiJetsNoLep if (j.p4().DeltaR(goodWCandidate_boostedW.p4())>=1.2)  ]
                goodPuppiJets_boostedW = [ b for b in isolatedPuppiJets_boostedW if (b.pfDeepCSVJetTags_probb+b.pfDeepCSVJetTags_probbb)<0.4941 ]
                goodPuppiBjets_boostedW = [ b for b in isolatedPuppiJets_boostedW if (b.pfDeepCSVJetTags_probb+b.pfDeepCSVJetTags_probbb)>0.4941 ]
                getattr( self, 'nGoodPuppiBjets_boostedW' ).Fill( len(goodPuppiBjets_boostedW) if goodPuppiBjets_boostedW else 0 )
                getattr( self, 'nGoodPuppiJets_boostedW' ).Fill( len(goodPuppiJets_boostedW) if goodPuppiJets_boostedW else 0 )
                getattr( self, 'WCandMass_boostedW' ).Fill( goodWCandidate_boostedW.msoftdrop )
                getattr( self, 'boostedHiggsCandMass_boostedW' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )

                if len(goodPuppiBjets_boostedW)>1:

                    ##### reconstructing ttbar
                    smallestDiffTop = 9999
                    bFromTop = []
                    bbCandidates = []
                    for bpair in permutations(goodPuppiBjets_boostedW, 2):
                        bbCandidates.append( bpair[0].p4()+bpair[1].p4() )
                        tmplepTop = lepW + bpair[0].p4()
                        tmphadTop = goodWCandidate_boostedW.p4() + bpair[1].p4()
                        tmpDiff = abs(tmplepTop.M() - tmphadTop.M())
                        if tmpDiff < smallestDiffTop:
                            smallestDiffTop = tmpDiff
                            bFromTop = [ bpair[0], bpair[1] ]
                    getattr( self, 'minDiffLepHadTop' ).Fill( smallestDiffTop )
                    lepTop = lepW + bFromTop[0].p4()
                    hadTop = goodWCandidate_boostedW.p4() + bFromTop[1].p4()
                    getattr( self, 'lepTopCandMass_2B_boostedW' ).Fill( lepTop.M() )
                    getattr( self, 'hadTopCandMass_2B_boostedW' ).Fill( hadTop.M() )
                    getattr( self, 'boostedHiggsCandMass_2B_boostedW' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )
                    getattr( self, 'boostedHiggsCandPt_2B_boostedW' ).Fill( goodHiggsCandidate.pt if goodHiggsCandidate else -999 )

                    getattr( self, 'leadingBjetPt_2B_boostedW' ).Fill( goodPuppiBjets_boostedW[0].pt )
                    getattr( self, 'leadingBjetEta_2B_boostedW' ).Fill( goodPuppiBjets_boostedW[0].eta )
                    getattr( self, 'leadingBjetBdisc_2B_boostedW' ).Fill( (goodPuppiBjets_boostedW[0].pfDeepCSVJetTags_probb+goodPuppiBjets_boostedW[0].pfDeepCSVJetTags_probbb) )
                    getattr( self, 'subleadingBjetPt_2B_boostedW' ).Fill( goodPuppiBjets_boostedW[1].pt )
                    getattr( self, 'subleadingBjetEta_2B_boostedW' ).Fill( goodPuppiBjets_boostedW[1].eta )
                    getattr( self, 'subleadingBjetBdisc_2B_boostedW' ).Fill( (goodPuppiBjets_boostedW[1].pfDeepCSVJetTags_probb+goodPuppiBjets_boostedW[1].pfDeepCSVJetTags_probbb) )

                    ##### reconstructing Higgs
                    resHiggs = goodPuppiBjets_boostedW[0].p4() + goodPuppiBjets_boostedW[1].p4()
                    deltaResHiggs = goodPuppiBjets_boostedW[0].pt + goodPuppiBjets_boostedW[1].pt - resHiggs.M()
                    getattr( self, 'deltaResHiggs_2B_boostedW' ).Fill( resHiggs.M(), deltaResHiggs )
                    getattr( self, 'ptMassResHiggs_2B_boostedW' ).Fill( resHiggs.M(), (resHiggs.M()-resHiggs.Pt()))
                    deltaR2B = goodPuppiBjets_boostedW[0].p4().DeltaR( goodPuppiBjets_boostedW[1].p4() )
                    getattr( self, 'deltaR2B_2B_boostedW' ).Fill( deltaR2B )
                    getattr( self, 'resolvedHiggsCandPt_2B_boostedW' ).Fill( resHiggs.Pt() )
                    getattr( self, 'resolvedHiggsCandMass_2B_boostedW' ).Fill( resHiggs.M() )
                    if (resHiggs.Pt()>100):
                        getattr( self, 'resolvedHiggsCandMass_2Bpt_boostedW' ).Fill( resHiggs.M() )

                    if (deltaR2B < 2): getattr( self, 'resolvedHiggsCandMass_2BdeltaR_boostedW' ).Fill( resHiggs.M() )

                    smallestDistancebb = 99999
                    bbCandidatesSmallR = []
                    for bpair in permutations(goodPuppiBjets_boostedW, 2):
                        deltaRbb = bpair[0].p4().DeltaR( bpair[1].p4() )
                        if deltaRbb < smallestDistancebb:
                            smallestDistancebb = deltaRbb
                            bbCandidatesSmallR = [ bpair[0], bpair[1] ]

                    getattr( self, 'resolvedHiggsCandMass_2BSmallR_boostedW' ).Fill( ( bpair[0].p4() + bpair[1].p4() ).M() )
                    goodPuppiBjets_noHiggs_boostedW = goodPuppiBjets_boostedW
                    goodPuppiBjets_noHiggs_boostedW.remove( bpair[0] )
                    goodPuppiBjets_noHiggs_boostedW.remove( bpair[1] )
                    if len(goodPuppiBjets_noHiggs_boostedW)>1:
                        for nobpair in permutations(goodPuppiBjets_noHiggs_boostedW, 2):
                            getattr( self, 'noResolvedHiggsCandMass_2BSmallR_boostedW' ).Fill( ( bpair[0].p4() + bpair[1].p4() ).M() )

                    if len(goodPuppiJets_boostedW)>1:
                        getattr( self, 'simplejjMass_2J_boostedW' ).Fill( ( goodPuppiJets_boostedW[0].p4() + goodPuppiJets_boostedW[1].p4() ).M() )
                        smallestDistancejj = 99999
                        jjCandidatesSmallR = []
                        for jpair in permutations(goodPuppiJets_boostedW, 2):
                            deltaRjj = jpair[0].p4().DeltaR( jpair[1].p4() )
                            if deltaRjj < smallestDistancejj:
                                smallestDistancejj = deltaRjj
                                jjCandidatesSmallR = [ jpair[0], jpair[1] ]
                        getattr( self, 'simplejjMass_2JSmallR_boostedW' ).Fill( ( jjCandidatesSmallR[0].p4() + jjCandidatesSmallR[1].p4() ).M() )

                    for bb in bbCandidates:
                        getattr( self, 'allResolvedHiggsCandPt_2B_boostedW' ).Fill( bb.Pt() )
                        getattr( self, 'allResolvedHiggsCandMass_2B_boostedW' ).Fill( bb.M() )
                        getattr( self, 'allResolvedHiggsCandMassPt_2B_boostedW' ).Fill( bb.M(), bb.Pt() )

            '''
            ######################################################################
            ######################################################################

            #### Just to see categories
            higgsCandidates = [ j for j in goodFatJets if ( (j.deepTagMD_HbbvsQCD > Hbbcut ) and (j.tau2/j.tau1 < tau21cut) ) ]
            goodHiggsCandidate = max(higgsCandidates, key=lambda j: j.deepTagMD_HbbvsQCD) if len(higgsCandidates)>0 else None
            if goodHiggsCandidate:
                badFatJets.remove(goodHiggsCandidate)

            ### W candidate
            wCandidates = [ j for j in badFatJets if (( j.tau1>0 ) and (j.tau2/j.tau1 < tau21cut)) ]
            goodWCandidate = min(wCandidates, key=lambda j: j.tau2/j.tau1 ) if len(wCandidates)>0 else None
            if goodWCandidate: badFatJets.remove(goodWCandidate)

            ### Top candidate
            topCandidates = [ j for j in badFatJets if ((j.tau2>0) and (j.tau3/j.tau2 < 0.4)) ]
            goodTopCandidate = min(topCandidates, key=lambda j: j.tau3/j.tau2 ) if len(topCandidates)>0 else None     ## in case there are more than one top Candidate, choose the one with minimum tau32
            if goodTopCandidate: badFatJets.remove(goodTopCandidate)

            #### Best case scenario (unrealistic) just compute mass for comparison
            if goodTopCandidate and goodHiggsCandidate and not goodWCandidate:
                goodEvents = 1
                getattr( self, 'TopCandMass_TopHiggs' ).Fill( goodTopCandidate.msoftdrop if goodTopCandidate else -999 )
                getattr( self, 'WCandMass_TopHiggs' ).Fill( goodWCandidate.msoftdrop if goodWCandidate else -999 )
                getattr( self, 'leadAK8JetMass_TopHiggs' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )

            #### Best boosted case scenario
            elif goodWCandidate and goodHiggsCandidate and not goodTopCandidate:
                goodEvents = 2
                getattr( self, 'TopCandMass_WHiggs' ).Fill( goodTopCandidate.msoftdrop if goodTopCandidate else -999 )
                getattr( self, 'WCandMass_WHiggs' ).Fill( goodWCandidate.msoftdrop if goodWCandidate else -999 )
                getattr( self, 'leadAK8JetMass_WHiggs' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )

            #### Wrong reconstruction, this category cannot exist
            elif goodWCandidate and goodTopCandidate and not goodHiggsCandidate:
                goodEvents = 3
                getattr( self, 'TopCandMass_WTop' ).Fill( goodTopCandidate.msoftdrop if goodTopCandidate else -999 )
                getattr( self, 'WCandMass_WTop' ).Fill( goodWCandidate.msoftdrop if goodWCandidate else -999 )
                getattr( self, 'leadAK8JetMass_WTop' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )

            #### Following categories just to know
            elif goodWCandidate and not ( goodTopCandidate and goodHiggsCandidate):
                goodEvents = 4
                getattr( self, 'WCandMass_W' ).Fill( goodWCandidate.msoftdrop if goodWCandidate else -999 )
            elif goodTopCandidate and not ( goodWCandidate and goodHiggsCandidate):
                goodEvents = 5
                getattr( self, 'TopCandMass_Top' ).Fill( goodTopCandidate.msoftdrop if goodTopCandidate else -999 )
            elif goodHiggsCandidate and not ( goodWCandidate and goodTopCandidate):
                goodEvents = 6
                getattr( self, 'leadAK8JetMass_Higgs' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )
            else: goodEvents = 0

            if goodHiggsCandidate:
                getattr( self, 'nEvents' ).Fill( 5 )
                if not (njetscut and nbjetscut): getattr( self, 'nEvents' ).Fill( 6 )
                goodEvents = 7

            getattr( self, 'nbadFatJets' ).Fill( len(badFatJets) )
            getattr( self, 'ngoodEvents' ).Fill( goodEvents )
            getattr( self, 'TopCandMass' ).Fill( goodTopCandidate.msoftdrop if goodTopCandidate else -999 )
            getattr( self, 'WCandMass' ).Fill( goodWCandidate.msoftdrop if goodWCandidate else -999 )



        return True


#myboostedAnalyzer = lambda : boostedAnalyzer()
