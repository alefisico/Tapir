from math import sqrt


class LHEScaleWeight:
    def __init__(self, tree, n):
        #self.id = tree.nLHEScaleWeight[n];
        self.wgt = tree.LHEScaleWeight[n];
        pass
    @staticmethod
    def make_array(input):
        return [LHEScaleWeight(input, i) for i in range(input.nLHEScaleWeight)]

class Electron:
    def __init__(self, tree, n, MC):
        self.charge = tree.Electron_charge[n];
        self.dxy = tree.Electron_dxy[n];
        self.dz = tree.Electron_dz[n];
        self.dxyErr = tree.Electron_dxyErr[n];
        self.dzErr = tree.Electron_dzErr[n];
        self.ip3d = tree.Electron_ip3d[n];
        self.sip3d = tree.Electron_sip3d[n];
        self.convVeto = tree.Electron_convVeto[n];
        self.lostHits = tree.Electron_lostHits[n];
        self.relIso03 = tree.Electron_pfRelIso03_all[n];
        self.tightCharge = tree.Electron_tightCharge[n];
        self.pt = tree.Electron_pt[n];
        self.eta = tree.Electron_eta[n];
        self.phi = tree.Electron_phi[n];
        self.mass = tree.Electron_mass[n];
        self.chargedHadRelIso03 = tree.Electron_pfRelIso03_chg[n];
        self.sieie = tree.Electron_sieie[n];
        self.DEta = -99#tree.Electron_DEta[n];#KS: Not in nanoAOD. Please check this var.
        self.DPhi = -99#tree.Electron_DPhi[n];#KS: Not in nanoAOD. Please check this var.
        self.hoe = tree.Electron_hoe[n];
        #Disabled until new nanoAOD
        self.mvaFall17Iso = tree.Electron_mvaFall17Iso[n];
        self.eleCutId = tree.Electron_cutBased[n]; #https://github.com/cms-nanoAOD/cmssw/blob/master/PhysicsTools/NanoAOD/python/electrons_cff.py#L187
        self.jetIdx = tree.Electron_jetIdx[n];
        self.etaSc = tree.Electron_deltaEtaSC[n] + tree.Electron_eta[n];
        self.pdgId = tree.Electron_pdgId[n];
        if MC:
            pass

        
        #### Old variables (for reference)
        #self.mcMatchIdx = tree.Electron_mcMatchIdx[n]; #KS: Not in nanoAOD. Please check this var.
        #self.mcMatchAny = tree.selLeptons_mcMatchAny[n];
        #self.mcMatchTau = tree.selLeptons_mcMatchTau[n];
        #self.mcPt = tree.selLeptons_mcPt[n];
        #self.mediumMuonId = tree.selLeptons_mediumMuonId[n];
        #self.tightId = tree.selLeptons_tightId[n];
        #self.relIso04 = tree.Electron_relIso04[n];
        #self.miniRelIso = tree.selLeptons_miniRelIso[n];
        #self.relIsoAn04 = tree.selLeptons_relIsoAn04[n];
        #self.eleExpMissingInnerHits = tree.selLeptons_eleExpMissingInnerHits[n];
        #self.combIsoAreaCorr = tree.selLeptons_combIsoAreaCorr[n];
        #self.ooEmooP = tree.Electron_ooEmooP[n];#KS: Not in nanoAOD. Please check what this var is.
        #self.dr03TkSumPt = tree.selLeptons_dr03TkSumPt[n];
        #self.eleEcalClusterIso = tree.selLeptons_eleEcalClusterIso[n];
        #self.eleHcalClusterIso = tree.selLeptons_eleHcalClusterIso[n];
        #self.miniIsoCharged = tree.selLeptons_miniIsoCharged[n];
        #self.miniIsoNeutral = tree.selLeptons_miniIsoNeutral[n];
        #self.mvaTTHjetPtRel = tree.selLeptons_mvaTTHjetPtRel[n];
        #self.chargedHadRelIso04 = tree.selLeptons_chargedHadRelIso04[n];
        #self.mvaTTHjetNDauChargedMVASel = tree.selLeptons_mvaTTHjetNDauChargedMVASel[n];
        #self.looseIdSusy = tree.selLeptons_looseIdSusy[n];
        #self.looseIdPOG = tree.selLeptons_looseIdPOG[n];
        #self.eleMissingHits = tree.selLeptons_eleMissingHits[n];
        #self.eleChi2 = tree.selLeptons_eleChi2[n];
        #self.convVetoFull = tree.selLeptons_convVetoFull[n];
        #self.eleMVArawSpring15Trig = tree.selLeptons_eleMVArawSpring15Trig[n];
        #self.eleMVAIdSpring15Trig = tree.selLeptons_eleMVAIdSpring15Trig[n];
        #self.eleMVArawSpring15NonTrig = tree.selLeptons_eleMVArawSpring15NonTrig[n];
        #self.eleMVAIdSpring15NonTrig = tree.selLeptons_eleMVAIdSpring15NonTrig[n];
        #self.eleMVArawSpring16GenPurp = tree.selLeptons_eleMVArawSpring16GenPurp[n];
        #self.eleCutIdSummer16 = tree.selLeptons_eleCutIdSummer16[n];
        #self.segmentCompatibility = tree.selLeptons_segmentCompatibility[n];
        #self.caloCompatibility = tree.selLeptons_caloCompatibility[n];
        #self.mvaTTHjetPtRatio = tree.selLeptons_mvaTTHjetPtRatio[n];
        #self.mvaTTHjetBTagCSV = tree.selLeptons_mvaTTHjetBTagCSV[n];
        #self.mvaTTHjetDR = tree.selLeptons_mvaTTHjetDR[n];
        #self.pfRelIso03 = tree.selLeptons_pfRelIso03[n];
        #self.pfRelIso04 = tree.selLeptons_pfRelIso04[n];
        #self.SF_IsoLoose = tree.selLeptons_SF_IsoLoose[n];
        #self.SFerr_IsoLoose = tree.selLeptons_SFerr_IsoLoose[n];
        #self.SF_IsoTight = tree.selLeptons_SF_IsoTight[n];
        #self.SFerr_IsoTight = tree.selLeptons_SFerr_IsoTight[n];
        #self.SF_IdCutLoose = tree.selLeptons_SF_IdCutLoose[n];
        #self.SFerr_IdCutLoose = tree.selLeptons_SFerr_IdCutLoose[n];
        #self.SF_IdCutTight = tree.selLeptons_SF_IdCutTight[n];
        #self.SFerr_IdCutTight = tree.selLeptons_SFerr_IdCutTight[n];
        #self.SF_IdMVALoose = tree.selLeptons_SF_IdMVALoose[n];
        #self.SFerr_IdMVALoose = tree.selLeptons_SFerr_IdMVALoose[n];
        #self.SF_IdMVATight = tree.selLeptons_SF_IdMVATight[n];
        #self.SFerr_IdMVATight = tree.selLeptons_SFerr_IdMVATight[n];
        #self.SF_HLT_RunD4p3 = tree.selLeptons_SF_HLT_RunD4p3[n];
        #self.SFerr_HLT_RunD4p3 = tree.selLeptons_SFerr_HLT_RunD4p3[n];
        #self.SF_HLT_RunD4p2 = tree.selLeptons_SF_HLT_RunD4p2[n];
        #self.SFerr_HLT_RunD4p2 = tree.selLeptons_SFerr_HLT_RunD4p2[n];
        #self.SF_HLT_RunC = tree.selLeptons_SF_HLT_RunC[n];
        #self.SFerr_HLT_RunC = tree.selLeptons_SFerr_HLT_RunC[n];
        #self.SF_trk_eta = tree.selLeptons_SF_trk_eta[n];
        #self.SFerr_trk_eta = tree.selLeptons_SFerr_trk_eta[n];
        #self.Eff_HLT_RunD4p3 = tree.selLeptons_Eff_HLT_RunD4p3[n];
        #self.Efferr_HLT_RunD4p3 = tree.selLeptons_Efferr_HLT_RunD4p3[n];
        #self.Eff_HLT_RunD4p2 = tree.selLeptons_Eff_HLT_RunD4p2[n];
        #self.Efferr_HLT_RunD4p2 = tree.selLeptons_Efferr_HLT_RunD4p2[n];
        #self.Eff_HLT_RunC = tree.selLeptons_Eff_HLT_RunC[n];
        #self.Efferr_HLT_RunC = tree.selLeptons_Efferr_HLT_RunC[n];
        pass
    @staticmethod
    def make_array(input, MC = False):
        return [Electron(input, i, MC) for i in range(input.nElectron)]
class Muon:
    def __init__(self, tree, n, MC):
        self.charge = tree.Muon_charge[n];
        self.tightId = tree.Muon_tightId[n];
        self.dxy = tree.Muon_dxy[n];
        self.dz = tree.Muon_dz[n];
        self.dxyErr = tree.Muon_dxyErr[n];
        self.dzErr = tree.Muon_dzErr[n];
        self.ip3d = tree.Muon_ip3d[n];
        self.sip3d = tree.Muon_sip3d[n];
        self.tightCharge = tree.Muon_tightCharge[n];
        self.mediumId = tree.Muon_mediumId[n];
        self.pt = tree.Muon_pt[n];
        self.eta = tree.Muon_eta[n];
        self.phi = tree.Muon_phi[n];
        self.mass = tree.Muon_mass[n];
        self.nStations = tree.Muon_nStations[n];
        self.mvaTTH = tree.Muon_mvaTTH[n];
        self.jetIdx = tree.Muon_jetIdx[n];
        self.PFIso03_all = tree.Muon_pfRelIso03_all[n];
        self.PFIso03_chg = tree.Muon_pfRelIso03_chg[n];
        self.PFIso04_all = tree.Muon_pfRelIso04_all[n];
        self.pdgId = tree.Muon_pdgId[n];
        if MC:
            pass

        
        #### Old variables (for reference)
        #self.convVeto = tree.selLeptons_convVeto[n];
        #self.lostHits = tree.selLeptons_lostHits[n];
        #self.relIso03 = tree.selLeptons_relIso03[n];
        #self.relIso04 = tree.selLeptons_relIso04[n];
        #self.miniRelIso = tree.selLeptons_miniRelIso[n];
        #self.relIsoAn04 = tree.selLeptons_relIsoAn04[n];
        #self.mcMatchIdx = tree.Muon_mcMatchIdx[n];#KS: Not in nanoAOD. Please check what this var is.
        #self.mcMatchAny = tree.selLeptons_mcMatchAny[n];
        #self.mcMatchTau = tree.selLeptons_mcMatchTau[n];
        #self.mcPt = tree.selLeptons_mcPt[n];
        #self.looseIdSusy = tree.selLeptons_looseIdSusy[n];
        #self.looseIdPOG = tree.selLeptons_looseIdPOG[n];
        #self.chargedHadRelIso03 = tree.selLeptons_chargedHadRelIso03[n];
        #self.chargedHadRelIso04 = tree.selLeptons_chargedHadRelIso04[n];
        #self.convVetoFull = tree.selLeptons_convVetoFull[n];
        #self.trkKink = tree.selLeptons_trkKink[n];
        #self.segmentCompatibility = tree.selLeptons_segmentCompatibility[n];
        #self.caloCompatibility = tree.selLeptons_caloCompatibility[n];
        #self.globalTrackChi2 = tree.selLeptons_globalTrackChi2[n];
        #self.nChamberHits = tree.selLeptons_nChamberHits[n];
        #self.isPFMuon = tree.selLeptons_isPFMuon[n];
        #self.isGlobalMuon = tree.selLeptons_isGlobalMuon[n];
        #self.isTrackerMuon = tree.selLeptons_isTrackerMuon[n];
        #self.pixelHits = tree.selLeptons_pixelHits[n];
        #self.trackerLayers = tree.selLeptons_trackerLayers[n];
        #self.pixelLayers = tree.selLeptons_pixelLayers[n];
        #self.jetPtRatio = tree.selLeptons_jetPtRatio[n];
        #self.jetBTagCSV = tree.selLeptons_jetBTagCSV[n];
        #self.jetDR = tree.selLeptons_jetDR[n];
        #self.mvaTTHjetPtRatio = tree.selLeptons_mvaTTHjetPtRatio[n];
        #self.mvaTTHjetBTagCSV = tree.selLeptons_mvaTTHjetBTagCSV[n];
        #self.mvaTTHjetDR = tree.selLeptons_mvaTTHjetDR[n];
        #self.combIsoAreaCorr = tree.selLeptons_combIsoAreaCorr[n];
        #self.dr03TkSumPt = tree.selLeptons_dr03TkSumPt[n];
        #self.miniIsoCharged = tree.selLeptons_miniIsoCharged[n];
        #self.miniIsoNeutral = tree.selLeptons_miniIsoNeutral[n];
        #self.mvaTTHjetPtRel = tree.selLeptons_mvaTTHjetPtRel[n];
        #self.mvaTTHjetNDauChargedMVASel = tree.selLeptons_mvaTTHjetNDauChargedMVASel[n];
        #self.uncalibratedPt = tree.selLeptons_uncalibratedPt[n];
        #self.SF_IsoLoose = tree.selLeptons_SF_IsoLoose[n];
        #self.SFerr_IsoLoose = tree.selLeptons_SFerr_IsoLoose[n];
        #self.SF_IsoTight = tree.selLeptons_SF_IsoTight[n];
        #self.SFerr_IsoTight = tree.selLeptons_SFerr_IsoTight[n];
        #self.SF_IdCutLoose = tree.selLeptons_SF_IdCutLoose[n];
        #self.SFerr_IdCutLoose = tree.selLeptons_SFerr_IdCutLoose[n];
        #self.SF_IdCutTight = tree.selLeptons_SF_IdCutTight[n];
        #self.SFerr_IdCutTight = tree.selLeptons_SFerr_IdCutTight[n];
        #self.SF_IdMVALoose = tree.selLeptons_SF_IdMVALoose[n];
        #self.SFerr_IdMVALoose = tree.selLeptons_SFerr_IdMVALoose[n];
        #self.SF_IdMVATight = tree.selLeptons_SF_IdMVATight[n];
        #self.SFerr_IdMVATight = tree.selLeptons_SFerr_IdMVATight[n];
        #self.SF_HLT_RunD4p3 = tree.selLeptons_SF_HLT_RunD4p3[n];
        #self.SFerr_HLT_RunD4p3 = tree.selLeptons_SFerr_HLT_RunD4p3[n];
        #self.SF_HLT_RunD4p2 = tree.selLeptons_SF_HLT_RunD4p2[n];
        #self.SFerr_HLT_RunD4p2 = tree.selLeptons_SFerr_HLT_RunD4p2[n];
        #self.SF_HLT_RunC = tree.selLeptons_SF_HLT_RunC[n];
        #self.SFerr_HLT_RunC = tree.selLeptons_SFerr_HLT_RunC[n];
        #self.SF_trk_eta = tree.selLeptons_SF_trk_eta[n];
        #self.SFerr_trk_eta = tree.selLeptons_SFerr_trk_eta[n];
        #self.Eff_HLT_RunD4p3 = tree.selLeptons_Eff_HLT_RunD4p3[n];
        #self.Efferr_HLT_RunD4p3 = tree.selLeptons_Efferr_HLT_RunD4p3[n];
        #self.Eff_HLT_RunD4p2 = tree.selLeptons_Eff_HLT_RunD4p2[n];
        #self.Efferr_HLT_RunD4p2 = tree.selLeptons_Efferr_HLT_RunD4p2[n];
        #self.Eff_HLT_RunC = tree.selLeptons_Eff_HLT_RunC[n];
        #self.Efferr_HLT_RunC = tree.selLeptons_Efferr_HLT_RunC[n];
        pass
    @staticmethod
    def make_array(input, MC = False):
        return [Muon(input, i, MC) for i in range(input.nMuon)]

class GenPart:
    def __init__(self, tree, n, MC):
        self.genPartIdxMother = tree.GenPart_genPartIdxMother[n]
        self.pdgId = tree.GenPart_pdgId[n]
        
        self.pt = tree.GenPart_pt[n]
        self.eta = tree.GenPart_eta[n]
        self.phi = tree.GenPart_phi[n]
        self.mass = tree.GenPart_mass[n]
        pass
    @staticmethod   
    def make_array(input, MC = True):
        return [GenPart(input, i, MC) for i in range(input.nGenPart)]

class Jet:
    def __init__(self, tree, n, MC):
        self.jetId = tree.Jet_jetId[n];
        self.puId = tree.Jet_puId[n];
        self.btagCSV = tree.Jet_btagCSVV2[n];
        self.btagCMVA = tree.Jet_btagCMVA[n];
        self.btagDeepCSV = tree.Jet_btagDeepB[n];
        self.eta = tree.Jet_eta[n];
        self.phi = tree.Jet_phi[n];
        self.mass = tree.Jet_mass[n];
        self.chHEF = tree.Jet_chHEF[n];
        self.neHEF = tree.Jet_neHEF[n];
        self.chEmEF = tree.Jet_chEmEF[n];
        self.neEmEF = tree.Jet_neEmEF[n];
        self.qgl = tree.Jet_qgl[n];
        self.nConstituents = tree.Jet_nConstituents[n];
        if MC:
            self.partonFlavour = tree.Jet_partonFlavour[n];
            self.hadronFlavour = tree.Jet_hadronFlavour[n];
            self.genJetIdx = tree.Jet_genJetIdx[n];
            pass
        
        self.rawPt = tree.Jet_pt[n] * (1 - tree.Jet_rawFactor[n]);#IMPORTANT: May has to be changed when JEC recorrection is implemented in postprocessing
        self.corr = (1 - tree.Jet_rawFactor[n]); #IMPORTANT: May has to be changed when JEC recorrection is implemented in postprocessing

        if not MC:
            self.pt = tree.Jet_pt[n];
        else:
            #self.pt = tree.Jet_pt[n]
            #self.corr_JER = 0.0
            self.pt = tree.Jet_pt_nom[n]; #corrected pt from nanoAOD * JER (from postprocessing)
            self.corr_JER = tree.Jet_pt_nom[n]/tree.Jet_pt[n];

            # btag Weights
            self.btagSF = tree.Jet_btagSF[n]
            self.btagSF_up = tree.Jet_btagSF_up[n]
            self.btagSF_down = tree.Jet_btagSF_down[n]
            self.btagSF_shape = tree.Jet_btagSF_shape[n]
            self.btagSF_shape_up_jes = tree.Jet_btagSF_shape_up_jes[n]
            self.btagSF_shape_down_jes = tree.Jet_btagSF_shape_down_jes[n]
            self.btagSF_shape_up_lf = tree.Jet_btagSF_shape_up_lf[n]
            self.btagSF_shape_down_lf = tree.Jet_btagSF_shape_down_lf[n]
            self.btagSF_shape_up_hf = tree.Jet_btagSF_shape_up_hf[n]
            self.btagSF_shape_down_hf = tree.Jet_btagSF_shape_down_hf[n]
            self.btagSF_shape_up_hfstats1 = tree.Jet_btagSF_shape_up_hfstats1[n]
            self.btagSF_shape_down_hfstats1 = tree.Jet_btagSF_shape_down_hfstats1[n]
            self.btagSF_shape_up_hfstats2 = tree.Jet_btagSF_shape_up_hfstats2[n]
            self.btagSF_shape_down_hfstats2 = tree.Jet_btagSF_shape_down_hfstats2[n]
            self.btagSF_shape_up_lfstats1 = tree.Jet_btagSF_shape_up_lfstats1[n]
            self.btagSF_shape_down_lfstats1 = tree.Jet_btagSF_shape_down_lfstats1[n]
            self.btagSF_shape_up_lfstats2 = tree.Jet_btagSF_shape_up_lfstats2[n]
            self.btagSF_shape_down_lfstats2 = tree.Jet_btagSF_shape_down_lfstats2[n]
            self.btagSF_shape_up_cferr1 = tree.Jet_btagSF_shape_up_cferr1[n]
            self.btagSF_shape_down_cferr1 = tree.Jet_btagSF_shape_down_cferr1[n]
            self.btagSF_shape_up_cferr2 = tree.Jet_btagSF_shape_up_cferr2[n]
            self.btagSF_shape_down_cferr2 = tree.Jet_btagSF_shape_down_cferr2[n]

            self.pt_corr_JERUp = tree.Jet_pt_jerUp[n]
            self.pt_corr_JERDown = tree.Jet_pt_jerDown[n]

            self.pt_corr_AbsoluteStatUp = tree.Jet_pt_jesAbsoluteStatUp[n]
            self.pt_corr_AbsoluteScaleUp = tree.Jet_pt_jesAbsoluteScaleUp[n]
            self.pt_corr_AbsoluteFlavMapUp = tree.Jet_pt_jesAbsoluteFlavMapUp[n]
            self.pt_corr_AbsoluteMPFBiasUp = tree.Jet_pt_jesAbsoluteMPFBiasUp[n]
            self.pt_corr_FragmentationUp = tree.Jet_pt_jesFragmentationUp[n]
            self.pt_corr_SinglePionECALUp = tree.Jet_pt_jesSinglePionECALUp[n]
            self.pt_corr_SinglePionHCALUp = tree.Jet_pt_jesSinglePionHCALUp[n]
            self.pt_corr_FlavorQCDUp = tree.Jet_pt_jesFlavorQCDUp[n]
            self.pt_corr_TimePtEtaUp = tree.Jet_pt_jesTimePtEtaUp[n]
            self.pt_corr_RelativeJEREC1Up = tree.Jet_pt_jesRelativeJEREC1Up[n]
            self.pt_corr_RelativeJEREC2Up = tree.Jet_pt_jesRelativeJEREC2Up[n]
            self.pt_corr_RelativeJERHFUp = tree.Jet_pt_jesRelativeJERHFUp[n]
            self.pt_corr_RelativePtBBUp = tree.Jet_pt_jesRelativePtBBUp[n]
            self.pt_corr_RelativePtEC1Up = tree.Jet_pt_jesRelativePtEC1Up[n]
            self.pt_corr_RelativePtEC2Up = tree.Jet_pt_jesRelativePtEC2Up[n]
            self.pt_corr_RelativePtHFUp = tree.Jet_pt_jesRelativePtHFUp[n]
            self.pt_corr_RelativeBalUp = tree.Jet_pt_jesRelativeBalUp[n]
            self.pt_corr_RelativeFSRUp = tree.Jet_pt_jesRelativeFSRUp[n]
            self.pt_corr_RelativeStatFSRUp = tree.Jet_pt_jesRelativeStatFSRUp[n]
            self.pt_corr_RelativeStatECUp = tree.Jet_pt_jesRelativeStatECUp[n]
            self.pt_corr_RelativeStatHFUp = tree.Jet_pt_jesRelativeStatHFUp[n]
            self.pt_corr_PileUpDataMCUp = tree.Jet_pt_jesPileUpDataMCUp[n]
            self.pt_corr_PileUpPtRefUp = tree.Jet_pt_jesPileUpPtRefUp[n]
            self.pt_corr_PileUpPtBBUp = tree.Jet_pt_jesPileUpPtBBUp[n]
            self.pt_corr_PileUpPtEC1Up = tree.Jet_pt_jesPileUpPtEC1Up[n]
            self.pt_corr_PileUpPtEC2Up = tree.Jet_pt_jesPileUpPtEC2Up[n]
            self.pt_corr_PileUpPtHFUp = tree.Jet_pt_jesPileUpPtHFUp[n]
            self.pt_corr_PileUpMuZeroUp = tree.Jet_pt_jesPileUpMuZeroUp[n]
            self.pt_corr_PileUpEnvelopeUp = tree.Jet_pt_jesPileUpEnvelopeUp[n]
            self.pt_corr_SubTotalPileUpUp = tree.Jet_pt_jesSubTotalPileUpUp[n]
            self.pt_corr_SubTotalRelativeUp = tree.Jet_pt_jesSubTotalRelativeUp[n]
            self.pt_corr_SubTotalPtUp = tree.Jet_pt_jesSubTotalPtUp[n]
            self.pt_corr_SubTotalScaleUp = tree.Jet_pt_jesSubTotalScaleUp[n]
            self.pt_corr_SubTotalAbsoluteUp = tree.Jet_pt_jesSubTotalAbsoluteUp[n]
            self.pt_corr_SubTotalMCUp = tree.Jet_pt_jesSubTotalMCUp[n]
            self.pt_corr_TotalUp = tree.Jet_pt_jesTotalUp[n]
            self.pt_corr_TotalNoFlavorUp = tree.Jet_pt_jesTotalNoFlavorUp[n]
            self.pt_corr_TotalNoTimeUp = tree.Jet_pt_jesTotalNoTimeUp[n]
            self.pt_corr_TotalNoFlavorNoTimeUp = tree.Jet_pt_jesTotalNoFlavorNoTimeUp[n]
            self.pt_corr_FlavorZJetUp = tree.Jet_pt_jesFlavorZJetUp[n]
            self.pt_corr_FlavorPhotonJetUp = tree.Jet_pt_jesFlavorPhotonJetUp[n]
            self.pt_corr_FlavorPureGluonUp = tree.Jet_pt_jesFlavorPureGluonUp[n]
            self.pt_corr_FlavorPureQuarkUp = tree.Jet_pt_jesFlavorPureQuarkUp[n]
            self.pt_corr_FlavorPureCharmUp = tree.Jet_pt_jesFlavorPureCharmUp[n]
            self.pt_corr_FlavorPureBottomUp = tree.Jet_pt_jesFlavorPureBottomUp[n]
            self.pt_corr_TimeRunBUp = tree.Jet_pt_jesTimeRunBUp[n]
            self.pt_corr_TimeRunCUp = tree.Jet_pt_jesTimeRunCUp[n]
            self.pt_corr_TimeRunDUp = tree.Jet_pt_jesTimeRunDUp[n]
            self.pt_corr_TimeRunEUp = tree.Jet_pt_jesTimeRunEUp[n]
            self.pt_corr_TimeRunFUp = tree.Jet_pt_jesTimeRunFUp[n]
            self.pt_corr_CorrelationGroupMPFInSituUp = tree.Jet_pt_jesCorrelationGroupMPFInSituUp[n]
            self.pt_corr_CorrelationGroupIntercalibrationUp = tree.Jet_pt_jesCorrelationGroupIntercalibrationUp[n]
            self.pt_corr_CorrelationGroupbJESUp = tree.Jet_pt_jesCorrelationGroupbJESUp[n]
            self.pt_corr_CorrelationGroupFlavorUp = tree.Jet_pt_jesCorrelationGroupFlavorUp[n]
            self.pt_corr_CorrelationGroupUncorrelatedUp = tree.Jet_pt_jesCorrelationGroupUncorrelatedUp[n]
            self.pt_corr_AbsoluteStatDown = tree.Jet_pt_jesAbsoluteStatDown[n]
            self.pt_corr_AbsoluteScaleDown = tree.Jet_pt_jesAbsoluteScaleDown[n]
            self.pt_corr_AbsoluteFlavMapDown = tree.Jet_pt_jesAbsoluteFlavMapDown[n]
            self.pt_corr_AbsoluteMPFBiasDown = tree.Jet_pt_jesAbsoluteMPFBiasDown[n]
            self.pt_corr_FragmentationDown = tree.Jet_pt_jesFragmentationDown[n]
            self.pt_corr_SinglePionECALDown = tree.Jet_pt_jesSinglePionECALDown[n]
            self.pt_corr_SinglePionHCALDown = tree.Jet_pt_jesSinglePionHCALDown[n]
            self.pt_corr_FlavorQCDDown = tree.Jet_pt_jesFlavorQCDDown[n]
            self.pt_corr_TimePtEtaDown = tree.Jet_pt_jesTimePtEtaDown[n]
            self.pt_corr_RelativeJEREC1Down = tree.Jet_pt_jesRelativeJEREC1Down[n]
            self.pt_corr_RelativeJEREC2Down = tree.Jet_pt_jesRelativeJEREC2Down[n]
            self.pt_corr_RelativeJERHFDown = tree.Jet_pt_jesRelativeJERHFDown[n]
            self.pt_corr_RelativePtBBDown = tree.Jet_pt_jesRelativePtBBDown[n]
            self.pt_corr_RelativePtEC1Down = tree.Jet_pt_jesRelativePtEC1Down[n]
            self.pt_corr_RelativePtEC2Down = tree.Jet_pt_jesRelativePtEC2Down[n]
            self.pt_corr_RelativePtHFDown = tree.Jet_pt_jesRelativePtHFDown[n]
            self.pt_corr_RelativeBalDown = tree.Jet_pt_jesRelativeBalDown[n]
            self.pt_corr_RelativeFSRDown = tree.Jet_pt_jesRelativeFSRDown[n]
            self.pt_corr_RelativeStatFSRDown = tree.Jet_pt_jesRelativeStatFSRDown[n]
            self.pt_corr_RelativeStatECDown = tree.Jet_pt_jesRelativeStatECDown[n]
            self.pt_corr_RelativeStatHFDown = tree.Jet_pt_jesRelativeStatHFDown[n]
            self.pt_corr_PileUpDataMCDown = tree.Jet_pt_jesPileUpDataMCDown[n]
            self.pt_corr_PileUpPtRefDown = tree.Jet_pt_jesPileUpPtRefDown[n]
            self.pt_corr_PileUpPtBBDown = tree.Jet_pt_jesPileUpPtBBDown[n]
            self.pt_corr_PileUpPtEC1Down = tree.Jet_pt_jesPileUpPtEC1Down[n]
            self.pt_corr_PileUpPtEC2Down = tree.Jet_pt_jesPileUpPtEC2Down[n]
            self.pt_corr_PileUpPtHFDown = tree.Jet_pt_jesPileUpPtHFDown[n]
            self.pt_corr_PileUpMuZeroDown = tree.Jet_pt_jesPileUpMuZeroDown[n]
            self.pt_corr_PileUpEnvelopeDown = tree.Jet_pt_jesPileUpEnvelopeDown[n]
            self.pt_corr_SubTotalPileUpDown = tree.Jet_pt_jesSubTotalPileUpDown[n]
            self.pt_corr_SubTotalRelativeDown = tree.Jet_pt_jesSubTotalRelativeDown[n]
            self.pt_corr_SubTotalPtDown = tree.Jet_pt_jesSubTotalPtDown[n]
            self.pt_corr_SubTotalScaleDown = tree.Jet_pt_jesSubTotalScaleDown[n]
            self.pt_corr_SubTotalAbsoluteDown = tree.Jet_pt_jesSubTotalAbsoluteDown[n]
            self.pt_corr_SubTotalMCDown = tree.Jet_pt_jesSubTotalMCDown[n]
            self.pt_corr_TotalDown = tree.Jet_pt_jesTotalDown[n]
            self.pt_corr_TotalNoFlavorDown = tree.Jet_pt_jesTotalNoFlavorDown[n]
            self.pt_corr_TotalNoTimeDown = tree.Jet_pt_jesTotalNoTimeDown[n]
            self.pt_corr_TotalNoFlavorNoTimeDown = tree.Jet_pt_jesTotalNoFlavorNoTimeDown[n]
            self.pt_corr_FlavorZJetDown = tree.Jet_pt_jesFlavorZJetDown[n]
            self.pt_corr_FlavorPhotonJetDown = tree.Jet_pt_jesFlavorPhotonJetDown[n]
            self.pt_corr_FlavorPureGluonDown = tree.Jet_pt_jesFlavorPureGluonDown[n]
            self.pt_corr_FlavorPureQuarkDown = tree.Jet_pt_jesFlavorPureQuarkDown[n]
            self.pt_corr_FlavorPureCharmDown = tree.Jet_pt_jesFlavorPureCharmDown[n]
            self.pt_corr_FlavorPureBottomDown = tree.Jet_pt_jesFlavorPureBottomDown[n]
            self.pt_corr_TimeRunBDown = tree.Jet_pt_jesTimeRunBDown[n]
            self.pt_corr_TimeRunCDown = tree.Jet_pt_jesTimeRunCDown[n]
            self.pt_corr_TimeRunDDown = tree.Jet_pt_jesTimeRunDDown[n]
            self.pt_corr_TimeRunEDown = tree.Jet_pt_jesTimeRunEDown[n]
            self.pt_corr_TimeRunFDown = tree.Jet_pt_jesTimeRunFDown[n]
            self.pt_corr_CorrelationGroupMPFInSituDown = tree.Jet_pt_jesCorrelationGroupMPFInSituDown[n]
            self.pt_corr_CorrelationGroupIntercalibrationDown = tree.Jet_pt_jesCorrelationGroupIntercalibrationDown[n]
            self.pt_corr_CorrelationGroupbJESDown = tree.Jet_pt_jesCorrelationGroupbJESDown[n]
            self.pt_corr_CorrelationGroupFlavorDown = tree.Jet_pt_jesCorrelationGroupFlavorDown[n]
            self.pt_corr_CorrelationGroupUncorrelatedDown = tree.Jet_pt_jesCorrelationGroupUncorrelatedDown[n]

        #### Old variables (for reference)
        #self.corr_JECUp = tree.Jet_corr_JECUp[n];
        #self.corr_JECDown = tree.Jet_corr_JECDown[n];
        #self.btagCMVAV2 = tree.Jet_btagCMVAV2[n];
        #self.muEF = tree.Jet_muEF[n];
        #self.chMult = tree.Jet_chMult[n];
        #self.nhMult = tree.Jet_nhMult[n];
        #self.ptd = tree.Jet_ptd[n];
        #self.axis2 = tree.Jet_axis2[n];
        #self.mult = tree.Jet_mult[n];
        pass
    @staticmethod
    def make_array(input, MC = False):
        return [Jet(input, i, MC) for i in range(input.nJet)]
class LHEPdfWeight:
    def __init__(self, tree, n):
        #self.id = tree.LHE_weights_pdf_id[n];
        self.wgt = tree.LHEPdfWeight[n];
        pass
    @staticmethod
    def make_array(input):
        return [LHEPdfWeight(input, i) for i in range(input.nLHEPdfWeight)]
class PV:
    def __init__(self, tree):
        self.x = tree.PV_x;
        self.y = tree.PV_y;
        self.z = tree.PV_z;
        #isFake is not in nanoAOD! It is defined as chi2==0 && ndof==0 && tracks.empty()
        #Since the PV selection also required ndof > 4 tracks.empty() is neglected!
        self.isFake = tree.PV_ndof == 0 and tree.PV_chi2 == 0
        self.ndof = tree.PV_ndof;
        self.chi2 = tree.PV_chi2
        self.Rho = sqrt(tree.PV_x*tree.PV_x + tree.PV_y*tree.PV_y)
        self.score = tree.PV_score;
        pass
    @staticmethod
    def make_array(input):
        return [PV(input)]
class met:
    """
    
    """
    @staticmethod
    def make_obj(tree, MC = False):
        _pt = getattr(tree, "MET_pt", None)
        _phi = getattr(tree, "MET_phi", None)
        _sumEt = getattr(tree, "MET_sumEt", None)
        #Not in nanoAOD but in VHbb code:
        #_rawPt = getattr(tree, "met_rawPt", None)
        #_rawPhi = getattr(tree, "met_rawPhi", None)
        #_rawSumEt = getattr(tree, "met_rawSumEt", None)
        #_eta = getattr(tree, "met_eta", None)
        #_phi = getattr(tree, "met_phi", None)
        #_mass = getattr(tree, "met_mass", None)
        
        
        if MC:
            _genPt = getattr(tree, "GenMET_pt", None)#KS: Not sure if this is correct
            _genPhi = getattr(tree, "GenMET_phi", None)#KS: Not sure if this is correct
        else:
            _genPt = -99
            _genPhi = -99
            
        #return met(_pt,0, _phi, 0, _sumEt, 0, 0, 0, _genPt, _genPhi, 0)
        return met(_pt, _phi, _sumEt, _genPt, _genPhi)
    #def __init__(self, pt,eta,phi,mass,sumEt,rawPt,rawPhi,rawSumEt,genPt,genPhi,genEta):
    def __init__(self, pt, phi, sumEt, genPt,genPhi ):
        self.pt = pt #
        #self.eta = eta #
        self.phi = phi #
        #self.mass = mass #
        self.sumEt = sumEt #
        #self.rawPt = rawPt #
        #self.rawPhi = rawPhi #
        #self.rawSumEt = rawSumEt #
        self.genPt = genPt #
        self.genPhi = genPhi #
        #self.genEta = genEta #
        pass


class trggerObject:
    """
    Accessing the trigger objects saved in nanoAOD. 

    Trigger Objects are saved in nanoAOD as TrigObj_* with len nTrigObj
    They can be identified with the TrigObj_id variable
     ---> see triggerObjects_cff.py in PhysicsTools/NanoAOD/python/ for id definition
    Call as usual with event.trigObj_Name = trggerObject.make_array(event.input, ID)
    """
    def __init__(self, tree, n):
        self.id = tree.TrigObj_id[n]
        self.pt = tree.TrigObj_pt[n]
        self.eta = tree.TrigObj_eta[n]
        self.phi = tree.TrigObj_phi[n]
    @staticmethod
    def make_array(input, objectID):
        list_ = []
        for i in range(input.nTrigObj):
            if int(input.TrigObj_id[i]) == objectID:
                list_.append(trggerObjects(input, i))

        return list_

class HTTV2:
    def __init__(self, tree, n, MC):
        self.pt = tree.HTTV2_pt[n];
        self.eta = tree.HTTV2_eta[n];
        self.phi = tree.HTTV2_phi[n];
        self.mass = tree.HTTV2_mass[n];
        self.area = tree.HTTV2_area[n];
        self.subJetIdx1 = tree.HTTV2_subJetIdx1[n];
        self.subJetIdx2 = tree.HTTV2_subJetIdx2[n];
        self.subJetIdx3 = tree.HTTV2_subJetIdx3[n];
        self.Ropt = tree.HTTV2_Ropt[n];
        self.RoptCalc = tree.HTTV2_RoptCalc[n];
        self.fRec = tree.HTTV2_fRec[n];
        self.ptForRoptCalc = tree.HTTV2_ptForRoptCalc[n];
        self.subjetIDPassed = tree.HTTV2Subjets_IDPassed[tree.HTTV2_subJetIdx1[n]] == 1 and tree.HTTV2Subjets_IDPassed[tree.HTTV2_subJetIdx2[n]] == 1 and tree.HTTV2Subjets_IDPassed[tree.HTTV2_subJetIdx3[n]] == 1
        pass
    @staticmethod
    def make_array(input, MC = False):
        return [HTTV2(input, i, MC) for i in range(input.nHTTV2)]

class HTTV2Subjet:
    def __init__(self, tree, n, MC):
        self.pt = tree.HTTV2Subjets_pt[n];
        self.eta = tree.HTTV2Subjets_eta[n];
        self.phi = tree.HTTV2Subjets_phi[n];
        self.mass = tree.HTTV2Subjets_mass[n];
        self.area = tree.HTTV2Subjets_area[n];
        self.btag = tree.HTTV2Subjets_btag[n];
        self.IDPassed = tree.HTTV2Subjets_IDPassed[n];
        pass
    @staticmethod
    def make_array(input, MC = False):
        return [HTTV2Subjet(input, i, MC) for i in range(input.nHTTV2Subjets)]

class FatjetCA15:
    def __init__(self, tree, n, MC):
        self.pt = tree.FatjetCA15_pt[n];
        self.eta = tree.FatjetCA15_eta[n];
        self.phi = tree.FatjetCA15_phi[n];
        self.mass = tree.FatjetCA15_mass[n];
        self.area = tree.FatjetCA15_area[n];
        self.bbtag = tree.FatjetCA15_bbtag[n];
        self.tau1 = tree.FatjetCA15_tau1[n];
        self.tau2 = tree.FatjetCA15_tau2[n];
        self.tau3 = tree.FatjetCA15_tau3[n];
        pass
    @staticmethod
    def make_array(input, MC = False):
        return [FatjetCA15(input, i, MC) for i in range(input.nFatjetCA15)]

class FatjetCA15SoftDrop:
    def __init__(self, tree, n, MC):
        self.pt = tree.FatjetCA15SoftDrop_pt[n];
        self.eta = tree.FatjetCA15SoftDrop_eta[n];
        self.phi = tree.FatjetCA15SoftDrop_phi[n];
        self.mass = tree.FatjetCA15SoftDrop_mass[n];
        self.area = tree.FatjetCA15SoftDrop_area[n];
        self.bbtag = tree.FatJet_btagHbb[n];
        self.tau1 = tree.FatJet_tau1[n];
        self.tau2 = tree.FatJet_tau2[n];
        self.tau3 = tree.FatJet_tau3[n];
        self.subJetIdx1 = tree.FatjetCA15SoftDrop_subJetIdx1[n];
        self.subJetIdx2 = tree.FatjetCA15SoftDrop_subJetIdx2[n];
        self.subjetIDPassed = tree.FatjetCA15SoftDropSubjets_IDPassed[tree.FatjetCA15SoftDrop_subJetIdx1[n]] == 1 and tree.FatjetCA15SoftDropSubjets_IDPassed[tree.FatjetCA15SoftDrop_subJetIdx2[n]] == 1 
        pass
    @staticmethod
    def make_array(input, MC = False):
        return [FatjetCA15SoftDrop(input, i, MC) for i in range(input.nFatjetCA15SoftDrop)]

class FatjetCA15SoftDropSubjet:
    def __init__(self, tree, n, MC):
        self.pt = tree.FatjetCA15SoftDropSubjets_pt[n];
        self.eta = tree.FatjetCA15SoftDropSubjets_eta[n];
        self.phi = tree.FatjetCA15SoftDropSubjets_phi[n];
        self.mass = tree.FatjetCA15SoftDropSubjets_mass[n];
        self.area = tree.FatjetCA15SoftDropSubjets_area[n];
        self.btag = tree.FatjetCA15SoftDropSubjets_btag[n];
        self.IDPassed = tree.FatjetCA15SoftDropSubjets_IDPassed[n];
        pass
    @staticmethod
    def make_array(input, MC = False):
        return [FatjetCA15SoftDropSubjet(input, i, MC) for i in range(input.nFatjetCA15SoftDropSubjets)]

class FatjetAK8:
    def __init__(self, tree, n, MC):
        self.pt = tree.FatJet_pt[n];
        self.eta = tree.FatJet_eta[n];
        self.phi = tree.FatJet_phi[n];
        self.mass = tree.FatJet_mass[n];
        self.area = tree.FatJet_area[n];
        self.bbtag = tree.FatJet_btagHbb[n];
        self.tau1 = tree.FatJet_tau1[n];
        self.tau2 = tree.FatJet_tau2[n];
        self.tau3 = tree.FatJet_tau3[n];
        self.btag = tree.FatJet_btagCSVV2[n];
        self.subJetIdx1 = tree.FatJet_subJetIdx1[n];
        self.subJetIdx2 = tree.FatJet_subJetIdx2[n];
        self.msoftdrop = tree.FatJet_msoftdrop[n];
        pass
    @staticmethod
    def make_array(input, MC = False):
        return [FatjetAK8(input, i, MC) for i in range(input.nFatJet)]

class SubjetAK8:
    def __init__(self, tree, n, MC):
        self.pt = tree.SubJet_pt[n];
        self.eta = tree.SubJet_eta[n];
        self.phi = tree.SubJet_phi[n];
        self.mass = tree.SubJet_mass[n];
        self.btag = tree.SubJet_btagCSVV2[n];
        pass
    @staticmethod
    def make_array(input, MC = False):
        return [SubjetAK8(input, i, MC) for i in range(input.nSubJet)]


##################################################################################
##################################################################################
#### Some shifted MET classes from VHbb code
"""
class met_shifted_UnclusteredEnUp:
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_UnclusteredEnUp_pt", None)
        _phi = getattr(tree, "met_shifted_UnclusteredEnUp_phi", None)
        _sumEt = getattr(tree, "met_shifted_UnclusteredEnUp_sumEt", None)
        return met_shifted_UnclusteredEnUp(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
        pass
class met_shifted_UnclusteredEnDown:
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_UnclusteredEnDown_pt", None)
        _phi = getattr(tree, "met_shifted_UnclusteredEnDown_phi", None)
        _sumEt = getattr(tree, "met_shifted_UnclusteredEnDown_sumEt", None)
        return met_shifted_UnclusteredEnDown(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
        pass
class met_shifted_JetResUp:
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_JetResUp_pt", None)
        _phi = getattr(tree, "met_shifted_JetResUp_phi", None)
        _sumEt = getattr(tree, "met_shifted_JetResUp_sumEt", None)
        return met_shifted_JetResUp(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
        pass
class met_shifted_JetResDown:
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_JetResDown_pt", None)
        _phi = getattr(tree, "met_shifted_JetResDown_phi", None)
        _sumEt = getattr(tree, "met_shifted_JetResDown_sumEt", None)
        return met_shifted_JetResDown(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
        pass
class met_shifted_JetEnUp:
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_JetEnUp_pt", None)
        _phi = getattr(tree, "met_shifted_JetEnUp_phi", None)
        _sumEt = getattr(tree, "met_shifted_JetEnUp_sumEt", None)
        return met_shifted_JetEnUp(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
        pass
class met_shifted_JetEnDown:
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_JetEnDown_pt", None)
        _phi = getattr(tree, "met_shifted_JetEnDown_phi", None)
        _sumEt = getattr(tree, "met_shifted_JetEnDown_sumEt", None)
        return met_shifted_JetEnDown(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
        pass
class met_shifted_MuonEnUp:
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_MuonEnUp_pt", None)
        _phi = getattr(tree, "met_shifted_MuonEnUp_phi", None)
        _sumEt = getattr(tree, "met_shifted_MuonEnUp_sumEt", None)
        return met_shifted_MuonEnUp(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
        pass
class met_shifted_MuonEnDown:
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_MuonEnDown_pt", None)
        _phi = getattr(tree, "met_shifted_MuonEnDown_phi", None)
        _sumEt = getattr(tree, "met_shifted_MuonEnDown_sumEt", None)
        return met_shifted_MuonEnDown(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
        pass
class met_shifted_ElectronEnUp:
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_ElectronEnUp_pt", None)
        _phi = getattr(tree, "met_shifted_ElectronEnUp_phi", None)
        _sumEt = getattr(tree, "met_shifted_ElectronEnUp_sumEt", None)
        return met_shifted_ElectronEnUp(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
        pass
class met_shifted_ElectronEnDown:
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_ElectronEnDown_pt", None)
        _phi = getattr(tree, "met_shifted_ElectronEnDown_phi", None)
        _sumEt = getattr(tree, "met_shifted_ElectronEnDown_sumEt", None)
        return met_shifted_ElectronEnDown(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
        pass
class met_shifted_TauEnUp:
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_TauEnUp_pt", None)
        _phi = getattr(tree, "met_shifted_TauEnUp_phi", None)
        _sumEt = getattr(tree, "met_shifted_TauEnUp_sumEt", None)
        return met_shifted_TauEnUp(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
        pass
class met_shifted_TauEnDown:
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_shifted_TauEnDown_pt", None)
        _phi = getattr(tree, "met_shifted_TauEnDown_phi", None)
        _sumEt = getattr(tree, "met_shifted_TauEnDown_sumEt", None)
        return met_shifted_TauEnDown(_pt, _phi, _sumEt)
    def __init__(self, pt,phi,sumEt):
        self.pt = pt #
        self.phi = phi #
        self.sumEt = sumEt #
        pass

"""