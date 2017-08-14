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
class trgObjects_hltQuadCentralJet30:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltQuadCentralJet30(input, i) for i in range(input.ntrgObjects_hltQuadCentralJet30)]
class trgObjects_hltSingleJet80:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltSingleJet80(input, i) for i in range(input.ntrgObjects_hltSingleJet80)]
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
class trgObjects_hltPFQuadJetLooseID15:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltPFQuadJetLooseID15(input, i) for i in range(input.ntrgObjects_hltPFQuadJetLooseID15)]
class trgObjects_hltMHTNoPU90:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltMHTNoPU90(input, i) for i in range(input.ntrgObjects_hltMHTNoPU90)]
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
class trgObjects_hltDoublePFCentralJetLooseID90:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltDoublePFCentralJetLooseID90(input, i) for i in range(input.ntrgObjects_hltDoublePFCentralJetLooseID90)]
class trgObjects_caloJets:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_caloJets_pt[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_caloJets(input, i) for i in range(input.ntrgObjects_caloJets)]
class trgObjects_hltPFSingleJetLooseID92:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltPFSingleJetLooseID92(input, i) for i in range(input.ntrgObjects_hltPFSingleJetLooseID92)]
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
class trgObjects_caloMet:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_caloMet_pt[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_caloMet(input, i) for i in range(input.ntrgObjects_caloMet)]
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
class trgObjects_hltDoubleCentralJet90:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltDoubleCentralJet90(input, i) for i in range(input.ntrgObjects_hltDoubleCentralJet90)]
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
class trgObjects_pfMet:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_pfMet_pt[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_pfMet(input, i) for i in range(input.ntrgObjects_pfMet)]
class trgObjects_pfHt:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_pfHt_pt[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_pfHt(input, i) for i in range(input.ntrgObjects_pfHt)]
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
class trgObjects_caloMhtNoPU:
    def __init__(self, tree, n):
        self.pt = tree.trgObjects_caloMhtNoPU_pt[n];
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_caloMhtNoPU(input, i) for i in range(input.ntrgObjects_caloMhtNoPU)]
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
class trgObjects_hltBTagCaloCSVp067Single:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltBTagCaloCSVp067Single(input, i) for i in range(input.ntrgObjects_hltBTagCaloCSVp067Single)]
class trgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2(input, i) for i in range(input.ntrgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2)]
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
        self.eleCutIdSummer16 = tree.selLeptons_eleCutIdSummer16[n];
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
        self.btagCMVAV2 = tree.Jet_btagCMVAV2[n];
        self.chHEF = tree.Jet_chHEF[n];
        self.neHEF = tree.Jet_neHEF[n];
        self.chEmEF = tree.Jet_chEmEF[n];
        self.neEmEF = tree.Jet_neEmEF[n];
        self.muEF = tree.Jet_muEF[n];
        self.chMult = tree.Jet_chMult[n];
        self.nhMult = tree.Jet_nhMult[n];
        self.mcEta = tree.Jet_mcEta[n];
        self.mcPhi = tree.Jet_mcPhi[n];
        self.mcM = tree.Jet_mcM[n];
        self.qgl = tree.Jet_qgl[n];
        self.ptd = tree.Jet_ptd[n];
        self.axis2 = tree.Jet_axis2[n];
        self.mult = tree.Jet_mult[n];
        self.numberOfDaughters = tree.Jet_numberOfDaughters[n];
        self.mcIdx = tree.Jet_mcIdx[n];
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
class trgObjects_hltQuadPFCentralJetLooseID45:
    def __init__(self, tree, n):
        pass
    @staticmethod
    def make_array(input):
        return [trgObjects_hltQuadPFCentralJetLooseID45(input, i) for i in range(input.ntrgObjects_hltQuadPFCentralJetLooseID45)]
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
        event.trgObjects_hltIsoMu20 = trgObjects_hltIsoMu20.make_array(event.input)
        event.trgObjects_hltQuadCentralJet30 = trgObjects_hltQuadCentralJet30.make_array(event.input)
        event.trgObjects_hltSingleJet80 = trgObjects_hltSingleJet80.make_array(event.input)
        event.GenBQuarkFromTop = GenBQuarkFromTop.make_array(event.input)
        event.GenLepFromTau = GenLepFromTau.make_array(event.input)
        event.GenHiggsBoson = GenHiggsBoson.make_array(event.input)
        event.GenNuFromTop = GenNuFromTop.make_array(event.input)
        event.GenBQuarkFromHafterISR = GenBQuarkFromHafterISR.make_array(event.input)
        event.trgObjects_hltPFDoubleJetLooseID76 = trgObjects_hltPFDoubleJetLooseID76.make_array(event.input)
        event.trgObjects_hltBTagPFCSVp016SingleWithMatching = trgObjects_hltBTagPFCSVp016SingleWithMatching.make_array(event.input)
        event.trgObjects_hltPFQuadJetLooseID15 = trgObjects_hltPFQuadJetLooseID15.make_array(event.input)
        event.trgObjects_hltMHTNoPU90 = trgObjects_hltMHTNoPU90.make_array(event.input)
        event.trgObjects_hltQuadPFCentralJetLooseID30 = trgObjects_hltQuadPFCentralJetLooseID30.make_array(event.input)
        event.GenNu = GenNu.make_array(event.input)
        event.trgObjects_hltBTagCaloCSVp087Triple = trgObjects_hltBTagCaloCSVp087Triple.make_array(event.input)
        event.trgObjects_hltDoublePFCentralJetLooseID90 = trgObjects_hltDoublePFCentralJetLooseID90.make_array(event.input)
        event.trgObjects_caloJets = trgObjects_caloJets.make_array(event.input)
        event.trgObjects_hltPFSingleJetLooseID92 = trgObjects_hltPFSingleJetLooseID92.make_array(event.input)
        event.trgObjects_hltL1sETM50ToETM100IorETM60Jet60dPhiMin0p4IorDoubleJetC60ETM60 = trgObjects_hltL1sETM50ToETM100IorETM60Jet60dPhiMin0p4IorDoubleJetC60ETM60.make_array(event.input)
        event.trgObjects_hltEle25WPTight = trgObjects_hltEle25WPTight.make_array(event.input)
        event.GenTop = GenTop.make_array(event.input)
        event.trgObjects_caloMet = trgObjects_caloMet.make_array(event.input)
        event.trgObjects_hltBTagCaloCSVp014DoubleWithMatching = trgObjects_hltBTagCaloCSVp014DoubleWithMatching.make_array(event.input)
        event.pileUpVertex_z = pileUpVertex_z.make_array(event.input)
        event.trgObjects_pfJets = trgObjects_pfJets.make_array(event.input)
        event.trgObjects_pfMht = trgObjects_pfMht.make_array(event.input)
        event.LHE_weights_scale = LHE_weights_scale.make_array(event.input)
        event.trgObjects_hltL1sQuadJetCIorTripleJetVBFIorHTT = trgObjects_hltL1sQuadJetCIorTripleJetVBFIorHTT.make_array(event.input)
        event.trgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5 = trgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5.make_array(event.input)
        event.trgObjects_caloMht = trgObjects_caloMht.make_array(event.input)
        event.trgObjects_hltDoubleCentralJet90 = trgObjects_hltDoubleCentralJet90.make_array(event.input)
        event.GenJet = GenJet.make_array(event.input)
        event.trgObjects_hltDoublePFJetsC100 = trgObjects_hltDoublePFJetsC100.make_array(event.input)
        event.trgObjects_pfMet = trgObjects_pfMet.make_array(event.input)
        event.trgObjects_pfHt = trgObjects_pfHt.make_array(event.input)
        event.GenStatus2bHad = GenStatus2bHad.make_array(event.input)
        event.GenGluonFromTop = GenGluonFromTop.make_array(event.input)
        event.GenBQuarkFromH = GenBQuarkFromH.make_array(event.input)
        event.trgObjects_hltDoubleJet65 = trgObjects_hltDoubleJet65.make_array(event.input)
        event.trgObjects_hltBTagCaloCSVp026DoubleWithMatching = trgObjects_hltBTagCaloCSVp026DoubleWithMatching.make_array(event.input)
        event.trgObjects_caloMhtNoPU = trgObjects_caloMhtNoPU.make_array(event.input)
        event.GenHiggsSisters = GenHiggsSisters.make_array(event.input)
        event.trgObjects_hltBTagCaloCSVp067Single = trgObjects_hltBTagCaloCSVp067Single.make_array(event.input)
        event.trgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2 = trgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2.make_array(event.input)
        event.GenWZQuark = GenWZQuark.make_array(event.input)
        event.trgObjects_hltPFMHTTightID90 = trgObjects_hltPFMHTTightID90.make_array(event.input)
        event.trgObjects_hltQuadCentralJet45 = trgObjects_hltQuadCentralJet45.make_array(event.input)
        event.trgObjects_hltBTagCaloCSVp022Single = trgObjects_hltBTagCaloCSVp022Single.make_array(event.input)
        event.selLeptons = selLeptons.make_array(event.input)
        event.trgObjects_hltPFMET90 = trgObjects_hltPFMET90.make_array(event.input)
        event.trgObjects_hltQuadJet15 = trgObjects_hltQuadJet15.make_array(event.input)
        event.GenNuFromTau = GenNuFromTau.make_array(event.input)
        event.GenGluonFromB = GenGluonFromB.make_array(event.input)
        event.trgObjects_hltTripleJet50 = trgObjects_hltTripleJet50.make_array(event.input)
        event.trgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1 = trgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1.make_array(event.input)
        event.trgObjects_hltEle25eta2p1WPLoose = trgObjects_hltEle25eta2p1WPLoose.make_array(event.input)
        event.GenTaus = GenTaus.make_array(event.input)
        event.trgObjects_hltMHT70 = trgObjects_hltMHT70.make_array(event.input)
        event.Jet = Jet.make_array(event.input)
        event.trgObjects_hltPFTripleJetLooseID64 = trgObjects_hltPFTripleJetLooseID64.make_array(event.input)
        event.LHE_weights_pdf = LHE_weights_pdf.make_array(event.input)
        event.GenLep = GenLep.make_array(event.input)
        event.primaryVertices = primaryVertices.make_array(event.input)
        event.trgObjects_hltQuadPFCentralJetLooseID45 = trgObjects_hltQuadPFCentralJetLooseID45.make_array(event.input)
        event.met = met.make_obj(event.input)
        event.met_shifted_UnclusteredEnUp = met_shifted_UnclusteredEnUp.make_obj(event.input)
        event.met_shifted_UnclusteredEnDown = met_shifted_UnclusteredEnDown.make_obj(event.input)
        event.met_shifted_JetResUp = met_shifted_JetResUp.make_obj(event.input)
        event.met_shifted_JetResDown = met_shifted_JetResDown.make_obj(event.input)
        event.met_shifted_JetEnUp = met_shifted_JetEnUp.make_obj(event.input)
        event.met_shifted_JetEnDown = met_shifted_JetEnDown.make_obj(event.input)
        event.met_shifted_MuonEnUp = met_shifted_MuonEnUp.make_obj(event.input)
        event.met_shifted_MuonEnDown = met_shifted_MuonEnDown.make_obj(event.input)
        event.met_shifted_ElectronEnUp = met_shifted_ElectronEnUp.make_obj(event.input)
        event.met_shifted_ElectronEnDown = met_shifted_ElectronEnDown.make_obj(event.input)
        event.met_shifted_TauEnUp = met_shifted_TauEnUp.make_obj(event.input)
        event.met_shifted_TauEnDown = met_shifted_TauEnDown.make_obj(event.input)
        event.puWeightUp = getattr(event.input, "puWeightUp", None)
        event.puWeightDown = getattr(event.input, "puWeightDown", None)
        event.json = getattr(event.input, "json", None)
        event.json_silver = getattr(event.input, "json_silver", None)
        event.nPU0 = getattr(event.input, "nPU0", None)
        event.nPVs = getattr(event.input, "nPVs", None)
        event.bx = getattr(event.input, "bx", None)
        event.rho = getattr(event.input, "rho", None)
        event.lheNj = getattr(event.input, "lheNj", None)
        event.lheNb = getattr(event.input, "lheNb", None)
        event.lheNc = getattr(event.input, "lheNc", None)
        event.lheNg = getattr(event.input, "lheNg", None)
        event.lheNl = getattr(event.input, "lheNl", None)
        event.lheV_pt = getattr(event.input, "lheV_pt", None)
        event.lheHT = getattr(event.input, "lheHT", None)
        event.ttCls = getattr(event.input, "ttCls", None)
        event.heavyFlavourCategory = getattr(event.input, "heavyFlavourCategory", None)
        event.genHiggsDecayMode = getattr(event.input, "genHiggsDecayMode", None)
        event.triggerEmulationWeight = getattr(event.input, "triggerEmulationWeight", None)
        event.btagWeightCSV_down_jesPileUpPtBB = getattr(event.input, "btagWeightCSV_down_jesPileUpPtBB", None)
        event.btagWeightCSV_down_jesFlavorQCD = getattr(event.input, "btagWeightCSV_down_jesFlavorQCD", None)
        event.btagWeightCSV_down_jesAbsoluteScale = getattr(event.input, "btagWeightCSV_down_jesAbsoluteScale", None)
        event.btagWeightCSV_down_jesPileUpPtRef = getattr(event.input, "btagWeightCSV_down_jesPileUpPtRef", None)
        event.btagWeightCSV_down_jesRelativeFSR = getattr(event.input, "btagWeightCSV_down_jesRelativeFSR", None)
        event.btagWeightCSV_down_jesTimePtEta = getattr(event.input, "btagWeightCSV_down_jesTimePtEta", None)
        event.btagWeightCSV_down_hf = getattr(event.input, "btagWeightCSV_down_hf", None)
        event.btagWeightCSV_down_cferr1 = getattr(event.input, "btagWeightCSV_down_cferr1", None)
        event.btagWeightCMVAV2_up_hf = getattr(event.input, "btagWeightCMVAV2_up_hf", None)
        event.btagWeightCMVAV2_down_hfstats2 = getattr(event.input, "btagWeightCMVAV2_down_hfstats2", None)
        event.btagWeightCSV_down_cferr2 = getattr(event.input, "btagWeightCSV_down_cferr2", None)
        event.btagWeightCSV_down_jes = getattr(event.input, "btagWeightCSV_down_jes", None)
        event.btagWeightCSV_down_jesAbsoluteMPFBias = getattr(event.input, "btagWeightCSV_down_jesAbsoluteMPFBias", None)
        event.btagWeightCSV_down_lf = getattr(event.input, "btagWeightCSV_down_lf", None)
        event.btagWeightCSV_down_jesPileUpPtEC1 = getattr(event.input, "btagWeightCSV_down_jesPileUpPtEC1", None)
        event.btagWeightCMVAV2_down_hfstats1 = getattr(event.input, "btagWeightCMVAV2_down_hfstats1", None)
        event.btagWeightCSV_up_lf = getattr(event.input, "btagWeightCSV_up_lf", None)
        event.btagWeightCMVAV2 = getattr(event.input, "btagWeightCMVAV2", None)
        event.btagWeightCSV_down_lfstats2 = getattr(event.input, "btagWeightCSV_down_lfstats2", None)
        event.btagWeightCSV_up_jesPileUpPtRef = getattr(event.input, "btagWeightCSV_up_jesPileUpPtRef", None)
        event.btagWeightCSV_down_lfstats1 = getattr(event.input, "btagWeightCSV_down_lfstats1", None)
        event.btagWeightCSV_up_jesFlavorQCD = getattr(event.input, "btagWeightCSV_up_jesFlavorQCD", None)
        event.btagWeightCSV_down_jesPileUpDataMC = getattr(event.input, "btagWeightCSV_down_jesPileUpDataMC", None)
        event.btagWeightCSV_up_lfstats1 = getattr(event.input, "btagWeightCSV_up_lfstats1", None)
        event.btagWeightCMVAV2_down_lf = getattr(event.input, "btagWeightCMVAV2_down_lf", None)
        event.btagWeightCSV_up_lfstats2 = getattr(event.input, "btagWeightCSV_up_lfstats2", None)
        event.btagWeightCSV = getattr(event.input, "btagWeightCSV", None)
        event.btagWeightCSV_up_cferr2 = getattr(event.input, "btagWeightCSV_up_cferr2", None)
        event.btagWeightCSV_up_jesAbsoluteMPFBias = getattr(event.input, "btagWeightCSV_up_jesAbsoluteMPFBias", None)
        event.btagWeightCSV_up_jesSinglePionECAL = getattr(event.input, "btagWeightCSV_up_jesSinglePionECAL", None)
        event.btagWeightCSV_up_cferr1 = getattr(event.input, "btagWeightCSV_up_cferr1", None)
        event.btagWeightCSV_up_jesPileUpPtBB = getattr(event.input, "btagWeightCSV_up_jesPileUpPtBB", None)
        event.btagWeightCMVAV2_down_hf = getattr(event.input, "btagWeightCMVAV2_down_hf", None)
        event.btagWeightCMVAV2_up_lfstats2 = getattr(event.input, "btagWeightCMVAV2_up_lfstats2", None)
        event.btagWeightCMVAV2_up_hfstats2 = getattr(event.input, "btagWeightCMVAV2_up_hfstats2", None)
        event.btagWeightCMVAV2_up_hfstats1 = getattr(event.input, "btagWeightCMVAV2_up_hfstats1", None)
        event.btagWeightCSV_up_jesAbsoluteScale = getattr(event.input, "btagWeightCSV_up_jesAbsoluteScale", None)
        event.btagWeightCMVAV2_up_lfstats1 = getattr(event.input, "btagWeightCMVAV2_up_lfstats1", None)
        event.btagWeightCMVAV2_down_cferr2 = getattr(event.input, "btagWeightCMVAV2_down_cferr2", None)
        event.btagWeightCSV_up_hf = getattr(event.input, "btagWeightCSV_up_hf", None)
        event.btagWeightCSV_up_jesPileUpPtEC1 = getattr(event.input, "btagWeightCSV_up_jesPileUpPtEC1", None)
        event.btagWeightCMVAV2_down_cferr1 = getattr(event.input, "btagWeightCMVAV2_down_cferr1", None)
        event.btagWeightCSV_up_jesRelativeFSR = getattr(event.input, "btagWeightCSV_up_jesRelativeFSR", None)
        event.btagWeightCSV_up_jesTimePtEta = getattr(event.input, "btagWeightCSV_up_jesTimePtEta", None)
        event.btagWeightCSV_up_jes = getattr(event.input, "btagWeightCSV_up_jes", None)
        event.btagWeightCMVAV2_up_jes = getattr(event.input, "btagWeightCMVAV2_up_jes", None)
        event.btagWeightCSV_down_jesSinglePionECAL = getattr(event.input, "btagWeightCSV_down_jesSinglePionECAL", None)
        event.btagWeightCMVAV2_up_lf = getattr(event.input, "btagWeightCMVAV2_up_lf", None)
        event.btagWeightCSV_down_hfstats2 = getattr(event.input, "btagWeightCSV_down_hfstats2", None)
        event.btagWeightCSV_up_jesPileUpDataMC = getattr(event.input, "btagWeightCSV_up_jesPileUpDataMC", None)
        event.btagWeightCSV_down_hfstats1 = getattr(event.input, "btagWeightCSV_down_hfstats1", None)
        event.btagWeightCSV_down_jesSinglePionHCAL = getattr(event.input, "btagWeightCSV_down_jesSinglePionHCAL", None)
        event.btagWeightCMVAV2_up_cferr1 = getattr(event.input, "btagWeightCMVAV2_up_cferr1", None)
        event.btagWeightCMVAV2_up_cferr2 = getattr(event.input, "btagWeightCMVAV2_up_cferr2", None)
        event.btagWeightCMVAV2_down_lfstats1 = getattr(event.input, "btagWeightCMVAV2_down_lfstats1", None)
        event.btagWeightCMVAV2_down_lfstats2 = getattr(event.input, "btagWeightCMVAV2_down_lfstats2", None)
        event.btagWeightCSV_up_hfstats2 = getattr(event.input, "btagWeightCSV_up_hfstats2", None)
        event.btagWeightCSV_up_hfstats1 = getattr(event.input, "btagWeightCSV_up_hfstats1", None)
        event.btagWeightCMVAV2_down_jes = getattr(event.input, "btagWeightCMVAV2_down_jes", None)
        event.btagWeightCSV_up_jesSinglePionHCAL = getattr(event.input, "btagWeightCSV_up_jesSinglePionHCAL", None)
