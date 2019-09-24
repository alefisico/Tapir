#!/usr/bin/env python
import os, sys
from collections import OrderedDict
from itertools import permutations
import numpy as np
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gSystem.Load("libTTHCommonClassifier")
#ROOT.gSystem.Load("libTTHMEIntegratorStandalone")

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

### Vector definitions for MEM
CvectorvectorLorentz = getattr(ROOT, "std::vector<vector<TLorentzVector>>")
CvectorLorentz = getattr(ROOT, "std::vector<TLorentzVector>")
Cvectordouble = getattr(ROOT, "std::vector<double>")
Cvectorvectordouble = getattr(ROOT, "std::vector<vector<double>>")
Cvectorvectorvectordouble = getattr(ROOT, "std::vector<vector<vector<double>>>")
CvectorJetType = getattr(ROOT, "std::vector<MEMClassifier::JetType>")
CvectorvectorJetType = getattr(ROOT, "std::vector<vector<MEMClassifier::JetType>>")
Cvectorbool = getattr(ROOT, "std::vector<bool>")
CvectorMEMResult = getattr(ROOT, "std::vector<MEMResult>")

##### Vector from list for MEM
def vec_from_list(vec_type, src):
    """
    Creates a std::vector<T> from a python list.
    vec_type (ROOT type): vector datatype, ex: std::vector<double>
    src (iterable): python list
    """
    v = vec_type()
    if vec_type == Cvectorvectordouble:
        for item in src:
            v2 = Cvectordouble()
            for item2 in item:
                v2.push_back(item2)
            v.push_back(v2)
    elif vec_type == Cvectorvectorvectordouble:
        for item in src:
            v2 = Cvectorvectordouble()
            for item2 in item:
                v3 = Cvectordouble()
                for item3 in item2:
                    v3.push_back(item3)
                v2.push_back(v3)
            v.push_back(v2)
    elif vec_type == CvectorvectorJetType:
        for item in src:
            v2 = CvectorJetType()
            for item2 in item:
                v2.push_back(item2)
            v.push_back(v2)
    else:
        for item in src:
            v.push_back(item)

    return v

#### List of jet corrections for MEM
jet_corrections = [
        "jesAbsoluteStat",
        "jesAbsoluteScale",
        "jesAbsoluteFlavMap",
        "jesAbsoluteMPFBias",
        "jer"
]


### ttbar classification
ttCls = OrderedDict()
ttCls['ttll'] = '(event.genTtbarId<1)'
ttCls['ttcc'] = '(event.genTtbarId>40) && (event.genTtbarId<50)'
ttCls['ttb'] = '(event.genTtbarId==51)'
ttCls['tt2b'] = '(event.genTtbarId==52)'
ttCls['ttbb'] = '(event.genTtbarId>52) && (event.genTtbarId<57)'


class resolvedAnalyzer(Module):
    def __init__(self, sample="None"):
    #def __init__(self, sample="None", parameters={}):
	self.writeHistFile=True
        self.sample= sample
        #self.parameters = parameters

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

        #for icut in ['presel', 'preselWeighted',  'lep', 'lepWeighted', 'met', 'metWeighted', 'jet', 'jetWeighted', 'bDeepCSV', 'bDeepCSVWeighted', 'bDeepFlav', 'bDeepFlavWeighted' ]:
        for icut in [ 'bDeepFlav', 'bDeepFlavWeighted' ]:
            if self.sample.startswith('TTTo'):
                for ttXX, ttXXcond in ttCls.items():
                    self.listOfHistos( '_'+ttXX+'_'+icut )
            else:
                self.listOfHistos( '_'+icut )

    def listOfHistos(self, t ):
        self.addObject( ROOT.TH1F('nPVs'+t,   ';number of PVs',   100, 0, 100) )
        self.addObject( ROOT.TH1F('njets'+t,   ';number of jets',   20, 0, 20) )
        self.addObject( ROOT.TH1F('nbjetsCSV'+t,   ';number of bjets deepCSV',   20, 0, 20) )
        self.addObject( ROOT.TH1F('nbjetsFlav'+t,   ';number of bjets deepFlav',   20, 0, 20) )
        self.addObject( ROOT.TH1F('MEM'+t,   ';MEM',   100, 0, 1) )
        for unc in jet_corrections:
            for ud in ["Up","Down"]:
                self.addObject( ROOT.TH1F('MEM'+t+'_'+unc+ud,   ';MEM',   100, 0, 1) )
        self.addObject( ROOT.TH1F('BLR'+t,   ';BLR',   100, 0, 1) )
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



    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("totalWeight",  "F");
        self.out.branch('MEM', 'F' )
        for unc in jet_corrections:
            for ud in ["Up","Down"]:
                self.out.branch('MEM'+'_'+unc+ud, 'F' )
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
        totalSelection = metcut and nlepcut and njetscut and nbjetscut

	if totalSelection:

	    ##### Calculate the MEM

	    ## Put leptons in format for MEM
	    leps_p4 = CvectorLorentz()
            lep_charge = []
	    for ilep in goodLeptons:
		v = ROOT.TLorentzVector()
		v.SetPtEtaPhiM(ilep.pt, ilep.eta, ilep.phi, ilep.mass)
		leps_p4.push_back(v)
                lep_charge.append(ilep.charge)
	    leps_charge = vec_from_list(Cvectordouble, lep_charge)

	    ## Put MET in format for MEM
            met = ROOT.TLorentzVector()
            met.SetPtEtaPhiM(MET.pt, 0, MET.phi, 0)

	    ## Put jets in format for MEM
            jets_p4 = CvectorvectorLorentz()
            jets_p4_nominal = CvectorLorentz()
            jettypes = []

            for iJet in goodJetsNoLep:
                v = ROOT.TLorentzVector()
		v.SetPtEtaPhiM(iJet.pt, iJet.eta, iJet.phi, iJet.mass)
                jets_p4_nominal.push_back(v)
                jettypes.append(0)

            jets_p4.push_back(jets_p4_nominal)

            changes = []
            changes.append(False)
            for unc in jet_corrections:
                for ud in ["Up","Down"]:
                    changes.append(False)
                    jets_p4_syst = CvectorLorentz()
                    for iJet in goodJetsNoLep:
                        pt = getattr(iJet,"pt_{a}{b}".format(a = unc, b = ud))
                        mass = getattr(iJet,"mass_{a}{b}".format(a = unc, b = ud))
                        v = ROOT.TLorentzVector()
                        v.SetPtEtaPhiM(pt, iJet.eta, iJet.phi, mass)
                        jets_p4_syst.push_back(v)
                    jets_p4.push_back(jets_p4_syst)

            changes_jet_category = vec_from_list(Cvectorbool, changes)

            jdeepcsvfull = []
            jtypefull = []
            jet_deepjet = []
            for b in goodJetsNoLep: jet_deepjet.append(b.btagDeepFlavB)
            for i in range(len(jet_corrections)*2+1):
                jdeepcsvfull.append(jet_deepjet)
                jtypefull.append(jettypes)

            jets_type = vec_from_list(CvectorvectorJetType, jtypefull)
            jets_tagger = vec_from_list(Cvectorvectordouble, jdeepcsvfull)

            jv = []
            for iJet in goodJetsNoLep:
                l  = []
                for unc in jet_corrections:
                    for ud in ["Up","Down"]:
                        l.append(iJet.corr_JER)
                jv.append(l)
            jvfull = []
            for i in range(len(jet_corrections)*2+1):
                jvfull.append(jv)

            jets_variations = vec_from_list(Cvectorvectorvectordouble, jvfull)

	    ### create the MEM classifier, specifying the verbosity and b-tagger type
            ### verbosity (debug code) 1=output,2=input,4=init,8=init_more,16=event,32=integration
	    cls_mem = ROOT.MEMClassifier(8, 'btagDeepFlavB_', '2017')

	    ret = cls_mem.GetOutput(
		leps_p4,
		leps_charge,
		jets_p4,
		jets_tagger,
		jets_type,
		jets_variations,
		met,
		changes_jet_category
	    )

	    ## save the output
	    print "mem_p=",ret[0].p
	    getattr( self, 'MEM_bDeepFlav' ).Fill( ret[0].p )
            self.out.fillBranch('MEM', ret[0].p )
	    getattr( self, 'MEM_bDeepFlavWeighted' ).Fill( ret[0].p, weight )
	    getattr( self, 'BLR_bDeepFlav' ).Fill( ret[0].blr_4b/ (ret[0].blr_4b + ret[0].blr_2b) )
	    getattr( self, 'BLR_bDeepFlavWeighted' ).Fill( ret[0].blr_4b/ (ret[0].blr_4b + ret[0].blr_2b), weight )

            index = 0
            for unc in jet_corrections:
                for ud in ["Up","Down"]:
                    if changes[1+index] == True:
	                getattr( self, 'MEM_bDeepFlav_'+unc+ud ).Fill( ret[1+index].p_variated[index] )
                        self.out.fillBranch('MEM_'+unc+ud, ret[1+index].p_variated[index] )
                    else:
	                getattr( self, 'MEM_bDeepFlav_'+unc+ud ).Fill( ret[0].p_variated[index] )
                        self.out.fillBranch('MEM_'+unc+ud, ret[0].p_variated[index] )
                    index += 1

            ################# Rest of sanity plots
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


#myresolvedAnalyzer = lambda : quickAnalyzer()
