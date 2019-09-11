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


class quickAnalyzer(Module):
    def __init__(self, sample="None"):
    #def __init__(self, sample="None", parameters={}):
	self.writeHistFile=True
        self.sample= sample
        #self.parameters = parameters

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

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
        self.addObject( ROOT.TH1F('HiggsCandMass',   ';Higgs candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('TopCandMass_TopHiggs',   ';Top candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('WCandMass_TopHiggs',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('HiggsCandMass_TopHiggs',   ';Higgs candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('TopCandMass_WHiggs',   ';Top candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('WCandMass_WHiggs',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('HiggsCandMass_WHiggs',   ';Higgs candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('TopCandMass_WTop',   ';Top candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('WCandMass_WTop',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('HiggsCandMass_WTop',   ';Higgs candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('TopCandMass_Top',   ';Top candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('WCandMass_W',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('HiggsCandMass_Higgs',   ';Higgs candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('TopCandMass_PuppiJets',   ';Top candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('WCandMass_PuppiJets',   ';W candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('HiggsCandMass_PuppiJets',   ';Higgs candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('nGoodPuppiBJets',   ';number of good puppi bjets',   10, 0, 10) )

        self.addObject( ROOT.TH1F('minDiffLepHadTop',   ';min difference between lep and had Top',   100, 0, 100) )
        self.addObject( ROOT.TH1F('lepTopCandMass_boostedW',   ';leptonic Top candidate masses', 60, 0, 300) )
        self.addObject( ROOT.TH1F('hadTopCandMass_boostedW',   ';hadronic Top candidate masses', 60, 0, 300) )
        self.addObject( ROOT.TH1F('boostedHiggsCandPt_boostedW',   ';boosted Higgs candidate pt', 1000, 0, 1000) )
        self.addObject( ROOT.TH1F('boostedHiggsCandMass_boostedW',   ';boosted Higgs candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('resolvedHiggsCandPt_boostedW',   ';resolved Higgs candidate pt', 1000, 0, 1000) )
        self.addObject( ROOT.TH1F('resolvedHiggsCandMass_boostedW',   ';resolved Higgs candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH1F('allResolvedHiggsCandPt_boostedW',   ';resolved Higgs candidate pt', 1000, 0, 1000) )
        self.addObject( ROOT.TH1F('allResolvedHiggsCandMass_boostedW',   ';resolved Higgs candidate mass', 60, 0, 300) )
        self.addObject( ROOT.TH2F('allResolvedHiggsCandMassPt_boostedW',   ';resolved Higgs candidate mass', 60, 0, 300, 100, 0, 1000) )

        self.addObject( ROOT.TH1F('leadingBjetPt_boostedW',   ';leading Bjet p_{T} (GeV)',   500, 0, 5000) )
        self.addObject( ROOT.TH1F('leadingBjetEta_boostedW',  ';leading Bjet #eta', 100, -4.0, 4.0 ) )
        self.addObject( ROOT.TH1F('leadingBjetBdisc_boostedW', ';leading Bjet Discriminator', 40, -1, 1) )
        self.addObject( ROOT.TH1F('subleadingBjetPt_boostedW',   ';subleading Bjet p_{T} (GeV)',   500, 0, 5000) )
        self.addObject( ROOT.TH1F('subleadingBjetEta_boostedW',  ';subleading Bjet #eta', 100, -4.0, 4.0 ) )
        self.addObject( ROOT.TH1F('subleadingBjetBdisc_boostedW', ';subleading Bjet Discriminator', 40, -1, 1) )

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

        ### Selection
        metcut = (MET.pt>20)
        nlepcut = (len(goodLeptons)>0)
        njetscut = (len(goodJetsNoLep)>3)
        nbjetscut = (len(goodBjetsDeepFlav)>2)

        #### Weight
        if isMC: weight = event.puWeight * np.sign(event.genWeight) * np.prod(leptonWeights)
        else: weight = 1
        self.out.fillBranch('totalWeight', weight)


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
            goodPuppiBjetsNoLep = [ j for j in loosePuppiJets for l in goodLeptons if j.p4().DeltaR(l.p4())>=0.4  ]

            ### Bjets
            goodBjetsDeepCSV = [ b for b in goodPuppiBjetsNoLep if (b.pfDeepCSVJetTags_probb+b.pfDeepCSVJetTags_probbb)>0.4941 ]

            if len(looseFatJets)>0:
                ### Higgs candidates
                ##higgsCandidates = [ j for j in looseFatJets if ( (j.btagHbb > 0.8 ) and (j.tau2/j.tau1 < 0.4) ) ] if len(looseFatJets)>0 else []
                higgsCandidates = [ j for j in looseFatJets if ( (j.deepTagMD_HbbvsQCD > 0.8 ) and (j.tau2/j.tau1 < 0.4) ) ] if len(looseFatJets)>0 else []
                goodHiggsCandidate = max(higgsCandidates, key=lambda j: j.btagHbb ) if len(higgsCandidates)>0 else None
                if goodHiggsCandidate:
                    looseFatJets.remove(goodHiggsCandidate)
                    #print 'Higgs', goodHiggsCandidate.pt, goodHiggsCandidate.btagHbb, goodHiggsCandidate.mass

                ### W candidate
                wCandidates = [ j for j in looseFatJets if (j.tau2/j.tau1 < 0.4) ]
                goodWCandidate = min(wCandidates, key=lambda j: j.tau2/j.tau1 ) if len(wCandidates)>0 else None

                if goodWCandidate:
                    if (goodWCandidate.msoftdrop > 50 ) and (goodWCandidate.msoftdrop < 120):
                        looseFatJets.remove(goodWCandidate)
                        #print 'W', goodWCandidate.pt, goodWCandidate.tau2/goodWCandidate.tau1, goodWCandidate.mass
                    else: goodWCandidate = None

                ### Top candidate
                topCandidates = [ j for j in looseFatJets if (j.tau3/j.tau2 < 0.4) ]
                goodTopCandidate = min(topCandidates, key=lambda j: j.tau3/j.tau2 ) if len(topCandidates)>0 else None     ## in case there are more than one top Candidate, choose the one with minimum tau32
                if goodTopCandidate:
                    if (goodTopCandidate.msoftdrop > 140 ) and (goodTopCandidate.msoftdrop < 200):
                        looseFatJets.remove(goodTopCandidate)
                        #print 'Top', goodTopCandidate.pt, goodTopCandidate.tau3/goodTopCandidate.tau2, goodTopCandidate.mass
                    else: goodTopCandidate = None

                badFatJets = looseFatJets
                goodCandidates = [ goodHiggsCandidate, goodWCandidate ]
                goodCandidates = list(filter(None, goodCandidates))

                goodEvent = False
                goodWEvent = False
                if goodTopCandidate and goodHiggsCandidate and not goodWCandidate:
                    goodEvents = 1
                    goodEvent = True
                    getattr( self, 'TopCandMass_TopHiggs' ).Fill( goodTopCandidate.msoftdrop if goodTopCandidate else -999 )
                    getattr( self, 'WCandMass_TopHiggs' ).Fill( goodWCandidate.msoftdrop if goodWCandidate else -999 )
                    getattr( self, 'HiggsCandMass_TopHiggs' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )
                elif goodWCandidate and goodHiggsCandidate and not goodTopCandidate:
                    goodEvent = goodWEvent = True
                    goodEvents = 2
                    getattr( self, 'TopCandMass_WHiggs' ).Fill( goodTopCandidate.msoftdrop if goodTopCandidate else -999 )
                    getattr( self, 'WCandMass_WHiggs' ).Fill( goodWCandidate.msoftdrop if goodWCandidate else -999 )
                    getattr( self, 'HiggsCandMass_WHiggs' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )
                elif goodWCandidate and goodTopCandidate and not goodHiggsCandidate:
                    goodEvents = 3
                    getattr( self, 'TopCandMass_WTop' ).Fill( goodTopCandidate.msoftdrop if goodTopCandidate else -999 )
                    getattr( self, 'WCandMass_WTop' ).Fill( goodWCandidate.msoftdrop if goodWCandidate else -999 )
                    getattr( self, 'HiggsCandMass_WTop' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )
                elif goodWCandidate and not ( goodTopCandidate and goodHiggsCandidate):
                    goodEvents = 4
                    goodWEvent = True
                    getattr( self, 'WCandMass_W' ).Fill( goodWCandidate.msoftdrop if goodWCandidate else -999 )
                elif goodTopCandidate and not ( goodWCandidate and goodHiggsCandidate):
                    goodEvents = 5
                    getattr( self, 'TopCandMass_Top' ).Fill( goodTopCandidate.msoftdrop if goodTopCandidate else -999 )
                elif goodHiggsCandidate and not ( goodWCandidate and goodTopCandidate):
                    goodEvents = 6
                    getattr( self, 'HiggsCandMass_Higgs' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )
                else: goodEvents = 0

                getattr( self, 'nbadFatJets' ).Fill( len(badFatJets) )
                getattr( self, 'ngoodEvents' ).Fill( goodEvents )
                getattr( self, 'TopCandMass' ).Fill( goodTopCandidate.msoftdrop if goodTopCandidate else -999 )
                getattr( self, 'WCandMass' ).Fill( goodWCandidate.msoftdrop if goodWCandidate else -999 )
                getattr( self, 'HiggsCandMass' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )

                if (len(goodBjetsDeepCSV)>0):

                    goodPuppiBjets = [ j for j in goodBjetsDeepCSV for f in goodCandidates if (j.p4().DeltaR(f.p4())>=1.2)  ]
                    getattr( self, 'nGoodPuppiBJets' ).Fill( len(goodPuppiBjets) )

                    if len(goodPuppiBjets)>1 and goodEvent:
                        getattr( self, 'TopCandMass_PuppiJets' ).Fill( goodTopCandidate.msoftdrop if goodTopCandidate else -999 )
                        getattr( self, 'WCandMass_PuppiJets' ).Fill( goodWCandidate.msoftdrop if goodWCandidate else -999 )
                        getattr( self, 'HiggsCandMass_PuppiJets' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )

                    if len(goodPuppiBjets)>1 and goodWEvent:

                        smallestDiffTop = 9999
                        bFromTop = []
                        bbCandidates = []
                        for bpair in permutations(goodPuppiBjets, 2):
                            bbCandidates.append( bpair[0].p4()+bpair[1].p4() )
                            tmplepTop = lepW + bpair[0].p4()
                            tmphadTop = goodWCandidate.p4() + bpair[1].p4()
                            tmpDiff = abs(tmplepTop.M() - tmphadTop.M())
                            if tmpDiff < smallestDiffTop:
                                smallestDiffTop = tmpDiff
                                bFromTop = [ bpair[0], bpair[1] ]
                        getattr( self, 'minDiffLepHadTop' ).Fill( smallestDiffTop )
                        lepTop = lepW + bFromTop[0].p4()
                        hadTop = goodWCandidate.p4() + bFromTop[1].p4()
                        getattr( self, 'lepTopCandMass_boostedW' ).Fill( lepTop.M() )
                        getattr( self, 'hadTopCandMass_boostedW' ).Fill( hadTop.M() )
                        getattr( self, 'boostedHiggsCandMass_boostedW' ).Fill( goodHiggsCandidate.msoftdrop if goodHiggsCandidate else -999 )
                        getattr( self, 'boostedHiggsCandPt_boostedW' ).Fill( goodHiggsCandidate.pt if goodHiggsCandidate else -999 )

                        if (lepTop.M() < 200) and (lepTop.M() > 140):
                            goodPuppiBjets.remove(bFromTop[0])
                            goodPuppiBjets.remove(bFromTop[1])

                        if len(goodPuppiBjets)>1:
                            getattr( self, 'leadingBjetPt_boostedW' ).Fill( goodPuppiBjets[0].pt )
                            getattr( self, 'leadingBjetEta_boostedW' ).Fill( goodPuppiBjets[0].eta )
                            getattr( self, 'leadingBjetBdisc_boostedW' ).Fill( (goodPuppiBjets[0].pfDeepCSVJetTags_probb+goodPuppiBjets[0].pfDeepCSVJetTags_probbb) )
                            getattr( self, 'subleadingBjetPt_boostedW' ).Fill( goodPuppiBjets[1].pt )
                            getattr( self, 'subleadingBjetEta_boostedW' ).Fill( goodPuppiBjets[1].eta )
                            getattr( self, 'subleadingBjetBdisc_boostedW' ).Fill( (goodPuppiBjets[1].pfDeepCSVJetTags_probb+goodPuppiBjets[1].pfDeepCSVJetTags_probbb) )
                            resHiggs = goodPuppiBjets[0].p4() + goodPuppiBjets[1].p4()
                            getattr( self, 'resolvedHiggsCandPt_boostedW' ).Fill( resHiggs.Pt() )
                            getattr( self, 'resolvedHiggsCandMass_boostedW' ).Fill( resHiggs.M() )
                            for bb in bbCandidates:
                                getattr( self, 'allResolvedHiggsCandPt_boostedW' ).Fill( bb.Pt() )
                                getattr( self, 'allResolvedHiggsCandMass_boostedW' ).Fill( bb.M() )
                                getattr( self, 'allResolvedHiggsCandMassPt_boostedW' ).Fill( bb.M(), bb.Pt() )



        #### FIlling trees
#        self.out.fillBranch('LeptonSFTrigger', leptonWeights[0])
#        self.out.fillBranch('LeptonSFID', leptonWeights[1])
#        self.out.fillBranch('LeptonSFISO', leptonWeights[2])
#        self.out.fillBranch('nGoodLep', len(goodLeptons))
#        self.out.fillBranch('GoodLep_pt', [l.pt for l in goodLeptons] )
#        self.out.fillBranch('GoodLep_eta', [l.eta for l in goodLeptons] )
#        self.out.fillBranch('GoodLep_phi', [l.phi for l in goodLeptons] )
#        self.out.fillBranch('GoodLep_mass', [l.mass for l in goodLeptons] )
#        self.out.fillBranch('nGoodLep', len(goodLeptons))
#        self.out.fillBranch('GoodJet_pt', [j.pt for j in goodJetsNoLep] )
#        self.out.fillBranch('GoodJet_eta', [j.eta for j in goodJetsNoLep] )
#        self.out.fillBranch('GoodJet_phi', [j.phi for j in goodJetsNoLep] )
#        self.out.fillBranch('GoodJet_mass', [j.mass for j in goodJetsNoLep] )
#        self.out.fillBranch('GoodJet_btagDeepCSV', [j.btagDeepB for j in goodJetsNoLep] )
#        self.out.fillBranch('GoodJet_btagDeepFlav', [j.btagDeepFlavB for j in goodJetsNoLep] )


        '''
        getattr( self, 'nPVs_presel' ).Fill( PV.npvsGood )
        getattr( self, 'njets_presel' ).Fill( len(goodJetsNoLep) )
        getattr( self, 'nbjetsCSV_presel' ).Fill( len(goodBjetsDeepCSV) )
        getattr( self, 'nbjetsFlav_presel' ).Fill( len(goodBjetsDeepFlav) )
        getattr( self, 'nleps_presel' ).Fill( len(goodLeptons) )
        getattr( self, 'met_pt_presel' ).Fill( MET.pt )
        if len(goodJetsNoLep)>0:
            getattr( self, 'jet0_pt_presel' ).Fill( goodJetsNoLep[0].pt )
            getattr( self, 'jet0_eta_presel' ).Fill( goodJetsNoLep[0].eta )
            getattr( self, 'jet0_phi_presel' ).Fill( goodJetsNoLep[0].phi )
            getattr( self, 'jet0_mass_presel' ).Fill( goodJetsNoLep[0].mass )
            getattr( self, 'jet0_bDeepCSV_presel' ).Fill( goodJetsNoLep[0].btagDeepB )
            getattr( self, 'jet0_bDeepFlav_presel' ).Fill( goodJetsNoLep[0].btagDeepFlavB )


        getattr( self, 'nPVs_preselWeighted' ).Fill( PV.npvsGood, weight )
        getattr( self, 'njets_preselWeighted' ).Fill( len(goodJetsNoLep), weight )
        getattr( self, 'nbjetsCSV_presel' ).Fill( len(goodBjetsDeepCSV), weight )
        getattr( self, 'nbjetsFlav_presel' ).Fill( len(goodBjetsDeepFlav), weight )
        getattr( self, 'nleps_preselWeighted' ).Fill( len(goodLeptons), weight )
        getattr( self, 'met_pt_preselWeighted' ).Fill( MET.pt, weight )
        if len(goodJetsNoLep)>0:
            getattr( self, 'jet0_pt_preselWeighted' ).Fill( goodJetsNoLep[0].pt, weight )
            getattr( self, 'jet0_eta_preselWeighted' ).Fill( goodJetsNoLep[0].eta, weight )
            getattr( self, 'jet0_phi_preselWeighted' ).Fill( goodJetsNoLep[0].phi, weight )
            getattr( self, 'jet0_mass_preselWeighted' ).Fill( goodJetsNoLep[0].mass, weight )
            getattr( self, 'jet0_bDeepCSV_preselWeighted' ).Fill( goodJetsNoLep[0].btagDeepB, weight )
            getattr( self, 'jet0_bDeepFlav_preselWeighted' ).Fill( goodJetsNoLep[0].btagDeepFlavB, weight )

        if nlepcut:
            getattr( self, 'nPVs_lep' ).Fill( PV.npvsGood )
            getattr( self, 'njets_lep' ).Fill( len(goodJetsNoLep) )
            getattr( self, 'nbjetsCSV_lep' ).Fill( len(goodBjetsDeepCSV) )
            getattr( self, 'nbjetsFlav_lep' ).Fill( len(goodBjetsDeepFlav) )
            getattr( self, 'nleps_lep' ).Fill( len(goodLeptons) )
            getattr( self, 'met_pt_lep' ).Fill( MET.pt )
            getattr( self, 'lep0_pt_lep' ).Fill( goodLeptons[0].pt )
            getattr( self, 'lep0_eta_lep' ).Fill( goodLeptons[0].eta )
            getattr( self, 'lep0_phi_lep' ).Fill( goodLeptons[0].phi )
            getattr( self, 'lep0_mass_lep' ).Fill( goodLeptons[0].mass )
            if len(goodJetsNoLep)>0:
                getattr( self, 'jet0_pt_lep' ).Fill( goodJetsNoLep[0].pt )
                getattr( self, 'jet0_eta_lep' ).Fill( goodJetsNoLep[0].eta )
                getattr( self, 'jet0_phi_lep' ).Fill( goodJetsNoLep[0].phi )
                getattr( self, 'jet0_mass_lep' ).Fill( goodJetsNoLep[0].mass )
                getattr( self, 'jet0_bDeepCSV_lep' ).Fill( goodJetsNoLep[0].btagDeepB )
                getattr( self, 'jet0_bDeepFlav_lep' ).Fill( goodJetsNoLep[0].btagDeepFlavB )


            getattr( self, 'nPVs_lepWeighted' ).Fill( PV.npvsGood, weight )
            getattr( self, 'njets_lepWeighted' ).Fill( len(goodJetsNoLep), weight )
            getattr( self, 'nbjetsCSV_lep' ).Fill( len(goodBjetsDeepCSV), weight )
            getattr( self, 'nbjetsFlav_lep' ).Fill( len(goodBjetsDeepFlav), weight )
            getattr( self, 'nleps_lepWeighted' ).Fill( len(goodLeptons), weight )
            getattr( self, 'met_pt_lepWeighted' ).Fill( MET.pt, weight )
            getattr( self, 'lep0_pt_lepWeighted' ).Fill( goodLeptons[0].pt )
            getattr( self, 'lep0_eta_lepWeighted' ).Fill( goodLeptons[0].eta )
            getattr( self, 'lep0_phi_lepWeighted' ).Fill( goodLeptons[0].phi )
            getattr( self, 'lep0_mass_lepWeighted' ).Fill( goodLeptons[0].mass )
            if len(goodJetsNoLep)>0:
                getattr( self, 'jet0_pt_lepWeighted' ).Fill( goodJetsNoLep[0].pt, weight )
                getattr( self, 'jet0_eta_lepWeighted' ).Fill( goodJetsNoLep[0].eta, weight )
                getattr( self, 'jet0_phi_lepWeighted' ).Fill( goodJetsNoLep[0].phi, weight )
                getattr( self, 'jet0_mass_lepWeighted' ).Fill( goodJetsNoLep[0].mass, weight )
                getattr( self, 'jet0_bDeepCSV_lepWeighted' ).Fill( goodJetsNoLep[0].btagDeepB, weight )
                getattr( self, 'jet0_bDeepFlav_lepWeighted' ).Fill( goodJetsNoLep[0].btagDeepFlavB, weight )

            if metcut:
                getattr( self, 'nPVs_met' ).Fill( PV.npvsGood )
                getattr( self, 'njets_met' ).Fill( len(goodJetsNoLep) )
                getattr( self, 'nbjetsCSV_met' ).Fill( len(goodBjetsDeepCSV) )
                getattr( self, 'nbjetsFlav_met' ).Fill( len(goodBjetsDeepFlav) )
                getattr( self, 'nleps_met' ).Fill( len(goodLeptons) )
                getattr( self, 'met_pt_met' ).Fill( MET.pt )
                getattr( self, 'lep0_pt_met' ).Fill( goodLeptons[0].pt )
                getattr( self, 'lep0_eta_met' ).Fill( goodLeptons[0].eta )
                getattr( self, 'lep0_phi_met' ).Fill( goodLeptons[0].phi )
                getattr( self, 'lep0_mass_met' ).Fill( goodLeptons[0].mass )
                if len(goodJetsNoLep)>0:
                    getattr( self, 'jet0_pt_met' ).Fill( goodJetsNoLep[0].pt )
                    getattr( self, 'jet0_eta_met' ).Fill( goodJetsNoLep[0].eta )
                    getattr( self, 'jet0_phi_met' ).Fill( goodJetsNoLep[0].phi )
                    getattr( self, 'jet0_mass_met' ).Fill( goodJetsNoLep[0].mass )
                    getattr( self, 'jet0_bDeepCSV_met' ).Fill( goodJetsNoLep[0].btagDeepB )
                    getattr( self, 'jet0_bDeepFlav_met' ).Fill( goodJetsNoLep[0].btagDeepFlavB )

                getattr( self, 'nPVs_metWeighted' ).Fill( PV.npvsGood, weight )
                getattr( self, 'njets_metWeighted' ).Fill( len(goodJetsNoLep), weight )
                getattr( self, 'nbjetsCSV_met' ).Fill( len(goodBjetsDeepCSV), weight )
                getattr( self, 'nbjetsFlav_met' ).Fill( len(goodBjetsDeepFlav), weight )
                getattr( self, 'nleps_metWeighted' ).Fill( len(goodLeptons), weight )
                getattr( self, 'met_pt_metWeighted' ).Fill( MET.pt, weight )
                getattr( self, 'lep0_pt_metWeighted' ).Fill( goodLeptons[0].pt )
                getattr( self, 'lep0_eta_metWeighted' ).Fill( goodLeptons[0].eta )
                getattr( self, 'lep0_phi_metWeighted' ).Fill( goodLeptons[0].phi )
                getattr( self, 'lep0_mass_metWeighted' ).Fill( goodLeptons[0].mass )
                if len(goodJetsNoLep)>0:
                    getattr( self, 'jet0_pt_metWeighted' ).Fill( goodJetsNoLep[0].pt, weight )
                    getattr( self, 'jet0_eta_metWeighted' ).Fill( goodJetsNoLep[0].eta, weight )
                    getattr( self, 'jet0_phi_metWeighted' ).Fill( goodJetsNoLep[0].phi, weight )
                    getattr( self, 'jet0_mass_metWeighted' ).Fill( goodJetsNoLep[0].mass, weight )
                    getattr( self, 'jet0_bDeepCSV_metWeighted' ).Fill( goodJetsNoLep[0].btagDeepB, weight )
                    getattr( self, 'jet0_bDeepFlav_metWeighted' ).Fill( goodJetsNoLep[0].btagDeepFlavB, weight )


                if njetscut:
                    getattr( self, 'nPVs_jet' ).Fill( PV.npvsGood )
                    getattr( self, 'njets_jet' ).Fill( len(goodJetsNoLep) )
                    getattr( self, 'nbjetsCSV_jet' ).Fill( len(goodBjetsDeepCSV) )
                    getattr( self, 'nbjetsFlav_jet' ).Fill( len(goodBjetsDeepFlav) )
                    getattr( self, 'nleps_jet' ).Fill( len(goodLeptons) )
                    getattr( self, 'met_pt_jet' ).Fill( MET.pt )
                    getattr( self, 'lep0_pt_jet' ).Fill( goodLeptons[0].pt )
                    getattr( self, 'lep0_eta_jet' ).Fill( goodLeptons[0].eta )
                    getattr( self, 'lep0_phi_jet' ).Fill( goodLeptons[0].phi )
                    getattr( self, 'lep0_mass_jet' ).Fill( goodLeptons[0].mass )
                    getattr( self, 'jet0_pt_jet' ).Fill( goodJetsNoLep[0].pt )
                    getattr( self, 'jet0_eta_jet' ).Fill( goodJetsNoLep[0].eta )
                    getattr( self, 'jet0_phi_jet' ).Fill( goodJetsNoLep[0].phi )
                    getattr( self, 'jet0_mass_jet' ).Fill( goodJetsNoLep[0].mass )
                    getattr( self, 'jet0_bDeepCSV_jet' ).Fill( goodJetsNoLep[0].btagDeepB )
                    getattr( self, 'jet0_bDeepFlav_jet' ).Fill( goodJetsNoLep[0].btagDeepFlavB )
                    getattr( self, 'jet3_pt_jet' ).Fill( goodJetsNoLep[3].pt )
                    getattr( self, 'jet3_eta_jet' ).Fill( goodJetsNoLep[3].eta )
                    getattr( self, 'jet3_phi_jet' ).Fill( goodJetsNoLep[3].phi )
                    getattr( self, 'jet3_mass_jet' ).Fill( goodJetsNoLep[3].mass )
                    getattr( self, 'jet3_bDeepCSV_jet' ).Fill( goodJetsNoLep[3].btagDeepB )
                    getattr( self, 'jet3_bDeepFlav_jet' ).Fill( goodJetsNoLep[3].btagDeepFlavB )

                    getattr( self, 'nPVs_jetWeighted' ).Fill( PV.npvsGood, weight )
                    getattr( self, 'njets_jetWeighted' ).Fill( len(goodJetsNoLep), weight )
                    getattr( self, 'nbjetsCSV_jetWeighted' ).Fill( len(goodBjetsDeepCSV), weight )
                    getattr( self, 'nbjetsFlav_jetWeighted' ).Fill( len(goodBjetsDeepFlav), weight )
                    getattr( self, 'nleps_jetWeighted' ).Fill( len(goodLeptons), weight )
                    getattr( self, 'met_pt_jetWeighted' ).Fill( MET.pt, weight )
                    getattr( self, 'jet3_pt_jetWeighted' ).Fill( goodJetsNoLep[3].pt, weight )
                    getattr( self, 'jet3_eta_jetWeighted' ).Fill( goodJetsNoLep[3].eta, weight )
                    getattr( self, 'jet3_phi_jetWeighted' ).Fill( goodJetsNoLep[3].phi, weight )
                    getattr( self, 'jet3_mass_jetWeighted' ).Fill( goodJetsNoLep[3].mass, weight )
                    getattr( self, 'jet3_bDeepCSV_jetWeighted' ).Fill( goodJetsNoLep[3].btagDeepB, weight )
                    getattr( self, 'jet3_bDeepFlav_jetWeighted' ).Fill( goodJetsNoLep[3].btagDeepFlavB, weight )

                    if len(goodBjetsDeepCSV)>2:
                        getattr( self, 'nPVs_bDeepCSV' ).Fill( PV.npvsGood )
                        getattr( self, 'njets_bDeepCSV' ).Fill( len(goodJetsNoLep) )
                        getattr( self, 'nbjetsCSV_bDeepCSV' ).Fill( len(goodBjetsDeepCSV) )
                        getattr( self, 'nbjetsFlav_bDeepCSV' ).Fill( len(goodBjetsDeepFlav) )
                        getattr( self, 'nleps_bDeepCSV' ).Fill( len(goodLeptons) )
                        getattr( self, 'met_pt_bDeepCSV' ).Fill( MET.pt )
                        getattr( self, 'lep0_pt_bDeepCSV' ).Fill( goodLeptons[0].pt )
                        getattr( self, 'lep0_eta_bDeepCSV' ).Fill( goodLeptons[0].eta )
                        getattr( self, 'lep0_phi_bDeepCSV' ).Fill( goodLeptons[0].phi )
                        getattr( self, 'lep0_mass_bDeepCSV' ).Fill( goodLeptons[0].mass )
                        getattr( self, 'jet0_pt_bDeepCSV' ).Fill( goodJetsNoLep[0].pt )
                        getattr( self, 'jet0_eta_bDeepCSV' ).Fill( goodJetsNoLep[0].eta )
                        getattr( self, 'jet0_phi_bDeepCSV' ).Fill( goodJetsNoLep[0].phi )
                        getattr( self, 'jet0_mass_bDeepCSV' ).Fill( goodJetsNoLep[0].mass )
                        getattr( self, 'jet0_bDeepCSV_bDeepCSV' ).Fill( goodJetsNoLep[0].btagDeepB )
                        getattr( self, 'jet0_bDeepFlav_bDeepCSV' ).Fill( goodJetsNoLep[0].btagDeepFlavB )
                        getattr( self, 'jet3_pt_bDeepCSV' ).Fill( goodJetsNoLep[3].pt )
                        getattr( self, 'jet3_eta_bDeepCSV' ).Fill( goodJetsNoLep[3].eta )
                        getattr( self, 'jet3_phi_bDeepCSV' ).Fill( goodJetsNoLep[3].phi )
                        getattr( self, 'jet3_mass_bDeepCSV' ).Fill( goodJetsNoLep[3].mass )
                        getattr( self, 'jet3_bDeepCSV_bDeepCSV' ).Fill( goodJetsNoLep[3].btagDeepB )
                        getattr( self, 'jet3_bDeepFlav_bDeepCSV' ).Fill( goodJetsNoLep[3].btagDeepFlavB )

                        getattr( self, 'nPVs_bDeepCSVWeighted' ).Fill( PV.npvsGood, weight )
                        getattr( self, 'njets_bDeepCSVWeighted' ).Fill( len(goodJetsNoLep), weight )
                        getattr( self, 'nbjetsCSV_bDeepCSVWeighted' ).Fill( len(goodBjetsDeepCSV), weight )
                        getattr( self, 'nbjetsFlav_bDeepCSVWeighted' ).Fill( len(goodBjetsDeepFlav), weight )
                        getattr( self, 'nleps_bDeepCSVWeighted' ).Fill( len(goodLeptons), weight )
                        getattr( self, 'met_pt_bDeepCSVWeighted' ).Fill( MET.pt, weight )
                        getattr( self, 'jet3_pt_bDeepCSVWeighted' ).Fill( goodJetsNoLep[3].pt, weight )
                        getattr( self, 'jet3_eta_bDeepCSVWeighted' ).Fill( goodJetsNoLep[3].eta, weight )
                        getattr( self, 'jet3_phi_bDeepCSVWeighted' ).Fill( goodJetsNoLep[3].phi, weight )
                        getattr( self, 'jet3_mass_bDeepCSVWeighted' ).Fill( goodJetsNoLep[3].mass, weight )
                        getattr( self, 'jet3_bDeepCSV_bDeepCSVWeighted' ).Fill( goodJetsNoLep[3].btagDeepB, weight )
                        getattr( self, 'jet3_bDeepFlav_bDeepCSVWeighted' ).Fill( goodJetsNoLep[3].btagDeepFlavB, weight )

                    if len(goodBjetsDeepFlav)>2:
                        getattr( self, 'nPVs_bDeepFlav' ).Fill( PV.npvsGood )
                        getattr( self, 'njets_bDeepFlav' ).Fill( len(goodJetsNoLep) )
                        getattr( self, 'nbjetsCSV_bDeepFlav' ).Fill( len(goodBjetsDeepCSV) )
                        getattr( self, 'nbjetsFlav_bDeepFlav' ).Fill( len(goodBjetsDeepFlav) )
                        getattr( self, 'nleps_bDeepFlav' ).Fill( len(goodLeptons) )
                        getattr( self, 'met_pt_bDeepFlav' ).Fill( MET.pt )
                        getattr( self, 'lep0_pt_bDeepFlav' ).Fill( goodLeptons[0].pt )
                        getattr( self, 'lep0_eta_bDeepFlav' ).Fill( goodLeptons[0].eta )
                        getattr( self, 'lep0_phi_bDeepFlav' ).Fill( goodLeptons[0].phi )
                        getattr( self, 'lep0_mass_bDeepFlav' ).Fill( goodLeptons[0].mass )
                        getattr( self, 'jet0_pt_bDeepFlav' ).Fill( goodJetsNoLep[0].pt )
                        getattr( self, 'jet0_eta_bDeepFlav' ).Fill( goodJetsNoLep[0].eta )
                        getattr( self, 'jet0_phi_bDeepFlav' ).Fill( goodJetsNoLep[0].phi )
                        getattr( self, 'jet0_mass_bDeepFlav' ).Fill( goodJetsNoLep[0].mass )
                        getattr( self, 'jet0_bDeepCSV_bDeepFlav' ).Fill( goodJetsNoLep[0].btagDeepB )
                        getattr( self, 'jet0_bDeepFlav_bDeepFlav' ).Fill( goodJetsNoLep[0].btagDeepFlavB )
                        getattr( self, 'jet3_pt_bDeepFlav' ).Fill( goodJetsNoLep[3].pt )
                        getattr( self, 'jet3_eta_bDeepFlav' ).Fill( goodJetsNoLep[3].eta )
                        getattr( self, 'jet3_phi_bDeepFlav' ).Fill( goodJetsNoLep[3].phi )
                        getattr( self, 'jet3_mass_bDeepFlav' ).Fill( goodJetsNoLep[3].mass )
                        getattr( self, 'jet3_bDeepCSV_bDeepFlav' ).Fill( goodJetsNoLep[3].btagDeepB )
                        getattr( self, 'jet3_bDeepFlav_bDeepFlav' ).Fill( goodJetsNoLep[3].btagDeepFlavB )

                        getattr( self, 'nPVs_bDeepFlavWeighted' ).Fill( PV.npvsGood, weight )
                        getattr( self, 'njets_bDeepFlavWeighted' ).Fill( len(goodJetsNoLep), weight )
                        getattr( self, 'nbjetsCSV_bDeepFlavWeighted' ).Fill( len(goodBjetsDeepCSV), weight )
                        getattr( self, 'nbjetsFlav_bDeepFlavWeighted' ).Fill( len(goodBjetsDeepFlav), weight )
                        getattr( self, 'nleps_bDeepFlavWeighted' ).Fill( len(goodLeptons), weight )
                        getattr( self, 'met_pt_bDeepFlavWeighted' ).Fill( MET.pt, weight )
                        getattr( self, 'jet3_pt_bDeepFlavWeighted' ).Fill( goodJetsNoLep[3].pt, weight )
                        getattr( self, 'jet3_eta_bDeepFlavWeighted' ).Fill( goodJetsNoLep[3].eta, weight )
                        getattr( self, 'jet3_phi_bDeepFlavWeighted' ).Fill( goodJetsNoLep[3].phi, weight )
                        getattr( self, 'jet3_mass_bDeepFlavWeighted' ).Fill( goodJetsNoLep[3].mass, weight )
                        getattr( self, 'jet3_bDeepCSV_bDeepFlavWeighted' ).Fill( goodJetsNoLep[3].btagDeepB, weight )
                        getattr( self, 'jet3_bDeepFlav_bDeepFlavWeighted' ).Fill( goodJetsNoLep[3].btagDeepFlavB, weight )
        '''


        return True


#myquickAnalyzer = lambda : quickAnalyzer()
