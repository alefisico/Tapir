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
ttCls = OrderedDict()
ttCls['ttll'] = '(event.genTtbarId<1)'
ttCls['ttcc'] = '(event.genTtbarId>40) && (event.genTtbarId<50)'
ttCls['ttb'] = '(event.genTtbarId==51)'
ttCls['tt2b'] = '(event.genTtbarId==52)'
ttCls['ttbb'] = '(event.genTtbarId>52) && (event.genTtbarId<57)'

rhalPtList = [ 250, 300, 350, 400, 450, 500, 550, 600, 700, 800, 1000, 10000 ]

class boostedAnalyzer(Module):
    def __init__(self, sample="None"):
    #def __init__(self, sample="None", parameters={}):
	self.writeHistFile=True
        self.sample= sample
        #self.parameters = parameters

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

        self.addObject( ROOT.TH1F('nEvents',   ';number of events in category',   10, 0, 10) )
        self.addObject( ROOT.TH1F('nlooseFatJets',   ';number of loose fatjets',   10, 0, 10) )
        self.addObject( ROOT.TH1F('nleps',   ';number of leptons',   20, 0, 20) )
        self.addObject( ROOT.TH1F('nCHSjets',   ';number of CHS jets',   20, 0, 20) )
        self.addObject( ROOT.TH1F('nCHSBjets',   ';number of CHS b jets',   20, 0, 20) )
        self.addObject( ROOT.TH1F('lepPt',   ';Lepton p_{T} (GeV)',   500, 0, 5000) )
        self.addObject( ROOT.TH1F('lepEta',  ';Lepton #eta', 100, -4.0, 4.0 ) )
        self.addObject( ROOT.TH1F('METPt',   ';MET (GeV)',   500, 0, 5000) )
        self.addObject( ROOT.TH1F('lepWMass',   ';Leptonic W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('nbadFatJets',   ';number of bad fatjets',   10, 0, 10) )
        self.addObject( ROOT.TH1F('ngoodEvents',   ';Good Events',   10, 0, 10) )
        self.addObject( ROOT.TH1F('TopCandMass',   ';Top candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('WCandMass',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetMass',   ';Leading AK8 jet mass', 60, 0, 300) )
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
        self.addObject( ROOT.TH1F('TopCandMass_PuppiJets',   ';Top candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('WCandMass_PuppiJets',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_PuppiJets',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('nGoodPuppiBJets',   ';number of good puppi bjets',   10, 0, 10) )
        self.addObject( ROOT.TH1F('nCleanPuppiJets_boostedHiggs',   ';number of clean puppi jets',   10, 0, 10) )
        self.addObject( ROOT.TH1F('nGoodPuppiJets_boostedHiggs',   ';number of good puppi jets',   10, 0, 10) )
        self.addObject( ROOT.TH1F('nGoodPuppiBjets_boostedHiggs',   ';number of good puppi bjets',   10, 0, 10) )
        self.addObject( ROOT.TH1F('leadAK8JetN2_boostedHiggs',   ';#rho', 40, 0, 1) )
        self.addObject( ROOT.TH2F('leadAK8JetdeepAK8HbbMDTop_boostedHiggs',   '', 40, 0, 1, 40, 0, 1) )
        self.addObject( ROOT.TH2F('leadAK8JetdeepAK8HbbMDDDB_boostedHiggs',   '', 40, 0, 1, 40, 0, 1) )
        self.addObject( ROOT.TH2F('leadAK8JetRhoHbb_boostedHiggs',   ';#rho', 40, -10, 10, 40, 0, 1) )
        self.addObject( ROOT.TH2F('leadAK8JetRhoTau21_boostedHiggs',   ';#tau_{21}', 40, -10, 10, 40, 0, 1) )
        self.addObject( ROOT.TH3F('leadAK8JetPtMassHbb_boostedHiggs',   ';pt', 50, 100, 600, 30, 0, 300, 40, 0, 1) )
        self.addObject( ROOT.TH2F('resolvedWCandHiggsCandMass_2J_boostedHiggs',   ';W candidate mass', 60, 0, 300, 60, 0, 300) )
        self.addObject( ROOT.TH1F('deltaRJJ_2J_boostedHiggs',   ';deltaR( J, J )', 50, 0, 5 ) )
        self.addObject( ROOT.TH1F('deltaRhadWHiggs_2J_boostedHiggs',   ';deltaR( hadW, Higgs )', 50, 0, 5 ) )
        self.addObject( ROOT.TH2F('deltaRhadWHiggsMass_2J_boostedHiggs',   ';deltaR( hadW, Higgs );Leading jet msd', 50, 0, 5, 60, 0, 300 ) )
        self.addObject( ROOT.TH1F('deltaRlepWHiggs_2J_boostedHiggs',   ';deltaR( lepW, Higgs )', 50, 0, 5 ) )
        self.addObject( ROOT.TH2F('deltaRlepWHiggsMass_2J_boostedHiggs',   ';deltaR( lepW, Higgs );Leading jet msd', 50, 0, 5, 60, 0, 300 ) )
        self.addObject( ROOT.TH2F('deltaRlepWHiggsdeltaRhadWHiggs_2J_boostedHiggs',   ';deltaR( lepW, Higgs );deltaR( hadW, Higgs )', 50, 0, 5, 50, 0, 5 ) )
        self.addObject( ROOT.TH1F('deltaRlepWhadW_2J_boostedHiggs',   ';deltaR( lepW, hadW )', 50, 0, 5 ) )
        self.addObject( ROOT.TH2F('deltaRlepWhadWHiggsMass_2J_boostedHiggs',   ';deltaR( lepW, hadW );Leading jet msd', 50, 0, 5, 60, 0, 300 ) )
        self.addObject( ROOT.TH1F('noHiggsCandTau21_2J2W_boostedHiggs',   ';#tau_{21}', 40, 0, 1) )
        self.addObject( ROOT.TH1F('noHiggsCandHbb_2J2W_boostedHiggs',   ';Hbb discriminator', 40, 0, 1) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_A_2Jno2W_boostedHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_2J2W1B_boostedHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetPt_2J2W1B_boostedHiggs',   ';Leading AK8 jet mass', 150, 0, 1500) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_2J2W2B_boostedHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetPt_2J2W2B_boostedHiggs',   ';Leading AK8 jet mass', 150, 0, 1500) )
        self.addObject( ROOT.TH2F('leadAK8JetRhoHbb_2J2W_boostedHiggs',   ';#rho', 40, -10, 10, 40, 0, 1) )
        self.addObject( ROOT.TH2F('leadAK8JetRhoTau21_2J2W_boostedHiggs',   ';#rho', 40, -10, 10, 40, 0, 1) )
        self.addObject( ROOT.TH3F('leadAK8JetPtMassHbb_2J2W_boostedHiggs',   ';#rho', 50, 100, 600, 30, 0, 300, 40, 0, 1) )
        self.addObject( ROOT.TH2F('resolvedWCandHiggsCandMass_2J2W_boostedHiggs',   ';W candidate mass', 60, 0, 300, 60, 0, 300) )
        self.addObject( ROOT.TH1F('deltaRJJ_2J2W_boostedHiggs',   ';deltaR( J, J )', 50, 0, 5 ) )
        self.addObject( ROOT.TH1F('deltaRhadWHiggs_2J2W_boostedHiggs',   ';deltaR( hadW, Higgs )', 50, 0, 5 ) )
        self.addObject( ROOT.TH2F('deltaRhadWHiggsMass_2J2W_boostedHiggs',   ';deltaR( hadW, Higgs );Leading jet msd', 50, 0, 5, 60, 0, 300 ) )
        self.addObject( ROOT.TH1F('deltaRlepWHiggs_2J2W_boostedHiggs',   ';deltaR( lepW, Higgs )', 50, 0, 5 ) )
        self.addObject( ROOT.TH2F('deltaRlepWHiggsMass_2J2W_boostedHiggs',   ';deltaR( lepW, Higgs );Leading jet msd', 50, 0, 5, 60, 0, 300 ) )
        self.addObject( ROOT.TH2F('deltaRlepWHiggsdeltaRhadWHiggs_2J2W_boostedHiggs',   ';deltaR( lepW, Higgs );deltaR( hadW, Higgs )', 50, 0, 5, 50, 0, 5 ) )
        self.addObject( ROOT.TH1F('deltaRlepWhadW_2J2W_boostedHiggs',   ';deltaR( lepW, hadW )', 50, 0, 5 ) )
        self.addObject( ROOT.TH2F('deltaRlepWhadWHiggsMass_2J2W_boostedHiggs',   ';deltaR( lepW, hadW );Leading jet msd', 50, 0, 5, 60, 0, 300 ) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_2J1B_boostedHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_2J2B_boostedHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_1B_boostedHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('leadAK8JetMass_2B_boostedHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('deltaR1BHiggs_2J1B_boostedHiggs',   ';deltaR( 1b, Higgs )', 50, 0, 5 ) )
        self.addObject( ROOT.TH1F('deltaR1BHiggs_1B_boostedHiggs',   ';deltaR( 1b, Higgs )', 50, 0, 5 ) )
        self.addObject( ROOT.TH1F('minDiffLepHadW',   ';min difference between lep and had W',   100, 0, 100) )


        #### general selection
        for isel in [ '',  '_2J',  '_2J2W', '_2JdeltaR', '_2JdeltaR2W', '_2JdeltaR2W1B', '_2JdeltaR2W2B', '_W', '_W1B', '_2JdeltaR2WTau21DDT' ]:
            self.addObject( ROOT.TH1F('leadAK8JetMass'+isel+'_boostedHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )
            self.addObject( ROOT.TH1F('leadAK8JetPt'+isel+'_boostedHiggs',   ';Leading AK8 jet mass', 150, 0, 1500) )
            self.addObject( ROOT.TH1F('resolvedWCandMass'+isel+'_boostedHiggs',   ';W candidate mass', 60, 0, 300) )
            self.addObject( ROOT.TH1F('boostedWCandMass'+isel+'_boostedHiggs',   ';W candidate mass', 60, 0, 300) )
            self.addObject( ROOT.TH1F('leadAK8JetRho'+isel+'_boostedHiggs',   ';#rho', 40, -10, 10) )
            self.addObject( ROOT.TH1F('leadAK8JetTau21'+isel+'_boostedHiggs',   ';#tau_{21}', 40, 0, 1) )
            self.addObject( ROOT.TH1F('leadAK8JetTau21DDT'+isel+'_boostedHiggs',   ';#tau_{21}^{DDT}', 40, 0, 1) )
            self.addObject( ROOT.TH1F('leadAK8JetHbb'+isel+'_boostedHiggs',   ';Hbb discriminator', 40, 0, 1) )
            self.addObject( ROOT.TH2F('HbbvsTau21'+isel+'_boostedHiggs',   ';', 20, 0, 1, 20, 0, 1) )
            self.addObject( ROOT.TH1F('noHiggsCandMass'+isel+'_boostedHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )

            #### For ABCD
            for side in [ 'A', 'B', 'C', 'D' ]:
                self.addObject( ROOT.TH2F('HbbvsTau21_'+side+isel+'_boostedHiggs',   ';', 20, 0, 1, 20, 0, 1) )
                self.addObject( ROOT.TH1F('leadAK8JetMass_'+side+isel+'_boostedHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )

        #### For rhalphabet
        for isel in [ '2JdeltaR2WTau21DDT_' ]:
            for ipass in [ 'Pass', 'Fail' ]:
                self.addObject( ROOT.TH1F('leadAK8JetHbb_'+isel+ipass+'_boostedHiggs',   ';Leading AK8 jet Hbb discriminator', 40, 0, 1) )
                self.addObject( ROOT.TH1F('leadAK8JetMass_'+isel+ipass+'_boostedHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )
                self.addObject( ROOT.TH1F('resolvedWCandMass_'+isel+ipass+'_boostedHiggs',   ';W candidate mass', 60, 0, 300) )
                self.addObject( ROOT.TH1F('leadAK8JetRho_'+isel+ipass+'_boostedHiggs',   ';Leading AK8 jet #rho', 40, -10, 10) )
                self.addObject( ROOT.TH1F('leadAK8JetTau21_'+isel+ipass+'_boostedHiggs',   ';#Leading AK8 jet tau_{21}', 40, 0, 1) )
                self.addObject( ROOT.TH1F('leadAK8JetTau21DDT_'+isel+ipass+'_boostedHiggs',   ';#Leading AK8 jet tau_{21}^{DDT}', 40, 0, 1) )
                self.addObject( ROOT.TH2F('leadAK8JetMassPt_'+isel+ipass+'_boostedHiggs',   ';Leading AK8 jet mass;Leading AK8 jet pt', 60, 0, 300,  1500, 0, 1500) )
                self.addObject( ROOT.TH2F('leadAK8JetRhoPt_'+isel+ipass+'_boostedHiggs',   ';Leading AK8 jet #rho;Leading AK8 jet pt', 40, -10, 10,  1500, 0, 1500) )
                self.addObject( ROOT.TH3F('leadAK8JetRhoPtMass_'+isel+ipass+'_boostedHiggs',   ';Leading AK8 jet #rho;Leading AK8 jet pt;Leading AK8 jet mass', 60, 0, 300,  1500, 0, 1500, 60, 0, 300) )

                '''
                for ipt in range(len(rhalPtList)-1):
                    self.addObject( ROOT.TH1F('resolvedWCandMass_'+isel+ipass+'Pt'+str(rhalPtList[ipt])+'_boostedHiggs',   ';W candidate mass', 60, 0, 300) )
                    self.addObject( ROOT.TH1F('leadAK8JetMass_'+isel+ipass+'Pt'+str(rhalPtList[ipt])+'_boostedHiggs',   ';Leading AK8 jet mass', 60, 0, 300) )
                    self.addObject( ROOT.TH1F('leadAK8JetPt_'+isel+ipass+'Pt'+str(rhalPtList[ipt])+'_boostedHiggs',   ';Leading AK8 jet mass', 1500, 0, 1500) )
                    self.addObject( ROOT.TH1F('leadAK8JetRho_'+isel+ipass+'Pt'+str(rhalPtList[ipt])+'_boostedHiggs',   ';#rho', 40, -10, 10) )
                    self.addObject( ROOT.TH2F('leadAK8JetMassPt_'+isel+ipass+'Pt'+str(rhalPtList[ipt])+'_boostedHiggs',   ';Leading AK8 jet mass;Leading AK8 jet pt', 60, 0, 300,  1500, 0, 1500) )
                    self.addObject( ROOT.TH2F('leadAK8JetRhoPt_'+isel+ipass+'Pt'+str(rhalPtList[ipt])+'_boostedHiggs',   ';Leading AK8 jet #rho;Leading AK8 jet pt', 60, 0, 300,  1500, 0, 1500) )
                '''



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

    def listOfHistos(self, t ):
        self.addObject( ROOT.TH1F('nPVs'+t,   ';number of PVs',   100, 0, 100) )
        self.addObject( ROOT.TH1F('njets'+t,   ';number of jets',   20, 0, 20) )
        self.addObject( ROOT.TH1F('nbjetsCSV'+t,   ';number of bjets deepCSV',   20, 0, 20) )
        self.addObject( ROOT.TH1F('nbjetsFlav'+t,   ';number of bjets deepFlav',   20, 0, 20) )
        self.addObject( ROOT.TH1F('nleps'+t,   ';number of leptons',   20, 0, 20) )
        self.histnames = ['jet0', 'jet3', 'lep0', 'lep1', 'met']
        for val in self.histnames: self.addP4Hists( val, t )

    def addP4Hists(self, s, t ):
        self.addObject( ROOT.TH1F(s+'_pt'+t,  s+';p_{T} (GeV)',   500, 0, 5000) )
        self.addObject( ROOT.TH1F(s+'_eta'+t, s+';#eta', 100, -4.0, 4.0 ) )
        self.addObject( ROOT.TH1F(s+'_phi'+t, s+';#phi', 100, -3.14259, 3.14159) )
        self.addObject( ROOT.TH1F(s+'_mass'+t,s+';mass (GeV)', 100, 0, 1000) )
        if s.startswith('jet'):
            self.addObject( ROOT.TH1F(s+'_bDeepCSV'+t,s+';b deepCSV Discriminator', 40, -1, 1) )
            self.addObject( ROOT.TH1F(s+'_bDeepFlav'+t,s+';b deepFlav Discriminator', 40, -1, 1) )

    def leptonSF(self, lepton, leptonP4 ):

        if lepton.startswith("muon"):
            SFFileTrigger = ROOT.TFile( os.environ['CMSSW_BASE']+"/src/TTH/Analyzer/data/EfficienciesAndSF_2018Data_AfterMuonHLTUpdate.root" )
            histoSFTrigger = SFFileTrigger.Get("IsoMu24_PtEtaBins/pt_abseta_ratio")
            SFTrigger = histoSFTrigger.GetBinContent( histoSFTrigger.GetXaxis().FindBin( leptonP4.pt ), histoSFTrigger.GetYaxis().FindBin( abs(leptonP4.eta ) ) )

            SFFileID = ROOT.TFile( os.environ['CMSSW_BASE']+"/src/TTH/Analyzer/data/RunABCD_SF_ID.root" )
            histoSFID = SFFileID.Get("NUM_TightID_DEN_TrackerMuons_pt_abseta")
            SFID = histoSFID.GetBinContent( histoSFID.GetXaxis().FindBin( leptonP4.pt ), histoSFID.GetYaxis().FindBin( abs(leptonP4.eta ) ) ) if (leptonP4.pt < 120) else 1

            SFFileISO = ROOT.TFile( os.environ['CMSSW_BASE']+"/src/TTH/Analyzer/data/RunABCD_SF_ISO.root" )
            histoSFISO = SFFileISO.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta")
            SFISO = histoSFISO.GetBinContent( histoSFISO.GetXaxis().FindBin( leptonP4.pt ), histoSFISO.GetYaxis().FindBin( abs(leptonP4.eta ) ) ) if (leptonP4.pt < 120) else 1

        elif lepton.startswith("electron"):
            #SFFileTrigger = ROOT.TFile("../data/SingleEG_JetHT_Trigger_Scale_Factors_ttHbb_Legacy2018_v1.root")
            #histoSFTrigger = SFFileTrigger.Get("ele28_ht150_OR_ele35_ele_pt_ele_sceta")
            SFTrigger = 0 #histoSFTrigger.GetBinContent( histoSFTrigger.GetXaxis().FindBin( leptonP4.pt ), histoSFTrigger.GetYaxis().FindBin( abs(leptonP4.eta ) ) )

            #SFFileID = ROOT.TFile("../data/RunABCD_SF_ID.root")
            #histoSFID = SFFileID.Get("NUM_TightID_DEN_TrackerMuons_pt_abseta")
            SFID = 0 #histoSFID.GetBinContent( histoSFID.GetXaxis().FindBin( leptonP4.pt ), histoSFID.GetYaxis().FindBin( abs(leptonP4.eta ) ) ) if (leptonP4.pt < 120) else 1

            #SFFileISO = ROOT.TFile("../data/RunABCD_SF_ISO.root")
            #histoSFISO = SFFileISO.Get("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta")
            SFISO = 0 #histoSFISO.GetBinContent( histoSFISO.GetXaxis().FindBin( leptonP4.pt ), histoSFISO.GetYaxis().FindBin( abs(leptonP4.eta ) ) ) if (leptonP4.pt < 120) else 1
        else:
            SFTrigger = 0
            SFISO = 0
            SFID = 0

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
        """docstring for ABCDRegions"""

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


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("totalWeight",  "F");
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
        if (event.HLT_IsoMu24_eta2p1==1) or (event.HLT_IsoMu27==1): isSLmu = True
        elif (event.HLT_Ele35_WPTight_Gsf==1) or (event.HLT_Ele28_eta2p1_WPTight_Gsf_HT150==1): isSLmu = False
        else: isDLmumu = False

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        puppijets = Collection(event, "selectedPatJetsAK4PFPuppi")
        fatjets = Collection(event, "FatJet")
        PV = Object(event, 'PV')
        MET = Object(event, 'MET')

        ### Leptons
        vetoMuons = [ m for m in muons if (abs(m.eta)<2.4) and (m.pt>15) and (m.pfRelIso04_all<0.25) and (m.tightId==1) ]
        goodMuons = [ m for m in vetoMuons if (m.pt>29) and (m.pfRelIso04_all<0.15) ]

        ### Electrons, not completed
        vetoElectrons = [ e for e in electrons if (abs(e.eta)<2.4) and (e.pt>15) and not ( abs(e.deltaEtaSC+e.eta)>=1.4442 and abs(e.deltaEtaSC+e.eta)<=1.5660) and (e.cutBased>=4) ]
        goodElectrons = [ e for e in vetoElectrons if e.pt>30 ]

        goodLeptons = goodMuons + goodElectrons
        goodLeptons.sort(key=lambda x:x.pt, reverse=True)

        if isMC:
            if len(goodMuons)>0 and len(goodElectrons)==0 and isSLmu: leptonWeights= self.leptonSF( "muon", goodMuons[0] )
            elif len(goodMuons)==0 and len(goodElectrons)>0 and not isSLmu: leptonWeights = self.leptonSF( "electron", goodElectrons[0] )
            else: leptonWeights = [0, 0, 0]
        else: leptonWeights = [1, 1, 1]

        ### Jets
        looseJets = [ j for j in jets if (abs(j.eta<2.4)) and (j.pt>20) and (j.jetId>=2) and (j.puId>=4) ]
        goodJets = looseJets if (len(looseJets)>0) and (looseJets[0].pt>30) else []
        goodJetsNoLep = [ j for j in goodJets for l in goodLeptons if j.p4().DeltaR(l.p4())>=0.4  ]

        ### Bjets
        goodBjetsDeepCSV = [ b for b in goodJetsNoLep if b.btagDeepB>0.4941 ]
        goodBjetsDeepFlav = [ b for b in goodJetsNoLep if b.btagDeepFlavB>0.3033 ]

        ### Fatjets
        looseFatJets = [ j for j in fatjets if (abs(j.eta<2.4)) and (j.pt>200) ]
        ## clones for further studies
        badFatJets = [ j for j in fatjets if (abs(j.eta<2.4)) and (j.pt>200) ]
        allhiggsCandidates = [ j for j in fatjets if (abs(j.eta<2.4)) and (j.pt>250) ]
        badFatJets_boostedW = [ j for j in fatjets if (abs(j.eta<2.4)) and (j.pt>200) ]

        ### Selection
        metcut = (MET.pt>20)
        nlepcut = (len(goodLeptons)>0)
        njetscut = (len(goodJetsNoLep)>3)
        nbjetscut = (len(goodBjetsDeepFlav)>1)

        #### Weight
        if isMC: weight = event.puWeight * np.sign(event.genWeight) * np.prod(leptonWeights)
        else: weight = 1
        self.out.fillBranch('totalWeight', weight)

        getattr( self, 'nEvents' ).Fill( 0 )
        if ( metcut and nlepcut ): getattr( self, 'nEvents' ).Fill( 1 )
        if ( metcut and nlepcut and (njetscut and nbjetscut) ) : getattr( self, 'nEvents' ).Fill( 2 )
        if ( metcut and nlepcut and not (njetscut and nbjetscut) ) : getattr( self, 'nEvents' ).Fill( 3 )
        if ( metcut and nlepcut and not (njetscut or nbjetscut) ) : getattr( self, 'nEvents' ).Fill( 4 )

        #################################### Boosted
        orthogonalcut = metcut and nlepcut #and not (njetscut and nbjetscut)

        if orthogonalcut:

            ### General
            getattr( self, 'nlooseFatJets' ).Fill( len(looseFatJets), weight )
            getattr( self, 'nleps' ).Fill( len(goodLeptons) )
            getattr( self, 'nCHSjets' ).Fill( len(goodJetsNoLep) )
            getattr( self, 'nCHSBjets' ).Fill( len(goodBjetsDeepFlav) )
            getattr( self, 'lepPt' ).Fill( goodLeptons[0].pt )
            getattr( self, 'lepEta' ).Fill( goodLeptons[0].eta )
            getattr( self, 'METPt' ).Fill( MET.pt )

            ### Leptonic W
            METp4 = ROOT.TLorentzVector()
            METp4.SetPtEtaPhiM( MET.pt, 0, MET.phi, 0 )#MET.pt )
            neuPz = self.METzCalculator( goodLeptons[0].p4(), METp4 )
            neutrinoP4 = ROOT.TLorentzVector()
            neutrinoP4.SetPxPyPzE( METp4.Px(), METp4.Py(), neuPz, ROOT.TMath.Sqrt( METp4.Px()*METp4.Px() + METp4.Py()*METp4.Py() + neuPz*neuPz )  )
            lepW = goodLeptons[0].p4() + neutrinoP4
            getattr( self, 'lepWMass' ).Fill( lepW.M() )

            ### Puppi Jets
            loosePuppiJets = [ j for j in puppijets if (abs(j.eta<2.4)) and (j.pt>30) and (j.jetId>=2) ]
            goodPuppiJetsNoLep = [ j for j in loosePuppiJets for l in goodLeptons if j.p4().DeltaR(l.p4())>=0.4  ]

            ### Bjets
            goodBjetsDeepCSV = [ b for b in goodPuppiJetsNoLep if (b.pfDeepCSVJetTags_probb+b.pfDeepCSVJetTags_probbb)>0.4941 ]

            if len(allhiggsCandidates)>0:
            #if len(looseFatJets)>0:

                ######################################################################
                ######################################################################
                ### If only boosted Higgs:
                Hbbcut = 0.9
                tau21cut = 0.35
                tau21DDTcut = 0.43
                FatJet_msoftdrop = allhiggsCandidates[0].msoftdrop
                FatJet_pt = allhiggsCandidates[0].pt
                #FatJet_Hbb = allhiggsCandidates[0].btagDDBvL
                #FatJet_Hbb = allhiggsCandidates[0].deepTag_H
                FatJet_Hbb = allhiggsCandidates[0].deepTagMD_HbbvsQCD
                FatJet_Top = allhiggsCandidates[0].deepTagMD_TvsQCD
                FatJet_tau21 = allhiggsCandidates[0].tau2/allhiggsCandidates[0].tau1
                FatJet_rho = ROOT.TMath.Log( FatJet_msoftdrop*FatJet_msoftdrop/(FatJet_pt*FatJet_pt) )
                FatJet_tau21DDT = FatJet_tau21 + 0.08 * ROOT.TMath.Log( FatJet_msoftdrop*FatJet_msoftdrop/(FatJet_pt) )
                getattr( self, 'leadAK8JetMass_boostedHiggs' ).Fill( FatJet_msoftdrop )
                getattr( self, 'leadAK8JetPt_boostedHiggs' ).Fill( FatJet_pt )
                getattr( self, 'leadAK8JetRho_boostedHiggs' ).Fill( FatJet_rho )
                getattr( self, 'leadAK8JetTau21_boostedHiggs' ).Fill( FatJet_tau21 )
                getattr( self, 'leadAK8JetTau21DDT_boostedHiggs' ).Fill( FatJet_tau21DDT )
                getattr( self, 'leadAK8JetN2_boostedHiggs' ).Fill( allhiggsCandidates[0].n2b1 )
                getattr( self, 'leadAK8JetHbb_boostedHiggs' ).Fill( FatJet_Hbb )
                getattr( self, 'leadAK8JetdeepAK8HbbMDTop_boostedHiggs' ).Fill( FatJet_Hbb, allhiggsCandidates[0].deepTagMD_TvsQCD )
                getattr( self, 'leadAK8JetdeepAK8HbbMDDDB_boostedHiggs' ).Fill( FatJet_Hbb, allhiggsCandidates[0].btagDDBvL )


                cleanPuppiJets_Hcand = [ j for j in goodPuppiJetsNoLep if (j.p4().DeltaR(allhiggsCandidates[0].p4())>=1.2)  ]
                goodPuppiBjets_Hcand = [ b for b in cleanPuppiJets_Hcand if (b.pfDeepCSVJetTags_probb+b.pfDeepCSVJetTags_probbb)>0.4941 ]
                goodPuppiJets_Hcand = [ b for b in cleanPuppiJets_Hcand if (b.pfDeepCSVJetTags_probb+b.pfDeepCSVJetTags_probbb)<0.4941 ]
                getattr( self, 'nCleanPuppiJets_boostedHiggs' ).Fill( len(cleanPuppiJets_Hcand) if cleanPuppiJets_Hcand else 0 )
                getattr( self, 'nGoodPuppiJets_boostedHiggs' ).Fill( len(goodPuppiJets_Hcand) if goodPuppiJets_Hcand else 0 )
                getattr( self, 'nGoodPuppiBjets_boostedHiggs' ).Fill( len(goodPuppiBjets_Hcand) if goodPuppiBjets_Hcand else 0 )

                ##### FOR ABCD
                higgsSideA = ( FatJet_Hbb > .1 ) and ( FatJet_Hbb > Hbbcut ) and ( FatJet_tau21 < tau21cut )
                higgsSideB = ( FatJet_Hbb > .1 ) and ( FatJet_Hbb > Hbbcut ) and ( FatJet_tau21 > .55 )
                higgsSideC = ( FatJet_Hbb > .1 ) and ( FatJet_Hbb < 0.6 ) and ( FatJet_tau21 < tau21cut )
                higgsSideD = ( FatJet_Hbb > .1 ) and ( FatJet_Hbb < 0.6 ) and ( FatJet_tau21 > .55 )

                self.ABCDRegions( FatJet_msoftdrop, FatJet_Hbb, FatJet_tau21,
                            higgsSideA, higgsSideB, higgsSideC, higgsSideD,
                            'HbbvsTau21__boostedHiggs', 'leadAK8JetMass__boostedHiggs'
                            )

                ### rhalphabet
                getattr( self, 'leadAK8JetRhoHbb_boostedHiggs' ).Fill( FatJet_rho, FatJet_Hbb )
                getattr( self, 'leadAK8JetRhoTau21_boostedHiggs' ).Fill( FatJet_rho, FatJet_tau21 )
                getattr( self, 'leadAK8JetPtMassHbb_boostedHiggs' ).Fill( FatJet_msoftdrop, FatJet_pt, FatJet_Hbb )

                #### check if has jets and later bjets
                if len(goodPuppiJets_Hcand)>1:
                    getattr( self, 'nEvents' ).Fill( 7 )
                    if not (njetscut and nbjetscut): getattr( self, 'nEvents' ).Fill( 8 )
                    getattr( self, 'leadAK8JetMass_2J_boostedHiggs' ).Fill( FatJet_msoftdrop )
                    getattr( self, 'leadAK8JetPt_2J_boostedHiggs' ).Fill( FatJet_pt )


                    ##### reconstructing WW
                    smallestDiffW = 9999
                    jFromW = []
                    jjCandidates = []
                    for jpair in permutations(goodPuppiJets_Hcand, 2):
                        jjCandidates.append( jpair[0].p4()+jpair[1].p4() )
                        tmphadW = jpair[0].p4()+jpair[1].p4()
                        tmpDiff = abs(lepW.M() - tmphadW.M())
                        if tmpDiff < smallestDiffW:
                            smallestDiffW = tmpDiff
                            jFromW = [ jpair[0], jpair[1] ]
                    getattr( self, 'minDiffLepHadW' ).Fill( smallestDiffW )
                    hadW = jFromW[0].p4() + jFromW[1].p4()
                    getattr( self, 'resolvedWCandMass_2J_boostedHiggs' ).Fill( hadW.M() )
                    getattr( self, 'resolvedWCandHiggsCandMass_2J_boostedHiggs' ).Fill( hadW.M(), FatJet_msoftdrop )
                    deltaRWHiggs = hadW.DeltaR( allhiggsCandidates[0].p4() )
                    getattr( self, 'deltaRhadWHiggs_2J_boostedHiggs' ).Fill( deltaRWHiggs )
                    getattr( self, 'deltaRhadWHiggsMass_2J_boostedHiggs' ).Fill( deltaRWHiggs, FatJet_msoftdrop )
                    deltaRJJ = jFromW[0].p4().DeltaR( jFromW[1].p4() )
                    getattr( self, 'deltaRJJ_2J_boostedHiggs' ).Fill( deltaRJJ )
                    deltaRlepWHiggs = lepW.DeltaR( allhiggsCandidates[0].p4() )
                    getattr( self, 'deltaRlepWHiggs_2J_boostedHiggs' ).Fill( deltaRlepWHiggs )
                    getattr( self, 'deltaRlepWHiggsMass_2J_boostedHiggs' ).Fill( deltaRlepWHiggs, FatJet_msoftdrop )
                    getattr( self, 'deltaRlepWHiggsdeltaRhadWHiggs_2J_boostedHiggs' ).Fill( deltaRlepWHiggs, deltaRWHiggs )
                    deltaRlepWhadW = lepW.DeltaR( hadW )
                    getattr( self, 'deltaRlepWhadW_2J_boostedHiggs' ).Fill( deltaRlepWhadW )
                    getattr( self, 'deltaRlepWhadWHiggsMass_2J_boostedHiggs' ).Fill( deltaRlepWhadW, FatJet_msoftdrop )

                    self.ABCDRegions( FatJet_msoftdrop, FatJet_Hbb, FatJet_tau21,
                                higgsSideA, higgsSideB, higgsSideC, higgsSideD,
                                'HbbvsTau21__2J_boostedHiggs', 'leadAK8JetMass__2J_boostedHiggs'
                                )


                    if (hadW.M()>65 and hadW.M()<105):
                        getattr( self, 'leadAK8JetMass_2J2W_boostedHiggs' ).Fill( FatJet_msoftdrop )
                        getattr( self, 'leadAK8JetPt_2J2W_boostedHiggs' ).Fill( FatJet_pt )
                        getattr( self, 'resolvedWCandMass_2J2W_boostedHiggs' ).Fill( hadW.M() )
                        getattr( self, 'resolvedWCandHiggsCandMass_2J2W_boostedHiggs' ).Fill( hadW.M(), FatJet_msoftdrop )
                        getattr( self, 'deltaRhadWHiggs_2J2W_boostedHiggs' ).Fill( deltaRWHiggs )
                        getattr( self, 'deltaRhadWHiggsMass_2J2W_boostedHiggs' ).Fill( deltaRWHiggs, FatJet_msoftdrop )
                        getattr( self, 'deltaRJJ_2J2W_boostedHiggs' ).Fill( deltaRJJ )
                        getattr( self, 'deltaRlepWHiggs_2J2W_boostedHiggs' ).Fill( deltaRlepWHiggs )
                        getattr( self, 'deltaRlepWHiggsMass_2J2W_boostedHiggs' ).Fill( deltaRlepWHiggs, FatJet_msoftdrop )
                        getattr( self, 'deltaRlepWHiggsdeltaRhadWHiggs_2J2W_boostedHiggs' ).Fill( deltaRlepWHiggs, deltaRWHiggs )
                        getattr( self, 'deltaRlepWhadW_2J2W_boostedHiggs' ).Fill( deltaRlepWhadW )
                        getattr( self, 'deltaRlepWhadWHiggsMass_2J2W_boostedHiggs' ).Fill( deltaRlepWhadW, FatJet_msoftdrop )

                        ##### FOR ABCD
                        self.ABCDRegions( FatJet_msoftdrop, FatJet_Hbb, FatJet_tau21,
                                    higgsSideA, higgsSideB, higgsSideC, higgsSideD,
                                    'HbbvsTau21__2J2W_boostedHiggs', 'leadAK8JetMass__2J2W_boostedHiggs'
                                    )
                        ### rhalphabet
                        getattr( self, 'leadAK8JetRho_2J2W_boostedHiggs' ).Fill( FatJet_rho )
                        getattr( self, 'leadAK8JetTau21_2J2W_boostedHiggs' ).Fill( FatJet_tau21 )
                        getattr( self, 'leadAK8JetHbb_2J2W_boostedHiggs' ).Fill( FatJet_Hbb )
                        getattr( self, 'leadAK8JetRhoHbb_2J2W_boostedHiggs' ).Fill( FatJet_rho, FatJet_Hbb )
                        getattr( self, 'leadAK8JetRhoTau21_2J2W_boostedHiggs' ).Fill( FatJet_rho, FatJet_tau21 )
                        getattr( self, 'leadAK8JetPtMassHbb_2J2W_boostedHiggs' ).Fill( FatJet_msoftdrop, FatJet_pt, FatJet_Hbb )

                        if len(goodPuppiBjets_Hcand)>0:
                            getattr( self, 'leadAK8JetMass_2J2W1B_boostedHiggs' ).Fill( FatJet_msoftdrop )
                            getattr( self, 'leadAK8JetPt_2J2W1B_boostedHiggs' ).Fill( FatJet_pt )
                        if len(goodPuppiBjets_Hcand)>1:
                            getattr( self, 'leadAK8JetMass_2J2W2B_boostedHiggs' ).Fill( FatJet_msoftdrop )
                            getattr( self, 'leadAK8JetPt_2J2W2B_boostedHiggs' ).Fill( FatJet_pt )
                    ### else no w mass window
                    else:
                        getattr( self, 'noHiggsCandMass_2J2W_boostedHiggs' ).Fill( FatJet_msoftdrop )
                        getattr( self, 'noHiggsCandHbb_2J2W_boostedHiggs' ).Fill(  FatJet_Hbb )
                        getattr( self, 'noHiggsCandTau21_2J2W_boostedHiggs' ).Fill(  FatJet_tau21 )
                        if higgsSideA:
                            getattr( self, 'leadAK8JetMass_A_2Jno2W_boostedHiggs' ).Fill( FatJet_msoftdrop )

                    if (deltaRlepWHiggs>1) and (deltaRWHiggs>1):
                        getattr( self, 'leadAK8JetMass_2JdeltaR_boostedHiggs' ).Fill( FatJet_msoftdrop )
                        getattr( self, 'leadAK8JetPt_2JdeltaR_boostedHiggs' ).Fill( FatJet_pt )
                        getattr( self, 'resolvedWCandMass_2JdeltaR_boostedHiggs' ).Fill( hadW.M() )
                        getattr( self, 'leadAK8JetRho_2JdeltaR_boostedHiggs' ).Fill( FatJet_rho )
                        getattr( self, 'leadAK8JetTau21_2JdeltaR_boostedHiggs' ).Fill( FatJet_tau21 )
                        getattr( self, 'leadAK8JetTau21DDT_2JdeltaR_boostedHiggs' ).Fill( FatJet_tau21DDT )
                        getattr( self, 'leadAK8JetHbb_2JdeltaR_boostedHiggs' ).Fill( FatJet_Hbb )
                        ##### FOR ABCD
                        self.ABCDRegions( FatJet_msoftdrop, FatJet_Hbb, FatJet_tau21,
                                    higgsSideA, higgsSideB, higgsSideC, higgsSideD,
                                    'HbbvsTau21__2JdeltaR_boostedHiggs', 'leadAK8JetMass__2JdeltaR_boostedHiggs'
                                    )

                        ############ THIS IS THE "FINAL" SELECTION
                        if (hadW.M()>65 and hadW.M()<105):
                            getattr( self, 'leadAK8JetMass_2JdeltaR2W_boostedHiggs' ).Fill( FatJet_msoftdrop )
                            getattr( self, 'leadAK8JetPt_2JdeltaR2W_boostedHiggs' ).Fill( FatJet_pt )
                            getattr( self, 'resolvedWCandMass_2JdeltaR2W_boostedHiggs' ).Fill( hadW.M() )
                            getattr( self, 'leadAK8JetRho_2JdeltaR2W_boostedHiggs' ).Fill( FatJet_rho )
                            getattr( self, 'leadAK8JetTau21_2JdeltaR2W_boostedHiggs' ).Fill( FatJet_tau21 )
                            getattr( self, 'leadAK8JetTau21DDT_2JdeltaR2W_boostedHiggs' ).Fill( FatJet_tau21DDT )
                            getattr( self, 'leadAK8JetHbb_2JdeltaR2W_boostedHiggs' ).Fill( FatJet_Hbb )
                            ##### FOR ABCD
                            self.ABCDRegions( FatJet_msoftdrop, FatJet_Hbb, FatJet_tau21,
                                        higgsSideA, higgsSideB, higgsSideC, higgsSideD,
                                        'HbbvsTau21__2JdeltaR2W_boostedHiggs', 'leadAK8JetMass__2JdeltaR2W_boostedHiggs'
                                        )
                            ##### FOR Rhalphabet
                            if (FatJet_tau21<tau21cut):
                            #if (FatJet_tau21DDT<tau21DDTcut):
                                getattr( self, 'leadAK8JetMass_2JdeltaR2WTau21DDT_boostedHiggs' ).Fill( FatJet_msoftdrop )
                                getattr( self, 'leadAK8JetMass_2JdeltaR2WTau21DDT_boostedHiggs' ).Fill( FatJet_msoftdrop )
                                getattr( self, 'resolvedWCandMass_2JdeltaR2WTau21DDT_boostedHiggs' ).Fill( hadW.M() )
                                getattr( self, 'leadAK8JetRho_2JdeltaR2WTau21DDT_boostedHiggs' ).Fill( FatJet_rho )
                                getattr( self, 'leadAK8JetTau21_2JdeltaR2WTau21DDT_boostedHiggs' ).Fill( FatJet_tau21 )
                                getattr( self, 'leadAK8JetTau21DDT_2JdeltaR2WTau21DDT_boostedHiggs' ).Fill( FatJet_tau21DDT )
                                getattr( self, 'leadAK8JetHbb_2JdeltaR2WTau21DDT_boostedHiggs' ).Fill( FatJet_Hbb )

                                if (FatJet_Hbb>Hbbcut):
                                    getattr( self, 'leadAK8JetMass_2JdeltaR2WTau21DDT_Pass_boostedHiggs' ).Fill( FatJet_msoftdrop )
                                    getattr( self, 'resolvedWCandMass_2JdeltaR2WTau21DDT_Pass_boostedHiggs' ).Fill( hadW.M() )
                                    getattr( self, 'leadAK8JetRho_2JdeltaR2WTau21DDT_Pass_boostedHiggs' ).Fill( FatJet_rho )
                                    getattr( self, 'leadAK8JetTau21_2JdeltaR2WTau21DDT_Pass_boostedHiggs' ).Fill( FatJet_tau21 )
                                    getattr( self, 'leadAK8JetTau21DDT_2JdeltaR2WTau21DDT_Pass_boostedHiggs' ).Fill( FatJet_tau21DDT )
                                    getattr( self, 'leadAK8JetHbb_2JdeltaR2WTau21DDT_Pass_boostedHiggs' ).Fill( FatJet_Hbb )
                                    getattr( self, 'leadAK8JetMassPt_2JdeltaR2WTau21DDT_Pass_boostedHiggs' ).Fill( FatJet_msoftdrop, FatJet_pt )
                                    getattr( self, 'leadAK8JetRhoPt_2JdeltaR2WTau21DDT_Pass_boostedHiggs' ).Fill( FatJet_rho, FatJet_pt )
                                    getattr( self, 'leadAK8JetRhoPtMass_2JdeltaR2WTau21DDT_Pass_boostedHiggs' ).Fill( FatJet_rho, FatJet_pt, FatJet_msoftdrop )

                                    '''
                                    for ipt in range(len(rhalPtList)-1):
                                        if (FatJet_pt > rhalPtList[ipt]) and (FatJet_pt<rhalPtList[ipt+1]):
                                            getattr( self, 'resolvedWCandMass_2JdeltaR2WTau21DDT_PassPt'+str(rhalPtList[ipt])+'_boostedHiggs' ).Fill( hadW.M() )
                                            getattr( self, 'leadAK8JetMass_2JdeltaR2WTau21DDT_PassPt'+str(rhalPtList[ipt])+'_boostedHiggs' ).Fill( FatJet_msoftdrop )
                                            getattr( self, 'leadAK8JetPt_2JdeltaR2WTau21DDT_PassPt'+str(rhalPtList[ipt])+'_boostedHiggs' ).Fill( FatJet_pt )
                                            getattr( self, 'leadAK8JetRho_2JdeltaR2WTau21DDT_PassPt'+str(rhalPtList[ipt])+'_boostedHiggs' ).Fill( FatJet_rho )
                                            getattr( self, 'leadAK8JetMassPt_2JdeltaR2WTau21DDT_PassPt'+str(rhalPtList[ipt])+'_boostedHiggs' ).Fill( FatJet_msoftdrop, FatJet_pt )
                                            getattr( self, 'leadAK8JetRhoPt_2JdeltaR2WTau21DDT_PassPt'+str(rhalPtList[ipt])+'_boostedHiggs' ).Fill( FatJet_rho, FatJet_pt )

                                    '''


                                else:
                                    getattr( self, 'leadAK8JetMass_2JdeltaR2WTau21DDT_Fail_boostedHiggs' ).Fill( FatJet_msoftdrop )
                                    getattr( self, 'resolvedWCandMass_2JdeltaR2WTau21DDT_Fail_boostedHiggs' ).Fill( hadW.M() )
                                    getattr( self, 'leadAK8JetRho_2JdeltaR2WTau21DDT_Fail_boostedHiggs' ).Fill( FatJet_rho )
                                    getattr( self, 'leadAK8JetTau21_2JdeltaR2WTau21DDT_Fail_boostedHiggs' ).Fill( FatJet_tau21 )
                                    getattr( self, 'leadAK8JetTau21DDT_2JdeltaR2WTau21DDT_Fail_boostedHiggs' ).Fill( FatJet_tau21DDT )
                                    getattr( self, 'leadAK8JetHbb_2JdeltaR2WTau21DDT_Fail_boostedHiggs' ).Fill( FatJet_Hbb )
                                    getattr( self, 'leadAK8JetMassPt_2JdeltaR2WTau21DDT_Fail_boostedHiggs' ).Fill( FatJet_msoftdrop, FatJet_pt )
                                    getattr( self, 'leadAK8JetRhoPt_2JdeltaR2WTau21DDT_Fail_boostedHiggs' ).Fill( FatJet_rho, FatJet_pt )
                                    getattr( self, 'leadAK8JetRhoPtMass_2JdeltaR2WTau21DDT_Fail_boostedHiggs' ).Fill( FatJet_rho, FatJet_pt, FatJet_msoftdrop )

                                    '''
                                    for ipt in range(len(rhalPtList)-1):
                                        if (FatJet_pt > rhalPtList[ipt]) and (FatJet_pt<rhalPtList[ipt+1]):
                                            getattr( self, 'resolvedWCandMass_2JdeltaR2WTau21DDT_FailPt'+str(rhalPtList[ipt])+'_boostedHiggs' ).Fill( hadW.M() )
                                            getattr( self, 'leadAK8JetMass_2JdeltaR2WTau21DDT_FailPt'+str(rhalPtList[ipt])+'_boostedHiggs' ).Fill( FatJet_msoftdrop )
                                            getattr( self, 'leadAK8JetPt_2JdeltaR2WTau21DDT_FailPt'+str(rhalPtList[ipt])+'_boostedHiggs' ).Fill( FatJet_pt )
                                            getattr( self, 'leadAK8JetRho_2JdeltaR2WTau21DDT_FailPt'+str(rhalPtList[ipt])+'_boostedHiggs' ).Fill( FatJet_rho )
                                            getattr( self, 'leadAK8JetMassPt_2JdeltaR2WTau21DDT_FailPt'+str(rhalPtList[ipt])+'_boostedHiggs' ).Fill( FatJet_msoftdrop, FatJet_pt )
                                            getattr( self, 'leadAK8JetRhoPt_2JdeltaR2WTau21DDT_FailPt'+str(rhalPtList[ipt])+'_boostedHiggs' ).Fill( FatJet_rho, FatJet_pt )
                                    '''


                            if len(goodPuppiBjets_Hcand)>0:
                                getattr( self, 'leadAK8JetMass_2JdeltaR2W1B_boostedHiggs' ).Fill( FatJet_msoftdrop )
                                getattr( self, 'resolvedWCandMass_2JdeltaR2W1B_boostedHiggs' ).Fill( hadW.M() )
                                getattr( self, 'leadAK8JetRho_2JdeltaR2W1B_boostedHiggs' ).Fill( FatJet_rho )
                                getattr( self, 'leadAK8JetTau21_2JdeltaR2W1B_boostedHiggs' ).Fill( FatJet_tau21 )
                                getattr( self, 'leadAK8JetHbb_2JdeltaR2W1B_boostedHiggs' ).Fill( FatJet_Hbb )
                                ##### FOR ABCD
                                self.ABCDRegions( FatJet_msoftdrop, FatJet_Hbb, FatJet_tau21,
                                            higgsSideA, higgsSideB, higgsSideC, higgsSideD,
                                            'HbbvsTau21__2JdeltaR2W1B_boostedHiggs', 'leadAK8JetMass__2JdeltaR2W1B_boostedHiggs'
                                            )
                            else:
                                getattr( self, 'noHiggsCandMass_2JdeltaR2W1B_boostedHiggs' ).Fill( FatJet_msoftdrop )

                            if len(goodPuppiBjets_Hcand)>1:
                                getattr( self, 'leadAK8JetMass_2JdeltaR2W2B_boostedHiggs' ).Fill( FatJet_msoftdrop )
                                getattr( self, 'resolvedWCandMass_2JdeltaR2W2B_boostedHiggs' ).Fill( hadW.M() )
                                getattr( self, 'leadAK8JetRho_2JdeltaR2W2B_boostedHiggs' ).Fill( FatJet_rho )
                                getattr( self, 'leadAK8JetTau21_2JdeltaR2W2B_boostedHiggs' ).Fill( FatJet_tau21 )
                                getattr( self, 'leadAK8JetHbb_2JdeltaR2W2B_boostedHiggs' ).Fill( FatJet_Hbb )
                                ##### FOR ABCD
                                self.ABCDRegions( FatJet_msoftdrop, FatJet_Hbb, FatJet_tau21,
                                            higgsSideA, higgsSideB, higgsSideC, higgsSideD,
                                            'HbbvsTau21__2JdeltaR2W2B_boostedHiggs', 'leadAK8JetMass__2JdeltaR2W2B_boostedHiggs'
                                            )
                            else:
                                getattr( self, 'noHiggsCandMass_2JdeltaR2W2B_boostedHiggs' ).Fill( FatJet_msoftdrop )

                        else:
                            getattr( self, 'noHiggsCandMass_2JdeltaR2W_boostedHiggs' ).Fill( FatJet_msoftdrop )

                    else:
                        getattr( self, 'noHiggsCandMass_2JdeltaR_boostedHiggs' ).Fill( FatJet_msoftdrop )


                    if len(goodPuppiBjets_Hcand)>0:
                        getattr( self, 'leadAK8JetMass_2J1B_boostedHiggs' ).Fill( FatJet_msoftdrop )
                        deltaR1BHiggs = goodPuppiBjets_Hcand[0].p4().DeltaR( allhiggsCandidates[0].p4() )
                        getattr( self, 'deltaR1BHiggs_2J1B_boostedHiggs' ).Fill( deltaR1BHiggs )
                    if len(goodPuppiBjets_Hcand)>1:
                        getattr( self, 'leadAK8JetMass_2J2B_boostedHiggs' ).Fill( FatJet_msoftdrop )



                #### check if has only bjets
                if len(goodPuppiBjets_Hcand)>0:
                    getattr( self, 'leadAK8JetMass_1B_boostedHiggs' ).Fill( FatJet_msoftdrop )
                    deltaR1BHiggs = goodPuppiBjets_Hcand[0].p4().DeltaR( allhiggsCandidates[0].p4() )
                    getattr( self, 'deltaR1BHiggs_1B_boostedHiggs' ).Fill( deltaR1BHiggs )
                if len(goodPuppiBjets_Hcand)>1:
                    getattr( self, 'leadAK8JetMass_2B_boostedHiggs' ).Fill( FatJet_msoftdrop )

                ### For boosted W:
                if len(looseFatJets)>0: looseFatJets.remove(allhiggsCandidates[0])

                goodWCandidate = looseFatJets[0] if (len(looseFatJets)>0) and ((looseFatJets[0].tau2/looseFatJets[0].tau1)<tau21cut) else None

                if goodWCandidate:

                    getattr( self, 'leadAK8JetMass_W_boostedHiggs' ).Fill( FatJet_msoftdrop )
                    getattr( self, 'boostedWCandMass_W_boostedHiggs' ).Fill( goodWCandidate.msoftdrop )

                    ##### FOR ABCD
                    self.ABCDRegions( FatJet_msoftdrop, FatJet_Hbb, FatJet_tau21,
                                higgsSideA, higgsSideB, higgsSideC, higgsSideD,
                                'HbbvsTau21__W_boostedHiggs', 'leadAK8JetMass__W_boostedHiggs'
                                )

                    if len(goodPuppiBjets_Hcand)>0:
                        getattr( self, 'leadAK8JetMass_W1B_boostedHiggs' ).Fill( FatJet_msoftdrop )
                        getattr( self, 'boostedWCandMass_W1B_boostedHiggs' ).Fill( goodWCandidate.msoftdrop )

                        ##### FOR ABCD
                        self.ABCDRegions( FatJet_msoftdrop, FatJet_Hbb, FatJet_tau21,
                                    higgsSideA, higgsSideB, higgsSideC, higgsSideD,
                                    'HbbvsTau21__W1B_boostedHiggs', 'leadAK8JetMass__W1B_boostedHiggs'
                                    )
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
                higgsCandidates = [ j for j in allhiggsCandidates if ( (j.deepTagMD_HbbvsQCD > Hbbcut ) and (j.tau2/j.tau1 < tau21cut) ) ]
                goodHiggsCandidate = max(higgsCandidates, key=lambda j: j.deepTagMD_HbbvsQCD) if len(higgsCandidates)>0 else None
                if goodHiggsCandidate:
                    badFatJets.remove(goodHiggsCandidate)

                ### W candidate
                wCandidates = [ j for j in badFatJets if (j.tau2/j.tau1 < tau21cut) ]
                goodWCandidate = min(wCandidates, key=lambda j: j.tau2/j.tau1 ) if len(wCandidates)>0 else None
                if goodWCandidate: badFatJets.remove(goodWCandidate)

                ### Top candidate
                topCandidates = [ j for j in badFatJets if (j.tau3/j.tau2 < 0.4) ]
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
                getattr( self, 'leadAK8JetMass' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )



        return True


#myboostedAnalyzer = lambda : boostedAnalyzer()
