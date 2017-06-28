class pileUpVertex_ptHat:
    def __init__(self, tree, n):
        self.pileUpVertex_ptHat = tree.pileUpVertex_ptHat[n];
        pass
    @staticmethod
    def make_array(input):
        return [pileUpVertex_ptHat(input, i) for i in range(input.npileUpVertex_ptHat)]
class trgObjects_hltMET70:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltMET70(input, i) for i in range(input.ntrgObjects_hltMET70)]
class trgObjects_hltL1sTripleJetVBFIorHTTIorDoubleJetCIorSingleJet:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltL1sTripleJetVBFIorHTTIorDoubleJetCIorSingleJet(input, i) for i in range(input.ntrgObjects_hltL1sTripleJetVBFIorHTTIorDoubleJetCIorSingleJet)]
class trgObjects_hltBTagPFCSVp11DoubleWithMatching:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltBTagPFCSVp11DoubleWithMatching(input, i) for i in range(input.ntrgObjects_hltBTagPFCSVp11DoubleWithMatching)]
class GenLepFromTop:
    def __init__(self, tree, n):
        self.pdgId = tree.GenLepFromTop_pdgId[n];
        self.pt = tree.GenLepFromTop_pt[n];
        self.eta = tree.GenLepFromTop_eta[n];
        self.phi = tree.GenLepFromTop_phi[n];
        self.mass = tree.GenLepFromTop_mass[n];
        self.charge = tree.GenLepFromTop_charge[n];
        self.status = tree.GenLepFromTop_status[n];
        self.isPromptHard = tree.GenLepFromTop_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenLepFromTop(input, i) for i in range(input.nGenLepFromTop)]
class ajidxaddJetsdR08:
    def __init__(self, tree, n):
        self.ajidxaddJetsdR08 = tree.ajidxaddJetsdR08[n];
        pass
    @staticmethod
    def make_array(input):
        return [ajidxaddJetsdR08(input, i) for i in range(input.najidxaddJetsdR08)]
class SubjetCA15softdrop:
    def __init__(self, tree, n):
        self.pt = tree.SubjetCA15softdrop_pt[n];
        self.eta = tree.SubjetCA15softdrop_eta[n];
        self.phi = tree.SubjetCA15softdrop_phi[n];
        self.mass = tree.SubjetCA15softdrop_mass[n];
        self.btag = tree.SubjetCA15softdrop_btag[n];
        self.jetID = tree.SubjetCA15softdrop_jetID[n];
        self.fromFJ = tree.SubjetCA15softdrop_fromFJ[n];
        pass
    @staticmethod
    def make_array(input):
        return [SubjetCA15softdrop(input, i) for i in range(input.nSubjetCA15softdrop)]
class trgObjects_hltIsoMu20:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_hltIsoMu20_pt[n];
        self.eta = tree.trgObjects_hltIsoMu20_eta[n];
        self.phi = tree.trgObjects_hltIsoMu20_phi[n];
        self.mass = tree.trgObjects_hltIsoMu20_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltIsoMu20(input, i) for i in range(input.ntrgObjects_hltIsoMu20)]
class aJCMVAV2idx:
    def __init__(self, tree, n):
        self.aJCMVAV2idx = tree.aJCMVAV2idx[n];
        pass
    @staticmethod
    def make_array(input):
        return [aJCMVAV2idx(input, i) for i in range(input.naJCMVAV2idx)]
class trgObjects_hltQuadCentralJet30:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltQuadCentralJet30(input, i) for i in range(input.ntrgObjects_hltQuadCentralJet30)]
class l1EGammas:
    def __init__(self, tree, n):
        self.pt = tree.l1EGammas_pt[n];
        self.eta = tree.l1EGammas_eta[n];
        self.phi = tree.l1EGammas_phi[n];
        self.qual = tree.l1EGammas_qual[n];
        self.iso = tree.l1EGammas_iso[n];
        pass
    @staticmethod
    def make_array(input):
        return [l1EGammas(input, i) for i in range(input.nl1EGammas)]
class hJidx_sortcsv:
    def __init__(self, tree, n):
        self.hJidx_sortcsv = tree.hJidx_sortcsv[n];
        pass
    @staticmethod
    def make_array(input):
        return [hJidx_sortcsv(input, i) for i in range(input.nhJidx_sortcsv)]
class primaryVertices:
    def __init__(self, tree, n):
        self.x = tree.primaryVertices_x[n];
        self.y = tree.primaryVertices_y[n];
        self.z = tree.primaryVertices_z[n];
        self.isFake = tree.primaryVertices_isFake[n];
        self.ndof = tree.primaryVertices_ndof[n];
        self.Rho = tree.primaryVertices_Rho[n];
        self.score = tree.primaryVertices_score[n];
        pass
    @staticmethod
    def make_array(input):
        return [primaryVertices(input, i) for i in range(input.nprimaryVertices)]
class aJCidx:
    def __init__(self, tree, n):
        self.aJCidx = tree.aJCidx[n];
        pass
    @staticmethod
    def make_array(input):
        return [aJCidx(input, i) for i in range(input.naJCidx)]
class SubjetCA15softdropz2b1:
    def __init__(self, tree, n):
        self.pt = tree.SubjetCA15softdropz2b1_pt[n];
        self.eta = tree.SubjetCA15softdropz2b1_eta[n];
        self.phi = tree.SubjetCA15softdropz2b1_phi[n];
        self.mass = tree.SubjetCA15softdropz2b1_mass[n];
        self.btag = tree.SubjetCA15softdropz2b1_btag[n];
        self.jetID = tree.SubjetCA15softdropz2b1_jetID[n];
        self.fromFJ = tree.SubjetCA15softdropz2b1_fromFJ[n];
        pass
    @staticmethod
    def make_array(input):
        return [SubjetCA15softdropz2b1(input, i) for i in range(input.nSubjetCA15softdropz2b1)]
class hJCidx:
    def __init__(self, tree, n):
        self.hJCidx = tree.hJCidx[n];
        pass
    @staticmethod
    def make_array(input):
        return [hJCidx(input, i) for i in range(input.nhJCidx)]
class l1Taus:
    def __init__(self, tree, n):
        self.pt = tree.l1Taus_pt[n];
        self.eta = tree.l1Taus_eta[n];
        self.phi = tree.l1Taus_phi[n];
        self.qual = tree.l1Taus_qual[n];
        self.iso = tree.l1Taus_iso[n];
        pass
    @staticmethod
    def make_array(input):
        return [l1Taus(input, i) for i in range(input.nl1Taus)]
class aJidx:
    def __init__(self, tree, n):
        self.aJidx = tree.aJidx[n];
        pass
    @staticmethod
    def make_array(input):
        return [aJidx(input, i) for i in range(input.naJidx)]
class GenBQuarkFromTop:
    def __init__(self, tree, n):
        self.pdgId = tree.GenBQuarkFromTop_pdgId[n];
        self.pt = tree.GenBQuarkFromTop_pt[n];
        self.eta = tree.GenBQuarkFromTop_eta[n];
        self.phi = tree.GenBQuarkFromTop_phi[n];
        self.mass = tree.GenBQuarkFromTop_mass[n];
        self.charge = tree.GenBQuarkFromTop_charge[n];
        self.status = tree.GenBQuarkFromTop_status[n];
        self.isPromptHard = tree.GenBQuarkFromTop_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenBQuarkFromTop(input, i) for i in range(input.nGenBQuarkFromTop)]
class GenLepFromTau:
    def __init__(self, tree, n):
        self.pdgId = tree.GenLepFromTau_pdgId[n];
        self.pt = tree.GenLepFromTau_pt[n];
        self.eta = tree.GenLepFromTau_eta[n];
        self.phi = tree.GenLepFromTau_phi[n];
        self.mass = tree.GenLepFromTau_mass[n];
        self.charge = tree.GenLepFromTau_charge[n];
        self.status = tree.GenLepFromTau_status[n];
        self.isPromptHard = tree.GenLepFromTau_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenLepFromTau(input, i) for i in range(input.nGenLepFromTau)]
class GenHiggsBoson:
    def __init__(self, tree, n):
        self.pdgId = tree.GenHiggsBoson_pdgId[n];
        self.pt = tree.GenHiggsBoson_pt[n];
        self.eta = tree.GenHiggsBoson_eta[n];
        self.phi = tree.GenHiggsBoson_phi[n];
        self.mass = tree.GenHiggsBoson_mass[n];
        self.charge = tree.GenHiggsBoson_charge[n];
        self.status = tree.GenHiggsBoson_status[n];
        self.isPromptHard = tree.GenHiggsBoson_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenHiggsBoson(input, i) for i in range(input.nGenHiggsBoson)]
class GenNuFromTop:
    def __init__(self, tree, n):
        self.pdgId = tree.GenNuFromTop_pdgId[n];
        self.pt = tree.GenNuFromTop_pt[n];
        self.eta = tree.GenNuFromTop_eta[n];
        self.phi = tree.GenNuFromTop_phi[n];
        self.mass = tree.GenNuFromTop_mass[n];
        self.charge = tree.GenNuFromTop_charge[n];
        self.status = tree.GenNuFromTop_status[n];
        self.isPromptHard = tree.GenNuFromTop_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenNuFromTop(input, i) for i in range(input.nGenNuFromTop)]
class GenBQuarkFromHafterISR:
    def __init__(self, tree, n):
        self.pdgId = tree.GenBQuarkFromHafterISR_pdgId[n];
        self.pt = tree.GenBQuarkFromHafterISR_pt[n];
        self.eta = tree.GenBQuarkFromHafterISR_eta[n];
        self.phi = tree.GenBQuarkFromHafterISR_phi[n];
        self.mass = tree.GenBQuarkFromHafterISR_mass[n];
        self.charge = tree.GenBQuarkFromHafterISR_charge[n];
        self.status = tree.GenBQuarkFromHafterISR_status[n];
        self.isPromptHard = tree.GenBQuarkFromHafterISR_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenBQuarkFromHafterISR(input, i) for i in range(input.nGenBQuarkFromHafterISR)]
class trgObjects_hltPFDoubleJetLooseID76:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltPFDoubleJetLooseID76(input, i) for i in range(input.ntrgObjects_hltPFDoubleJetLooseID76)]
class trgObjects_hltBTagPFCSVp016SingleWithMatching:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltBTagPFCSVp016SingleWithMatching(input, i) for i in range(input.ntrgObjects_hltBTagPFCSVp016SingleWithMatching)]
class softActivityEWKJets:
    def __init__(self, tree, n):
        self.pt = tree.softActivityEWKJets_pt[n];
        self.eta = tree.softActivityEWKJets_eta[n];
        self.phi = tree.softActivityEWKJets_phi[n];
        self.mass = tree.softActivityEWKJets_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [softActivityEWKJets(input, i) for i in range(input.nsoftActivityEWKJets)]
class HTXSRivetProducer_cat0:
    def __init__(self, tree, n):
        self.HTXSRivetProducer_cat0 = tree.HTXSRivetProducer_cat0[n];
        pass
    @staticmethod
    def make_array(input):
        return [HTXSRivetProducer_cat0(input, i) for i in range(input.nHTXSRivetProducer_cat0)]
class HTXSRivetProducer_cat1:
    def __init__(self, tree, n):
        self.HTXSRivetProducer_cat1 = tree.HTXSRivetProducer_cat1[n];
        pass
    @staticmethod
    def make_array(input):
        return [HTXSRivetProducer_cat1(input, i) for i in range(input.nHTXSRivetProducer_cat1)]
class softActivityVHJets:
    def __init__(self, tree, n):
        self.pt = tree.softActivityVHJets_pt[n];
        self.eta = tree.softActivityVHJets_eta[n];
        self.phi = tree.softActivityVHJets_phi[n];
        self.mass = tree.softActivityVHJets_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [softActivityVHJets(input, i) for i in range(input.nsoftActivityVHJets)]
class trgObjects_hltQuadPFCentralJetLooseID30:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltQuadPFCentralJetLooseID30(input, i) for i in range(input.ntrgObjects_hltQuadPFCentralJetLooseID30)]
class GenNu:
    def __init__(self, tree, n):
        self.charge = tree.GenNu_charge[n];
        self.status = tree.GenNu_status[n];
        self.isPromptHard = tree.GenNu_isPromptHard[n];
        self.pdgId = tree.GenNu_pdgId[n];
        self.pt = tree.GenNu_pt[n];
        self.eta = tree.GenNu_eta[n];
        self.phi = tree.GenNu_phi[n];
        self.mass = tree.GenNu_mass[n];
        self.motherId = tree.GenNu_motherId[n];
        self.grandmotherId = tree.GenNu_grandmotherId[n];
        self.sourceId = tree.GenNu_sourceId[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenNu(input, i) for i in range(input.nGenNu)]
class trgObjects_hltBTagCaloCSVp087Triple:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltBTagCaloCSVp087Triple(input, i) for i in range(input.ntrgObjects_hltBTagCaloCSVp087Triple)]
class trgObjects_hltEle25eta2p1WPLoose:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_hltEle25eta2p1WPLoose_pt[n];
        self.eta = tree.trgObjects_hltEle25eta2p1WPLoose_eta[n];
        self.phi = tree.trgObjects_hltEle25eta2p1WPLoose_phi[n];
        self.mass = tree.trgObjects_hltEle25eta2p1WPLoose_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltEle25eta2p1WPLoose(input, i) for i in range(input.ntrgObjects_hltEle25eta2p1WPLoose)]
class SubjetAK08softdrop:
    def __init__(self, tree, n):
        self.pt = tree.SubjetAK08softdrop_pt[n];
        self.eta = tree.SubjetAK08softdrop_eta[n];
        self.phi = tree.SubjetAK08softdrop_phi[n];
        self.mass = tree.SubjetAK08softdrop_mass[n];
        self.btag = tree.SubjetAK08softdrop_btag[n];
        self.fromFJ = tree.SubjetAK08softdrop_fromFJ[n];
        self.corr = tree.SubjetAK08softdrop_corr[n];
        self.corr_AbsoluteStatUp = tree.SubjetAK08softdrop_corr_AbsoluteStatUp[n];
        self.corr_AbsoluteStatDown = tree.SubjetAK08softdrop_corr_AbsoluteStatDown[n];
        self.corr_AbsoluteScaleUp = tree.SubjetAK08softdrop_corr_AbsoluteScaleUp[n];
        self.corr_AbsoluteScaleDown = tree.SubjetAK08softdrop_corr_AbsoluteScaleDown[n];
        self.corr_AbsoluteFlavMapUp = tree.SubjetAK08softdrop_corr_AbsoluteFlavMapUp[n];
        self.corr_AbsoluteFlavMapDown = tree.SubjetAK08softdrop_corr_AbsoluteFlavMapDown[n];
        self.corr_AbsoluteMPFBiasUp = tree.SubjetAK08softdrop_corr_AbsoluteMPFBiasUp[n];
        self.corr_AbsoluteMPFBiasDown = tree.SubjetAK08softdrop_corr_AbsoluteMPFBiasDown[n];
        self.corr_FragmentationUp = tree.SubjetAK08softdrop_corr_FragmentationUp[n];
        self.corr_FragmentationDown = tree.SubjetAK08softdrop_corr_FragmentationDown[n];
        self.corr_SinglePionECALUp = tree.SubjetAK08softdrop_corr_SinglePionECALUp[n];
        self.corr_SinglePionECALDown = tree.SubjetAK08softdrop_corr_SinglePionECALDown[n];
        self.corr_SinglePionHCALUp = tree.SubjetAK08softdrop_corr_SinglePionHCALUp[n];
        self.corr_SinglePionHCALDown = tree.SubjetAK08softdrop_corr_SinglePionHCALDown[n];
        self.corr_FlavorQCDUp = tree.SubjetAK08softdrop_corr_FlavorQCDUp[n];
        self.corr_FlavorQCDDown = tree.SubjetAK08softdrop_corr_FlavorQCDDown[n];
        self.corr_TimePtEtaUp = tree.SubjetAK08softdrop_corr_TimePtEtaUp[n];
        self.corr_TimePtEtaDown = tree.SubjetAK08softdrop_corr_TimePtEtaDown[n];
        self.corr_RelativeJEREC1Up = tree.SubjetAK08softdrop_corr_RelativeJEREC1Up[n];
        self.corr_RelativeJEREC1Down = tree.SubjetAK08softdrop_corr_RelativeJEREC1Down[n];
        self.corr_RelativeJEREC2Up = tree.SubjetAK08softdrop_corr_RelativeJEREC2Up[n];
        self.corr_RelativeJEREC2Down = tree.SubjetAK08softdrop_corr_RelativeJEREC2Down[n];
        self.corr_RelativeJERHFUp = tree.SubjetAK08softdrop_corr_RelativeJERHFUp[n];
        self.corr_RelativeJERHFDown = tree.SubjetAK08softdrop_corr_RelativeJERHFDown[n];
        self.corr_RelativePtBBUp = tree.SubjetAK08softdrop_corr_RelativePtBBUp[n];
        self.corr_RelativePtBBDown = tree.SubjetAK08softdrop_corr_RelativePtBBDown[n];
        self.corr_RelativePtEC1Up = tree.SubjetAK08softdrop_corr_RelativePtEC1Up[n];
        self.corr_RelativePtEC1Down = tree.SubjetAK08softdrop_corr_RelativePtEC1Down[n];
        self.corr_RelativePtEC2Up = tree.SubjetAK08softdrop_corr_RelativePtEC2Up[n];
        self.corr_RelativePtEC2Down = tree.SubjetAK08softdrop_corr_RelativePtEC2Down[n];
        self.corr_RelativePtHFUp = tree.SubjetAK08softdrop_corr_RelativePtHFUp[n];
        self.corr_RelativePtHFDown = tree.SubjetAK08softdrop_corr_RelativePtHFDown[n];
        self.corr_RelativeBalUp = tree.SubjetAK08softdrop_corr_RelativeBalUp[n];
        self.corr_RelativeBalDown = tree.SubjetAK08softdrop_corr_RelativeBalDown[n];
        self.corr_RelativeFSRUp = tree.SubjetAK08softdrop_corr_RelativeFSRUp[n];
        self.corr_RelativeFSRDown = tree.SubjetAK08softdrop_corr_RelativeFSRDown[n];
        self.corr_RelativeStatFSRUp = tree.SubjetAK08softdrop_corr_RelativeStatFSRUp[n];
        self.corr_RelativeStatFSRDown = tree.SubjetAK08softdrop_corr_RelativeStatFSRDown[n];
        self.corr_RelativeStatECUp = tree.SubjetAK08softdrop_corr_RelativeStatECUp[n];
        self.corr_RelativeStatECDown = tree.SubjetAK08softdrop_corr_RelativeStatECDown[n];
        self.corr_RelativeStatHFUp = tree.SubjetAK08softdrop_corr_RelativeStatHFUp[n];
        self.corr_RelativeStatHFDown = tree.SubjetAK08softdrop_corr_RelativeStatHFDown[n];
        self.corr_PileUpDataMCUp = tree.SubjetAK08softdrop_corr_PileUpDataMCUp[n];
        self.corr_PileUpDataMCDown = tree.SubjetAK08softdrop_corr_PileUpDataMCDown[n];
        self.corr_PileUpPtRefUp = tree.SubjetAK08softdrop_corr_PileUpPtRefUp[n];
        self.corr_PileUpPtRefDown = tree.SubjetAK08softdrop_corr_PileUpPtRefDown[n];
        self.corr_PileUpPtBBUp = tree.SubjetAK08softdrop_corr_PileUpPtBBUp[n];
        self.corr_PileUpPtBBDown = tree.SubjetAK08softdrop_corr_PileUpPtBBDown[n];
        self.corr_PileUpPtEC1Up = tree.SubjetAK08softdrop_corr_PileUpPtEC1Up[n];
        self.corr_PileUpPtEC1Down = tree.SubjetAK08softdrop_corr_PileUpPtEC1Down[n];
        self.corr_PileUpPtEC2Up = tree.SubjetAK08softdrop_corr_PileUpPtEC2Up[n];
        self.corr_PileUpPtEC2Down = tree.SubjetAK08softdrop_corr_PileUpPtEC2Down[n];
        self.corr_PileUpPtHFUp = tree.SubjetAK08softdrop_corr_PileUpPtHFUp[n];
        self.corr_PileUpPtHFDown = tree.SubjetAK08softdrop_corr_PileUpPtHFDown[n];
        self.corr_PileUpMuZeroUp = tree.SubjetAK08softdrop_corr_PileUpMuZeroUp[n];
        self.corr_PileUpMuZeroDown = tree.SubjetAK08softdrop_corr_PileUpMuZeroDown[n];
        self.corr_PileUpEnvelopeUp = tree.SubjetAK08softdrop_corr_PileUpEnvelopeUp[n];
        self.corr_PileUpEnvelopeDown = tree.SubjetAK08softdrop_corr_PileUpEnvelopeDown[n];
        self.corr_SubTotalPileUpUp = tree.SubjetAK08softdrop_corr_SubTotalPileUpUp[n];
        self.corr_SubTotalPileUpDown = tree.SubjetAK08softdrop_corr_SubTotalPileUpDown[n];
        self.corr_SubTotalRelativeUp = tree.SubjetAK08softdrop_corr_SubTotalRelativeUp[n];
        self.corr_SubTotalRelativeDown = tree.SubjetAK08softdrop_corr_SubTotalRelativeDown[n];
        self.corr_SubTotalPtUp = tree.SubjetAK08softdrop_corr_SubTotalPtUp[n];
        self.corr_SubTotalPtDown = tree.SubjetAK08softdrop_corr_SubTotalPtDown[n];
        self.corr_SubTotalScaleUp = tree.SubjetAK08softdrop_corr_SubTotalScaleUp[n];
        self.corr_SubTotalScaleDown = tree.SubjetAK08softdrop_corr_SubTotalScaleDown[n];
        self.corr_SubTotalAbsoluteUp = tree.SubjetAK08softdrop_corr_SubTotalAbsoluteUp[n];
        self.corr_SubTotalAbsoluteDown = tree.SubjetAK08softdrop_corr_SubTotalAbsoluteDown[n];
        self.corr_SubTotalMCUp = tree.SubjetAK08softdrop_corr_SubTotalMCUp[n];
        self.corr_SubTotalMCDown = tree.SubjetAK08softdrop_corr_SubTotalMCDown[n];
        self.corr_TotalUp = tree.SubjetAK08softdrop_corr_TotalUp[n];
        self.corr_TotalDown = tree.SubjetAK08softdrop_corr_TotalDown[n];
        self.corr_TotalNoFlavorUp = tree.SubjetAK08softdrop_corr_TotalNoFlavorUp[n];
        self.corr_TotalNoFlavorDown = tree.SubjetAK08softdrop_corr_TotalNoFlavorDown[n];
        self.corr_TotalNoTimeUp = tree.SubjetAK08softdrop_corr_TotalNoTimeUp[n];
        self.corr_TotalNoTimeDown = tree.SubjetAK08softdrop_corr_TotalNoTimeDown[n];
        self.corr_TotalNoFlavorNoTimeUp = tree.SubjetAK08softdrop_corr_TotalNoFlavorNoTimeUp[n];
        self.corr_TotalNoFlavorNoTimeDown = tree.SubjetAK08softdrop_corr_TotalNoFlavorNoTimeDown[n];
        self.corr_FlavorZJetUp = tree.SubjetAK08softdrop_corr_FlavorZJetUp[n];
        self.corr_FlavorZJetDown = tree.SubjetAK08softdrop_corr_FlavorZJetDown[n];
        self.corr_FlavorPhotonJetUp = tree.SubjetAK08softdrop_corr_FlavorPhotonJetUp[n];
        self.corr_FlavorPhotonJetDown = tree.SubjetAK08softdrop_corr_FlavorPhotonJetDown[n];
        self.corr_FlavorPureGluonUp = tree.SubjetAK08softdrop_corr_FlavorPureGluonUp[n];
        self.corr_FlavorPureGluonDown = tree.SubjetAK08softdrop_corr_FlavorPureGluonDown[n];
        self.corr_FlavorPureQuarkUp = tree.SubjetAK08softdrop_corr_FlavorPureQuarkUp[n];
        self.corr_FlavorPureQuarkDown = tree.SubjetAK08softdrop_corr_FlavorPureQuarkDown[n];
        self.corr_FlavorPureCharmUp = tree.SubjetAK08softdrop_corr_FlavorPureCharmUp[n];
        self.corr_FlavorPureCharmDown = tree.SubjetAK08softdrop_corr_FlavorPureCharmDown[n];
        self.corr_FlavorPureBottomUp = tree.SubjetAK08softdrop_corr_FlavorPureBottomUp[n];
        self.corr_FlavorPureBottomDown = tree.SubjetAK08softdrop_corr_FlavorPureBottomDown[n];
        self.corr_TimeRunBCDUp = tree.SubjetAK08softdrop_corr_TimeRunBCDUp[n];
        self.corr_TimeRunBCDDown = tree.SubjetAK08softdrop_corr_TimeRunBCDDown[n];
        self.corr_TimeRunEFUp = tree.SubjetAK08softdrop_corr_TimeRunEFUp[n];
        self.corr_TimeRunEFDown = tree.SubjetAK08softdrop_corr_TimeRunEFDown[n];
        self.corr_TimeRunGUp = tree.SubjetAK08softdrop_corr_TimeRunGUp[n];
        self.corr_TimeRunGDown = tree.SubjetAK08softdrop_corr_TimeRunGDown[n];
        self.corr_TimeRunHUp = tree.SubjetAK08softdrop_corr_TimeRunHUp[n];
        self.corr_TimeRunHDown = tree.SubjetAK08softdrop_corr_TimeRunHDown[n];
        self.corr_CorrelationGroupMPFInSituUp = tree.SubjetAK08softdrop_corr_CorrelationGroupMPFInSituUp[n];
        self.corr_CorrelationGroupMPFInSituDown = tree.SubjetAK08softdrop_corr_CorrelationGroupMPFInSituDown[n];
        self.corr_CorrelationGroupIntercalibrationUp = tree.SubjetAK08softdrop_corr_CorrelationGroupIntercalibrationUp[n];
        self.corr_CorrelationGroupIntercalibrationDown = tree.SubjetAK08softdrop_corr_CorrelationGroupIntercalibrationDown[n];
        self.corr_CorrelationGroupbJESUp = tree.SubjetAK08softdrop_corr_CorrelationGroupbJESUp[n];
        self.corr_CorrelationGroupbJESDown = tree.SubjetAK08softdrop_corr_CorrelationGroupbJESDown[n];
        self.corr_CorrelationGroupFlavorUp = tree.SubjetAK08softdrop_corr_CorrelationGroupFlavorUp[n];
        self.corr_CorrelationGroupFlavorDown = tree.SubjetAK08softdrop_corr_CorrelationGroupFlavorDown[n];
        self.corr_CorrelationGroupUncorrelatedUp = tree.SubjetAK08softdrop_corr_CorrelationGroupUncorrelatedUp[n];
        self.corr_CorrelationGroupUncorrelatedDown = tree.SubjetAK08softdrop_corr_CorrelationGroupUncorrelatedDown[n];
        pass
    @staticmethod
    def make_array(input):
        return [SubjetAK08softdrop(input, i) for i in range(input.nSubjetAK08softdrop)]
class GenLepRecovered:
    def __init__(self, tree, n):
        self.pdgId = tree.GenLepRecovered_pdgId[n];
        self.pt = tree.GenLepRecovered_pt[n];
        self.eta = tree.GenLepRecovered_eta[n];
        self.phi = tree.GenLepRecovered_phi[n];
        self.mass = tree.GenLepRecovered_mass[n];
        self.charge = tree.GenLepRecovered_charge[n];
        self.status = tree.GenLepRecovered_status[n];
        self.isPromptHard = tree.GenLepRecovered_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenLepRecovered(input, i) for i in range(input.nGenLepRecovered)]
class trgObjects_caloJets:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_caloJets_pt[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_caloJets(input, i) for i in range(input.ntrgObjects_caloJets)]
class hJCMVAV2idx:
    def __init__(self, tree, n):
        self.hJCMVAV2idx = tree.hJCMVAV2idx[n];
        pass
    @staticmethod
    def make_array(input):
        return [hJCMVAV2idx(input, i) for i in range(input.nhJCMVAV2idx)]
class trgObjects_hltPFSingleJetLooseID92:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltPFSingleJetLooseID92(input, i) for i in range(input.ntrgObjects_hltPFSingleJetLooseID92)]
class GenHadTaus:
    def __init__(self, tree, n):
        self.charge = tree.GenHadTaus_charge[n];
        self.status = tree.GenHadTaus_status[n];
        self.isPromptHard = tree.GenHadTaus_isPromptHard[n];
        self.pdgId = tree.GenHadTaus_pdgId[n];
        self.pt = tree.GenHadTaus_pt[n];
        self.eta = tree.GenHadTaus_eta[n];
        self.phi = tree.GenHadTaus_phi[n];
        self.mass = tree.GenHadTaus_mass[n];
        self.decayMode = tree.GenHadTaus_decayMode[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenHadTaus(input, i) for i in range(input.nGenHadTaus)]
class trgObjects_hltDoubleCentralJet90:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltDoubleCentralJet90(input, i) for i in range(input.ntrgObjects_hltDoubleCentralJet90)]
class trgObjects_hltL1sETM50ToETM100IorETM60Jet60dPhiMin0p4IorDoubleJetC60ETM60:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltL1sETM50ToETM100IorETM60Jet60dPhiMin0p4IorDoubleJetC60ETM60(input, i) for i in range(input.ntrgObjects_hltL1sETM50ToETM100IorETM60Jet60dPhiMin0p4IorDoubleJetC60ETM60)]
class trgObjects_hltEle25WPTight:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_hltEle25WPTight_pt[n];
        self.eta = tree.trgObjects_hltEle25WPTight_eta[n];
        self.phi = tree.trgObjects_hltEle25WPTight_phi[n];
        self.mass = tree.trgObjects_hltEle25WPTight_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltEle25WPTight(input, i) for i in range(input.ntrgObjects_hltEle25WPTight)]
class GenVbosonsRecovered:
    def __init__(self, tree, n):
        self.pdgId = tree.GenVbosonsRecovered_pdgId[n];
        self.pt = tree.GenVbosonsRecovered_pt[n];
        self.eta = tree.GenVbosonsRecovered_eta[n];
        self.phi = tree.GenVbosonsRecovered_phi[n];
        self.mass = tree.GenVbosonsRecovered_mass[n];
        self.charge = tree.GenVbosonsRecovered_charge[n];
        self.status = tree.GenVbosonsRecovered_status[n];
        self.isPromptHard = tree.GenVbosonsRecovered_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenVbosonsRecovered(input, i) for i in range(input.nGenVbosonsRecovered)]
class SubjetCA15subjetfiltered:
    def __init__(self, tree, n):
        self.pt = tree.SubjetCA15subjetfiltered_pt[n];
        self.eta = tree.SubjetCA15subjetfiltered_eta[n];
        self.phi = tree.SubjetCA15subjetfiltered_phi[n];
        self.mass = tree.SubjetCA15subjetfiltered_mass[n];
        self.btag = tree.SubjetCA15subjetfiltered_btag[n];
        self.jetID = tree.SubjetCA15subjetfiltered_jetID[n];
        self.fromFJ = tree.SubjetCA15subjetfiltered_fromFJ[n];
        self.corr = tree.SubjetCA15subjetfiltered_corr[n];
        self.corr_AbsoluteStatUp = tree.SubjetCA15subjetfiltered_corr_AbsoluteStatUp[n];
        self.corr_AbsoluteStatDown = tree.SubjetCA15subjetfiltered_corr_AbsoluteStatDown[n];
        self.corr_AbsoluteScaleUp = tree.SubjetCA15subjetfiltered_corr_AbsoluteScaleUp[n];
        self.corr_AbsoluteScaleDown = tree.SubjetCA15subjetfiltered_corr_AbsoluteScaleDown[n];
        self.corr_AbsoluteFlavMapUp = tree.SubjetCA15subjetfiltered_corr_AbsoluteFlavMapUp[n];
        self.corr_AbsoluteFlavMapDown = tree.SubjetCA15subjetfiltered_corr_AbsoluteFlavMapDown[n];
        self.corr_AbsoluteMPFBiasUp = tree.SubjetCA15subjetfiltered_corr_AbsoluteMPFBiasUp[n];
        self.corr_AbsoluteMPFBiasDown = tree.SubjetCA15subjetfiltered_corr_AbsoluteMPFBiasDown[n];
        self.corr_FragmentationUp = tree.SubjetCA15subjetfiltered_corr_FragmentationUp[n];
        self.corr_FragmentationDown = tree.SubjetCA15subjetfiltered_corr_FragmentationDown[n];
        self.corr_SinglePionECALUp = tree.SubjetCA15subjetfiltered_corr_SinglePionECALUp[n];
        self.corr_SinglePionECALDown = tree.SubjetCA15subjetfiltered_corr_SinglePionECALDown[n];
        self.corr_SinglePionHCALUp = tree.SubjetCA15subjetfiltered_corr_SinglePionHCALUp[n];
        self.corr_SinglePionHCALDown = tree.SubjetCA15subjetfiltered_corr_SinglePionHCALDown[n];
        self.corr_FlavorQCDUp = tree.SubjetCA15subjetfiltered_corr_FlavorQCDUp[n];
        self.corr_FlavorQCDDown = tree.SubjetCA15subjetfiltered_corr_FlavorQCDDown[n];
        self.corr_TimePtEtaUp = tree.SubjetCA15subjetfiltered_corr_TimePtEtaUp[n];
        self.corr_TimePtEtaDown = tree.SubjetCA15subjetfiltered_corr_TimePtEtaDown[n];
        self.corr_RelativeJEREC1Up = tree.SubjetCA15subjetfiltered_corr_RelativeJEREC1Up[n];
        self.corr_RelativeJEREC1Down = tree.SubjetCA15subjetfiltered_corr_RelativeJEREC1Down[n];
        self.corr_RelativeJEREC2Up = tree.SubjetCA15subjetfiltered_corr_RelativeJEREC2Up[n];
        self.corr_RelativeJEREC2Down = tree.SubjetCA15subjetfiltered_corr_RelativeJEREC2Down[n];
        self.corr_RelativeJERHFUp = tree.SubjetCA15subjetfiltered_corr_RelativeJERHFUp[n];
        self.corr_RelativeJERHFDown = tree.SubjetCA15subjetfiltered_corr_RelativeJERHFDown[n];
        self.corr_RelativePtBBUp = tree.SubjetCA15subjetfiltered_corr_RelativePtBBUp[n];
        self.corr_RelativePtBBDown = tree.SubjetCA15subjetfiltered_corr_RelativePtBBDown[n];
        self.corr_RelativePtEC1Up = tree.SubjetCA15subjetfiltered_corr_RelativePtEC1Up[n];
        self.corr_RelativePtEC1Down = tree.SubjetCA15subjetfiltered_corr_RelativePtEC1Down[n];
        self.corr_RelativePtEC2Up = tree.SubjetCA15subjetfiltered_corr_RelativePtEC2Up[n];
        self.corr_RelativePtEC2Down = tree.SubjetCA15subjetfiltered_corr_RelativePtEC2Down[n];
        self.corr_RelativePtHFUp = tree.SubjetCA15subjetfiltered_corr_RelativePtHFUp[n];
        self.corr_RelativePtHFDown = tree.SubjetCA15subjetfiltered_corr_RelativePtHFDown[n];
        self.corr_RelativeBalUp = tree.SubjetCA15subjetfiltered_corr_RelativeBalUp[n];
        self.corr_RelativeBalDown = tree.SubjetCA15subjetfiltered_corr_RelativeBalDown[n];
        self.corr_RelativeFSRUp = tree.SubjetCA15subjetfiltered_corr_RelativeFSRUp[n];
        self.corr_RelativeFSRDown = tree.SubjetCA15subjetfiltered_corr_RelativeFSRDown[n];
        self.corr_RelativeStatFSRUp = tree.SubjetCA15subjetfiltered_corr_RelativeStatFSRUp[n];
        self.corr_RelativeStatFSRDown = tree.SubjetCA15subjetfiltered_corr_RelativeStatFSRDown[n];
        self.corr_RelativeStatECUp = tree.SubjetCA15subjetfiltered_corr_RelativeStatECUp[n];
        self.corr_RelativeStatECDown = tree.SubjetCA15subjetfiltered_corr_RelativeStatECDown[n];
        self.corr_RelativeStatHFUp = tree.SubjetCA15subjetfiltered_corr_RelativeStatHFUp[n];
        self.corr_RelativeStatHFDown = tree.SubjetCA15subjetfiltered_corr_RelativeStatHFDown[n];
        self.corr_PileUpDataMCUp = tree.SubjetCA15subjetfiltered_corr_PileUpDataMCUp[n];
        self.corr_PileUpDataMCDown = tree.SubjetCA15subjetfiltered_corr_PileUpDataMCDown[n];
        self.corr_PileUpPtRefUp = tree.SubjetCA15subjetfiltered_corr_PileUpPtRefUp[n];
        self.corr_PileUpPtRefDown = tree.SubjetCA15subjetfiltered_corr_PileUpPtRefDown[n];
        self.corr_PileUpPtBBUp = tree.SubjetCA15subjetfiltered_corr_PileUpPtBBUp[n];
        self.corr_PileUpPtBBDown = tree.SubjetCA15subjetfiltered_corr_PileUpPtBBDown[n];
        self.corr_PileUpPtEC1Up = tree.SubjetCA15subjetfiltered_corr_PileUpPtEC1Up[n];
        self.corr_PileUpPtEC1Down = tree.SubjetCA15subjetfiltered_corr_PileUpPtEC1Down[n];
        self.corr_PileUpPtEC2Up = tree.SubjetCA15subjetfiltered_corr_PileUpPtEC2Up[n];
        self.corr_PileUpPtEC2Down = tree.SubjetCA15subjetfiltered_corr_PileUpPtEC2Down[n];
        self.corr_PileUpPtHFUp = tree.SubjetCA15subjetfiltered_corr_PileUpPtHFUp[n];
        self.corr_PileUpPtHFDown = tree.SubjetCA15subjetfiltered_corr_PileUpPtHFDown[n];
        self.corr_PileUpMuZeroUp = tree.SubjetCA15subjetfiltered_corr_PileUpMuZeroUp[n];
        self.corr_PileUpMuZeroDown = tree.SubjetCA15subjetfiltered_corr_PileUpMuZeroDown[n];
        self.corr_PileUpEnvelopeUp = tree.SubjetCA15subjetfiltered_corr_PileUpEnvelopeUp[n];
        self.corr_PileUpEnvelopeDown = tree.SubjetCA15subjetfiltered_corr_PileUpEnvelopeDown[n];
        self.corr_SubTotalPileUpUp = tree.SubjetCA15subjetfiltered_corr_SubTotalPileUpUp[n];
        self.corr_SubTotalPileUpDown = tree.SubjetCA15subjetfiltered_corr_SubTotalPileUpDown[n];
        self.corr_SubTotalRelativeUp = tree.SubjetCA15subjetfiltered_corr_SubTotalRelativeUp[n];
        self.corr_SubTotalRelativeDown = tree.SubjetCA15subjetfiltered_corr_SubTotalRelativeDown[n];
        self.corr_SubTotalPtUp = tree.SubjetCA15subjetfiltered_corr_SubTotalPtUp[n];
        self.corr_SubTotalPtDown = tree.SubjetCA15subjetfiltered_corr_SubTotalPtDown[n];
        self.corr_SubTotalScaleUp = tree.SubjetCA15subjetfiltered_corr_SubTotalScaleUp[n];
        self.corr_SubTotalScaleDown = tree.SubjetCA15subjetfiltered_corr_SubTotalScaleDown[n];
        self.corr_SubTotalAbsoluteUp = tree.SubjetCA15subjetfiltered_corr_SubTotalAbsoluteUp[n];
        self.corr_SubTotalAbsoluteDown = tree.SubjetCA15subjetfiltered_corr_SubTotalAbsoluteDown[n];
        self.corr_SubTotalMCUp = tree.SubjetCA15subjetfiltered_corr_SubTotalMCUp[n];
        self.corr_SubTotalMCDown = tree.SubjetCA15subjetfiltered_corr_SubTotalMCDown[n];
        self.corr_TotalUp = tree.SubjetCA15subjetfiltered_corr_TotalUp[n];
        self.corr_TotalDown = tree.SubjetCA15subjetfiltered_corr_TotalDown[n];
        self.corr_TotalNoFlavorUp = tree.SubjetCA15subjetfiltered_corr_TotalNoFlavorUp[n];
        self.corr_TotalNoFlavorDown = tree.SubjetCA15subjetfiltered_corr_TotalNoFlavorDown[n];
        self.corr_TotalNoTimeUp = tree.SubjetCA15subjetfiltered_corr_TotalNoTimeUp[n];
        self.corr_TotalNoTimeDown = tree.SubjetCA15subjetfiltered_corr_TotalNoTimeDown[n];
        self.corr_TotalNoFlavorNoTimeUp = tree.SubjetCA15subjetfiltered_corr_TotalNoFlavorNoTimeUp[n];
        self.corr_TotalNoFlavorNoTimeDown = tree.SubjetCA15subjetfiltered_corr_TotalNoFlavorNoTimeDown[n];
        self.corr_FlavorZJetUp = tree.SubjetCA15subjetfiltered_corr_FlavorZJetUp[n];
        self.corr_FlavorZJetDown = tree.SubjetCA15subjetfiltered_corr_FlavorZJetDown[n];
        self.corr_FlavorPhotonJetUp = tree.SubjetCA15subjetfiltered_corr_FlavorPhotonJetUp[n];
        self.corr_FlavorPhotonJetDown = tree.SubjetCA15subjetfiltered_corr_FlavorPhotonJetDown[n];
        self.corr_FlavorPureGluonUp = tree.SubjetCA15subjetfiltered_corr_FlavorPureGluonUp[n];
        self.corr_FlavorPureGluonDown = tree.SubjetCA15subjetfiltered_corr_FlavorPureGluonDown[n];
        self.corr_FlavorPureQuarkUp = tree.SubjetCA15subjetfiltered_corr_FlavorPureQuarkUp[n];
        self.corr_FlavorPureQuarkDown = tree.SubjetCA15subjetfiltered_corr_FlavorPureQuarkDown[n];
        self.corr_FlavorPureCharmUp = tree.SubjetCA15subjetfiltered_corr_FlavorPureCharmUp[n];
        self.corr_FlavorPureCharmDown = tree.SubjetCA15subjetfiltered_corr_FlavorPureCharmDown[n];
        self.corr_FlavorPureBottomUp = tree.SubjetCA15subjetfiltered_corr_FlavorPureBottomUp[n];
        self.corr_FlavorPureBottomDown = tree.SubjetCA15subjetfiltered_corr_FlavorPureBottomDown[n];
        self.corr_TimeRunBCDUp = tree.SubjetCA15subjetfiltered_corr_TimeRunBCDUp[n];
        self.corr_TimeRunBCDDown = tree.SubjetCA15subjetfiltered_corr_TimeRunBCDDown[n];
        self.corr_TimeRunEFUp = tree.SubjetCA15subjetfiltered_corr_TimeRunEFUp[n];
        self.corr_TimeRunEFDown = tree.SubjetCA15subjetfiltered_corr_TimeRunEFDown[n];
        self.corr_TimeRunGUp = tree.SubjetCA15subjetfiltered_corr_TimeRunGUp[n];
        self.corr_TimeRunGDown = tree.SubjetCA15subjetfiltered_corr_TimeRunGDown[n];
        self.corr_TimeRunHUp = tree.SubjetCA15subjetfiltered_corr_TimeRunHUp[n];
        self.corr_TimeRunHDown = tree.SubjetCA15subjetfiltered_corr_TimeRunHDown[n];
        self.corr_CorrelationGroupMPFInSituUp = tree.SubjetCA15subjetfiltered_corr_CorrelationGroupMPFInSituUp[n];
        self.corr_CorrelationGroupMPFInSituDown = tree.SubjetCA15subjetfiltered_corr_CorrelationGroupMPFInSituDown[n];
        self.corr_CorrelationGroupIntercalibrationUp = tree.SubjetCA15subjetfiltered_corr_CorrelationGroupIntercalibrationUp[n];
        self.corr_CorrelationGroupIntercalibrationDown = tree.SubjetCA15subjetfiltered_corr_CorrelationGroupIntercalibrationDown[n];
        self.corr_CorrelationGroupbJESUp = tree.SubjetCA15subjetfiltered_corr_CorrelationGroupbJESUp[n];
        self.corr_CorrelationGroupbJESDown = tree.SubjetCA15subjetfiltered_corr_CorrelationGroupbJESDown[n];
        self.corr_CorrelationGroupFlavorUp = tree.SubjetCA15subjetfiltered_corr_CorrelationGroupFlavorUp[n];
        self.corr_CorrelationGroupFlavorDown = tree.SubjetCA15subjetfiltered_corr_CorrelationGroupFlavorDown[n];
        self.corr_CorrelationGroupUncorrelatedUp = tree.SubjetCA15subjetfiltered_corr_CorrelationGroupUncorrelatedUp[n];
        self.corr_CorrelationGroupUncorrelatedDown = tree.SubjetCA15subjetfiltered_corr_CorrelationGroupUncorrelatedDown[n];
        pass
    @staticmethod
    def make_array(input):
        return [SubjetCA15subjetfiltered(input, i) for i in range(input.nSubjetCA15subjetfiltered)]
class LHE_weights_pdf_eigen:
    def __init__(self, tree, n):
        self.LHE_weights_pdf_eigen = tree.LHE_weights_pdf_eigen[n];
        pass
    @staticmethod
    def make_array(input):
        return [LHE_weights_pdf_eigen(input, i) for i in range(input.nLHE_weights_pdf_eigen)]
class vLeptons:
    def __init__(self, tree, n):
        self.charge = tree.vLeptons_charge[n];
        self.tightId = tree.vLeptons_tightId[n];
        self.eleCutIdCSA14_25ns_v1 = tree.vLeptons_eleCutIdCSA14_25ns_v1[n];
        self.eleCutIdCSA14_50ns_v1 = tree.vLeptons_eleCutIdCSA14_50ns_v1[n];
        self.eleCutIdSpring15_25ns_v1 = tree.vLeptons_eleCutIdSpring15_25ns_v1[n];
        self.mediumIdPOG_ICHEP2016 = tree.vLeptons_mediumIdPOG_ICHEP2016[n];
        self.dxy = tree.vLeptons_dxy[n];
        self.dz = tree.vLeptons_dz[n];
        self.edxy = tree.vLeptons_edxy[n];
        self.edz = tree.vLeptons_edz[n];
        self.ip3d = tree.vLeptons_ip3d[n];
        self.sip3d = tree.vLeptons_sip3d[n];
        self.convVeto = tree.vLeptons_convVeto[n];
        self.lostHits = tree.vLeptons_lostHits[n];
        self.relIso03 = tree.vLeptons_relIso03[n];
        self.relIso04 = tree.vLeptons_relIso04[n];
        self.miniRelIso = tree.vLeptons_miniRelIso[n];
        self.relIsoAn04 = tree.vLeptons_relIsoAn04[n];
        self.tightCharge = tree.vLeptons_tightCharge[n];
        self.mcMatchId = tree.vLeptons_mcMatchId[n];
        self.mcMatchAny = tree.vLeptons_mcMatchAny[n];
        self.mcMatchTau = tree.vLeptons_mcMatchTau[n];
        self.mcPt = tree.vLeptons_mcPt[n];
        self.mediumMuonId = tree.vLeptons_mediumMuonId[n];
        self.pdgId = tree.vLeptons_pdgId[n];
        self.pt = tree.vLeptons_pt[n];
        self.eta = tree.vLeptons_eta[n];
        self.phi = tree.vLeptons_phi[n];
        self.mass = tree.vLeptons_mass[n];
        self.looseIdSusy = tree.vLeptons_looseIdSusy[n];
        self.looseIdPOG = tree.vLeptons_looseIdPOG[n];
        self.chargedHadRelIso03 = tree.vLeptons_chargedHadRelIso03[n];
        self.chargedHadRelIso04 = tree.vLeptons_chargedHadRelIso04[n];
        self.eleSieie = tree.vLeptons_eleSieie[n];
        self.eleDEta = tree.vLeptons_eleDEta[n];
        self.eleDPhi = tree.vLeptons_eleDPhi[n];
        self.eleHoE = tree.vLeptons_eleHoE[n];
        self.eleMissingHits = tree.vLeptons_eleMissingHits[n];
        self.eleChi2 = tree.vLeptons_eleChi2[n];
        self.convVetoFull = tree.vLeptons_convVetoFull[n];
        self.eleMVArawSpring15Trig = tree.vLeptons_eleMVArawSpring15Trig[n];
        self.eleMVAIdSpring15Trig = tree.vLeptons_eleMVAIdSpring15Trig[n];
        self.eleMVArawSpring15NonTrig = tree.vLeptons_eleMVArawSpring15NonTrig[n];
        self.eleMVAIdSpring15NonTrig = tree.vLeptons_eleMVAIdSpring15NonTrig[n];
        self.eleMVArawSpring16GenPurp = tree.vLeptons_eleMVArawSpring16GenPurp[n];
        self.eleMVAIdSppring16GenPurp = tree.vLeptons_eleMVAIdSppring16GenPurp[n];
        self.nStations = tree.vLeptons_nStations[n];
        self.trkKink = tree.vLeptons_trkKink[n];
        self.segmentCompatibility = tree.vLeptons_segmentCompatibility[n];
        self.caloCompatibility = tree.vLeptons_caloCompatibility[n];
        self.globalTrackChi2 = tree.vLeptons_globalTrackChi2[n];
        self.nChamberHits = tree.vLeptons_nChamberHits[n];
        self.isPFMuon = tree.vLeptons_isPFMuon[n];
        self.isGlobalMuon = tree.vLeptons_isGlobalMuon[n];
        self.isTrackerMuon = tree.vLeptons_isTrackerMuon[n];
        self.pixelHits = tree.vLeptons_pixelHits[n];
        self.trackerLayers = tree.vLeptons_trackerLayers[n];
        self.pixelLayers = tree.vLeptons_pixelLayers[n];
        self.mvaTTH = tree.vLeptons_mvaTTH[n];
        self.jetOverlapIdx = tree.vLeptons_jetOverlapIdx[n];
        self.jetPtRatio = tree.vLeptons_jetPtRatio[n];
        self.jetBTagCSV = tree.vLeptons_jetBTagCSV[n];
        self.jetDR = tree.vLeptons_jetDR[n];
        self.mvaTTHjetPtRatio = tree.vLeptons_mvaTTHjetPtRatio[n];
        self.mvaTTHjetBTagCSV = tree.vLeptons_mvaTTHjetBTagCSV[n];
        self.mvaTTHjetDR = tree.vLeptons_mvaTTHjetDR[n];
        self.pfRelIso03 = tree.vLeptons_pfRelIso03[n];
        self.pfRelIso04 = tree.vLeptons_pfRelIso04[n];
        self.etaSc = tree.vLeptons_etaSc[n];
        self.eleExpMissingInnerHits = tree.vLeptons_eleExpMissingInnerHits[n];
        self.combIsoAreaCorr = tree.vLeptons_combIsoAreaCorr[n];
        self.eleooEmooP = tree.vLeptons_eleooEmooP[n];
        self.dr03TkSumPt = tree.vLeptons_dr03TkSumPt[n];
        self.eleEcalClusterIso = tree.vLeptons_eleEcalClusterIso[n];
        self.eleHcalClusterIso = tree.vLeptons_eleHcalClusterIso[n];
        self.miniIsoCharged = tree.vLeptons_miniIsoCharged[n];
        self.miniIsoNeutral = tree.vLeptons_miniIsoNeutral[n];
        self.mvaTTHjetPtRel = tree.vLeptons_mvaTTHjetPtRel[n];
        self.mvaTTHjetNDauChargedMVASel = tree.vLeptons_mvaTTHjetNDauChargedMVASel[n];
        self.uncalibratedPt = tree.vLeptons_uncalibratedPt[n];
        self.SF_IsoLoose = tree.vLeptons_SF_IsoLoose[n];
        self.SFerr_IsoLoose = tree.vLeptons_SFerr_IsoLoose[n];
        self.SF_IsoTight = tree.vLeptons_SF_IsoTight[n];
        self.SFerr_IsoTight = tree.vLeptons_SFerr_IsoTight[n];
        self.SF_IdCutLoose = tree.vLeptons_SF_IdCutLoose[n];
        self.SFerr_IdCutLoose = tree.vLeptons_SFerr_IdCutLoose[n];
        self.SF_IdCutTight = tree.vLeptons_SF_IdCutTight[n];
        self.SFerr_IdCutTight = tree.vLeptons_SFerr_IdCutTight[n];
        self.SF_IdMVALoose = tree.vLeptons_SF_IdMVALoose[n];
        self.SFerr_IdMVALoose = tree.vLeptons_SFerr_IdMVALoose[n];
        self.SF_IdMVATight = tree.vLeptons_SF_IdMVATight[n];
        self.SFerr_IdMVATight = tree.vLeptons_SFerr_IdMVATight[n];
        self.SF_HLT_RunD4p3 = tree.vLeptons_SF_HLT_RunD4p3[n];
        self.SFerr_HLT_RunD4p3 = tree.vLeptons_SFerr_HLT_RunD4p3[n];
        self.SF_HLT_RunD4p2 = tree.vLeptons_SF_HLT_RunD4p2[n];
        self.SFerr_HLT_RunD4p2 = tree.vLeptons_SFerr_HLT_RunD4p2[n];
        self.SF_HLT_RunC = tree.vLeptons_SF_HLT_RunC[n];
        self.SFerr_HLT_RunC = tree.vLeptons_SFerr_HLT_RunC[n];
        self.SF_trk_eta = tree.vLeptons_SF_trk_eta[n];
        self.SFerr_trk_eta = tree.vLeptons_SFerr_trk_eta[n];
        self.Eff_HLT_RunD4p3 = tree.vLeptons_Eff_HLT_RunD4p3[n];
        self.Efferr_HLT_RunD4p3 = tree.vLeptons_Efferr_HLT_RunD4p3[n];
        self.Eff_HLT_RunD4p2 = tree.vLeptons_Eff_HLT_RunD4p2[n];
        self.Efferr_HLT_RunD4p2 = tree.vLeptons_Efferr_HLT_RunD4p2[n];
        self.Eff_HLT_RunC = tree.vLeptons_Eff_HLT_RunC[n];
        self.Efferr_HLT_RunC = tree.vLeptons_Efferr_HLT_RunC[n];
        pass
    @staticmethod
    def make_array(input):
        return [vLeptons(input, i) for i in range(input.nvLeptons)]
class trgObjects_hltBTagCaloCSVp014DoubleWithMatching:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_hltBTagCaloCSVp014DoubleWithMatching_pt[n];
        self.eta = tree.trgObjects_hltBTagCaloCSVp014DoubleWithMatching_eta[n];
        self.phi = tree.trgObjects_hltBTagCaloCSVp014DoubleWithMatching_phi[n];
        self.mass = tree.trgObjects_hltBTagCaloCSVp014DoubleWithMatching_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltBTagCaloCSVp014DoubleWithMatching(input, i) for i in range(input.ntrgObjects_hltBTagCaloCSVp014DoubleWithMatching)]
class pileUpVertex_z:
    def __init__(self, tree, n):
        self.pileUpVertex_z = tree.pileUpVertex_z[n];
        pass
    @staticmethod
    def make_array(input):
        return [pileUpVertex_z(input, i) for i in range(input.npileUpVertex_z)]
class trgObjects_pfJets:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_pfJets_pt[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_pfJets(input, i) for i in range(input.ntrgObjects_pfJets)]
class trgObjects_pfMht:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_pfMht_pt[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_pfMht(input, i) for i in range(input.ntrgObjects_pfMht)]
class LHE_weights_scale:
    def __init__(self, tree, n):
        self.id = tree.LHE_weights_scale_id[n];
        self.wgt = tree.LHE_weights_scale_wgt[n];
        pass
    @staticmethod
    def make_array(input):
        return [LHE_weights_scale(input, i) for i in range(input.nLHE_weights_scale)]
class trgObjects_hltL1sQuadJetCIorTripleJetVBFIorHTT:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltL1sQuadJetCIorTripleJetVBFIorHTT(input, i) for i in range(input.ntrgObjects_hltL1sQuadJetCIorTripleJetVBFIorHTT)]
class FatjetCA15pruned:
    def __init__(self, tree, n):
        self.pt = tree.FatjetCA15pruned_pt[n];
        self.eta = tree.FatjetCA15pruned_eta[n];
        self.phi = tree.FatjetCA15pruned_phi[n];
        self.mass = tree.FatjetCA15pruned_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [FatjetCA15pruned(input, i) for i in range(input.nFatjetCA15pruned)]
class trgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5(input, i) for i in range(input.ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5)]
class trgObjects_caloMht:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_caloMht_pt[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_caloMht(input, i) for i in range(input.ntrgObjects_caloMht)]
class FatjetCA15softdropz2b1filt:
    def __init__(self, tree, n):
        self.pt = tree.FatjetCA15softdropz2b1filt_pt[n];
        self.eta = tree.FatjetCA15softdropz2b1filt_eta[n];
        self.phi = tree.FatjetCA15softdropz2b1filt_phi[n];
        self.mass = tree.FatjetCA15softdropz2b1filt_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [FatjetCA15softdropz2b1filt(input, i) for i in range(input.nFatjetCA15softdropz2b1filt)]
class trgObjects_hltDoublePFCentralJetLooseID90:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltDoublePFCentralJetLooseID90(input, i) for i in range(input.ntrgObjects_hltDoublePFCentralJetLooseID90)]
class GenJet:
    def __init__(self, tree, n):
        self.charge = tree.GenJet_charge[n];
        self.status = tree.GenJet_status[n];
        self.isPromptHard = tree.GenJet_isPromptHard[n];
        self.pdgId = tree.GenJet_pdgId[n];
        self.pt = tree.GenJet_pt[n];
        self.eta = tree.GenJet_eta[n];
        self.phi = tree.GenJet_phi[n];
        self.mass = tree.GenJet_mass[n];
        self.numBHadrons = tree.GenJet_numBHadrons[n];
        self.numCHadrons = tree.GenJet_numCHadrons[n];
        self.numBHadronsFromTop = tree.GenJet_numBHadronsFromTop[n];
        self.numCHadronsFromTop = tree.GenJet_numCHadronsFromTop[n];
        self.numBHadronsAfterTop = tree.GenJet_numBHadronsAfterTop[n];
        self.numCHadronsAfterTop = tree.GenJet_numCHadronsAfterTop[n];
        self.wNuPt = tree.GenJet_wNuPt[n];
        self.wNuEta = tree.GenJet_wNuEta[n];
        self.wNuPhi = tree.GenJet_wNuPhi[n];
        self.wNuM = tree.GenJet_wNuM[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenJet(input, i) for i in range(input.nGenJet)]
class GenVbosons:
    def __init__(self, tree, n):
        self.pdgId = tree.GenVbosons_pdgId[n];
        self.pt = tree.GenVbosons_pt[n];
        self.eta = tree.GenVbosons_eta[n];
        self.phi = tree.GenVbosons_phi[n];
        self.mass = tree.GenVbosons_mass[n];
        self.charge = tree.GenVbosons_charge[n];
        self.status = tree.GenVbosons_status[n];
        self.isPromptHard = tree.GenVbosons_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenVbosons(input, i) for i in range(input.nGenVbosons)]
class trgObjects_hltDoublePFJetsC100:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_hltDoublePFJetsC100_pt[n];
        self.eta = tree.trgObjects_hltDoublePFJetsC100_eta[n];
        self.phi = tree.trgObjects_hltDoublePFJetsC100_phi[n];
        self.mass = tree.trgObjects_hltDoublePFJetsC100_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltDoublePFJetsC100(input, i) for i in range(input.ntrgObjects_hltDoublePFJetsC100)]
class SubjetCA15pruned:
    def __init__(self, tree, n):
        self.pt = tree.SubjetCA15pruned_pt[n];
        self.eta = tree.SubjetCA15pruned_eta[n];
        self.phi = tree.SubjetCA15pruned_phi[n];
        self.mass = tree.SubjetCA15pruned_mass[n];
        self.btag = tree.SubjetCA15pruned_btag[n];
        self.jetID = tree.SubjetCA15pruned_jetID[n];
        self.fromFJ = tree.SubjetCA15pruned_fromFJ[n];
        pass
    @staticmethod
    def make_array(input):
        return [SubjetCA15pruned(input, i) for i in range(input.nSubjetCA15pruned)]
class trgObjects_caloMet:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_caloMet_pt[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_caloMet(input, i) for i in range(input.ntrgObjects_caloMet)]
class FatjetCA15ungroomed:
    def __init__(self, tree, n):
        self.pt = tree.FatjetCA15ungroomed_pt[n];
        self.eta = tree.FatjetCA15ungroomed_eta[n];
        self.phi = tree.FatjetCA15ungroomed_phi[n];
        self.mass = tree.FatjetCA15ungroomed_mass[n];
        self.tau1 = tree.FatjetCA15ungroomed_tau1[n];
        self.tau2 = tree.FatjetCA15ungroomed_tau2[n];
        self.tau3 = tree.FatjetCA15ungroomed_tau3[n];
        self.bbtag = tree.FatjetCA15ungroomed_bbtag[n];
        pass
    @staticmethod
    def make_array(input):
        return [FatjetCA15ungroomed(input, i) for i in range(input.nFatjetCA15ungroomed)]
class trgObjects_pfMet:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_pfMet_pt[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_pfMet(input, i) for i in range(input.ntrgObjects_pfMet)]
class trgObjects_hltBTagCaloCSVp067Single:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltBTagCaloCSVp067Single(input, i) for i in range(input.ntrgObjects_hltBTagCaloCSVp067Single)]
class dRaddJetsdR08:
    def __init__(self, tree, n):
        self.dRaddJetsdR08 = tree.dRaddJetsdR08[n];
        pass
    @staticmethod
    def make_array(input):
        return [dRaddJetsdR08(input, i) for i in range(input.ndRaddJetsdR08)]
class l1Jets:
    def __init__(self, tree, n):
        self.pt = tree.l1Jets_pt[n];
        self.eta = tree.l1Jets_eta[n];
        self.phi = tree.l1Jets_phi[n];
        self.qual = tree.l1Jets_qual[n];
        self.iso = tree.l1Jets_iso[n];
        pass
    @staticmethod
    def make_array(input):
        return [l1Jets(input, i) for i in range(input.nl1Jets)]
class SubjetCA15softdropz2b1filt:
    def __init__(self, tree, n):
        self.pt = tree.SubjetCA15softdropz2b1filt_pt[n];
        self.eta = tree.SubjetCA15softdropz2b1filt_eta[n];
        self.phi = tree.SubjetCA15softdropz2b1filt_phi[n];
        self.mass = tree.SubjetCA15softdropz2b1filt_mass[n];
        self.btag = tree.SubjetCA15softdropz2b1filt_btag[n];
        self.jetID = tree.SubjetCA15softdropz2b1filt_jetID[n];
        self.fromFJ = tree.SubjetCA15softdropz2b1filt_fromFJ[n];
        pass
    @staticmethod
    def make_array(input):
        return [SubjetCA15softdropz2b1filt(input, i) for i in range(input.nSubjetCA15softdropz2b1filt)]
class GenBQuarkFromH:
    def __init__(self, tree, n):
        self.pdgId = tree.GenBQuarkFromH_pdgId[n];
        self.pt = tree.GenBQuarkFromH_pt[n];
        self.eta = tree.GenBQuarkFromH_eta[n];
        self.phi = tree.GenBQuarkFromH_phi[n];
        self.mass = tree.GenBQuarkFromH_mass[n];
        self.charge = tree.GenBQuarkFromH_charge[n];
        self.status = tree.GenBQuarkFromH_status[n];
        self.isPromptHard = tree.GenBQuarkFromH_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenBQuarkFromH(input, i) for i in range(input.nGenBQuarkFromH)]
class trgObjects_hltDoubleJet65:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltDoubleJet65(input, i) for i in range(input.ntrgObjects_hltDoubleJet65)]
class FatjetCA15trimmed:
    def __init__(self, tree, n):
        self.pt = tree.FatjetCA15trimmed_pt[n];
        self.eta = tree.FatjetCA15trimmed_eta[n];
        self.phi = tree.FatjetCA15trimmed_phi[n];
        self.mass = tree.FatjetCA15trimmed_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [FatjetCA15trimmed(input, i) for i in range(input.nFatjetCA15trimmed)]
class SubjetCA15softdropfilt:
    def __init__(self, tree, n):
        self.pt = tree.SubjetCA15softdropfilt_pt[n];
        self.eta = tree.SubjetCA15softdropfilt_eta[n];
        self.phi = tree.SubjetCA15softdropfilt_phi[n];
        self.mass = tree.SubjetCA15softdropfilt_mass[n];
        self.btag = tree.SubjetCA15softdropfilt_btag[n];
        self.jetID = tree.SubjetCA15softdropfilt_jetID[n];
        self.fromFJ = tree.SubjetCA15softdropfilt_fromFJ[n];
        pass
    @staticmethod
    def make_array(input):
        return [SubjetCA15softdropfilt(input, i) for i in range(input.nSubjetCA15softdropfilt)]
class trgObjects_hltBTagCaloCSVp026DoubleWithMatching:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_hltBTagCaloCSVp026DoubleWithMatching_pt[n];
        self.eta = tree.trgObjects_hltBTagCaloCSVp026DoubleWithMatching_eta[n];
        self.phi = tree.trgObjects_hltBTagCaloCSVp026DoubleWithMatching_phi[n];
        self.mass = tree.trgObjects_hltBTagCaloCSVp026DoubleWithMatching_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltBTagCaloCSVp026DoubleWithMatching(input, i) for i in range(input.ntrgObjects_hltBTagCaloCSVp026DoubleWithMatching)]
class aLeptons:
    def __init__(self, tree, n):
        self.charge = tree.aLeptons_charge[n];
        self.tightId = tree.aLeptons_tightId[n];
        self.eleCutIdCSA14_25ns_v1 = tree.aLeptons_eleCutIdCSA14_25ns_v1[n];
        self.eleCutIdCSA14_50ns_v1 = tree.aLeptons_eleCutIdCSA14_50ns_v1[n];
        self.eleCutIdSpring15_25ns_v1 = tree.aLeptons_eleCutIdSpring15_25ns_v1[n];
        self.mediumIdPOG_ICHEP2016 = tree.aLeptons_mediumIdPOG_ICHEP2016[n];
        self.dxy = tree.aLeptons_dxy[n];
        self.dz = tree.aLeptons_dz[n];
        self.edxy = tree.aLeptons_edxy[n];
        self.edz = tree.aLeptons_edz[n];
        self.ip3d = tree.aLeptons_ip3d[n];
        self.sip3d = tree.aLeptons_sip3d[n];
        self.convVeto = tree.aLeptons_convVeto[n];
        self.lostHits = tree.aLeptons_lostHits[n];
        self.relIso03 = tree.aLeptons_relIso03[n];
        self.relIso04 = tree.aLeptons_relIso04[n];
        self.miniRelIso = tree.aLeptons_miniRelIso[n];
        self.relIsoAn04 = tree.aLeptons_relIsoAn04[n];
        self.tightCharge = tree.aLeptons_tightCharge[n];
        self.mcMatchId = tree.aLeptons_mcMatchId[n];
        self.mcMatchAny = tree.aLeptons_mcMatchAny[n];
        self.mcMatchTau = tree.aLeptons_mcMatchTau[n];
        self.mcPt = tree.aLeptons_mcPt[n];
        self.mediumMuonId = tree.aLeptons_mediumMuonId[n];
        self.pdgId = tree.aLeptons_pdgId[n];
        self.pt = tree.aLeptons_pt[n];
        self.eta = tree.aLeptons_eta[n];
        self.phi = tree.aLeptons_phi[n];
        self.mass = tree.aLeptons_mass[n];
        self.looseIdSusy = tree.aLeptons_looseIdSusy[n];
        self.looseIdPOG = tree.aLeptons_looseIdPOG[n];
        self.chargedHadRelIso03 = tree.aLeptons_chargedHadRelIso03[n];
        self.chargedHadRelIso04 = tree.aLeptons_chargedHadRelIso04[n];
        self.eleSieie = tree.aLeptons_eleSieie[n];
        self.eleDEta = tree.aLeptons_eleDEta[n];
        self.eleDPhi = tree.aLeptons_eleDPhi[n];
        self.eleHoE = tree.aLeptons_eleHoE[n];
        self.eleMissingHits = tree.aLeptons_eleMissingHits[n];
        self.eleChi2 = tree.aLeptons_eleChi2[n];
        self.convVetoFull = tree.aLeptons_convVetoFull[n];
        self.eleMVArawSpring15Trig = tree.aLeptons_eleMVArawSpring15Trig[n];
        self.eleMVAIdSpring15Trig = tree.aLeptons_eleMVAIdSpring15Trig[n];
        self.eleMVArawSpring15NonTrig = tree.aLeptons_eleMVArawSpring15NonTrig[n];
        self.eleMVAIdSpring15NonTrig = tree.aLeptons_eleMVAIdSpring15NonTrig[n];
        self.eleMVArawSpring16GenPurp = tree.aLeptons_eleMVArawSpring16GenPurp[n];
        self.eleMVAIdSppring16GenPurp = tree.aLeptons_eleMVAIdSppring16GenPurp[n];
        self.nStations = tree.aLeptons_nStations[n];
        self.trkKink = tree.aLeptons_trkKink[n];
        self.segmentCompatibility = tree.aLeptons_segmentCompatibility[n];
        self.caloCompatibility = tree.aLeptons_caloCompatibility[n];
        self.globalTrackChi2 = tree.aLeptons_globalTrackChi2[n];
        self.nChamberHits = tree.aLeptons_nChamberHits[n];
        self.isPFMuon = tree.aLeptons_isPFMuon[n];
        self.isGlobalMuon = tree.aLeptons_isGlobalMuon[n];
        self.isTrackerMuon = tree.aLeptons_isTrackerMuon[n];
        self.pixelHits = tree.aLeptons_pixelHits[n];
        self.trackerLayers = tree.aLeptons_trackerLayers[n];
        self.pixelLayers = tree.aLeptons_pixelLayers[n];
        self.mvaTTH = tree.aLeptons_mvaTTH[n];
        self.jetOverlapIdx = tree.aLeptons_jetOverlapIdx[n];
        self.jetPtRatio = tree.aLeptons_jetPtRatio[n];
        self.jetBTagCSV = tree.aLeptons_jetBTagCSV[n];
        self.jetDR = tree.aLeptons_jetDR[n];
        self.mvaTTHjetPtRatio = tree.aLeptons_mvaTTHjetPtRatio[n];
        self.mvaTTHjetBTagCSV = tree.aLeptons_mvaTTHjetBTagCSV[n];
        self.mvaTTHjetDR = tree.aLeptons_mvaTTHjetDR[n];
        self.pfRelIso03 = tree.aLeptons_pfRelIso03[n];
        self.pfRelIso04 = tree.aLeptons_pfRelIso04[n];
        self.etaSc = tree.aLeptons_etaSc[n];
        self.eleExpMissingInnerHits = tree.aLeptons_eleExpMissingInnerHits[n];
        self.combIsoAreaCorr = tree.aLeptons_combIsoAreaCorr[n];
        self.eleooEmooP = tree.aLeptons_eleooEmooP[n];
        self.dr03TkSumPt = tree.aLeptons_dr03TkSumPt[n];
        self.eleEcalClusterIso = tree.aLeptons_eleEcalClusterIso[n];
        self.eleHcalClusterIso = tree.aLeptons_eleHcalClusterIso[n];
        self.miniIsoCharged = tree.aLeptons_miniIsoCharged[n];
        self.miniIsoNeutral = tree.aLeptons_miniIsoNeutral[n];
        self.mvaTTHjetPtRel = tree.aLeptons_mvaTTHjetPtRel[n];
        self.mvaTTHjetNDauChargedMVASel = tree.aLeptons_mvaTTHjetNDauChargedMVASel[n];
        self.uncalibratedPt = tree.aLeptons_uncalibratedPt[n];
        self.SF_IsoLoose = tree.aLeptons_SF_IsoLoose[n];
        self.SFerr_IsoLoose = tree.aLeptons_SFerr_IsoLoose[n];
        self.SF_IsoTight = tree.aLeptons_SF_IsoTight[n];
        self.SFerr_IsoTight = tree.aLeptons_SFerr_IsoTight[n];
        self.SF_IdCutLoose = tree.aLeptons_SF_IdCutLoose[n];
        self.SFerr_IdCutLoose = tree.aLeptons_SFerr_IdCutLoose[n];
        self.SF_IdCutTight = tree.aLeptons_SF_IdCutTight[n];
        self.SFerr_IdCutTight = tree.aLeptons_SFerr_IdCutTight[n];
        self.SF_IdMVALoose = tree.aLeptons_SF_IdMVALoose[n];
        self.SFerr_IdMVALoose = tree.aLeptons_SFerr_IdMVALoose[n];
        self.SF_IdMVATight = tree.aLeptons_SF_IdMVATight[n];
        self.SFerr_IdMVATight = tree.aLeptons_SFerr_IdMVATight[n];
        self.SF_HLT_RunD4p3 = tree.aLeptons_SF_HLT_RunD4p3[n];
        self.SFerr_HLT_RunD4p3 = tree.aLeptons_SFerr_HLT_RunD4p3[n];
        self.SF_HLT_RunD4p2 = tree.aLeptons_SF_HLT_RunD4p2[n];
        self.SFerr_HLT_RunD4p2 = tree.aLeptons_SFerr_HLT_RunD4p2[n];
        self.SF_HLT_RunC = tree.aLeptons_SF_HLT_RunC[n];
        self.SFerr_HLT_RunC = tree.aLeptons_SFerr_HLT_RunC[n];
        self.SF_trk_eta = tree.aLeptons_SF_trk_eta[n];
        self.SFerr_trk_eta = tree.aLeptons_SFerr_trk_eta[n];
        self.Eff_HLT_RunD4p3 = tree.aLeptons_Eff_HLT_RunD4p3[n];
        self.Efferr_HLT_RunD4p3 = tree.aLeptons_Efferr_HLT_RunD4p3[n];
        self.Eff_HLT_RunD4p2 = tree.aLeptons_Eff_HLT_RunD4p2[n];
        self.Efferr_HLT_RunD4p2 = tree.aLeptons_Efferr_HLT_RunD4p2[n];
        self.Eff_HLT_RunC = tree.aLeptons_Eff_HLT_RunC[n];
        self.Efferr_HLT_RunC = tree.aLeptons_Efferr_HLT_RunC[n];
        pass
    @staticmethod
    def make_array(input):
        return [aLeptons(input, i) for i in range(input.naLeptons)]
class trgObjects_hltPFQuadJetLooseID15:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltPFQuadJetLooseID15(input, i) for i in range(input.ntrgObjects_hltPFQuadJetLooseID15)]
class trgObjects_hltQuadPFCentralJetLooseID45:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltQuadPFCentralJetLooseID45(input, i) for i in range(input.ntrgObjects_hltQuadPFCentralJetLooseID45)]
class GenHiggsSisters:
    def __init__(self, tree, n):
        self.pdgId = tree.GenHiggsSisters_pdgId[n];
        self.pt = tree.GenHiggsSisters_pt[n];
        self.eta = tree.GenHiggsSisters_eta[n];
        self.phi = tree.GenHiggsSisters_phi[n];
        self.mass = tree.GenHiggsSisters_mass[n];
        self.charge = tree.GenHiggsSisters_charge[n];
        self.status = tree.GenHiggsSisters_status[n];
        self.isPromptHard = tree.GenHiggsSisters_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenHiggsSisters(input, i) for i in range(input.nGenHiggsSisters)]
class trgObjects_pfHt:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_pfHt_pt[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_pfHt(input, i) for i in range(input.ntrgObjects_pfHt)]
class trgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2(input, i) for i in range(input.ntrgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2)]
class hjidxaddJetsdR08:
    def __init__(self, tree, n):
        self.hjidxaddJetsdR08 = tree.hjidxaddJetsdR08[n];
        pass
    @staticmethod
    def make_array(input):
        return [hjidxaddJetsdR08(input, i) for i in range(input.nhjidxaddJetsdR08)]
class FatjetCA15softdropfilt:
    def __init__(self, tree, n):
        self.pt = tree.FatjetCA15softdropfilt_pt[n];
        self.eta = tree.FatjetCA15softdropfilt_eta[n];
        self.phi = tree.FatjetCA15softdropfilt_phi[n];
        self.mass = tree.FatjetCA15softdropfilt_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [FatjetCA15softdropfilt(input, i) for i in range(input.nFatjetCA15softdropfilt)]
class l1Muons:
    def __init__(self, tree, n):
        self.pt = tree.l1Muons_pt[n];
        self.eta = tree.l1Muons_eta[n];
        self.phi = tree.l1Muons_phi[n];
        self.qual = tree.l1Muons_qual[n];
        self.iso = tree.l1Muons_iso[n];
        pass
    @staticmethod
    def make_array(input):
        return [l1Muons(input, i) for i in range(input.nl1Muons)]
class trgObjects_hltMHTNoPU90:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltMHTNoPU90(input, i) for i in range(input.ntrgObjects_hltMHTNoPU90)]
class FatjetAK08ungroomed:
    def __init__(self, tree, n):
        self.pt = tree.FatjetAK08ungroomed_pt[n];
        self.eta = tree.FatjetAK08ungroomed_eta[n];
        self.phi = tree.FatjetAK08ungroomed_phi[n];
        self.mass = tree.FatjetAK08ungroomed_mass[n];
        self.tau1 = tree.FatjetAK08ungroomed_tau1[n];
        self.tau2 = tree.FatjetAK08ungroomed_tau2[n];
        self.tau3 = tree.FatjetAK08ungroomed_tau3[n];
        self.msoftdrop = tree.FatjetAK08ungroomed_msoftdrop[n];
        self.mpruned = tree.FatjetAK08ungroomed_mpruned[n];
        self.mprunedcorr = tree.FatjetAK08ungroomed_mprunedcorr[n];
        self.JEC_L2L3 = tree.FatjetAK08ungroomed_JEC_L2L3[n];
        self.JEC_L1L2L3 = tree.FatjetAK08ungroomed_JEC_L1L2L3[n];
        self.JEC_L2L3Unc = tree.FatjetAK08ungroomed_JEC_L2L3Unc[n];
        self.JEC_L1L2L3Unc = tree.FatjetAK08ungroomed_JEC_L1L2L3Unc[n];
        self.bbtag = tree.FatjetAK08ungroomed_bbtag[n];
        self.id_Tight = tree.FatjetAK08ungroomed_id_Tight[n];
        self.numberOfDaughters = tree.FatjetAK08ungroomed_numberOfDaughters[n];
        self.neutralEmEnergyFraction = tree.FatjetAK08ungroomed_neutralEmEnergyFraction[n];
        self.neutralHadronEnergyFraction = tree.FatjetAK08ungroomed_neutralHadronEnergyFraction[n];
        self.muonEnergyFraction = tree.FatjetAK08ungroomed_muonEnergyFraction[n];
        self.chargedEmEnergyFraction = tree.FatjetAK08ungroomed_chargedEmEnergyFraction[n];
        self.chargedHadronEnergyFraction = tree.FatjetAK08ungroomed_chargedHadronEnergyFraction[n];
        self.chargedMultiplicity = tree.FatjetAK08ungroomed_chargedMultiplicity[n];
        self.electronMultiplicity = tree.FatjetAK08ungroomed_electronMultiplicity[n];
        self.muonMultiplicity = tree.FatjetAK08ungroomed_muonMultiplicity[n];
        self.Flavour = tree.FatjetAK08ungroomed_Flavour[n];
        self.BhadronFlavour = tree.FatjetAK08ungroomed_BhadronFlavour[n];
        self.ChadronFlavour = tree.FatjetAK08ungroomed_ChadronFlavour[n];
        self.GenPt = tree.FatjetAK08ungroomed_GenPt[n];
        self.puppi_pt = tree.FatjetAK08ungroomed_puppi_pt[n];
        self.puppi_eta = tree.FatjetAK08ungroomed_puppi_eta[n];
        self.puppi_phi = tree.FatjetAK08ungroomed_puppi_phi[n];
        self.puppi_mass = tree.FatjetAK08ungroomed_puppi_mass[n];
        self.puppi_tau1 = tree.FatjetAK08ungroomed_puppi_tau1[n];
        self.puppi_tau2 = tree.FatjetAK08ungroomed_puppi_tau2[n];
        self.puppi_msoftdrop = tree.FatjetAK08ungroomed_puppi_msoftdrop[n];
        self.puppi_msoftdrop_corrL2L3 = tree.FatjetAK08ungroomed_puppi_msoftdrop_corrL2L3[n];
        self.puppi_msoftdrop_raw = tree.FatjetAK08ungroomed_puppi_msoftdrop_raw[n];
        self.PFLepton_ptrel = tree.FatjetAK08ungroomed_PFLepton_ptrel[n];
        self.PFLepton_IP2D = tree.FatjetAK08ungroomed_PFLepton_IP2D[n];
        self.nSL = tree.FatjetAK08ungroomed_nSL[n];
        self.nVtx = tree.FatjetAK08ungroomed_nVtx[n];
        self.VtxMass_1 = tree.FatjetAK08ungroomed_VtxMass_1[n];
        self.VtxMass_2 = tree.FatjetAK08ungroomed_VtxMass_2[n];
        pass
    @staticmethod
    def make_array(input):
        return [FatjetAK08ungroomed(input, i) for i in range(input.nFatjetAK08ungroomed)]
class GenWZQuark:
    def __init__(self, tree, n):
        self.pdgId = tree.GenWZQuark_pdgId[n];
        self.pt = tree.GenWZQuark_pt[n];
        self.eta = tree.GenWZQuark_eta[n];
        self.phi = tree.GenWZQuark_phi[n];
        self.mass = tree.GenWZQuark_mass[n];
        self.charge = tree.GenWZQuark_charge[n];
        self.status = tree.GenWZQuark_status[n];
        self.isPromptHard = tree.GenWZQuark_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenWZQuark(input, i) for i in range(input.nGenWZQuark)]
class trgObjects_hltPFMHTTightID90:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltPFMHTTightID90(input, i) for i in range(input.ntrgObjects_hltPFMHTTightID90)]
class trgObjects_hltQuadCentralJet45:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltQuadCentralJet45(input, i) for i in range(input.ntrgObjects_hltQuadCentralJet45)]
class trgObjects_hltBTagCaloCSVp022Single:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltBTagCaloCSVp022Single(input, i) for i in range(input.ntrgObjects_hltBTagCaloCSVp022Single)]
class selLeptons:
    def __init__(self, tree, n):
        self.charge = tree.selLeptons_charge[n];
        self.tightId = tree.selLeptons_tightId[n];
        self.eleCutIdCSA14_25ns_v1 = tree.selLeptons_eleCutIdCSA14_25ns_v1[n];
        self.eleCutIdCSA14_50ns_v1 = tree.selLeptons_eleCutIdCSA14_50ns_v1[n];
        self.eleCutIdSpring15_25ns_v1 = tree.selLeptons_eleCutIdSpring15_25ns_v1[n];
        self.mediumIdPOG_ICHEP2016 = tree.selLeptons_mediumIdPOG_ICHEP2016[n];
        self.dxy = tree.selLeptons_dxy[n];
        self.dz = tree.selLeptons_dz[n];
        self.edxy = tree.selLeptons_edxy[n];
        self.edz = tree.selLeptons_edz[n];
        self.ip3d = tree.selLeptons_ip3d[n];
        self.sip3d = tree.selLeptons_sip3d[n];
        self.convVeto = tree.selLeptons_convVeto[n];
        self.lostHits = tree.selLeptons_lostHits[n];
        self.relIso03 = tree.selLeptons_relIso03[n];
        self.relIso04 = tree.selLeptons_relIso04[n];
        self.miniRelIso = tree.selLeptons_miniRelIso[n];
        self.relIsoAn04 = tree.selLeptons_relIsoAn04[n];
        self.tightCharge = tree.selLeptons_tightCharge[n];
        self.mcMatchId = tree.selLeptons_mcMatchId[n];
        self.mcMatchAny = tree.selLeptons_mcMatchAny[n];
        self.mcMatchTau = tree.selLeptons_mcMatchTau[n];
        self.mcPt = tree.selLeptons_mcPt[n];
        self.mediumMuonId = tree.selLeptons_mediumMuonId[n];
        self.pdgId = tree.selLeptons_pdgId[n];
        self.pt = tree.selLeptons_pt[n];
        self.eta = tree.selLeptons_eta[n];
        self.phi = tree.selLeptons_phi[n];
        self.mass = tree.selLeptons_mass[n];
        self.looseIdSusy = tree.selLeptons_looseIdSusy[n];
        self.looseIdPOG = tree.selLeptons_looseIdPOG[n];
        self.chargedHadRelIso03 = tree.selLeptons_chargedHadRelIso03[n];
        self.chargedHadRelIso04 = tree.selLeptons_chargedHadRelIso04[n];
        self.eleSieie = tree.selLeptons_eleSieie[n];
        self.eleDEta = tree.selLeptons_eleDEta[n];
        self.eleDPhi = tree.selLeptons_eleDPhi[n];
        self.eleHoE = tree.selLeptons_eleHoE[n];
        self.eleMissingHits = tree.selLeptons_eleMissingHits[n];
        self.eleChi2 = tree.selLeptons_eleChi2[n];
        self.convVetoFull = tree.selLeptons_convVetoFull[n];
        self.eleMVArawSpring15Trig = tree.selLeptons_eleMVArawSpring15Trig[n];
        self.eleMVAIdSpring15Trig = tree.selLeptons_eleMVAIdSpring15Trig[n];
        self.eleMVArawSpring15NonTrig = tree.selLeptons_eleMVArawSpring15NonTrig[n];
        self.eleMVAIdSpring15NonTrig = tree.selLeptons_eleMVAIdSpring15NonTrig[n];
        self.eleMVArawSpring16GenPurp = tree.selLeptons_eleMVArawSpring16GenPurp[n];
        self.eleMVAIdSppring16GenPurp = tree.selLeptons_eleMVAIdSppring16GenPurp[n];
        self.nStations = tree.selLeptons_nStations[n];
        self.trkKink = tree.selLeptons_trkKink[n];
        self.segmentCompatibility = tree.selLeptons_segmentCompatibility[n];
        self.caloCompatibility = tree.selLeptons_caloCompatibility[n];
        self.globalTrackChi2 = tree.selLeptons_globalTrackChi2[n];
        self.nChamberHits = tree.selLeptons_nChamberHits[n];
        self.isPFMuon = tree.selLeptons_isPFMuon[n];
        self.isGlobalMuon = tree.selLeptons_isGlobalMuon[n];
        self.isTrackerMuon = tree.selLeptons_isTrackerMuon[n];
        self.pixelHits = tree.selLeptons_pixelHits[n];
        self.trackerLayers = tree.selLeptons_trackerLayers[n];
        self.pixelLayers = tree.selLeptons_pixelLayers[n];
        self.mvaTTH = tree.selLeptons_mvaTTH[n];
        self.jetOverlapIdx = tree.selLeptons_jetOverlapIdx[n];
        self.jetPtRatio = tree.selLeptons_jetPtRatio[n];
        self.jetBTagCSV = tree.selLeptons_jetBTagCSV[n];
        self.jetDR = tree.selLeptons_jetDR[n];
        self.mvaTTHjetPtRatio = tree.selLeptons_mvaTTHjetPtRatio[n];
        self.mvaTTHjetBTagCSV = tree.selLeptons_mvaTTHjetBTagCSV[n];
        self.mvaTTHjetDR = tree.selLeptons_mvaTTHjetDR[n];
        self.pfRelIso03 = tree.selLeptons_pfRelIso03[n];
        self.pfRelIso04 = tree.selLeptons_pfRelIso04[n];
        self.etaSc = tree.selLeptons_etaSc[n];
        self.eleExpMissingInnerHits = tree.selLeptons_eleExpMissingInnerHits[n];
        self.combIsoAreaCorr = tree.selLeptons_combIsoAreaCorr[n];
        self.eleooEmooP = tree.selLeptons_eleooEmooP[n];
        self.dr03TkSumPt = tree.selLeptons_dr03TkSumPt[n];
        self.eleEcalClusterIso = tree.selLeptons_eleEcalClusterIso[n];
        self.eleHcalClusterIso = tree.selLeptons_eleHcalClusterIso[n];
        self.miniIsoCharged = tree.selLeptons_miniIsoCharged[n];
        self.miniIsoNeutral = tree.selLeptons_miniIsoNeutral[n];
        self.mvaTTHjetPtRel = tree.selLeptons_mvaTTHjetPtRel[n];
        self.mvaTTHjetNDauChargedMVASel = tree.selLeptons_mvaTTHjetNDauChargedMVASel[n];
        self.uncalibratedPt = tree.selLeptons_uncalibratedPt[n];
        self.SF_IsoLoose = tree.selLeptons_SF_IsoLoose[n];
        self.SFerr_IsoLoose = tree.selLeptons_SFerr_IsoLoose[n];
        self.SF_IsoTight = tree.selLeptons_SF_IsoTight[n];
        self.SFerr_IsoTight = tree.selLeptons_SFerr_IsoTight[n];
        self.SF_IdCutLoose = tree.selLeptons_SF_IdCutLoose[n];
        self.SFerr_IdCutLoose = tree.selLeptons_SFerr_IdCutLoose[n];
        self.SF_IdCutTight = tree.selLeptons_SF_IdCutTight[n];
        self.SFerr_IdCutTight = tree.selLeptons_SFerr_IdCutTight[n];
        self.SF_IdMVALoose = tree.selLeptons_SF_IdMVALoose[n];
        self.SFerr_IdMVALoose = tree.selLeptons_SFerr_IdMVALoose[n];
        self.SF_IdMVATight = tree.selLeptons_SF_IdMVATight[n];
        self.SFerr_IdMVATight = tree.selLeptons_SFerr_IdMVATight[n];
        self.SF_HLT_RunD4p3 = tree.selLeptons_SF_HLT_RunD4p3[n];
        self.SFerr_HLT_RunD4p3 = tree.selLeptons_SFerr_HLT_RunD4p3[n];
        self.SF_HLT_RunD4p2 = tree.selLeptons_SF_HLT_RunD4p2[n];
        self.SFerr_HLT_RunD4p2 = tree.selLeptons_SFerr_HLT_RunD4p2[n];
        self.SF_HLT_RunC = tree.selLeptons_SF_HLT_RunC[n];
        self.SFerr_HLT_RunC = tree.selLeptons_SFerr_HLT_RunC[n];
        self.SF_trk_eta = tree.selLeptons_SF_trk_eta[n];
        self.SFerr_trk_eta = tree.selLeptons_SFerr_trk_eta[n];
        self.Eff_HLT_RunD4p3 = tree.selLeptons_Eff_HLT_RunD4p3[n];
        self.Efferr_HLT_RunD4p3 = tree.selLeptons_Efferr_HLT_RunD4p3[n];
        self.Eff_HLT_RunD4p2 = tree.selLeptons_Eff_HLT_RunD4p2[n];
        self.Efferr_HLT_RunD4p2 = tree.selLeptons_Efferr_HLT_RunD4p2[n];
        self.Eff_HLT_RunC = tree.selLeptons_Eff_HLT_RunC[n];
        self.Efferr_HLT_RunC = tree.selLeptons_Efferr_HLT_RunC[n];
        pass
    @staticmethod
    def make_array(input):
        return [selLeptons(input, i) for i in range(input.nselLeptons)]
class trgObjects_hltPFMET90:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltPFMET90(input, i) for i in range(input.ntrgObjects_hltPFMET90)]
class trgObjects_hltQuadJet15:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltQuadJet15(input, i) for i in range(input.ntrgObjects_hltQuadJet15)]
class TauGood:
    def __init__(self, tree, n):
        self.charge = tree.TauGood_charge[n];
        self.decayMode = tree.TauGood_decayMode[n];
        self.idDecayMode = tree.TauGood_idDecayMode[n];
        self.idDecayModeNewDMs = tree.TauGood_idDecayModeNewDMs[n];
        self.dxy = tree.TauGood_dxy[n];
        self.dz = tree.TauGood_dz[n];
        self.idMVArun2 = tree.TauGood_idMVArun2[n];
        self.rawMVArun2 = tree.TauGood_rawMVArun2[n];
        self.idMVArun2dR03 = tree.TauGood_idMVArun2dR03[n];
        self.rawMVArun2dR03 = tree.TauGood_rawMVArun2dR03[n];
        self.idMVArun2NewDM = tree.TauGood_idMVArun2NewDM[n];
        self.rawMVArun2NewDM = tree.TauGood_rawMVArun2NewDM[n];
        self.idCI3hit = tree.TauGood_idCI3hit[n];
        self.idAntiMu = tree.TauGood_idAntiMu[n];
        self.idAntiErun2 = tree.TauGood_idAntiErun2[n];
        self.isoCI3hit = tree.TauGood_isoCI3hit[n];
        self.photonOutsideSigCone = tree.TauGood_photonOutsideSigCone[n];
        self.mcMatchId = tree.TauGood_mcMatchId[n];
        self.pdgId = tree.TauGood_pdgId[n];
        self.pt = tree.TauGood_pt[n];
        self.eta = tree.TauGood_eta[n];
        self.phi = tree.TauGood_phi[n];
        self.mass = tree.TauGood_mass[n];
        self.idxJetMatch = tree.TauGood_idxJetMatch[n];
        self.genMatchType = tree.TauGood_genMatchType[n];
        pass
    @staticmethod
    def make_array(input):
        return [TauGood(input, i) for i in range(input.nTauGood)]
class GenStatus2bHad:
    def __init__(self, tree, n):
        self.pdgId = tree.GenStatus2bHad_pdgId[n];
        self.pt = tree.GenStatus2bHad_pt[n];
        self.eta = tree.GenStatus2bHad_eta[n];
        self.phi = tree.GenStatus2bHad_phi[n];
        self.mass = tree.GenStatus2bHad_mass[n];
        self.charge = tree.GenStatus2bHad_charge[n];
        self.status = tree.GenStatus2bHad_status[n];
        self.isPromptHard = tree.GenStatus2bHad_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenStatus2bHad(input, i) for i in range(input.nGenStatus2bHad)]
class hJidx:
    def __init__(self, tree, n):
        self.hJidx = tree.hJidx[n];
        pass
    @staticmethod
    def make_array(input):
        return [hJidx(input, i) for i in range(input.nhJidx)]
class GenNuFromTau:
    def __init__(self, tree, n):
        self.pdgId = tree.GenNuFromTau_pdgId[n];
        self.pt = tree.GenNuFromTau_pt[n];
        self.eta = tree.GenNuFromTau_eta[n];
        self.phi = tree.GenNuFromTau_phi[n];
        self.mass = tree.GenNuFromTau_mass[n];
        self.charge = tree.GenNuFromTau_charge[n];
        self.status = tree.GenNuFromTau_status[n];
        self.isPromptHard = tree.GenNuFromTau_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenNuFromTau(input, i) for i in range(input.nGenNuFromTau)]
class FatjetCA15softdropz2b1:
    def __init__(self, tree, n):
        self.pt = tree.FatjetCA15softdropz2b1_pt[n];
        self.eta = tree.FatjetCA15softdropz2b1_eta[n];
        self.phi = tree.FatjetCA15softdropz2b1_phi[n];
        self.mass = tree.FatjetCA15softdropz2b1_mass[n];
        self.tau1 = tree.FatjetCA15softdropz2b1_tau1[n];
        self.tau2 = tree.FatjetCA15softdropz2b1_tau2[n];
        self.tau3 = tree.FatjetCA15softdropz2b1_tau3[n];
        pass
    @staticmethod
    def make_array(input):
        return [FatjetCA15softdropz2b1(input, i) for i in range(input.nFatjetCA15softdropz2b1)]
class GenGluonFromB:
    def __init__(self, tree, n):
        self.pdgId = tree.GenGluonFromB_pdgId[n];
        self.pt = tree.GenGluonFromB_pt[n];
        self.eta = tree.GenGluonFromB_eta[n];
        self.phi = tree.GenGluonFromB_phi[n];
        self.mass = tree.GenGluonFromB_mass[n];
        self.charge = tree.GenGluonFromB_charge[n];
        self.status = tree.GenGluonFromB_status[n];
        self.isPromptHard = tree.GenGluonFromB_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenGluonFromB(input, i) for i in range(input.nGenGluonFromB)]
class trgObjects_hltTripleJet50:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltTripleJet50(input, i) for i in range(input.ntrgObjects_hltTripleJet50)]
class trgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1(input, i) for i in range(input.ntrgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1)]
class httCandidates:
    def __init__(self, tree, n):
        self.pt = tree.httCandidates_pt[n];
        self.eta = tree.httCandidates_eta[n];
        self.phi = tree.httCandidates_phi[n];
        self.mass = tree.httCandidates_mass[n];
        self.ptcal = tree.httCandidates_ptcal[n];
        self.etacal = tree.httCandidates_etacal[n];
        self.phical = tree.httCandidates_phical[n];
        self.masscal = tree.httCandidates_masscal[n];
        self.fRec = tree.httCandidates_fRec[n];
        self.Ropt = tree.httCandidates_Ropt[n];
        self.RoptCalc = tree.httCandidates_RoptCalc[n];
        self.ptForRoptCalc = tree.httCandidates_ptForRoptCalc[n];
        self.subjetIDPassed = tree.httCandidates_subjetIDPassed[n];
        self.sjW1ptcal = tree.httCandidates_sjW1ptcal[n];
        self.sjW1pt = tree.httCandidates_sjW1pt[n];
        self.sjW1eta = tree.httCandidates_sjW1eta[n];
        self.sjW1phi = tree.httCandidates_sjW1phi[n];
        self.sjW1masscal = tree.httCandidates_sjW1masscal[n];
        self.sjW1mass = tree.httCandidates_sjW1mass[n];
        self.sjW1btag = tree.httCandidates_sjW1btag[n];
        self.sjW1corr = tree.httCandidates_sjW1corr[n];
        self.sjW2ptcal = tree.httCandidates_sjW2ptcal[n];
        self.sjW2pt = tree.httCandidates_sjW2pt[n];
        self.sjW2eta = tree.httCandidates_sjW2eta[n];
        self.sjW2phi = tree.httCandidates_sjW2phi[n];
        self.sjW2masscal = tree.httCandidates_sjW2masscal[n];
        self.sjW2mass = tree.httCandidates_sjW2mass[n];
        self.sjW2btag = tree.httCandidates_sjW2btag[n];
        self.sjW2corr = tree.httCandidates_sjW2corr[n];
        self.sjNonWptcal = tree.httCandidates_sjNonWptcal[n];
        self.sjNonWpt = tree.httCandidates_sjNonWpt[n];
        self.sjNonWeta = tree.httCandidates_sjNonWeta[n];
        self.sjNonWphi = tree.httCandidates_sjNonWphi[n];
        self.sjNonWmasscal = tree.httCandidates_sjNonWmasscal[n];
        self.sjNonWmass = tree.httCandidates_sjNonWmass[n];
        self.sjNonWbtag = tree.httCandidates_sjNonWbtag[n];
        self.sjNonWcorr = tree.httCandidates_sjNonWcorr[n];
        self.sjW1_corr_AbsoluteStatUp = tree.httCandidates_sjW1_corr_AbsoluteStatUp[n];
        self.sjW1_corr_AbsoluteStatDown = tree.httCandidates_sjW1_corr_AbsoluteStatDown[n];
        self.sjW1_corr_AbsoluteScaleUp = tree.httCandidates_sjW1_corr_AbsoluteScaleUp[n];
        self.sjW1_corr_AbsoluteScaleDown = tree.httCandidates_sjW1_corr_AbsoluteScaleDown[n];
        self.sjW1_corr_AbsoluteFlavMapUp = tree.httCandidates_sjW1_corr_AbsoluteFlavMapUp[n];
        self.sjW1_corr_AbsoluteFlavMapDown = tree.httCandidates_sjW1_corr_AbsoluteFlavMapDown[n];
        self.sjW1_corr_AbsoluteMPFBiasUp = tree.httCandidates_sjW1_corr_AbsoluteMPFBiasUp[n];
        self.sjW1_corr_AbsoluteMPFBiasDown = tree.httCandidates_sjW1_corr_AbsoluteMPFBiasDown[n];
        self.sjW1_corr_FragmentationUp = tree.httCandidates_sjW1_corr_FragmentationUp[n];
        self.sjW1_corr_FragmentationDown = tree.httCandidates_sjW1_corr_FragmentationDown[n];
        self.sjW1_corr_SinglePionECALUp = tree.httCandidates_sjW1_corr_SinglePionECALUp[n];
        self.sjW1_corr_SinglePionECALDown = tree.httCandidates_sjW1_corr_SinglePionECALDown[n];
        self.sjW1_corr_SinglePionHCALUp = tree.httCandidates_sjW1_corr_SinglePionHCALUp[n];
        self.sjW1_corr_SinglePionHCALDown = tree.httCandidates_sjW1_corr_SinglePionHCALDown[n];
        self.sjW1_corr_FlavorQCDUp = tree.httCandidates_sjW1_corr_FlavorQCDUp[n];
        self.sjW1_corr_FlavorQCDDown = tree.httCandidates_sjW1_corr_FlavorQCDDown[n];
        self.sjW1_corr_TimePtEtaUp = tree.httCandidates_sjW1_corr_TimePtEtaUp[n];
        self.sjW1_corr_TimePtEtaDown = tree.httCandidates_sjW1_corr_TimePtEtaDown[n];
        self.sjW1_corr_RelativeJEREC1Up = tree.httCandidates_sjW1_corr_RelativeJEREC1Up[n];
        self.sjW1_corr_RelativeJEREC1Down = tree.httCandidates_sjW1_corr_RelativeJEREC1Down[n];
        self.sjW1_corr_RelativeJEREC2Up = tree.httCandidates_sjW1_corr_RelativeJEREC2Up[n];
        self.sjW1_corr_RelativeJEREC2Down = tree.httCandidates_sjW1_corr_RelativeJEREC2Down[n];
        self.sjW1_corr_RelativeJERHFUp = tree.httCandidates_sjW1_corr_RelativeJERHFUp[n];
        self.sjW1_corr_RelativeJERHFDown = tree.httCandidates_sjW1_corr_RelativeJERHFDown[n];
        self.sjW1_corr_RelativePtBBUp = tree.httCandidates_sjW1_corr_RelativePtBBUp[n];
        self.sjW1_corr_RelativePtBBDown = tree.httCandidates_sjW1_corr_RelativePtBBDown[n];
        self.sjW1_corr_RelativePtEC1Up = tree.httCandidates_sjW1_corr_RelativePtEC1Up[n];
        self.sjW1_corr_RelativePtEC1Down = tree.httCandidates_sjW1_corr_RelativePtEC1Down[n];
        self.sjW1_corr_RelativePtEC2Up = tree.httCandidates_sjW1_corr_RelativePtEC2Up[n];
        self.sjW1_corr_RelativePtEC2Down = tree.httCandidates_sjW1_corr_RelativePtEC2Down[n];
        self.sjW1_corr_RelativePtHFUp = tree.httCandidates_sjW1_corr_RelativePtHFUp[n];
        self.sjW1_corr_RelativePtHFDown = tree.httCandidates_sjW1_corr_RelativePtHFDown[n];
        self.sjW1_corr_RelativeBalUp = tree.httCandidates_sjW1_corr_RelativeBalUp[n];
        self.sjW1_corr_RelativeBalDown = tree.httCandidates_sjW1_corr_RelativeBalDown[n];
        self.sjW1_corr_RelativeFSRUp = tree.httCandidates_sjW1_corr_RelativeFSRUp[n];
        self.sjW1_corr_RelativeFSRDown = tree.httCandidates_sjW1_corr_RelativeFSRDown[n];
        self.sjW1_corr_RelativeStatFSRUp = tree.httCandidates_sjW1_corr_RelativeStatFSRUp[n];
        self.sjW1_corr_RelativeStatFSRDown = tree.httCandidates_sjW1_corr_RelativeStatFSRDown[n];
        self.sjW1_corr_RelativeStatECUp = tree.httCandidates_sjW1_corr_RelativeStatECUp[n];
        self.sjW1_corr_RelativeStatECDown = tree.httCandidates_sjW1_corr_RelativeStatECDown[n];
        self.sjW1_corr_RelativeStatHFUp = tree.httCandidates_sjW1_corr_RelativeStatHFUp[n];
        self.sjW1_corr_RelativeStatHFDown = tree.httCandidates_sjW1_corr_RelativeStatHFDown[n];
        self.sjW1_corr_PileUpDataMCUp = tree.httCandidates_sjW1_corr_PileUpDataMCUp[n];
        self.sjW1_corr_PileUpDataMCDown = tree.httCandidates_sjW1_corr_PileUpDataMCDown[n];
        self.sjW1_corr_PileUpPtRefUp = tree.httCandidates_sjW1_corr_PileUpPtRefUp[n];
        self.sjW1_corr_PileUpPtRefDown = tree.httCandidates_sjW1_corr_PileUpPtRefDown[n];
        self.sjW1_corr_PileUpPtBBUp = tree.httCandidates_sjW1_corr_PileUpPtBBUp[n];
        self.sjW1_corr_PileUpPtBBDown = tree.httCandidates_sjW1_corr_PileUpPtBBDown[n];
        self.sjW1_corr_PileUpPtEC1Up = tree.httCandidates_sjW1_corr_PileUpPtEC1Up[n];
        self.sjW1_corr_PileUpPtEC1Down = tree.httCandidates_sjW1_corr_PileUpPtEC1Down[n];
        self.sjW1_corr_PileUpPtEC2Up = tree.httCandidates_sjW1_corr_PileUpPtEC2Up[n];
        self.sjW1_corr_PileUpPtEC2Down = tree.httCandidates_sjW1_corr_PileUpPtEC2Down[n];
        self.sjW1_corr_PileUpPtHFUp = tree.httCandidates_sjW1_corr_PileUpPtHFUp[n];
        self.sjW1_corr_PileUpPtHFDown = tree.httCandidates_sjW1_corr_PileUpPtHFDown[n];
        self.sjW1_corr_PileUpMuZeroUp = tree.httCandidates_sjW1_corr_PileUpMuZeroUp[n];
        self.sjW1_corr_PileUpMuZeroDown = tree.httCandidates_sjW1_corr_PileUpMuZeroDown[n];
        self.sjW1_corr_PileUpEnvelopeUp = tree.httCandidates_sjW1_corr_PileUpEnvelopeUp[n];
        self.sjW1_corr_PileUpEnvelopeDown = tree.httCandidates_sjW1_corr_PileUpEnvelopeDown[n];
        self.sjW1_corr_SubTotalPileUpUp = tree.httCandidates_sjW1_corr_SubTotalPileUpUp[n];
        self.sjW1_corr_SubTotalPileUpDown = tree.httCandidates_sjW1_corr_SubTotalPileUpDown[n];
        self.sjW1_corr_SubTotalRelativeUp = tree.httCandidates_sjW1_corr_SubTotalRelativeUp[n];
        self.sjW1_corr_SubTotalRelativeDown = tree.httCandidates_sjW1_corr_SubTotalRelativeDown[n];
        self.sjW1_corr_SubTotalPtUp = tree.httCandidates_sjW1_corr_SubTotalPtUp[n];
        self.sjW1_corr_SubTotalPtDown = tree.httCandidates_sjW1_corr_SubTotalPtDown[n];
        self.sjW1_corr_SubTotalScaleUp = tree.httCandidates_sjW1_corr_SubTotalScaleUp[n];
        self.sjW1_corr_SubTotalScaleDown = tree.httCandidates_sjW1_corr_SubTotalScaleDown[n];
        self.sjW1_corr_SubTotalAbsoluteUp = tree.httCandidates_sjW1_corr_SubTotalAbsoluteUp[n];
        self.sjW1_corr_SubTotalAbsoluteDown = tree.httCandidates_sjW1_corr_SubTotalAbsoluteDown[n];
        self.sjW1_corr_SubTotalMCUp = tree.httCandidates_sjW1_corr_SubTotalMCUp[n];
        self.sjW1_corr_SubTotalMCDown = tree.httCandidates_sjW1_corr_SubTotalMCDown[n];
        self.sjW1_corr_TotalUp = tree.httCandidates_sjW1_corr_TotalUp[n];
        self.sjW1_corr_TotalDown = tree.httCandidates_sjW1_corr_TotalDown[n];
        self.sjW1_corr_TotalNoFlavorUp = tree.httCandidates_sjW1_corr_TotalNoFlavorUp[n];
        self.sjW1_corr_TotalNoFlavorDown = tree.httCandidates_sjW1_corr_TotalNoFlavorDown[n];
        self.sjW1_corr_TotalNoTimeUp = tree.httCandidates_sjW1_corr_TotalNoTimeUp[n];
        self.sjW1_corr_TotalNoTimeDown = tree.httCandidates_sjW1_corr_TotalNoTimeDown[n];
        self.sjW1_corr_TotalNoFlavorNoTimeUp = tree.httCandidates_sjW1_corr_TotalNoFlavorNoTimeUp[n];
        self.sjW1_corr_TotalNoFlavorNoTimeDown = tree.httCandidates_sjW1_corr_TotalNoFlavorNoTimeDown[n];
        self.sjW1_corr_FlavorZJetUp = tree.httCandidates_sjW1_corr_FlavorZJetUp[n];
        self.sjW1_corr_FlavorZJetDown = tree.httCandidates_sjW1_corr_FlavorZJetDown[n];
        self.sjW1_corr_FlavorPhotonJetUp = tree.httCandidates_sjW1_corr_FlavorPhotonJetUp[n];
        self.sjW1_corr_FlavorPhotonJetDown = tree.httCandidates_sjW1_corr_FlavorPhotonJetDown[n];
        self.sjW1_corr_FlavorPureGluonUp = tree.httCandidates_sjW1_corr_FlavorPureGluonUp[n];
        self.sjW1_corr_FlavorPureGluonDown = tree.httCandidates_sjW1_corr_FlavorPureGluonDown[n];
        self.sjW1_corr_FlavorPureQuarkUp = tree.httCandidates_sjW1_corr_FlavorPureQuarkUp[n];
        self.sjW1_corr_FlavorPureQuarkDown = tree.httCandidates_sjW1_corr_FlavorPureQuarkDown[n];
        self.sjW1_corr_FlavorPureCharmUp = tree.httCandidates_sjW1_corr_FlavorPureCharmUp[n];
        self.sjW1_corr_FlavorPureCharmDown = tree.httCandidates_sjW1_corr_FlavorPureCharmDown[n];
        self.sjW1_corr_FlavorPureBottomUp = tree.httCandidates_sjW1_corr_FlavorPureBottomUp[n];
        self.sjW1_corr_FlavorPureBottomDown = tree.httCandidates_sjW1_corr_FlavorPureBottomDown[n];
        self.sjW1_corr_TimeRunBCDUp = tree.httCandidates_sjW1_corr_TimeRunBCDUp[n];
        self.sjW1_corr_TimeRunBCDDown = tree.httCandidates_sjW1_corr_TimeRunBCDDown[n];
        self.sjW1_corr_TimeRunEFUp = tree.httCandidates_sjW1_corr_TimeRunEFUp[n];
        self.sjW1_corr_TimeRunEFDown = tree.httCandidates_sjW1_corr_TimeRunEFDown[n];
        self.sjW1_corr_TimeRunGUp = tree.httCandidates_sjW1_corr_TimeRunGUp[n];
        self.sjW1_corr_TimeRunGDown = tree.httCandidates_sjW1_corr_TimeRunGDown[n];
        self.sjW1_corr_TimeRunHUp = tree.httCandidates_sjW1_corr_TimeRunHUp[n];
        self.sjW1_corr_TimeRunHDown = tree.httCandidates_sjW1_corr_TimeRunHDown[n];
        self.sjW1_corr_CorrelationGroupMPFInSituUp = tree.httCandidates_sjW1_corr_CorrelationGroupMPFInSituUp[n];
        self.sjW1_corr_CorrelationGroupMPFInSituDown = tree.httCandidates_sjW1_corr_CorrelationGroupMPFInSituDown[n];
        self.sjW1_corr_CorrelationGroupIntercalibrationUp = tree.httCandidates_sjW1_corr_CorrelationGroupIntercalibrationUp[n];
        self.sjW1_corr_CorrelationGroupIntercalibrationDown = tree.httCandidates_sjW1_corr_CorrelationGroupIntercalibrationDown[n];
        self.sjW1_corr_CorrelationGroupbJESUp = tree.httCandidates_sjW1_corr_CorrelationGroupbJESUp[n];
        self.sjW1_corr_CorrelationGroupbJESDown = tree.httCandidates_sjW1_corr_CorrelationGroupbJESDown[n];
        self.sjW1_corr_CorrelationGroupFlavorUp = tree.httCandidates_sjW1_corr_CorrelationGroupFlavorUp[n];
        self.sjW1_corr_CorrelationGroupFlavorDown = tree.httCandidates_sjW1_corr_CorrelationGroupFlavorDown[n];
        self.sjW1_corr_CorrelationGroupUncorrelatedUp = tree.httCandidates_sjW1_corr_CorrelationGroupUncorrelatedUp[n];
        self.sjW1_corr_CorrelationGroupUncorrelatedDown = tree.httCandidates_sjW1_corr_CorrelationGroupUncorrelatedDown[n];
        self.sjW2_corr_AbsoluteStatUp = tree.httCandidates_sjW2_corr_AbsoluteStatUp[n];
        self.sjW2_corr_AbsoluteStatDown = tree.httCandidates_sjW2_corr_AbsoluteStatDown[n];
        self.sjW2_corr_AbsoluteScaleUp = tree.httCandidates_sjW2_corr_AbsoluteScaleUp[n];
        self.sjW2_corr_AbsoluteScaleDown = tree.httCandidates_sjW2_corr_AbsoluteScaleDown[n];
        self.sjW2_corr_AbsoluteFlavMapUp = tree.httCandidates_sjW2_corr_AbsoluteFlavMapUp[n];
        self.sjW2_corr_AbsoluteFlavMapDown = tree.httCandidates_sjW2_corr_AbsoluteFlavMapDown[n];
        self.sjW2_corr_AbsoluteMPFBiasUp = tree.httCandidates_sjW2_corr_AbsoluteMPFBiasUp[n];
        self.sjW2_corr_AbsoluteMPFBiasDown = tree.httCandidates_sjW2_corr_AbsoluteMPFBiasDown[n];
        self.sjW2_corr_FragmentationUp = tree.httCandidates_sjW2_corr_FragmentationUp[n];
        self.sjW2_corr_FragmentationDown = tree.httCandidates_sjW2_corr_FragmentationDown[n];
        self.sjW2_corr_SinglePionECALUp = tree.httCandidates_sjW2_corr_SinglePionECALUp[n];
        self.sjW2_corr_SinglePionECALDown = tree.httCandidates_sjW2_corr_SinglePionECALDown[n];
        self.sjW2_corr_SinglePionHCALUp = tree.httCandidates_sjW2_corr_SinglePionHCALUp[n];
        self.sjW2_corr_SinglePionHCALDown = tree.httCandidates_sjW2_corr_SinglePionHCALDown[n];
        self.sjW2_corr_FlavorQCDUp = tree.httCandidates_sjW2_corr_FlavorQCDUp[n];
        self.sjW2_corr_FlavorQCDDown = tree.httCandidates_sjW2_corr_FlavorQCDDown[n];
        self.sjW2_corr_TimePtEtaUp = tree.httCandidates_sjW2_corr_TimePtEtaUp[n];
        self.sjW2_corr_TimePtEtaDown = tree.httCandidates_sjW2_corr_TimePtEtaDown[n];
        self.sjW2_corr_RelativeJEREC1Up = tree.httCandidates_sjW2_corr_RelativeJEREC1Up[n];
        self.sjW2_corr_RelativeJEREC1Down = tree.httCandidates_sjW2_corr_RelativeJEREC1Down[n];
        self.sjW2_corr_RelativeJEREC2Up = tree.httCandidates_sjW2_corr_RelativeJEREC2Up[n];
        self.sjW2_corr_RelativeJEREC2Down = tree.httCandidates_sjW2_corr_RelativeJEREC2Down[n];
        self.sjW2_corr_RelativeJERHFUp = tree.httCandidates_sjW2_corr_RelativeJERHFUp[n];
        self.sjW2_corr_RelativeJERHFDown = tree.httCandidates_sjW2_corr_RelativeJERHFDown[n];
        self.sjW2_corr_RelativePtBBUp = tree.httCandidates_sjW2_corr_RelativePtBBUp[n];
        self.sjW2_corr_RelativePtBBDown = tree.httCandidates_sjW2_corr_RelativePtBBDown[n];
        self.sjW2_corr_RelativePtEC1Up = tree.httCandidates_sjW2_corr_RelativePtEC1Up[n];
        self.sjW2_corr_RelativePtEC1Down = tree.httCandidates_sjW2_corr_RelativePtEC1Down[n];
        self.sjW2_corr_RelativePtEC2Up = tree.httCandidates_sjW2_corr_RelativePtEC2Up[n];
        self.sjW2_corr_RelativePtEC2Down = tree.httCandidates_sjW2_corr_RelativePtEC2Down[n];
        self.sjW2_corr_RelativePtHFUp = tree.httCandidates_sjW2_corr_RelativePtHFUp[n];
        self.sjW2_corr_RelativePtHFDown = tree.httCandidates_sjW2_corr_RelativePtHFDown[n];
        self.sjW2_corr_RelativeBalUp = tree.httCandidates_sjW2_corr_RelativeBalUp[n];
        self.sjW2_corr_RelativeBalDown = tree.httCandidates_sjW2_corr_RelativeBalDown[n];
        self.sjW2_corr_RelativeFSRUp = tree.httCandidates_sjW2_corr_RelativeFSRUp[n];
        self.sjW2_corr_RelativeFSRDown = tree.httCandidates_sjW2_corr_RelativeFSRDown[n];
        self.sjW2_corr_RelativeStatFSRUp = tree.httCandidates_sjW2_corr_RelativeStatFSRUp[n];
        self.sjW2_corr_RelativeStatFSRDown = tree.httCandidates_sjW2_corr_RelativeStatFSRDown[n];
        self.sjW2_corr_RelativeStatECUp = tree.httCandidates_sjW2_corr_RelativeStatECUp[n];
        self.sjW2_corr_RelativeStatECDown = tree.httCandidates_sjW2_corr_RelativeStatECDown[n];
        self.sjW2_corr_RelativeStatHFUp = tree.httCandidates_sjW2_corr_RelativeStatHFUp[n];
        self.sjW2_corr_RelativeStatHFDown = tree.httCandidates_sjW2_corr_RelativeStatHFDown[n];
        self.sjW2_corr_PileUpDataMCUp = tree.httCandidates_sjW2_corr_PileUpDataMCUp[n];
        self.sjW2_corr_PileUpDataMCDown = tree.httCandidates_sjW2_corr_PileUpDataMCDown[n];
        self.sjW2_corr_PileUpPtRefUp = tree.httCandidates_sjW2_corr_PileUpPtRefUp[n];
        self.sjW2_corr_PileUpPtRefDown = tree.httCandidates_sjW2_corr_PileUpPtRefDown[n];
        self.sjW2_corr_PileUpPtBBUp = tree.httCandidates_sjW2_corr_PileUpPtBBUp[n];
        self.sjW2_corr_PileUpPtBBDown = tree.httCandidates_sjW2_corr_PileUpPtBBDown[n];
        self.sjW2_corr_PileUpPtEC1Up = tree.httCandidates_sjW2_corr_PileUpPtEC1Up[n];
        self.sjW2_corr_PileUpPtEC1Down = tree.httCandidates_sjW2_corr_PileUpPtEC1Down[n];
        self.sjW2_corr_PileUpPtEC2Up = tree.httCandidates_sjW2_corr_PileUpPtEC2Up[n];
        self.sjW2_corr_PileUpPtEC2Down = tree.httCandidates_sjW2_corr_PileUpPtEC2Down[n];
        self.sjW2_corr_PileUpPtHFUp = tree.httCandidates_sjW2_corr_PileUpPtHFUp[n];
        self.sjW2_corr_PileUpPtHFDown = tree.httCandidates_sjW2_corr_PileUpPtHFDown[n];
        self.sjW2_corr_PileUpMuZeroUp = tree.httCandidates_sjW2_corr_PileUpMuZeroUp[n];
        self.sjW2_corr_PileUpMuZeroDown = tree.httCandidates_sjW2_corr_PileUpMuZeroDown[n];
        self.sjW2_corr_PileUpEnvelopeUp = tree.httCandidates_sjW2_corr_PileUpEnvelopeUp[n];
        self.sjW2_corr_PileUpEnvelopeDown = tree.httCandidates_sjW2_corr_PileUpEnvelopeDown[n];
        self.sjW2_corr_SubTotalPileUpUp = tree.httCandidates_sjW2_corr_SubTotalPileUpUp[n];
        self.sjW2_corr_SubTotalPileUpDown = tree.httCandidates_sjW2_corr_SubTotalPileUpDown[n];
        self.sjW2_corr_SubTotalRelativeUp = tree.httCandidates_sjW2_corr_SubTotalRelativeUp[n];
        self.sjW2_corr_SubTotalRelativeDown = tree.httCandidates_sjW2_corr_SubTotalRelativeDown[n];
        self.sjW2_corr_SubTotalPtUp = tree.httCandidates_sjW2_corr_SubTotalPtUp[n];
        self.sjW2_corr_SubTotalPtDown = tree.httCandidates_sjW2_corr_SubTotalPtDown[n];
        self.sjW2_corr_SubTotalScaleUp = tree.httCandidates_sjW2_corr_SubTotalScaleUp[n];
        self.sjW2_corr_SubTotalScaleDown = tree.httCandidates_sjW2_corr_SubTotalScaleDown[n];
        self.sjW2_corr_SubTotalAbsoluteUp = tree.httCandidates_sjW2_corr_SubTotalAbsoluteUp[n];
        self.sjW2_corr_SubTotalAbsoluteDown = tree.httCandidates_sjW2_corr_SubTotalAbsoluteDown[n];
        self.sjW2_corr_SubTotalMCUp = tree.httCandidates_sjW2_corr_SubTotalMCUp[n];
        self.sjW2_corr_SubTotalMCDown = tree.httCandidates_sjW2_corr_SubTotalMCDown[n];
        self.sjW2_corr_TotalUp = tree.httCandidates_sjW2_corr_TotalUp[n];
        self.sjW2_corr_TotalDown = tree.httCandidates_sjW2_corr_TotalDown[n];
        self.sjW2_corr_TotalNoFlavorUp = tree.httCandidates_sjW2_corr_TotalNoFlavorUp[n];
        self.sjW2_corr_TotalNoFlavorDown = tree.httCandidates_sjW2_corr_TotalNoFlavorDown[n];
        self.sjW2_corr_TotalNoTimeUp = tree.httCandidates_sjW2_corr_TotalNoTimeUp[n];
        self.sjW2_corr_TotalNoTimeDown = tree.httCandidates_sjW2_corr_TotalNoTimeDown[n];
        self.sjW2_corr_TotalNoFlavorNoTimeUp = tree.httCandidates_sjW2_corr_TotalNoFlavorNoTimeUp[n];
        self.sjW2_corr_TotalNoFlavorNoTimeDown = tree.httCandidates_sjW2_corr_TotalNoFlavorNoTimeDown[n];
        self.sjW2_corr_FlavorZJetUp = tree.httCandidates_sjW2_corr_FlavorZJetUp[n];
        self.sjW2_corr_FlavorZJetDown = tree.httCandidates_sjW2_corr_FlavorZJetDown[n];
        self.sjW2_corr_FlavorPhotonJetUp = tree.httCandidates_sjW2_corr_FlavorPhotonJetUp[n];
        self.sjW2_corr_FlavorPhotonJetDown = tree.httCandidates_sjW2_corr_FlavorPhotonJetDown[n];
        self.sjW2_corr_FlavorPureGluonUp = tree.httCandidates_sjW2_corr_FlavorPureGluonUp[n];
        self.sjW2_corr_FlavorPureGluonDown = tree.httCandidates_sjW2_corr_FlavorPureGluonDown[n];
        self.sjW2_corr_FlavorPureQuarkUp = tree.httCandidates_sjW2_corr_FlavorPureQuarkUp[n];
        self.sjW2_corr_FlavorPureQuarkDown = tree.httCandidates_sjW2_corr_FlavorPureQuarkDown[n];
        self.sjW2_corr_FlavorPureCharmUp = tree.httCandidates_sjW2_corr_FlavorPureCharmUp[n];
        self.sjW2_corr_FlavorPureCharmDown = tree.httCandidates_sjW2_corr_FlavorPureCharmDown[n];
        self.sjW2_corr_FlavorPureBottomUp = tree.httCandidates_sjW2_corr_FlavorPureBottomUp[n];
        self.sjW2_corr_FlavorPureBottomDown = tree.httCandidates_sjW2_corr_FlavorPureBottomDown[n];
        self.sjW2_corr_TimeRunBCDUp = tree.httCandidates_sjW2_corr_TimeRunBCDUp[n];
        self.sjW2_corr_TimeRunBCDDown = tree.httCandidates_sjW2_corr_TimeRunBCDDown[n];
        self.sjW2_corr_TimeRunEFUp = tree.httCandidates_sjW2_corr_TimeRunEFUp[n];
        self.sjW2_corr_TimeRunEFDown = tree.httCandidates_sjW2_corr_TimeRunEFDown[n];
        self.sjW2_corr_TimeRunGUp = tree.httCandidates_sjW2_corr_TimeRunGUp[n];
        self.sjW2_corr_TimeRunGDown = tree.httCandidates_sjW2_corr_TimeRunGDown[n];
        self.sjW2_corr_TimeRunHUp = tree.httCandidates_sjW2_corr_TimeRunHUp[n];
        self.sjW2_corr_TimeRunHDown = tree.httCandidates_sjW2_corr_TimeRunHDown[n];
        self.sjW2_corr_CorrelationGroupMPFInSituUp = tree.httCandidates_sjW2_corr_CorrelationGroupMPFInSituUp[n];
        self.sjW2_corr_CorrelationGroupMPFInSituDown = tree.httCandidates_sjW2_corr_CorrelationGroupMPFInSituDown[n];
        self.sjW2_corr_CorrelationGroupIntercalibrationUp = tree.httCandidates_sjW2_corr_CorrelationGroupIntercalibrationUp[n];
        self.sjW2_corr_CorrelationGroupIntercalibrationDown = tree.httCandidates_sjW2_corr_CorrelationGroupIntercalibrationDown[n];
        self.sjW2_corr_CorrelationGroupbJESUp = tree.httCandidates_sjW2_corr_CorrelationGroupbJESUp[n];
        self.sjW2_corr_CorrelationGroupbJESDown = tree.httCandidates_sjW2_corr_CorrelationGroupbJESDown[n];
        self.sjW2_corr_CorrelationGroupFlavorUp = tree.httCandidates_sjW2_corr_CorrelationGroupFlavorUp[n];
        self.sjW2_corr_CorrelationGroupFlavorDown = tree.httCandidates_sjW2_corr_CorrelationGroupFlavorDown[n];
        self.sjW2_corr_CorrelationGroupUncorrelatedUp = tree.httCandidates_sjW2_corr_CorrelationGroupUncorrelatedUp[n];
        self.sjW2_corr_CorrelationGroupUncorrelatedDown = tree.httCandidates_sjW2_corr_CorrelationGroupUncorrelatedDown[n];
        self.sjNonW_corr_AbsoluteStatUp = tree.httCandidates_sjNonW_corr_AbsoluteStatUp[n];
        self.sjNonW_corr_AbsoluteStatDown = tree.httCandidates_sjNonW_corr_AbsoluteStatDown[n];
        self.sjNonW_corr_AbsoluteScaleUp = tree.httCandidates_sjNonW_corr_AbsoluteScaleUp[n];
        self.sjNonW_corr_AbsoluteScaleDown = tree.httCandidates_sjNonW_corr_AbsoluteScaleDown[n];
        self.sjNonW_corr_AbsoluteFlavMapUp = tree.httCandidates_sjNonW_corr_AbsoluteFlavMapUp[n];
        self.sjNonW_corr_AbsoluteFlavMapDown = tree.httCandidates_sjNonW_corr_AbsoluteFlavMapDown[n];
        self.sjNonW_corr_AbsoluteMPFBiasUp = tree.httCandidates_sjNonW_corr_AbsoluteMPFBiasUp[n];
        self.sjNonW_corr_AbsoluteMPFBiasDown = tree.httCandidates_sjNonW_corr_AbsoluteMPFBiasDown[n];
        self.sjNonW_corr_FragmentationUp = tree.httCandidates_sjNonW_corr_FragmentationUp[n];
        self.sjNonW_corr_FragmentationDown = tree.httCandidates_sjNonW_corr_FragmentationDown[n];
        self.sjNonW_corr_SinglePionECALUp = tree.httCandidates_sjNonW_corr_SinglePionECALUp[n];
        self.sjNonW_corr_SinglePionECALDown = tree.httCandidates_sjNonW_corr_SinglePionECALDown[n];
        self.sjNonW_corr_SinglePionHCALUp = tree.httCandidates_sjNonW_corr_SinglePionHCALUp[n];
        self.sjNonW_corr_SinglePionHCALDown = tree.httCandidates_sjNonW_corr_SinglePionHCALDown[n];
        self.sjNonW_corr_FlavorQCDUp = tree.httCandidates_sjNonW_corr_FlavorQCDUp[n];
        self.sjNonW_corr_FlavorQCDDown = tree.httCandidates_sjNonW_corr_FlavorQCDDown[n];
        self.sjNonW_corr_TimePtEtaUp = tree.httCandidates_sjNonW_corr_TimePtEtaUp[n];
        self.sjNonW_corr_TimePtEtaDown = tree.httCandidates_sjNonW_corr_TimePtEtaDown[n];
        self.sjNonW_corr_RelativeJEREC1Up = tree.httCandidates_sjNonW_corr_RelativeJEREC1Up[n];
        self.sjNonW_corr_RelativeJEREC1Down = tree.httCandidates_sjNonW_corr_RelativeJEREC1Down[n];
        self.sjNonW_corr_RelativeJEREC2Up = tree.httCandidates_sjNonW_corr_RelativeJEREC2Up[n];
        self.sjNonW_corr_RelativeJEREC2Down = tree.httCandidates_sjNonW_corr_RelativeJEREC2Down[n];
        self.sjNonW_corr_RelativeJERHFUp = tree.httCandidates_sjNonW_corr_RelativeJERHFUp[n];
        self.sjNonW_corr_RelativeJERHFDown = tree.httCandidates_sjNonW_corr_RelativeJERHFDown[n];
        self.sjNonW_corr_RelativePtBBUp = tree.httCandidates_sjNonW_corr_RelativePtBBUp[n];
        self.sjNonW_corr_RelativePtBBDown = tree.httCandidates_sjNonW_corr_RelativePtBBDown[n];
        self.sjNonW_corr_RelativePtEC1Up = tree.httCandidates_sjNonW_corr_RelativePtEC1Up[n];
        self.sjNonW_corr_RelativePtEC1Down = tree.httCandidates_sjNonW_corr_RelativePtEC1Down[n];
        self.sjNonW_corr_RelativePtEC2Up = tree.httCandidates_sjNonW_corr_RelativePtEC2Up[n];
        self.sjNonW_corr_RelativePtEC2Down = tree.httCandidates_sjNonW_corr_RelativePtEC2Down[n];
        self.sjNonW_corr_RelativePtHFUp = tree.httCandidates_sjNonW_corr_RelativePtHFUp[n];
        self.sjNonW_corr_RelativePtHFDown = tree.httCandidates_sjNonW_corr_RelativePtHFDown[n];
        self.sjNonW_corr_RelativeBalUp = tree.httCandidates_sjNonW_corr_RelativeBalUp[n];
        self.sjNonW_corr_RelativeBalDown = tree.httCandidates_sjNonW_corr_RelativeBalDown[n];
        self.sjNonW_corr_RelativeFSRUp = tree.httCandidates_sjNonW_corr_RelativeFSRUp[n];
        self.sjNonW_corr_RelativeFSRDown = tree.httCandidates_sjNonW_corr_RelativeFSRDown[n];
        self.sjNonW_corr_RelativeStatFSRUp = tree.httCandidates_sjNonW_corr_RelativeStatFSRUp[n];
        self.sjNonW_corr_RelativeStatFSRDown = tree.httCandidates_sjNonW_corr_RelativeStatFSRDown[n];
        self.sjNonW_corr_RelativeStatECUp = tree.httCandidates_sjNonW_corr_RelativeStatECUp[n];
        self.sjNonW_corr_RelativeStatECDown = tree.httCandidates_sjNonW_corr_RelativeStatECDown[n];
        self.sjNonW_corr_RelativeStatHFUp = tree.httCandidates_sjNonW_corr_RelativeStatHFUp[n];
        self.sjNonW_corr_RelativeStatHFDown = tree.httCandidates_sjNonW_corr_RelativeStatHFDown[n];
        self.sjNonW_corr_PileUpDataMCUp = tree.httCandidates_sjNonW_corr_PileUpDataMCUp[n];
        self.sjNonW_corr_PileUpDataMCDown = tree.httCandidates_sjNonW_corr_PileUpDataMCDown[n];
        self.sjNonW_corr_PileUpPtRefUp = tree.httCandidates_sjNonW_corr_PileUpPtRefUp[n];
        self.sjNonW_corr_PileUpPtRefDown = tree.httCandidates_sjNonW_corr_PileUpPtRefDown[n];
        self.sjNonW_corr_PileUpPtBBUp = tree.httCandidates_sjNonW_corr_PileUpPtBBUp[n];
        self.sjNonW_corr_PileUpPtBBDown = tree.httCandidates_sjNonW_corr_PileUpPtBBDown[n];
        self.sjNonW_corr_PileUpPtEC1Up = tree.httCandidates_sjNonW_corr_PileUpPtEC1Up[n];
        self.sjNonW_corr_PileUpPtEC1Down = tree.httCandidates_sjNonW_corr_PileUpPtEC1Down[n];
        self.sjNonW_corr_PileUpPtEC2Up = tree.httCandidates_sjNonW_corr_PileUpPtEC2Up[n];
        self.sjNonW_corr_PileUpPtEC2Down = tree.httCandidates_sjNonW_corr_PileUpPtEC2Down[n];
        self.sjNonW_corr_PileUpPtHFUp = tree.httCandidates_sjNonW_corr_PileUpPtHFUp[n];
        self.sjNonW_corr_PileUpPtHFDown = tree.httCandidates_sjNonW_corr_PileUpPtHFDown[n];
        self.sjNonW_corr_PileUpMuZeroUp = tree.httCandidates_sjNonW_corr_PileUpMuZeroUp[n];
        self.sjNonW_corr_PileUpMuZeroDown = tree.httCandidates_sjNonW_corr_PileUpMuZeroDown[n];
        self.sjNonW_corr_PileUpEnvelopeUp = tree.httCandidates_sjNonW_corr_PileUpEnvelopeUp[n];
        self.sjNonW_corr_PileUpEnvelopeDown = tree.httCandidates_sjNonW_corr_PileUpEnvelopeDown[n];
        self.sjNonW_corr_SubTotalPileUpUp = tree.httCandidates_sjNonW_corr_SubTotalPileUpUp[n];
        self.sjNonW_corr_SubTotalPileUpDown = tree.httCandidates_sjNonW_corr_SubTotalPileUpDown[n];
        self.sjNonW_corr_SubTotalRelativeUp = tree.httCandidates_sjNonW_corr_SubTotalRelativeUp[n];
        self.sjNonW_corr_SubTotalRelativeDown = tree.httCandidates_sjNonW_corr_SubTotalRelativeDown[n];
        self.sjNonW_corr_SubTotalPtUp = tree.httCandidates_sjNonW_corr_SubTotalPtUp[n];
        self.sjNonW_corr_SubTotalPtDown = tree.httCandidates_sjNonW_corr_SubTotalPtDown[n];
        self.sjNonW_corr_SubTotalScaleUp = tree.httCandidates_sjNonW_corr_SubTotalScaleUp[n];
        self.sjNonW_corr_SubTotalScaleDown = tree.httCandidates_sjNonW_corr_SubTotalScaleDown[n];
        self.sjNonW_corr_SubTotalAbsoluteUp = tree.httCandidates_sjNonW_corr_SubTotalAbsoluteUp[n];
        self.sjNonW_corr_SubTotalAbsoluteDown = tree.httCandidates_sjNonW_corr_SubTotalAbsoluteDown[n];
        self.sjNonW_corr_SubTotalMCUp = tree.httCandidates_sjNonW_corr_SubTotalMCUp[n];
        self.sjNonW_corr_SubTotalMCDown = tree.httCandidates_sjNonW_corr_SubTotalMCDown[n];
        self.sjNonW_corr_TotalUp = tree.httCandidates_sjNonW_corr_TotalUp[n];
        self.sjNonW_corr_TotalDown = tree.httCandidates_sjNonW_corr_TotalDown[n];
        self.sjNonW_corr_TotalNoFlavorUp = tree.httCandidates_sjNonW_corr_TotalNoFlavorUp[n];
        self.sjNonW_corr_TotalNoFlavorDown = tree.httCandidates_sjNonW_corr_TotalNoFlavorDown[n];
        self.sjNonW_corr_TotalNoTimeUp = tree.httCandidates_sjNonW_corr_TotalNoTimeUp[n];
        self.sjNonW_corr_TotalNoTimeDown = tree.httCandidates_sjNonW_corr_TotalNoTimeDown[n];
        self.sjNonW_corr_TotalNoFlavorNoTimeUp = tree.httCandidates_sjNonW_corr_TotalNoFlavorNoTimeUp[n];
        self.sjNonW_corr_TotalNoFlavorNoTimeDown = tree.httCandidates_sjNonW_corr_TotalNoFlavorNoTimeDown[n];
        self.sjNonW_corr_FlavorZJetUp = tree.httCandidates_sjNonW_corr_FlavorZJetUp[n];
        self.sjNonW_corr_FlavorZJetDown = tree.httCandidates_sjNonW_corr_FlavorZJetDown[n];
        self.sjNonW_corr_FlavorPhotonJetUp = tree.httCandidates_sjNonW_corr_FlavorPhotonJetUp[n];
        self.sjNonW_corr_FlavorPhotonJetDown = tree.httCandidates_sjNonW_corr_FlavorPhotonJetDown[n];
        self.sjNonW_corr_FlavorPureGluonUp = tree.httCandidates_sjNonW_corr_FlavorPureGluonUp[n];
        self.sjNonW_corr_FlavorPureGluonDown = tree.httCandidates_sjNonW_corr_FlavorPureGluonDown[n];
        self.sjNonW_corr_FlavorPureQuarkUp = tree.httCandidates_sjNonW_corr_FlavorPureQuarkUp[n];
        self.sjNonW_corr_FlavorPureQuarkDown = tree.httCandidates_sjNonW_corr_FlavorPureQuarkDown[n];
        self.sjNonW_corr_FlavorPureCharmUp = tree.httCandidates_sjNonW_corr_FlavorPureCharmUp[n];
        self.sjNonW_corr_FlavorPureCharmDown = tree.httCandidates_sjNonW_corr_FlavorPureCharmDown[n];
        self.sjNonW_corr_FlavorPureBottomUp = tree.httCandidates_sjNonW_corr_FlavorPureBottomUp[n];
        self.sjNonW_corr_FlavorPureBottomDown = tree.httCandidates_sjNonW_corr_FlavorPureBottomDown[n];
        self.sjNonW_corr_TimeRunBCDUp = tree.httCandidates_sjNonW_corr_TimeRunBCDUp[n];
        self.sjNonW_corr_TimeRunBCDDown = tree.httCandidates_sjNonW_corr_TimeRunBCDDown[n];
        self.sjNonW_corr_TimeRunEFUp = tree.httCandidates_sjNonW_corr_TimeRunEFUp[n];
        self.sjNonW_corr_TimeRunEFDown = tree.httCandidates_sjNonW_corr_TimeRunEFDown[n];
        self.sjNonW_corr_TimeRunGUp = tree.httCandidates_sjNonW_corr_TimeRunGUp[n];
        self.sjNonW_corr_TimeRunGDown = tree.httCandidates_sjNonW_corr_TimeRunGDown[n];
        self.sjNonW_corr_TimeRunHUp = tree.httCandidates_sjNonW_corr_TimeRunHUp[n];
        self.sjNonW_corr_TimeRunHDown = tree.httCandidates_sjNonW_corr_TimeRunHDown[n];
        self.sjNonW_corr_CorrelationGroupMPFInSituUp = tree.httCandidates_sjNonW_corr_CorrelationGroupMPFInSituUp[n];
        self.sjNonW_corr_CorrelationGroupMPFInSituDown = tree.httCandidates_sjNonW_corr_CorrelationGroupMPFInSituDown[n];
        self.sjNonW_corr_CorrelationGroupIntercalibrationUp = tree.httCandidates_sjNonW_corr_CorrelationGroupIntercalibrationUp[n];
        self.sjNonW_corr_CorrelationGroupIntercalibrationDown = tree.httCandidates_sjNonW_corr_CorrelationGroupIntercalibrationDown[n];
        self.sjNonW_corr_CorrelationGroupbJESUp = tree.httCandidates_sjNonW_corr_CorrelationGroupbJESUp[n];
        self.sjNonW_corr_CorrelationGroupbJESDown = tree.httCandidates_sjNonW_corr_CorrelationGroupbJESDown[n];
        self.sjNonW_corr_CorrelationGroupFlavorUp = tree.httCandidates_sjNonW_corr_CorrelationGroupFlavorUp[n];
        self.sjNonW_corr_CorrelationGroupFlavorDown = tree.httCandidates_sjNonW_corr_CorrelationGroupFlavorDown[n];
        self.sjNonW_corr_CorrelationGroupUncorrelatedUp = tree.httCandidates_sjNonW_corr_CorrelationGroupUncorrelatedUp[n];
        self.sjNonW_corr_CorrelationGroupUncorrelatedDown = tree.httCandidates_sjNonW_corr_CorrelationGroupUncorrelatedDown[n];
        pass
    @staticmethod
    def make_array(input):
        return [httCandidates(input, i) for i in range(input.nhttCandidates)]
class GenTop:
    def __init__(self, tree, n):
        self.charge = tree.GenTop_charge[n];
        self.status = tree.GenTop_status[n];
        self.isPromptHard = tree.GenTop_isPromptHard[n];
        self.pdgId = tree.GenTop_pdgId[n];
        self.pt = tree.GenTop_pt[n];
        self.eta = tree.GenTop_eta[n];
        self.phi = tree.GenTop_phi[n];
        self.mass = tree.GenTop_mass[n];
        self.decayMode = tree.GenTop_decayMode[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenTop(input, i) for i in range(input.nGenTop)]
class GenTaus:
    def __init__(self, tree, n):
        self.charge = tree.GenTaus_charge[n];
        self.status = tree.GenTaus_status[n];
        self.isPromptHard = tree.GenTaus_isPromptHard[n];
        self.pdgId = tree.GenTaus_pdgId[n];
        self.pt = tree.GenTaus_pt[n];
        self.eta = tree.GenTaus_eta[n];
        self.phi = tree.GenTaus_phi[n];
        self.mass = tree.GenTaus_mass[n];
        self.motherId = tree.GenTaus_motherId[n];
        self.grandmotherId = tree.GenTaus_grandmotherId[n];
        self.sourceId = tree.GenTaus_sourceId[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenTaus(input, i) for i in range(input.nGenTaus)]
class trgObjects_hltMHT70:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltMHT70(input, i) for i in range(input.ntrgObjects_hltMHT70)]
class Jet:
    def __init__(self, tree, n):
        self.id = tree.Jet_id[n];
        self.puId = tree.Jet_puId[n];
        self.btagCSV = tree.Jet_btagCSV[n];
        self.btagCMVA = tree.Jet_btagCMVA[n];
        self.rawPt = tree.Jet_rawPt[n];
        self.mcPt = tree.Jet_mcPt[n];
        self.mcFlavour = tree.Jet_mcFlavour[n];
        self.partonFlavour = tree.Jet_partonFlavour[n];
        self.hadronFlavour = tree.Jet_hadronFlavour[n];
        self.mcMatchId = tree.Jet_mcMatchId[n];
        self.corr_JECUp = tree.Jet_corr_JECUp[n];
        self.corr_JECDown = tree.Jet_corr_JECDown[n];
        self.corr = tree.Jet_corr[n];
        self.corr_JERUp = tree.Jet_corr_JERUp[n];
        self.corr_JERDown = tree.Jet_corr_JERDown[n];
        self.corr_JER = tree.Jet_corr_JER[n];
        self.pt = tree.Jet_pt[n];
        self.eta = tree.Jet_eta[n];
        self.phi = tree.Jet_phi[n];
        self.mass = tree.Jet_mass[n];
        self.rawPtAfterSmearing = tree.Jet_rawPtAfterSmearing[n];
        self.idxFirstTauMatch = tree.Jet_idxFirstTauMatch[n];
        self.heppyFlavour = tree.Jet_heppyFlavour[n];
        self.ctagVsL = tree.Jet_ctagVsL[n];
        self.ctagVsB = tree.Jet_ctagVsB[n];
        self.btagBDT = tree.Jet_btagBDT[n];
        self.btagProb = tree.Jet_btagProb[n];
        self.btagBProb = tree.Jet_btagBProb[n];
        self.btagSoftEl = tree.Jet_btagSoftEl[n];
        self.btagSoftMu = tree.Jet_btagSoftMu[n];
        self.btagDeepCSVdusg = tree.Jet_btagDeepCSVdusg[n];
        self.btagDeepCSVb = tree.Jet_btagDeepCSVb[n];
        self.btagDeepCSVc = tree.Jet_btagDeepCSVc[n];
        self.btagDeepCSVbb = tree.Jet_btagDeepCSVbb[n];
        self.btagDeepCMVAdusg = tree.Jet_btagDeepCMVAdusg[n];
        self.btagDeepCMVAb = tree.Jet_btagDeepCMVAb[n];
        self.btagDeepCMVAc = tree.Jet_btagDeepCMVAc[n];
        self.btagDeepCMVAbb = tree.Jet_btagDeepCMVAbb[n];
        self.btagCSVV0 = tree.Jet_btagCSVV0[n];
        self.btagCMVAV2 = tree.Jet_btagCMVAV2[n];
        self.chHEF = tree.Jet_chHEF[n];
        self.neHEF = tree.Jet_neHEF[n];
        self.chEmEF = tree.Jet_chEmEF[n];
        self.neEmEF = tree.Jet_neEmEF[n];
        self.muEF = tree.Jet_muEF[n];
        self.chMult = tree.Jet_chMult[n];
        self.nhMult = tree.Jet_nhMult[n];
        self.leadTrackPt = tree.Jet_leadTrackPt[n];
        self.mcEta = tree.Jet_mcEta[n];
        self.mcPhi = tree.Jet_mcPhi[n];
        self.mcM = tree.Jet_mcM[n];
        self.leptonPdgId = tree.Jet_leptonPdgId[n];
        self.leptonPt = tree.Jet_leptonPt[n];
        self.leptonPtRel = tree.Jet_leptonPtRel[n];
        self.leptonPtRelInv = tree.Jet_leptonPtRelInv[n];
        self.leptonDeltaR = tree.Jet_leptonDeltaR[n];
        self.leptonDeltaPhi = tree.Jet_leptonDeltaPhi[n];
        self.leptonDeltaEta = tree.Jet_leptonDeltaEta[n];
        self.vtxMass = tree.Jet_vtxMass[n];
        self.vtxNtracks = tree.Jet_vtxNtracks[n];
        self.vtxPt = tree.Jet_vtxPt[n];
        self.vtx3DSig = tree.Jet_vtx3DSig[n];
        self.vtx3DVal = tree.Jet_vtx3DVal[n];
        self.vtxPosX = tree.Jet_vtxPosX[n];
        self.vtxPosY = tree.Jet_vtxPosY[n];
        self.vtxPosZ = tree.Jet_vtxPosZ[n];
        self.pullVectorPhi = tree.Jet_pullVectorPhi[n];
        self.pullVectorMag = tree.Jet_pullVectorMag[n];
        self.qgl = tree.Jet_qgl[n];
        self.ptd = tree.Jet_ptd[n];
        self.axis2 = tree.Jet_axis2[n];
        self.mult = tree.Jet_mult[n];
        self.numberOfDaughters = tree.Jet_numberOfDaughters[n];
        self.btagIdx = tree.Jet_btagIdx[n];
        self.btagCmvaIdx = tree.Jet_btagCmvaIdx[n];
        self.mcIdx = tree.Jet_mcIdx[n];
        self.blike_VBF = tree.Jet_blike_VBF[n];
        self.pt_puppi = tree.Jet_pt_puppi[n];
        self.pt_reg = tree.Jet_pt_reg[n];
        self.pt_regVBF = tree.Jet_pt_regVBF[n];
        self.pt_reg_corrJECUp = tree.Jet_pt_reg_corrJECUp[n];
        self.pt_regVBF_corrJECUp = tree.Jet_pt_regVBF_corrJECUp[n];
        self.pt_reg_corrJECDown = tree.Jet_pt_reg_corrJECDown[n];
        self.pt_regVBF_corrJECDown = tree.Jet_pt_regVBF_corrJECDown[n];
        self.pt_reg_corrJERUp = tree.Jet_pt_reg_corrJERUp[n];
        self.pt_regVBF_corrJERUp = tree.Jet_pt_regVBF_corrJERUp[n];
        self.pt_reg_corrJERDown = tree.Jet_pt_reg_corrJERDown[n];
        self.pt_regVBF_corrJERDown = tree.Jet_pt_regVBF_corrJERDown[n];
        self.btagCSVL_SF = tree.Jet_btagCSVL_SF[n];
        self.btagCSVL_SF_up = tree.Jet_btagCSVL_SF_up[n];
        self.btagCSVL_SF_down = tree.Jet_btagCSVL_SF_down[n];
        self.btagCSVM_SF = tree.Jet_btagCSVM_SF[n];
        self.btagCSVM_SF_up = tree.Jet_btagCSVM_SF_up[n];
        self.btagCSVM_SF_down = tree.Jet_btagCSVM_SF_down[n];
        self.btagCSVT_SF = tree.Jet_btagCSVT_SF[n];
        self.btagCSVT_SF_up = tree.Jet_btagCSVT_SF_up[n];
        self.btagCSVT_SF_down = tree.Jet_btagCSVT_SF_down[n];
        self.btagWeightCSV = tree.Jet_btagWeightCSV[n];
        self.btagWeightCSV_up_jes = tree.Jet_btagWeightCSV_up_jes[n];
        self.btagWeightCSV_down_jes = tree.Jet_btagWeightCSV_down_jes[n];
        self.btagWeightCSV_up_lf = tree.Jet_btagWeightCSV_up_lf[n];
        self.btagWeightCSV_down_lf = tree.Jet_btagWeightCSV_down_lf[n];
        self.btagWeightCSV_up_hf = tree.Jet_btagWeightCSV_up_hf[n];
        self.btagWeightCSV_down_hf = tree.Jet_btagWeightCSV_down_hf[n];
        self.btagWeightCSV_up_hfstats1 = tree.Jet_btagWeightCSV_up_hfstats1[n];
        self.btagWeightCSV_down_hfstats1 = tree.Jet_btagWeightCSV_down_hfstats1[n];
        self.btagWeightCSV_up_hfstats2 = tree.Jet_btagWeightCSV_up_hfstats2[n];
        self.btagWeightCSV_down_hfstats2 = tree.Jet_btagWeightCSV_down_hfstats2[n];
        self.btagWeightCSV_up_lfstats1 = tree.Jet_btagWeightCSV_up_lfstats1[n];
        self.btagWeightCSV_down_lfstats1 = tree.Jet_btagWeightCSV_down_lfstats1[n];
        self.btagWeightCSV_up_lfstats2 = tree.Jet_btagWeightCSV_up_lfstats2[n];
        self.btagWeightCSV_down_lfstats2 = tree.Jet_btagWeightCSV_down_lfstats2[n];
        self.btagWeightCSV_up_cferr1 = tree.Jet_btagWeightCSV_up_cferr1[n];
        self.btagWeightCSV_down_cferr1 = tree.Jet_btagWeightCSV_down_cferr1[n];
        self.btagWeightCSV_up_cferr2 = tree.Jet_btagWeightCSV_up_cferr2[n];
        self.btagWeightCSV_down_cferr2 = tree.Jet_btagWeightCSV_down_cferr2[n];
        self.btagCMVAV2L_SF = tree.Jet_btagCMVAV2L_SF[n];
        self.btagCMVAV2L_SF_up = tree.Jet_btagCMVAV2L_SF_up[n];
        self.btagCMVAV2L_SF_down = tree.Jet_btagCMVAV2L_SF_down[n];
        self.btagCMVAV2M_SF = tree.Jet_btagCMVAV2M_SF[n];
        self.btagCMVAV2M_SF_up = tree.Jet_btagCMVAV2M_SF_up[n];
        self.btagCMVAV2M_SF_down = tree.Jet_btagCMVAV2M_SF_down[n];
        self.btagCMVAV2T_SF = tree.Jet_btagCMVAV2T_SF[n];
        self.btagCMVAV2T_SF_up = tree.Jet_btagCMVAV2T_SF_up[n];
        self.btagCMVAV2T_SF_down = tree.Jet_btagCMVAV2T_SF_down[n];
        self.btagWeightCMVAV2 = tree.Jet_btagWeightCMVAV2[n];
        self.btagWeightCMVAV2_up_jes = tree.Jet_btagWeightCMVAV2_up_jes[n];
        self.btagWeightCMVAV2_down_jes = tree.Jet_btagWeightCMVAV2_down_jes[n];
        self.btagWeightCMVAV2_up_lf = tree.Jet_btagWeightCMVAV2_up_lf[n];
        self.btagWeightCMVAV2_down_lf = tree.Jet_btagWeightCMVAV2_down_lf[n];
        self.btagWeightCMVAV2_up_hf = tree.Jet_btagWeightCMVAV2_up_hf[n];
        self.btagWeightCMVAV2_down_hf = tree.Jet_btagWeightCMVAV2_down_hf[n];
        self.btagWeightCMVAV2_up_hfstats1 = tree.Jet_btagWeightCMVAV2_up_hfstats1[n];
        self.btagWeightCMVAV2_down_hfstats1 = tree.Jet_btagWeightCMVAV2_down_hfstats1[n];
        self.btagWeightCMVAV2_up_hfstats2 = tree.Jet_btagWeightCMVAV2_up_hfstats2[n];
        self.btagWeightCMVAV2_down_hfstats2 = tree.Jet_btagWeightCMVAV2_down_hfstats2[n];
        self.btagWeightCMVAV2_up_lfstats1 = tree.Jet_btagWeightCMVAV2_up_lfstats1[n];
        self.btagWeightCMVAV2_down_lfstats1 = tree.Jet_btagWeightCMVAV2_down_lfstats1[n];
        self.btagWeightCMVAV2_up_lfstats2 = tree.Jet_btagWeightCMVAV2_up_lfstats2[n];
        self.btagWeightCMVAV2_down_lfstats2 = tree.Jet_btagWeightCMVAV2_down_lfstats2[n];
        self.btagWeightCMVAV2_up_cferr1 = tree.Jet_btagWeightCMVAV2_up_cferr1[n];
        self.btagWeightCMVAV2_down_cferr1 = tree.Jet_btagWeightCMVAV2_down_cferr1[n];
        self.btagWeightCMVAV2_up_cferr2 = tree.Jet_btagWeightCMVAV2_up_cferr2[n];
        self.btagWeightCMVAV2_down_cferr2 = tree.Jet_btagWeightCMVAV2_down_cferr2[n];
        self.corr_AbsoluteStatUp = tree.Jet_corr_AbsoluteStatUp[n];
        self.corr_AbsoluteStatDown = tree.Jet_corr_AbsoluteStatDown[n];
        self.corr_AbsoluteScaleUp = tree.Jet_corr_AbsoluteScaleUp[n];
        self.corr_AbsoluteScaleDown = tree.Jet_corr_AbsoluteScaleDown[n];
        self.corr_AbsoluteFlavMapUp = tree.Jet_corr_AbsoluteFlavMapUp[n];
        self.corr_AbsoluteFlavMapDown = tree.Jet_corr_AbsoluteFlavMapDown[n];
        self.corr_AbsoluteMPFBiasUp = tree.Jet_corr_AbsoluteMPFBiasUp[n];
        self.corr_AbsoluteMPFBiasDown = tree.Jet_corr_AbsoluteMPFBiasDown[n];
        self.corr_FragmentationUp = tree.Jet_corr_FragmentationUp[n];
        self.corr_FragmentationDown = tree.Jet_corr_FragmentationDown[n];
        self.corr_SinglePionECALUp = tree.Jet_corr_SinglePionECALUp[n];
        self.corr_SinglePionECALDown = tree.Jet_corr_SinglePionECALDown[n];
        self.corr_SinglePionHCALUp = tree.Jet_corr_SinglePionHCALUp[n];
        self.corr_SinglePionHCALDown = tree.Jet_corr_SinglePionHCALDown[n];
        self.corr_FlavorQCDUp = tree.Jet_corr_FlavorQCDUp[n];
        self.corr_FlavorQCDDown = tree.Jet_corr_FlavorQCDDown[n];
        self.corr_TimePtEtaUp = tree.Jet_corr_TimePtEtaUp[n];
        self.corr_TimePtEtaDown = tree.Jet_corr_TimePtEtaDown[n];
        self.corr_RelativeJEREC1Up = tree.Jet_corr_RelativeJEREC1Up[n];
        self.corr_RelativeJEREC1Down = tree.Jet_corr_RelativeJEREC1Down[n];
        self.corr_RelativeJEREC2Up = tree.Jet_corr_RelativeJEREC2Up[n];
        self.corr_RelativeJEREC2Down = tree.Jet_corr_RelativeJEREC2Down[n];
        self.corr_RelativeJERHFUp = tree.Jet_corr_RelativeJERHFUp[n];
        self.corr_RelativeJERHFDown = tree.Jet_corr_RelativeJERHFDown[n];
        self.corr_RelativePtBBUp = tree.Jet_corr_RelativePtBBUp[n];
        self.corr_RelativePtBBDown = tree.Jet_corr_RelativePtBBDown[n];
        self.corr_RelativePtEC1Up = tree.Jet_corr_RelativePtEC1Up[n];
        self.corr_RelativePtEC1Down = tree.Jet_corr_RelativePtEC1Down[n];
        self.corr_RelativePtEC2Up = tree.Jet_corr_RelativePtEC2Up[n];
        self.corr_RelativePtEC2Down = tree.Jet_corr_RelativePtEC2Down[n];
        self.corr_RelativePtHFUp = tree.Jet_corr_RelativePtHFUp[n];
        self.corr_RelativePtHFDown = tree.Jet_corr_RelativePtHFDown[n];
        self.corr_RelativeBalUp = tree.Jet_corr_RelativeBalUp[n];
        self.corr_RelativeBalDown = tree.Jet_corr_RelativeBalDown[n];
        self.corr_RelativeFSRUp = tree.Jet_corr_RelativeFSRUp[n];
        self.corr_RelativeFSRDown = tree.Jet_corr_RelativeFSRDown[n];
        self.corr_RelativeStatFSRUp = tree.Jet_corr_RelativeStatFSRUp[n];
        self.corr_RelativeStatFSRDown = tree.Jet_corr_RelativeStatFSRDown[n];
        self.corr_RelativeStatECUp = tree.Jet_corr_RelativeStatECUp[n];
        self.corr_RelativeStatECDown = tree.Jet_corr_RelativeStatECDown[n];
        self.corr_RelativeStatHFUp = tree.Jet_corr_RelativeStatHFUp[n];
        self.corr_RelativeStatHFDown = tree.Jet_corr_RelativeStatHFDown[n];
        self.corr_PileUpDataMCUp = tree.Jet_corr_PileUpDataMCUp[n];
        self.corr_PileUpDataMCDown = tree.Jet_corr_PileUpDataMCDown[n];
        self.corr_PileUpPtRefUp = tree.Jet_corr_PileUpPtRefUp[n];
        self.corr_PileUpPtRefDown = tree.Jet_corr_PileUpPtRefDown[n];
        self.corr_PileUpPtBBUp = tree.Jet_corr_PileUpPtBBUp[n];
        self.corr_PileUpPtBBDown = tree.Jet_corr_PileUpPtBBDown[n];
        self.corr_PileUpPtEC1Up = tree.Jet_corr_PileUpPtEC1Up[n];
        self.corr_PileUpPtEC1Down = tree.Jet_corr_PileUpPtEC1Down[n];
        self.corr_PileUpPtEC2Up = tree.Jet_corr_PileUpPtEC2Up[n];
        self.corr_PileUpPtEC2Down = tree.Jet_corr_PileUpPtEC2Down[n];
        self.corr_PileUpPtHFUp = tree.Jet_corr_PileUpPtHFUp[n];
        self.corr_PileUpPtHFDown = tree.Jet_corr_PileUpPtHFDown[n];
        self.corr_PileUpMuZeroUp = tree.Jet_corr_PileUpMuZeroUp[n];
        self.corr_PileUpMuZeroDown = tree.Jet_corr_PileUpMuZeroDown[n];
        self.corr_PileUpEnvelopeUp = tree.Jet_corr_PileUpEnvelopeUp[n];
        self.corr_PileUpEnvelopeDown = tree.Jet_corr_PileUpEnvelopeDown[n];
        self.corr_SubTotalPileUpUp = tree.Jet_corr_SubTotalPileUpUp[n];
        self.corr_SubTotalPileUpDown = tree.Jet_corr_SubTotalPileUpDown[n];
        self.corr_SubTotalRelativeUp = tree.Jet_corr_SubTotalRelativeUp[n];
        self.corr_SubTotalRelativeDown = tree.Jet_corr_SubTotalRelativeDown[n];
        self.corr_SubTotalPtUp = tree.Jet_corr_SubTotalPtUp[n];
        self.corr_SubTotalPtDown = tree.Jet_corr_SubTotalPtDown[n];
        self.corr_SubTotalScaleUp = tree.Jet_corr_SubTotalScaleUp[n];
        self.corr_SubTotalScaleDown = tree.Jet_corr_SubTotalScaleDown[n];
        self.corr_SubTotalAbsoluteUp = tree.Jet_corr_SubTotalAbsoluteUp[n];
        self.corr_SubTotalAbsoluteDown = tree.Jet_corr_SubTotalAbsoluteDown[n];
        self.corr_SubTotalMCUp = tree.Jet_corr_SubTotalMCUp[n];
        self.corr_SubTotalMCDown = tree.Jet_corr_SubTotalMCDown[n];
        self.corr_TotalUp = tree.Jet_corr_TotalUp[n];
        self.corr_TotalDown = tree.Jet_corr_TotalDown[n];
        self.corr_TotalNoFlavorUp = tree.Jet_corr_TotalNoFlavorUp[n];
        self.corr_TotalNoFlavorDown = tree.Jet_corr_TotalNoFlavorDown[n];
        self.corr_TotalNoTimeUp = tree.Jet_corr_TotalNoTimeUp[n];
        self.corr_TotalNoTimeDown = tree.Jet_corr_TotalNoTimeDown[n];
        self.corr_TotalNoFlavorNoTimeUp = tree.Jet_corr_TotalNoFlavorNoTimeUp[n];
        self.corr_TotalNoFlavorNoTimeDown = tree.Jet_corr_TotalNoFlavorNoTimeDown[n];
        self.corr_FlavorZJetUp = tree.Jet_corr_FlavorZJetUp[n];
        self.corr_FlavorZJetDown = tree.Jet_corr_FlavorZJetDown[n];
        self.corr_FlavorPhotonJetUp = tree.Jet_corr_FlavorPhotonJetUp[n];
        self.corr_FlavorPhotonJetDown = tree.Jet_corr_FlavorPhotonJetDown[n];
        self.corr_FlavorPureGluonUp = tree.Jet_corr_FlavorPureGluonUp[n];
        self.corr_FlavorPureGluonDown = tree.Jet_corr_FlavorPureGluonDown[n];
        self.corr_FlavorPureQuarkUp = tree.Jet_corr_FlavorPureQuarkUp[n];
        self.corr_FlavorPureQuarkDown = tree.Jet_corr_FlavorPureQuarkDown[n];
        self.corr_FlavorPureCharmUp = tree.Jet_corr_FlavorPureCharmUp[n];
        self.corr_FlavorPureCharmDown = tree.Jet_corr_FlavorPureCharmDown[n];
        self.corr_FlavorPureBottomUp = tree.Jet_corr_FlavorPureBottomUp[n];
        self.corr_FlavorPureBottomDown = tree.Jet_corr_FlavorPureBottomDown[n];
        self.corr_TimeRunBCDUp = tree.Jet_corr_TimeRunBCDUp[n];
        self.corr_TimeRunBCDDown = tree.Jet_corr_TimeRunBCDDown[n];
        self.corr_TimeRunEFUp = tree.Jet_corr_TimeRunEFUp[n];
        self.corr_TimeRunEFDown = tree.Jet_corr_TimeRunEFDown[n];
        self.corr_TimeRunGUp = tree.Jet_corr_TimeRunGUp[n];
        self.corr_TimeRunGDown = tree.Jet_corr_TimeRunGDown[n];
        self.corr_TimeRunHUp = tree.Jet_corr_TimeRunHUp[n];
        self.corr_TimeRunHDown = tree.Jet_corr_TimeRunHDown[n];
        self.corr_CorrelationGroupMPFInSituUp = tree.Jet_corr_CorrelationGroupMPFInSituUp[n];
        self.corr_CorrelationGroupMPFInSituDown = tree.Jet_corr_CorrelationGroupMPFInSituDown[n];
        self.corr_CorrelationGroupIntercalibrationUp = tree.Jet_corr_CorrelationGroupIntercalibrationUp[n];
        self.corr_CorrelationGroupIntercalibrationDown = tree.Jet_corr_CorrelationGroupIntercalibrationDown[n];
        self.corr_CorrelationGroupbJESUp = tree.Jet_corr_CorrelationGroupbJESUp[n];
        self.corr_CorrelationGroupbJESDown = tree.Jet_corr_CorrelationGroupbJESDown[n];
        self.corr_CorrelationGroupFlavorUp = tree.Jet_corr_CorrelationGroupFlavorUp[n];
        self.corr_CorrelationGroupFlavorDown = tree.Jet_corr_CorrelationGroupFlavorDown[n];
        self.corr_CorrelationGroupUncorrelatedUp = tree.Jet_corr_CorrelationGroupUncorrelatedUp[n];
        self.corr_CorrelationGroupUncorrelatedDown = tree.Jet_corr_CorrelationGroupUncorrelatedDown[n];
        pass
    @staticmethod
    def make_array(input):
        return [Jet(input, i) for i in range(input.nJet)]
class FatjetCA15softdrop:
    def __init__(self, tree, n):
        self.pt = tree.FatjetCA15softdrop_pt[n];
        self.eta = tree.FatjetCA15softdrop_eta[n];
        self.phi = tree.FatjetCA15softdrop_phi[n];
        self.mass = tree.FatjetCA15softdrop_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [FatjetCA15softdrop(input, i) for i in range(input.nFatjetCA15softdrop)]
class trgObjects_hltPFTripleJetLooseID64:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltPFTripleJetLooseID64(input, i) for i in range(input.ntrgObjects_hltPFTripleJetLooseID64)]
class LHE_weights_pdf:
    def __init__(self, tree, n):
        self.id = tree.LHE_weights_pdf_id[n];
        self.wgt = tree.LHE_weights_pdf_wgt[n];
        pass
    @staticmethod
    def make_array(input):
        return [LHE_weights_pdf(input, i) for i in range(input.nLHE_weights_pdf)]
class trgObjects_caloMhtNoPU:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_caloMhtNoPU_pt[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_caloMhtNoPU(input, i) for i in range(input.ntrgObjects_caloMhtNoPU)]
class GenLep:
    def __init__(self, tree, n):
        self.charge = tree.GenLep_charge[n];
        self.status = tree.GenLep_status[n];
        self.isPromptHard = tree.GenLep_isPromptHard[n];
        self.pdgId = tree.GenLep_pdgId[n];
        self.pt = tree.GenLep_pt[n];
        self.eta = tree.GenLep_eta[n];
        self.phi = tree.GenLep_phi[n];
        self.mass = tree.GenLep_mass[n];
        self.motherId = tree.GenLep_motherId[n];
        self.grandmotherId = tree.GenLep_grandmotherId[n];
        self.sourceId = tree.GenLep_sourceId[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenLep(input, i) for i in range(input.nGenLep)]
class GenGluonFromTop:
    def __init__(self, tree, n):
        self.pdgId = tree.GenGluonFromTop_pdgId[n];
        self.pt = tree.GenGluonFromTop_pt[n];
        self.eta = tree.GenGluonFromTop_eta[n];
        self.phi = tree.GenGluonFromTop_phi[n];
        self.mass = tree.GenGluonFromTop_mass[n];
        self.charge = tree.GenGluonFromTop_charge[n];
        self.status = tree.GenGluonFromTop_status[n];
        self.isPromptHard = tree.GenGluonFromTop_isPromptHard[n];
        pass
    @staticmethod
    def make_array(input):
        return [GenGluonFromTop(input, i) for i in range(input.nGenGluonFromTop)]
class softActivityJets:
    def __init__(self, tree, n):
        self.pt = tree.softActivityJets_pt[n];
        self.eta = tree.softActivityJets_eta[n];
        self.phi = tree.softActivityJets_phi[n];
        self.mass = tree.softActivityJets_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [softActivityJets(input, i) for i in range(input.nsoftActivityJets)]
class FatjetCA15subjetfiltered:
    def __init__(self, tree, n):
        self.pt = tree.FatjetCA15subjetfiltered_pt[n];
        self.eta = tree.FatjetCA15subjetfiltered_eta[n];
        self.phi = tree.FatjetCA15subjetfiltered_phi[n];
        self.mass = tree.FatjetCA15subjetfiltered_mass[n];
        pass
    @staticmethod
    def make_array(input):
        return [FatjetCA15subjetfiltered(input, i) for i in range(input.nFatjetCA15subjetfiltered)]
class trgObjects_hltSingleJet80:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltSingleJet80(input, i) for i in range(input.ntrgObjects_hltSingleJet80)]
class l1MHT:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "l1MHT_pt", None)
        _phi = getattr(tree, "l1MHT_phi", None)
        return l1MHT(_pt, _phi)
    def __init__(self, pt,phi):
        self.pt = pt #
        self.phi = phi #
        pass
class HCMVAV2_reg_corrJECDown:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCMVAV2_reg_corrJECDown_pt", None)
        _eta = getattr(tree, "HCMVAV2_reg_corrJECDown_eta", None)
        _phi = getattr(tree, "HCMVAV2_reg_corrJECDown_phi", None)
        _mass = getattr(tree, "HCMVAV2_reg_corrJECDown_mass", None)
        return HCMVAV2_reg_corrJECDown(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class HCMVAV2_reg_corrJERDown:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCMVAV2_reg_corrJERDown_pt", None)
        _eta = getattr(tree, "HCMVAV2_reg_corrJERDown_eta", None)
        _phi = getattr(tree, "HCMVAV2_reg_corrJERDown_phi", None)
        _mass = getattr(tree, "HCMVAV2_reg_corrJERDown_mass", None)
        return HCMVAV2_reg_corrJERDown(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class l1MET:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "l1MET_pt", None)
        _phi = getattr(tree, "l1MET_phi", None)
        return l1MET(_pt, _phi)
    def __init__(self, pt,phi):
        self.pt = pt #
        self.phi = phi #
        pass
class V:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "V_pt", None)
        _eta = getattr(tree, "V_eta", None)
        _phi = getattr(tree, "V_phi", None)
        _mass = getattr(tree, "V_mass", None)
        return V(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class H_reg:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "H_reg_pt", None)
        _eta = getattr(tree, "H_reg_eta", None)
        _phi = getattr(tree, "H_reg_phi", None)
        _mass = getattr(tree, "H_reg_mass", None)
        return H_reg(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class HCSV_reg_corrJERDown:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCSV_reg_corrJERDown_pt", None)
        _eta = getattr(tree, "HCSV_reg_corrJERDown_eta", None)
        _phi = getattr(tree, "HCSV_reg_corrJERDown_phi", None)
        _mass = getattr(tree, "HCSV_reg_corrJERDown_mass", None)
        return HCSV_reg_corrJERDown(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class HCSV:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCSV_pt", None)
        _eta = getattr(tree, "HCSV_eta", None)
        _phi = getattr(tree, "HCSV_phi", None)
        _mass = getattr(tree, "HCSV_mass", None)
        return HCSV(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class l1HT:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "l1HT_pt", None)
        _phi = getattr(tree, "l1HT_phi", None)
        return l1HT(_pt, _phi)
    def __init__(self, pt,phi):
        self.pt = pt #
        self.phi = phi #
        pass
class fakeMET:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "fakeMET_pt", None)
        _eta = getattr(tree, "fakeMET_eta", None)
        _phi = getattr(tree, "fakeMET_phi", None)
        _mass = getattr(tree, "fakeMET_mass", None)
        return fakeMET(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class HCSV_reg_corrJERUp:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCSV_reg_corrJERUp_pt", None)
        _eta = getattr(tree, "HCSV_reg_corrJERUp_eta", None)
        _phi = getattr(tree, "HCSV_reg_corrJERUp_phi", None)
        _mass = getattr(tree, "HCSV_reg_corrJERUp_mass", None)
        return HCSV_reg_corrJERUp(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class HCMVAV2_reg_corrJERUp:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCMVAV2_reg_corrJERUp_pt", None)
        _eta = getattr(tree, "HCMVAV2_reg_corrJERUp_eta", None)
        _phi = getattr(tree, "HCMVAV2_reg_corrJERUp_phi", None)
        _mass = getattr(tree, "HCMVAV2_reg_corrJERUp_mass", None)
        return HCMVAV2_reg_corrJERUp(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class HCSV_reg_corrJECUp:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCSV_reg_corrJECUp_pt", None)
        _eta = getattr(tree, "HCSV_reg_corrJECUp_eta", None)
        _phi = getattr(tree, "HCSV_reg_corrJECUp_phi", None)
        _mass = getattr(tree, "HCSV_reg_corrJECUp_mass", None)
        return HCSV_reg_corrJECUp(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class met_shifted_UnclusteredEnUp:
    """
    
    """
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
    """
    
    """
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
class HCSV_reg:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCSV_reg_pt", None)
        _eta = getattr(tree, "HCSV_reg_eta", None)
        _phi = getattr(tree, "HCSV_reg_phi", None)
        _mass = getattr(tree, "HCSV_reg_mass", None)
        return HCSV_reg(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class H_reg_corrJERUp:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "H_reg_corrJERUp_pt", None)
        _eta = getattr(tree, "H_reg_corrJERUp_eta", None)
        _phi = getattr(tree, "H_reg_corrJERUp_phi", None)
        _mass = getattr(tree, "H_reg_corrJERUp_mass", None)
        return H_reg_corrJERUp(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class H_reg_corrJECUp:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "H_reg_corrJECUp_pt", None)
        _eta = getattr(tree, "H_reg_corrJECUp_eta", None)
        _phi = getattr(tree, "H_reg_corrJECUp_phi", None)
        _mass = getattr(tree, "H_reg_corrJECUp_mass", None)
        return H_reg_corrJECUp(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class HCMVAV2_reg:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCMVAV2_reg_pt", None)
        _eta = getattr(tree, "HCMVAV2_reg_eta", None)
        _phi = getattr(tree, "HCMVAV2_reg_phi", None)
        _mass = getattr(tree, "HCMVAV2_reg_mass", None)
        return HCMVAV2_reg(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class H:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "H_pt", None)
        _eta = getattr(tree, "H_eta", None)
        _phi = getattr(tree, "H_phi", None)
        _mass = getattr(tree, "H_mass", None)
        return H(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class softActivityVH:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _njets2 = getattr(tree, "softActivityVH_njets2", None)
        _njets5 = getattr(tree, "softActivityVH_njets5", None)
        _njets10 = getattr(tree, "softActivityVH_njets10", None)
        _HT = getattr(tree, "softActivityVH_HT", None)
        return softActivityVH(_njets2, _njets5, _njets10, _HT)
    def __init__(self, njets2,njets5,njets10,HT):
        self.njets2 = njets2 #number of jets from soft activity with pt>2Gev
        self.njets5 = njets5 #number of jets from soft activity with pt>5Gev
        self.njets10 = njets10 #number of jets from soft activity with pt>10Gev
        self.HT = HT #sum pt of sa jets
        pass
class met_shifted_JetResUp:
    """
    
    """
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
class met:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "met_pt", None)
        _eta = getattr(tree, "met_eta", None)
        _phi = getattr(tree, "met_phi", None)
        _mass = getattr(tree, "met_mass", None)
        _sumEt = getattr(tree, "met_sumEt", None)
        _rawPt = getattr(tree, "met_rawPt", None)
        _rawPhi = getattr(tree, "met_rawPhi", None)
        _rawSumEt = getattr(tree, "met_rawSumEt", None)
        _genPt = getattr(tree, "met_genPt", None)
        _genPhi = getattr(tree, "met_genPhi", None)
        _genEta = getattr(tree, "met_genEta", None)
        return met(_pt, _eta, _phi, _mass, _sumEt, _rawPt, _rawPhi, _rawSumEt, _genPt, _genPhi, _genEta)
    def __init__(self, pt,eta,phi,mass,sumEt,rawPt,rawPhi,rawSumEt,genPt,genPhi,genEta):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        self.sumEt = sumEt #
        self.rawPt = rawPt #
        self.rawPhi = rawPhi #
        self.rawSumEt = rawSumEt #
        self.genPt = genPt #
        self.genPhi = genPhi #
        self.genEta = genEta #
        pass
class met_shifted_JetEnUp:
    """
    
    """
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
    """
    
    """
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
    """
    
    """
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
    """
    
    """
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
    """
    
    """
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
    """
    
    """
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
    """
    
    """
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
    """
    
    """
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
class l1ET:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "l1ET_pt", None)
        _phi = getattr(tree, "l1ET_phi", None)
        return l1ET(_pt, _phi)
    def __init__(self, pt,phi):
        self.pt = pt #
        self.phi = phi #
        pass
class softActivityEWK:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _njets2 = getattr(tree, "softActivityEWK_njets2", None)
        _njets5 = getattr(tree, "softActivityEWK_njets5", None)
        _njets10 = getattr(tree, "softActivityEWK_njets10", None)
        _HT = getattr(tree, "softActivityEWK_HT", None)
        return softActivityEWK(_njets2, _njets5, _njets10, _HT)
    def __init__(self, njets2,njets5,njets10,HT):
        self.njets2 = njets2 #number of jets from soft activity with pt>2Gev
        self.njets5 = njets5 #number of jets from soft activity with pt>5Gev
        self.njets10 = njets10 #number of jets from soft activity with pt>10Gev
        self.HT = HT #sum pt of sa jets
        pass
class met_shifted_JetResDown:
    """
    
    """
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
class HaddJetsdR08:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HaddJetsdR08_pt", None)
        _eta = getattr(tree, "HaddJetsdR08_eta", None)
        _phi = getattr(tree, "HaddJetsdR08_phi", None)
        _mass = getattr(tree, "HaddJetsdR08_mass", None)
        return HaddJetsdR08(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class H_reg_corrJERDown:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "H_reg_corrJERDown_pt", None)
        _eta = getattr(tree, "H_reg_corrJERDown_eta", None)
        _phi = getattr(tree, "H_reg_corrJERDown_phi", None)
        _mass = getattr(tree, "H_reg_corrJERDown_mass", None)
        return H_reg_corrJERDown(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class HCMVAV2_reg_corrJECUp:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCMVAV2_reg_corrJECUp_pt", None)
        _eta = getattr(tree, "HCMVAV2_reg_corrJECUp_eta", None)
        _phi = getattr(tree, "HCMVAV2_reg_corrJECUp_phi", None)
        _mass = getattr(tree, "HCMVAV2_reg_corrJECUp_mass", None)
        return HCMVAV2_reg_corrJECUp(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class softActivity:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _njets2 = getattr(tree, "softActivity_njets2", None)
        _njets5 = getattr(tree, "softActivity_njets5", None)
        _njets10 = getattr(tree, "softActivity_njets10", None)
        _HT = getattr(tree, "softActivity_HT", None)
        return softActivity(_njets2, _njets5, _njets10, _HT)
    def __init__(self, njets2,njets5,njets10,HT):
        self.njets2 = njets2 #number of jets from soft activity with pt>2Gev
        self.njets5 = njets5 #number of jets from soft activity with pt>5Gev
        self.njets10 = njets10 #number of jets from soft activity with pt>10Gev
        self.HT = HT #sum pt of sa jets
        pass
class HCSV_reg_corrJECDown:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCSV_reg_corrJECDown_pt", None)
        _eta = getattr(tree, "HCSV_reg_corrJECDown_eta", None)
        _phi = getattr(tree, "HCSV_reg_corrJECDown_phi", None)
        _mass = getattr(tree, "HCSV_reg_corrJECDown_mass", None)
        return HCSV_reg_corrJECDown(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class HCMVAV2:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "HCMVAV2_pt", None)
        _eta = getattr(tree, "HCMVAV2_eta", None)
        _phi = getattr(tree, "HCMVAV2_phi", None)
        _mass = getattr(tree, "HCMVAV2_mass", None)
        return HCMVAV2(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass
class H_reg_corrJECDown:
    """
    
    """
    @staticmethod
    def make_obj(tree):
        _pt = getattr(tree, "H_reg_corrJECDown_pt", None)
        _eta = getattr(tree, "H_reg_corrJECDown_eta", None)
        _phi = getattr(tree, "H_reg_corrJECDown_phi", None)
        _mass = getattr(tree, "H_reg_corrJECDown_mass", None)
        return H_reg_corrJECDown(_pt, _eta, _phi, _mass)
    def __init__(self, pt,eta,phi,mass):
        self.pt = pt #
        self.eta = eta #
        self.phi = phi #
        self.mass = mass #
        pass

from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
class EventAnalyzer(Analyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
    def process(self, event):
        event.pileUpVertex_ptHat = pileUpVertex_ptHat.make_array(event.input)
        event.trgObjects_hltMET70 = trgObjects_hltMET70.make_array(event.input)
        event.trgObjects_hltL1sTripleJetVBFIorHTTIorDoubleJetCIorSingleJet = trgObjects_hltL1sTripleJetVBFIorHTTIorDoubleJetCIorSingleJet.make_array(event.input)
        event.trgObjects_hltBTagPFCSVp11DoubleWithMatching = trgObjects_hltBTagPFCSVp11DoubleWithMatching.make_array(event.input)
        event.GenLepFromTop = GenLepFromTop.make_array(event.input)
        event.ajidxaddJetsdR08 = ajidxaddJetsdR08.make_array(event.input)
        event.SubjetCA15softdrop = SubjetCA15softdrop.make_array(event.input)
        event.trgObjects_hltIsoMu20 = trgObjects_hltIsoMu20.make_array(event.input)
        event.aJCMVAV2idx = aJCMVAV2idx.make_array(event.input)
        event.trgObjects_hltQuadCentralJet30 = trgObjects_hltQuadCentralJet30.make_array(event.input)
        event.l1EGammas = l1EGammas.make_array(event.input)
        event.hJidx_sortcsv = hJidx_sortcsv.make_array(event.input)
        event.primaryVertices = primaryVertices.make_array(event.input)
        event.aJCidx = aJCidx.make_array(event.input)
        event.SubjetCA15softdropz2b1 = SubjetCA15softdropz2b1.make_array(event.input)
        event.hJCidx = hJCidx.make_array(event.input)
        event.l1Taus = l1Taus.make_array(event.input)
        event.aJidx = aJidx.make_array(event.input)
        event.GenBQuarkFromTop = GenBQuarkFromTop.make_array(event.input)
        event.GenLepFromTau = GenLepFromTau.make_array(event.input)
        event.GenHiggsBoson = GenHiggsBoson.make_array(event.input)
        event.GenNuFromTop = GenNuFromTop.make_array(event.input)
        event.GenBQuarkFromHafterISR = GenBQuarkFromHafterISR.make_array(event.input)
        event.trgObjects_hltPFDoubleJetLooseID76 = trgObjects_hltPFDoubleJetLooseID76.make_array(event.input)
        event.trgObjects_hltBTagPFCSVp016SingleWithMatching = trgObjects_hltBTagPFCSVp016SingleWithMatching.make_array(event.input)
        event.softActivityEWKJets = softActivityEWKJets.make_array(event.input)
        event.HTXSRivetProducer_cat0 = HTXSRivetProducer_cat0.make_array(event.input)
        event.HTXSRivetProducer_cat1 = HTXSRivetProducer_cat1.make_array(event.input)
        event.softActivityVHJets = softActivityVHJets.make_array(event.input)
        event.trgObjects_hltQuadPFCentralJetLooseID30 = trgObjects_hltQuadPFCentralJetLooseID30.make_array(event.input)
        event.GenNu = GenNu.make_array(event.input)
        event.trgObjects_hltBTagCaloCSVp087Triple = trgObjects_hltBTagCaloCSVp087Triple.make_array(event.input)
        event.trgObjects_hltEle25eta2p1WPLoose = trgObjects_hltEle25eta2p1WPLoose.make_array(event.input)
        event.SubjetAK08softdrop = SubjetAK08softdrop.make_array(event.input)
        event.GenLepRecovered = GenLepRecovered.make_array(event.input)
        event.trgObjects_caloJets = trgObjects_caloJets.make_array(event.input)
        event.hJCMVAV2idx = hJCMVAV2idx.make_array(event.input)
        event.trgObjects_hltPFSingleJetLooseID92 = trgObjects_hltPFSingleJetLooseID92.make_array(event.input)
        event.GenHadTaus = GenHadTaus.make_array(event.input)
        event.trgObjects_hltDoubleCentralJet90 = trgObjects_hltDoubleCentralJet90.make_array(event.input)
        event.trgObjects_hltL1sETM50ToETM100IorETM60Jet60dPhiMin0p4IorDoubleJetC60ETM60 = trgObjects_hltL1sETM50ToETM100IorETM60Jet60dPhiMin0p4IorDoubleJetC60ETM60.make_array(event.input)
        event.trgObjects_hltEle25WPTight = trgObjects_hltEle25WPTight.make_array(event.input)
        event.GenVbosonsRecovered = GenVbosonsRecovered.make_array(event.input)
        event.SubjetCA15subjetfiltered = SubjetCA15subjetfiltered.make_array(event.input)
        event.LHE_weights_pdf_eigen = LHE_weights_pdf_eigen.make_array(event.input)
        event.vLeptons = vLeptons.make_array(event.input)
        event.trgObjects_hltBTagCaloCSVp014DoubleWithMatching = trgObjects_hltBTagCaloCSVp014DoubleWithMatching.make_array(event.input)
        event.pileUpVertex_z = pileUpVertex_z.make_array(event.input)
        event.trgObjects_pfJets = trgObjects_pfJets.make_array(event.input)
        event.trgObjects_pfMht = trgObjects_pfMht.make_array(event.input)
        event.LHE_weights_scale = LHE_weights_scale.make_array(event.input)
        event.trgObjects_hltL1sQuadJetCIorTripleJetVBFIorHTT = trgObjects_hltL1sQuadJetCIorTripleJetVBFIorHTT.make_array(event.input)
        event.FatjetCA15pruned = FatjetCA15pruned.make_array(event.input)
        event.trgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5 = trgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5.make_array(event.input)
        event.trgObjects_caloMht = trgObjects_caloMht.make_array(event.input)
        event.FatjetCA15softdropz2b1filt = FatjetCA15softdropz2b1filt.make_array(event.input)
        event.trgObjects_hltDoublePFCentralJetLooseID90 = trgObjects_hltDoublePFCentralJetLooseID90.make_array(event.input)
        event.GenJet = GenJet.make_array(event.input)
        event.GenVbosons = GenVbosons.make_array(event.input)
        event.trgObjects_hltDoublePFJetsC100 = trgObjects_hltDoublePFJetsC100.make_array(event.input)
        event.SubjetCA15pruned = SubjetCA15pruned.make_array(event.input)
        event.trgObjects_caloMet = trgObjects_caloMet.make_array(event.input)
        event.FatjetCA15ungroomed = FatjetCA15ungroomed.make_array(event.input)
        event.trgObjects_pfMet = trgObjects_pfMet.make_array(event.input)
        event.trgObjects_hltBTagCaloCSVp067Single = trgObjects_hltBTagCaloCSVp067Single.make_array(event.input)
        event.dRaddJetsdR08 = dRaddJetsdR08.make_array(event.input)
        event.l1Jets = l1Jets.make_array(event.input)
        event.SubjetCA15softdropz2b1filt = SubjetCA15softdropz2b1filt.make_array(event.input)
        event.GenBQuarkFromH = GenBQuarkFromH.make_array(event.input)
        event.trgObjects_hltDoubleJet65 = trgObjects_hltDoubleJet65.make_array(event.input)
        event.FatjetCA15trimmed = FatjetCA15trimmed.make_array(event.input)
        event.SubjetCA15softdropfilt = SubjetCA15softdropfilt.make_array(event.input)
        event.trgObjects_hltBTagCaloCSVp026DoubleWithMatching = trgObjects_hltBTagCaloCSVp026DoubleWithMatching.make_array(event.input)
        event.aLeptons = aLeptons.make_array(event.input)
        event.trgObjects_hltPFQuadJetLooseID15 = trgObjects_hltPFQuadJetLooseID15.make_array(event.input)
        event.trgObjects_hltQuadPFCentralJetLooseID45 = trgObjects_hltQuadPFCentralJetLooseID45.make_array(event.input)
        event.GenHiggsSisters = GenHiggsSisters.make_array(event.input)
        event.trgObjects_pfHt = trgObjects_pfHt.make_array(event.input)
        event.trgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2 = trgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2.make_array(event.input)
        event.hjidxaddJetsdR08 = hjidxaddJetsdR08.make_array(event.input)
        event.FatjetCA15softdropfilt = FatjetCA15softdropfilt.make_array(event.input)
        event.l1Muons = l1Muons.make_array(event.input)
        event.trgObjects_hltMHTNoPU90 = trgObjects_hltMHTNoPU90.make_array(event.input)
        event.FatjetAK08ungroomed = FatjetAK08ungroomed.make_array(event.input)
        event.GenWZQuark = GenWZQuark.make_array(event.input)
        event.trgObjects_hltPFMHTTightID90 = trgObjects_hltPFMHTTightID90.make_array(event.input)
        event.trgObjects_hltQuadCentralJet45 = trgObjects_hltQuadCentralJet45.make_array(event.input)
        event.trgObjects_hltBTagCaloCSVp022Single = trgObjects_hltBTagCaloCSVp022Single.make_array(event.input)
        event.selLeptons = selLeptons.make_array(event.input)
        event.trgObjects_hltPFMET90 = trgObjects_hltPFMET90.make_array(event.input)
        event.trgObjects_hltQuadJet15 = trgObjects_hltQuadJet15.make_array(event.input)
        event.TauGood = TauGood.make_array(event.input)
        event.GenStatus2bHad = GenStatus2bHad.make_array(event.input)
        event.hJidx = hJidx.make_array(event.input)
        event.GenNuFromTau = GenNuFromTau.make_array(event.input)
        event.FatjetCA15softdropz2b1 = FatjetCA15softdropz2b1.make_array(event.input)
        event.GenGluonFromB = GenGluonFromB.make_array(event.input)
        event.trgObjects_hltTripleJet50 = trgObjects_hltTripleJet50.make_array(event.input)
        event.trgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1 = trgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1.make_array(event.input)
        event.httCandidates = httCandidates.make_array(event.input)
        event.GenTop = GenTop.make_array(event.input)
        event.GenTaus = GenTaus.make_array(event.input)
        event.trgObjects_hltMHT70 = trgObjects_hltMHT70.make_array(event.input)
        event.Jet = Jet.make_array(event.input)
        event.FatjetCA15softdrop = FatjetCA15softdrop.make_array(event.input)
        event.trgObjects_hltPFTripleJetLooseID64 = trgObjects_hltPFTripleJetLooseID64.make_array(event.input)
        event.LHE_weights_pdf = LHE_weights_pdf.make_array(event.input)
        event.trgObjects_caloMhtNoPU = trgObjects_caloMhtNoPU.make_array(event.input)
        event.GenLep = GenLep.make_array(event.input)
        event.GenGluonFromTop = GenGluonFromTop.make_array(event.input)
        event.softActivityJets = softActivityJets.make_array(event.input)
        event.FatjetCA15subjetfiltered = FatjetCA15subjetfiltered.make_array(event.input)
        event.trgObjects_hltSingleJet80 = trgObjects_hltSingleJet80.make_array(event.input)
        event.l1MHT = l1MHT.make_obj(event.input)
        event.HCMVAV2_reg_corrJECDown = HCMVAV2_reg_corrJECDown.make_obj(event.input)
        event.HCMVAV2_reg_corrJERDown = HCMVAV2_reg_corrJERDown.make_obj(event.input)
        event.l1MET = l1MET.make_obj(event.input)
        event.V = V.make_obj(event.input)
        event.H_reg = H_reg.make_obj(event.input)
        event.HCSV_reg_corrJERDown = HCSV_reg_corrJERDown.make_obj(event.input)
        event.HCSV = HCSV.make_obj(event.input)
        event.l1HT = l1HT.make_obj(event.input)
        event.fakeMET = fakeMET.make_obj(event.input)
        event.HCSV_reg_corrJERUp = HCSV_reg_corrJERUp.make_obj(event.input)
        event.HCMVAV2_reg_corrJERUp = HCMVAV2_reg_corrJERUp.make_obj(event.input)
        event.HCSV_reg_corrJECUp = HCSV_reg_corrJECUp.make_obj(event.input)
        event.met_shifted_UnclusteredEnUp = met_shifted_UnclusteredEnUp.make_obj(event.input)
        event.met_shifted_UnclusteredEnDown = met_shifted_UnclusteredEnDown.make_obj(event.input)
        event.HCSV_reg = HCSV_reg.make_obj(event.input)
        event.H_reg_corrJERUp = H_reg_corrJERUp.make_obj(event.input)
        event.H_reg_corrJECUp = H_reg_corrJECUp.make_obj(event.input)
        event.HCMVAV2_reg = HCMVAV2_reg.make_obj(event.input)
        event.H = H.make_obj(event.input)
        event.softActivityVH = softActivityVH.make_obj(event.input)
        event.met_shifted_JetResUp = met_shifted_JetResUp.make_obj(event.input)
        event.met = met.make_obj(event.input)
        event.met_shifted_JetEnUp = met_shifted_JetEnUp.make_obj(event.input)
        event.met_shifted_JetEnDown = met_shifted_JetEnDown.make_obj(event.input)
        event.met_shifted_MuonEnUp = met_shifted_MuonEnUp.make_obj(event.input)
        event.met_shifted_MuonEnDown = met_shifted_MuonEnDown.make_obj(event.input)
        event.met_shifted_ElectronEnUp = met_shifted_ElectronEnUp.make_obj(event.input)
        event.met_shifted_ElectronEnDown = met_shifted_ElectronEnDown.make_obj(event.input)
        event.met_shifted_TauEnUp = met_shifted_TauEnUp.make_obj(event.input)
        event.met_shifted_TauEnDown = met_shifted_TauEnDown.make_obj(event.input)
        event.l1ET = l1ET.make_obj(event.input)
        event.softActivityEWK = softActivityEWK.make_obj(event.input)
        event.met_shifted_JetResDown = met_shifted_JetResDown.make_obj(event.input)
        event.HaddJetsdR08 = HaddJetsdR08.make_obj(event.input)
        event.H_reg_corrJERDown = H_reg_corrJERDown.make_obj(event.input)
        event.HCMVAV2_reg_corrJECUp = HCMVAV2_reg_corrJECUp.make_obj(event.input)
        event.softActivity = softActivity.make_obj(event.input)
        event.HCSV_reg_corrJECDown = HCSV_reg_corrJECDown.make_obj(event.input)
        event.HCMVAV2 = HCMVAV2.make_obj(event.input)
        event.H_reg_corrJECDown = H_reg_corrJECDown.make_obj(event.input)
        event.puWeightUp = getattr(event.input, "puWeightUp", None)
        event.puWeightDown = getattr(event.input, "puWeightDown", None)
        event.json = getattr(event.input, "json", None)
        event.json_silver = getattr(event.input, "json_silver", None)
        event.nPU0 = getattr(event.input, "nPU0", None)
        event.nPVs = getattr(event.input, "nPVs", None)
        event.Vtype = getattr(event.input, "Vtype", None)
        event.VtypeSim = getattr(event.input, "VtypeSim", None)
        event.VMt = getattr(event.input, "VMt", None)
        event.HVdPhi = getattr(event.input, "HVdPhi", None)
        event.fakeMET_sumet = getattr(event.input, "fakeMET_sumet", None)
        event.bx = getattr(event.input, "bx", None)
        event.caloMetPt = getattr(event.input, "caloMetPt", None)
        event.caloMetPhi = getattr(event.input, "caloMetPhi", None)
        event.rho = getattr(event.input, "rho", None)
        event.rhoN = getattr(event.input, "rhoN", None)
        event.rhoCHPU = getattr(event.input, "rhoCHPU", None)
        event.rhoCentral = getattr(event.input, "rhoCentral", None)
        event.deltaR_jj = getattr(event.input, "deltaR_jj", None)
        event.lheNj = getattr(event.input, "lheNj", None)
        event.lheNb = getattr(event.input, "lheNb", None)
        event.lheNc = getattr(event.input, "lheNc", None)
        event.lheNg = getattr(event.input, "lheNg", None)
        event.lheNl = getattr(event.input, "lheNl", None)
        event.lheV_pt = getattr(event.input, "lheV_pt", None)
        event.lheHT = getattr(event.input, "lheHT", None)
        event.genTTHtoTauTauDecayMode = getattr(event.input, "genTTHtoTauTauDecayMode", None)
        event.ttCls = getattr(event.input, "ttCls", None)
        event.heavyFlavourCategory = getattr(event.input, "heavyFlavourCategory", None)
        event.mhtJet30 = getattr(event.input, "mhtJet30", None)
        event.mhtPhiJet30 = getattr(event.input, "mhtPhiJet30", None)
        event.htJet30 = getattr(event.input, "htJet30", None)
        event.met_sig = getattr(event.input, "met_sig", None)
        event.met_covXX = getattr(event.input, "met_covXX", None)
        event.met_covXY = getattr(event.input, "met_covXY", None)
        event.met_covYY = getattr(event.input, "met_covYY", None)
        event.met_rawpt = getattr(event.input, "met_rawpt", None)
        event.metPuppi_pt = getattr(event.input, "metPuppi_pt", None)
        event.metPuppi_phi = getattr(event.input, "metPuppi_phi", None)
        event.metPuppi_rawpt = getattr(event.input, "metPuppi_rawpt", None)
        event.metType1p2_pt = getattr(event.input, "metType1p2_pt", None)
        event.tkMet_pt = getattr(event.input, "tkMet_pt", None)
        event.tkMet_phi = getattr(event.input, "tkMet_phi", None)
        event.isrJetVH = getattr(event.input, "isrJetVH", None)
        event.simPrimaryVertex_z = getattr(event.input, "simPrimaryVertex_z", None)
        event.genHiggsDecayMode = getattr(event.input, "genHiggsDecayMode", None)
        event.triggerEmulationWeight = getattr(event.input, "triggerEmulationWeight", None)
        event.btagWeightCSV_down_cferr1 = getattr(event.input, "btagWeightCSV_down_cferr1", None)
        event.btagWeightCMVAV2_down_hfstats1 = getattr(event.input, "btagWeightCMVAV2_down_hfstats1", None)
        event.btagWeightCMVAV2_down_hfstats2 = getattr(event.input, "btagWeightCMVAV2_down_hfstats2", None)
        event.btagWeightCSV_down_cferr2 = getattr(event.input, "btagWeightCSV_down_cferr2", None)
        event.btagWeightCSV_down_jes = getattr(event.input, "btagWeightCSV_down_jes", None)
        event.btagWeightCSV_down_lf = getattr(event.input, "btagWeightCSV_down_lf", None)
        event.btagWeightCSV_up_lf = getattr(event.input, "btagWeightCSV_up_lf", None)
        event.btagWeightCSV_down_lfstats2 = getattr(event.input, "btagWeightCSV_down_lfstats2", None)
        event.btagWeightCSV_down_lfstats1 = getattr(event.input, "btagWeightCSV_down_lfstats1", None)
        event.btagWeightCSV_down_hf = getattr(event.input, "btagWeightCSV_down_hf", None)
        event.btagWeightCSV_up_lfstats1 = getattr(event.input, "btagWeightCSV_up_lfstats1", None)
        event.btagWeightCMVAV2_down_lf = getattr(event.input, "btagWeightCMVAV2_down_lf", None)
        event.btagWeightCSV_up_lfstats2 = getattr(event.input, "btagWeightCSV_up_lfstats2", None)
        event.btagWeightCSV = getattr(event.input, "btagWeightCSV", None)
        event.btagWeightCSV_up_cferr2 = getattr(event.input, "btagWeightCSV_up_cferr2", None)
        event.btagWeightCSV_up_cferr1 = getattr(event.input, "btagWeightCSV_up_cferr1", None)
        event.btagWeightCSV_up_hf = getattr(event.input, "btagWeightCSV_up_hf", None)
        event.btagWeightCMVAV2_down_hf = getattr(event.input, "btagWeightCMVAV2_down_hf", None)
        event.btagWeightCMVAV2_up_lfstats2 = getattr(event.input, "btagWeightCMVAV2_up_lfstats2", None)
        event.btagWeightCMVAV2_up_hfstats2 = getattr(event.input, "btagWeightCMVAV2_up_hfstats2", None)
        event.btagWeightCMVAV2_up_hfstats1 = getattr(event.input, "btagWeightCMVAV2_up_hfstats1", None)
        event.btagWeightCMVAV2 = getattr(event.input, "btagWeightCMVAV2", None)
        event.btagWeightCMVAV2_up_lfstats1 = getattr(event.input, "btagWeightCMVAV2_up_lfstats1", None)
        event.btagWeightCMVAV2_down_cferr2 = getattr(event.input, "btagWeightCMVAV2_down_cferr2", None)
        event.btagWeightCMVAV2_up_hf = getattr(event.input, "btagWeightCMVAV2_up_hf", None)
        event.btagWeightCMVAV2_down_cferr1 = getattr(event.input, "btagWeightCMVAV2_down_cferr1", None)
        event.btagWeightCSV_up_jes = getattr(event.input, "btagWeightCSV_up_jes", None)
        event.btagWeightCMVAV2_up_jes = getattr(event.input, "btagWeightCMVAV2_up_jes", None)
        event.btagWeightCMVAV2_up_lf = getattr(event.input, "btagWeightCMVAV2_up_lf", None)
        event.btagWeightCSV_down_hfstats2 = getattr(event.input, "btagWeightCSV_down_hfstats2", None)
        event.btagWeightCSV_down_hfstats1 = getattr(event.input, "btagWeightCSV_down_hfstats1", None)
        event.btagWeightCMVAV2_up_cferr1 = getattr(event.input, "btagWeightCMVAV2_up_cferr1", None)
        event.btagWeightCMVAV2_up_cferr2 = getattr(event.input, "btagWeightCMVAV2_up_cferr2", None)
        event.btagWeightCMVAV2_down_lfstats1 = getattr(event.input, "btagWeightCMVAV2_down_lfstats1", None)
        event.btagWeightCMVAV2_down_lfstats2 = getattr(event.input, "btagWeightCMVAV2_down_lfstats2", None)
        event.btagWeightCSV_up_hfstats1 = getattr(event.input, "btagWeightCSV_up_hfstats1", None)
        event.btagWeightCMVAV2_down_jes = getattr(event.input, "btagWeightCMVAV2_down_jes", None)
        event.btagWeightCSV_up_hfstats2 = getattr(event.input, "btagWeightCSV_up_hfstats2", None)
        event.ZllKinFit_corrJERUp_mass = getattr(event.input, "ZllKinFit_corrJERUp_mass", None)
        event.ZllKinFit_status = getattr(event.input, "ZllKinFit_status", None)
        event.ZllKinFit_corrJERDown_status = getattr(event.input, "ZllKinFit_corrJERDown_status", None)
        event.ZllKinFit_corrJECDown_status = getattr(event.input, "ZllKinFit_corrJECDown_status", None)
        event.ZllKinFit_njet = getattr(event.input, "ZllKinFit_njet", None)
        event.ZllKinFit_corrJECDown_njet = getattr(event.input, "ZllKinFit_corrJECDown_njet", None)
        event.ZllKinFit_corrJERUp_njet = getattr(event.input, "ZllKinFit_corrJERUp_njet", None)
        event.ZllKinFit_corrJERUp_status = getattr(event.input, "ZllKinFit_corrJERUp_status", None)
        event.ZllKinFit_corrJECUp_njet = getattr(event.input, "ZllKinFit_corrJECUp_njet", None)
        event.ZllKinFit_mass = getattr(event.input, "ZllKinFit_mass", None)
        event.ZllKinFit_corrJERDown_mass = getattr(event.input, "ZllKinFit_corrJERDown_mass", None)
        event.ZllKinFit_corrJECUp_mass = getattr(event.input, "ZllKinFit_corrJECUp_mass", None)
        event.ZllKinFit_corrJECDown_mass = getattr(event.input, "ZllKinFit_corrJECDown_mass", None)
        event.ZllKinFit_corrJECUp_status = getattr(event.input, "ZllKinFit_corrJECUp_status", None)
        event.ZllKinFit_corrJERDown_njet = getattr(event.input, "ZllKinFit_corrJERDown_njet", None)
