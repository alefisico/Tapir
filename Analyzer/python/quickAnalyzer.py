#!/usr/bin/env python
import os, sys
from collections import OrderedDict
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

        for icut in ['presel', 'preselPU', 'preselGen', 'preselTotal',  'lep', 'lepPU', 'lepGen', 'lepTrig', 'lepID', 'lepISO', 'lepSF', 'lepTotal', 'jet', 'jetPU', 'jetGen', 'jetSF', 'jetTotal', 'bjet']:
            #if self.sample.startswith('TTTo'):
            #    for ttXX, ttXXcond in ttCls.items():
            #        self.listOfHistos( '_'+ttXX+'_'+icut )
            #else:
                self.listOfHistos( '_'+icut )

    def listOfHistos(self, t ):
        self.addObject( ROOT.TH1F('nPVs'+t,   ';number of PVs',   100, 0, 100) )
        self.addObject( ROOT.TH1F('njets'+t,   ';number of jets',   20, 0, 20) )
        self.addObject( ROOT.TH1F('nleps'+t,   ';number of leptons',   20, 0, 20) )
        self.histnames = ['jet0', 'jet1', 'jet2', 'jet3', 'lep0', 'lep1', 'met']
        for val in self.histnames: self.addP4Hists( val, t )

    def addP4Hists(self, s, t ):
        self.addObject( ROOT.TH1F(s+'_pt'+t,  s+';p_{T} (GeV)',   100, 0, 5000) )
        self.addObject( ROOT.TH1F(s+'_eta'+t, s+';#eta', 100, -4.0, 4.0 ) )
        self.addObject( ROOT.TH1F(s+'_phi'+t, s+';#phi', 100, -3.14259, 3.14159) )
        self.addObject( ROOT.TH1F(s+'_mass'+t,s+';mass (GeV)', 100, 0, 1000) )

    def leptonSF(self, lepton, leptonP4 ):

        if lepton.startswith("muon"):
            SFFileTrigger = ROOT.TFile( ("" if os.path.isfile('EfficienciesAndSF_2018Data_AfterMuonHLTUpdate.root') else "../data/")+"EfficienciesAndSF_2018Data_AfterMuonHLTUpdate.root" )
            histoSFTrigger = SFFileTrigger.Get("IsoMu24_PtEtaBins/pt_abseta_ratio")
            SFTrigger = histoSFTrigger.GetBinContent( histoSFTrigger.GetXaxis().FindBin( leptonP4.pt ), histoSFTrigger.GetYaxis().FindBin( abs(leptonP4.eta ) ) )

            SFFileID = ROOT.TFile( ("" if os.path.isfile('RunABCD_SF_ID.root') else "../data/")+"RunABCD_SF_ID.root" )
            histoSFID = SFFileID.Get("NUM_TightID_DEN_TrackerMuons_pt_abseta")
            SFID = histoSFID.GetBinContent( histoSFID.GetXaxis().FindBin( leptonP4.pt ), histoSFID.GetYaxis().FindBin( abs(leptonP4.eta ) ) ) if (leptonP4.pt < 120) else 1

            SFFileISO = ROOT.TFile( ("" if os.path.isfile('RunABCD_SF_ISO.root') else "../data/")+"RunABCD_SF_ISO.root")
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


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("LeptonSFTrigger",  "F");
        self.out.branch("LeptonSFISO",  "F");
        self.out.branch("LeptonSFID",  "F");
        self.out.branch("nGoodLep",  "I");
        self.out.branch("GoodLep_pt",  "F", lenVar="nGoodLep");
        self.out.branch("GoodLep_eta",  "F", lenVar="nGoodLep");
        self.out.branch("GoodLep_phi",  "F", lenVar="nGoodLep");
        self.out.branch("GoodLep_mass",  "F", lenVar="nGoodLep");
        self.out.branch("nGoodJet",  "I");
        self.out.branch("GoodJet_pt",  "F", lenVar="nGoodJet");
        self.out.branch("GoodJet_eta",  "F", lenVar="nGoodJet");
        self.out.branch("GoodJet_phi",  "F", lenVar="nGoodJet");
        self.out.branch("GoodJet_mass",  "F", lenVar="nGoodJet");

    def analyze(self, event):

        isMC = event.run == 1

        if isMC: weight = event.puWeight #* ( event.genWeight/event.genWeight )
        else: weight = 1

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        PV = Object(event, 'PV')
        MET = Object(event, 'MET')

        ### Leptons
        vetoMuons = [ m for m in muons if (abs(m.eta)<2.4) and (m.pt>15) and (m.pfRelIso04_all<0.25) and (m.tightId==1) ]
        goodMuons = [ m for m in vetoMuons if (m.pt>29) and (m.pfRelIso04_all<0.15) ]

        ### Electrons, not completed
        vetoElectrons = [ e for e in electrons if (abs(e.eta)<2.4) and (e.pt>15) and not ( abs(e.deltaEtaSC+e.eta)>=1.4442 and abs(e.deltaEtaSC+e.eta)<=1.5660) and (e.cutBased>=4) ]
        goodElectrons = [ e for e in vetoElectrons if e.pt>30 ]

        goodLeptons = goodMuons #+ goodElectrons
        goodLeptons.sort(key=lambda x:x.pt, reverse=True)

        if isMC:
            if len(goodMuons)>0 and len(goodElectrons)==0: leptonWeights= self.leptonSF( "muon", goodMuons[0] )
            elif len(goodMuons)==0 and len(goodElectrons)>0: leptonWeights = self.leptonSF( "electron", goodElectrons[0] )
            else: leptonWeights = [0, 0, 0]
        else: leptonWeights = [1, 1, 1]

        ### Jets
        looseJets = [ j for j in jets if (abs(j.eta<2.4)) and (j.pt>20) and (j.jetId>=2) and (j.puId>=4) ]
        goodJets = looseJets if (len(looseJets)>0) and (looseJets[0].pt>30) else []
        goodJetsNoLep = [ j for j in jets for l in goodLeptons if j.p4().DeltaR(l.p4())>=0.4  ]

        #### FIlling trees
        self.out.fillBranch('LeptonSFTrigger', leptonWeights[0])
        self.out.fillBranch('LeptonSFID', leptonWeights[1])
        self.out.fillBranch('LeptonSFISO', leptonWeights[2])
        self.out.fillBranch('nGoodLep', len(goodLeptons))
        self.out.fillBranch('GoodLep_pt', [l.pt for l in goodLeptons] )
        self.out.fillBranch('GoodLep_eta', [l.eta for l in goodLeptons] )
        self.out.fillBranch('GoodLep_phi', [l.phi for l in goodLeptons] )
        self.out.fillBranch('GoodLep_mass', [l.mass for l in goodLeptons] )
        self.out.fillBranch('nGoodLep', len(goodLeptons))
        self.out.fillBranch('GoodJet_pt', [j.pt for j in goodJetsNoLep] )
        self.out.fillBranch('GoodJet_eta', [j.eta for j in goodJetsNoLep] )
        self.out.fillBranch('GoodJet_phi', [j.phi for j in goodJetsNoLep] )
        self.out.fillBranch('GoodJet_mass', [j.mass for j in goodJetsNoLep] )

        #### Filling histograms
        getattr( self, 'nPVs_presel' ).Fill( PV.npvsGood )
        getattr( self, 'njets_presel' ).Fill( len(jets) )
        getattr( self, 'nleps_presel' ).Fill( len(muons)+len(electrons) )
        getattr( self, 'met_pt_presel' ).Fill( MET.pt )
        if len(jets)>0:
            getattr( self, 'jet0_pt_presel' ).Fill( jets[0].pt )
            getattr( self, 'jet0_eta_presel' ).Fill( jets[0].eta )
            getattr( self, 'jet0_phi_presel' ).Fill( jets[0].phi )
            getattr( self, 'jet0_mass_presel' ).Fill( jets[0].mass )

        getattr( self, 'nPVs_preselPU' ).Fill( PV.npvsGood, event.puWeight )
        getattr( self, 'njets_preselPU' ).Fill( len(jets), event.puWeight )
        getattr( self, 'nleps_preselPU' ).Fill( len(muons)+len(electrons), event.puWeight )
        getattr( self, 'met_pt_preselPU' ).Fill( MET.pt, event.puWeight )
        if len(jets)>0:
            getattr( self, 'jet0_pt_preselPU' ).Fill( jets[0].pt, event.puWeight )
            getattr( self, 'jet0_eta_preselPU' ).Fill( jets[0].eta, event.puWeight )
            getattr( self, 'jet0_phi_preselPU' ).Fill( jets[0].phi, event.puWeight )
            getattr( self, 'jet0_mass_preselPU' ).Fill( jets[0].mass, event.puWeight )

        getattr( self, 'nPVs_preselGen' ).Fill( PV.npvsGood, np.sign(event.genWeight ) )
        getattr( self, 'njets_preselGen' ).Fill( len(jets), np.sign(event.genWeight ) )
        getattr( self, 'nleps_preselGen' ).Fill( len(muons)+len(electrons), np.sign(event.genWeight ) )
        getattr( self, 'met_pt_preselGen' ).Fill( MET.pt, np.sign(event.genWeight ) )
        if len(jets)>0:
            getattr( self, 'jet0_pt_preselGen' ).Fill( jets[0].pt, np.sign(event.genWeight ) )
            getattr( self, 'jet0_eta_preselGen' ).Fill( jets[0].eta, np.sign(event.genWeight ) )
            getattr( self, 'jet0_phi_preselGen' ).Fill( jets[0].phi, np.sign(event.genWeight ) )
            getattr( self, 'jet0_mass_preselGen' ).Fill( jets[0].mass, np.sign(event.genWeight ) )

        getattr( self, 'nPVs_preselTotal' ).Fill( PV.npvsGood, event.puWeight * np.sign(event.genWeight ) )
        getattr( self, 'njets_preselTotal' ).Fill( len(jets), event.puWeight * np.sign(event.genWeight ) )
        getattr( self, 'nleps_preselTotal' ).Fill( len(muons)+len(electrons), event.puWeight * np.sign(event.genWeight ) )
        getattr( self, 'met_pt_preselTotal' ).Fill( MET.pt, event.puWeight * np.sign(event.genWeight ) )
        if len(jets)>0:
            getattr( self, 'jet0_pt_preselTotal' ).Fill( jets[0].pt, event.puWeight * np.sign(event.genWeight ) )
            getattr( self, 'jet0_eta_preselTotal' ).Fill( jets[0].eta, event.puWeight * np.sign(event.genWeight ) )
            getattr( self, 'jet0_phi_preselTotal' ).Fill( jets[0].phi, event.puWeight * np.sign(event.genWeight ) )
            getattr( self, 'jet0_mass_preselTotal' ).Fill( jets[0].mass, event.puWeight * np.sign(event.genWeight ) )

        if len(goodLeptons)>0:
            getattr( self, 'nPVs_lep' ).Fill( PV.npvsGood )
            getattr( self, 'njets_lep' ).Fill( len(jets) )
            getattr( self, 'nleps_lep' ).Fill( len(goodLeptons) )
            getattr( self, 'met_pt_lep' ).Fill( MET.pt )
            getattr( self, 'lep0_pt_lep' ).Fill( goodLeptons[0].pt )
            getattr( self, 'lep0_eta_lep' ).Fill( goodLeptons[0].eta )
            getattr( self, 'lep0_phi_lep' ).Fill( goodLeptons[0].phi )
            getattr( self, 'lep0_mass_lep' ).Fill( goodLeptons[0].mass )
            if len(jets)>0:
                getattr( self, 'jet0_pt_lep' ).Fill( jets[0].pt )
                getattr( self, 'jet0_eta_lep' ).Fill( jets[0].eta )
                getattr( self, 'jet0_phi_lep' ).Fill( jets[0].phi )
                getattr( self, 'jet0_mass_lep' ).Fill( jets[0].mass )

            getattr( self, 'nPVs_lepPU' ).Fill( PV.npvsGood, event.puWeight )
            getattr( self, 'njets_lepPU' ).Fill( len(jets), event.puWeight )
            getattr( self, 'nleps_lepPU' ).Fill( len(muons)+len(electrons), event.puWeight )
            getattr( self, 'met_pt_lepPU' ).Fill( MET.pt, event.puWeight )
            if len(jets)>0:
                getattr( self, 'jet0_pt_lepPU' ).Fill( jets[0].pt, event.puWeight )
                getattr( self, 'jet0_eta_lepPU' ).Fill( jets[0].eta, event.puWeight )
                getattr( self, 'jet0_phi_lepPU' ).Fill( jets[0].phi, event.puWeight )
                getattr( self, 'jet0_mass_lepPU' ).Fill( jets[0].mass, event.puWeight )

            getattr( self, 'nPVs_lepGen' ).Fill( PV.npvsGood, np.sign(event.genWeight ) )
            getattr( self, 'njets_lepGen' ).Fill( len(jets), np.sign(event.genWeight ) )
            getattr( self, 'nleps_lepGen' ).Fill( len(muons)+len(electrons), np.sign(event.genWeight ) )
            getattr( self, 'met_pt_lepGen' ).Fill( MET.pt, np.sign(event.genWeight ) )
            if len(jets)>0:
                getattr( self, 'jet0_pt_lepGen' ).Fill( jets[0].pt, np.sign(event.genWeight ) )
                getattr( self, 'jet0_eta_lepGen' ).Fill( jets[0].eta, np.sign(event.genWeight ) )
                getattr( self, 'jet0_phi_lepGen' ).Fill( jets[0].phi, np.sign(event.genWeight ) )
                getattr( self, 'jet0_mass_lepGen' ).Fill( jets[0].mass, np.sign(event.genWeight ) )

            getattr( self, 'nPVs_lepTrig' ).Fill( PV.npvsGood, leptonWeights[0] )
            getattr( self, 'njets_lepTrig' ).Fill( len(jets), leptonWeights[0] )
            getattr( self, 'nleps_lepTrig' ).Fill( len(muons)+len(electrons), leptonWeights[0] )
            getattr( self, 'met_pt_lepTrig' ).Fill( MET.pt, leptonWeights[0] )
            if len(jets)>0:
                getattr( self, 'jet0_pt_lepTrig' ).Fill( jets[0].pt, leptonWeights[0] )
                getattr( self, 'jet0_eta_lepTrig' ).Fill( jets[0].eta, leptonWeights[0] )
                getattr( self, 'jet0_phi_lepTrig' ).Fill( jets[0].phi, leptonWeights[0] )
                getattr( self, 'jet0_mass_lepTrig' ).Fill( jets[0].mass, leptonWeights[0] )

            getattr( self, 'nPVs_lepID' ).Fill( PV.npvsGood, leptonWeights[1] )
            getattr( self, 'njets_lepID' ).Fill( len(jets), leptonWeights[1] )
            getattr( self, 'nleps_lepID' ).Fill( len(muons)+len(electrons), leptonWeights[1] )
            getattr( self, 'met_pt_lepID' ).Fill( MET.pt, leptonWeights[1] )
            if len(jets)>0:
                getattr( self, 'jet0_pt_lepID' ).Fill( jets[0].pt, leptonWeights[1] )
                getattr( self, 'jet0_eta_lepID' ).Fill( jets[0].eta, leptonWeights[1] )
                getattr( self, 'jet0_phi_lepID' ).Fill( jets[0].phi, leptonWeights[1] )
                getattr( self, 'jet0_mass_lepID' ).Fill( jets[0].mass, leptonWeights[1] )

            getattr( self, 'nPVs_lepISO' ).Fill( PV.npvsGood, leptonWeights[2] )
            getattr( self, 'njets_lepISO' ).Fill( len(jets), leptonWeights[2] )
            getattr( self, 'nleps_lepISO' ).Fill( len(muons)+len(electrons), leptonWeights[2] )
            getattr( self, 'met_pt_lepISO' ).Fill( MET.pt, leptonWeights[2] )
            if len(jets)>0:
                getattr( self, 'jet0_pt_lepISO' ).Fill( jets[0].pt, leptonWeights[2] )
                getattr( self, 'jet0_eta_lepISO' ).Fill( jets[0].eta, leptonWeights[2] )
                getattr( self, 'jet0_phi_lepISO' ).Fill( jets[0].phi, leptonWeights[2] )
                getattr( self, 'jet0_mass_lepISO' ).Fill( jets[0].mass, leptonWeights[2] )

            getattr( self, 'nPVs_lepSF' ).Fill( PV.npvsGood, np.prod(leptonWeights) )
            getattr( self, 'njets_lepSF' ).Fill( len(jets), np.prod(leptonWeights) )
            getattr( self, 'nleps_lepSF' ).Fill( len(muons)+len(electrons), np.prod(leptonWeights) )
            getattr( self, 'met_pt_lepSF' ).Fill( MET.pt, np.prod(leptonWeights) )
            if len(jets)>0:
                getattr( self, 'jet0_pt_lepSF' ).Fill( jets[0].pt, np.prod(leptonWeights) )
                getattr( self, 'jet0_eta_lepSF' ).Fill( jets[0].eta, np.prod(leptonWeights) )
                getattr( self, 'jet0_phi_lepSF' ).Fill( jets[0].phi, np.prod(leptonWeights) )
                getattr( self, 'jet0_mass_lepSF' ).Fill( jets[0].mass, np.prod(leptonWeights) )

            getattr( self, 'nPVs_lepTotal' ).Fill( PV.npvsGood, event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
            getattr( self, 'njets_lepTotal' ).Fill( len(jets), event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
            getattr( self, 'nleps_lepTotal' ).Fill( len(muons)+len(electrons), event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
            getattr( self, 'met_pt_lepTotal' ).Fill( MET.pt, event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
            if len(jets)>0:
                getattr( self, 'jet0_pt_lepTotal' ).Fill( jets[0].pt, event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
                getattr( self, 'jet0_eta_lepTotal' ).Fill( jets[0].eta, event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
                getattr( self, 'jet0_phi_lepTotal' ).Fill( jets[0].phi, event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
                getattr( self, 'jet0_mass_lepTotal' ).Fill( jets[0].mass, event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )

            if MET.pt>20:
                if len(goodJetsNoLep)>2:
                    getattr( self, 'nPVs_jet' ).Fill( PV.npvsGood )
                    getattr( self, 'njets_jet' ).Fill( len(jets) )
                    getattr( self, 'nleps_jet' ).Fill( len(goodLeptons) )
                    getattr( self, 'met_pt_jet' ).Fill( MET.pt )
                    getattr( self, 'lep0_pt_jet' ).Fill( goodLeptons[0].pt )
                    getattr( self, 'lep0_eta_jet' ).Fill( goodLeptons[0].eta )
                    getattr( self, 'lep0_phi_jet' ).Fill( goodLeptons[0].phi )
                    getattr( self, 'lep0_mass_jet' ).Fill( goodLeptons[0].mass )
                    if len(jets)>0:
                        getattr( self, 'jet0_pt_jet' ).Fill( jets[0].pt )
                        getattr( self, 'jet0_eta_jet' ).Fill( jets[0].eta )
                        getattr( self, 'jet0_phi_jet' ).Fill( jets[0].phi )
                        getattr( self, 'jet0_mass_jet' ).Fill( jets[0].mass )

                    getattr( self, 'nPVs_jetPU' ).Fill( PV.npvsGood, event.puWeight )
                    getattr( self, 'njets_jetPU' ).Fill( len(jets), event.puWeight )
                    getattr( self, 'nleps_jetPU' ).Fill( len(muons)+len(electrons), event.puWeight )
                    getattr( self, 'met_pt_jetPU' ).Fill( MET.pt, event.puWeight )
                    if len(jets)>0:
                        getattr( self, 'jet0_pt_jetPU' ).Fill( jets[0].pt, event.puWeight )
                        getattr( self, 'jet0_eta_jetPU' ).Fill( jets[0].eta, event.puWeight )
                        getattr( self, 'jet0_phi_jetPU' ).Fill( jets[0].phi, event.puWeight )
                        getattr( self, 'jet0_mass_jetPU' ).Fill( jets[0].mass, event.puWeight )

                    getattr( self, 'nPVs_jetGen' ).Fill( PV.npvsGood, np.sign(event.genWeight ) )
                    getattr( self, 'njets_jetGen' ).Fill( len(jets), np.sign(event.genWeight ) )
                    getattr( self, 'nleps_jetGen' ).Fill( len(muons)+len(electrons), np.sign(event.genWeight ) )
                    getattr( self, 'met_pt_jetGen' ).Fill( MET.pt, np.sign(event.genWeight ) )
                    if len(jets)>0:
                        getattr( self, 'jet0_pt_jetGen' ).Fill( jets[0].pt, np.sign(event.genWeight ) )
                        getattr( self, 'jet0_eta_jetGen' ).Fill( jets[0].eta, np.sign(event.genWeight ) )
                        getattr( self, 'jet0_phi_jetGen' ).Fill( jets[0].phi, np.sign(event.genWeight ) )
                        getattr( self, 'jet0_mass_jetGen' ).Fill( jets[0].mass, np.sign(event.genWeight ) )

                    getattr( self, 'nPVs_jetSF' ).Fill( PV.npvsGood, np.prod(leptonWeights) )
                    getattr( self, 'njets_jetSF' ).Fill( len(jets), np.prod(leptonWeights) )
                    getattr( self, 'nleps_jetSF' ).Fill( len(muons)+len(electrons), np.prod(leptonWeights) )
                    getattr( self, 'met_pt_jetSF' ).Fill( MET.pt, np.prod(leptonWeights) )
                    if len(jets)>0:
                        getattr( self, 'jet0_pt_jetSF' ).Fill( jets[0].pt, np.prod(leptonWeights) )
                        getattr( self, 'jet0_eta_jetSF' ).Fill( jets[0].eta, np.prod(leptonWeights) )
                        getattr( self, 'jet0_phi_jetSF' ).Fill( jets[0].phi, np.prod(leptonWeights) )
                        getattr( self, 'jet0_mass_jetSF' ).Fill( jets[0].mass, np.prod(leptonWeights) )

                    getattr( self, 'nPVs_jetTotal' ).Fill( PV.npvsGood, event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
                    getattr( self, 'njets_jetTotal' ).Fill( len(jets), event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
                    getattr( self, 'nleps_jetTotal' ).Fill( len(muons)+len(electrons), event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
                    getattr( self, 'met_pt_jetTotal' ).Fill( MET.pt, event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
                    if len(jets)>0:
                        getattr( self, 'jet0_pt_jetTotal' ).Fill( jets[0].pt, event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
                        getattr( self, 'jet0_eta_jetTotal' ).Fill( jets[0].eta, event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
                        getattr( self, 'jet0_phi_jetTotal' ).Fill( jets[0].phi, event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )
                        getattr( self, 'jet0_mass_jetTotal' ).Fill( jets[0].mass, event.puWeight * np.sign(event.genWeight ) * np.prod(leptonWeights) )


        return True


#myquickAnalyzer = lambda : quickAnalyzer()
