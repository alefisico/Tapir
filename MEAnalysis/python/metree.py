import PhysicsTools.HeppyCore.framework.config as cfg


#Defines the output TTree branch structures
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer import *

#Override the default fillCoreVariables function, which
#by default looks for FWLite variables
#FIXME: this is a hack to run heppy on non-EDM formats. Better to propagate it to heppy
def fillCoreVariables(self, tr, event, isMC):
    for x in ["run", "lumi", "evt", "xsec", "nTrueInt", "puWeight", "genWeight"]:
        tr.fill(x, getattr(event.input, x))
AutoFillTreeProducer.fillCoreVariables = fillCoreVariables

#Specifies what to save for jets
jetType = NTupleObjectType("jetType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("id", lambda x : x.id),
    NTupleVariable("btagCSV", lambda x : x.btagCSV),
    NTupleVariable("mcFlavour", lambda x : x.mcFlavour, type=int),
    NTupleVariable("mcMatchId", lambda x : x.mcMatchId, type=int),
    NTupleVariable("hadronFlavour", lambda x : x.hadronFlavour, type=int),
    NTupleVariable("matchFlag", lambda x : x.tth_match_label_numeric, type=int),
    NTupleVariable("mcPt", lambda x : x.mcPt),
    NTupleVariable("mcEta", lambda x : x.mcEta),
    NTupleVariable("mcPhi", lambda x : x.mcPhi),
    NTupleVariable("mcM", lambda x : x.mcM),
])

"""
# Maybe implement later
#Specifies what to save for objects in the subjet lists
subjetType = NTupleObjectType("subjetType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("id", lambda x : x.id),
    NTupleVariable("btagFlag", lambda x : x.btagFlag),
    NTupleVariable("origin_subjet", lambda x : x.origin_subjet \
        if hasattr(x,'origin_subjet') else 0, type=int),
])
"""

#Specifies what to save for leptons
leptonType = NTupleObjectType("leptonType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("pdgId", lambda x : x.pdgId),
    NTupleVariable("relIso03", lambda x : x.relIso03),
    NTupleVariable("relIso04", lambda x : x.relIso04),
    #NTupleVariable("mcPt", lambda x : x.mcPt),
    #NTupleVariable("mcEta", lambda x : x.mcEta),
    #NTupleVariable("mcPhi", lambda x : x.mcPhi),
    #NTupleVariable("mcMass", lambda x : x.mcMass),
])

#Specifies what to save for leptons
quarkType = NTupleObjectType("quarkType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("pdgId", lambda x : x.pdgId),
])

metType = NTupleObjectType("metType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("px", lambda x : x.px),
    NTupleVariable("py", lambda x : x.py),
    NTupleVariable("sumEt", lambda x : x.sumEt),
    NTupleVariable("genPt", lambda x : x.genPt),
    NTupleVariable("genPhi", lambda x : x.genPhi),
])

memType = NTupleObjectType("memType", variables = [
    NTupleVariable("p",             lambda x : x.p ),
    NTupleVariable("p_err",         lambda x : x.p_err ),
    NTupleVariable("chi2",          lambda x : x.chi2 ),
    NTupleVariable("time",          lambda x : x.time ),
    NTupleVariable("error_code",    lambda x : x.error_code ),
    NTupleVariable("efficiency",    lambda x : x.efficiency ),
    NTupleVariable("nperm",         lambda x : x.num_perm ),
])

quarkType = NTupleObjectType("quarkType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("id", lambda x : x.pdgId),
])


# V11 & V12
# ==============================

httCandidateType = NTupleObjectType("httCandidateType", variables = [
    NTupleVariable("fRec", lambda x: x.fRec ),
    NTupleVariable("Ropt", lambda x: x.Ropt ),
    NTupleVariable("RoptCalc", lambda x: x.RoptCalc ),
    NTupleVariable("ptForRoptCalc", lambda x: x.ptForRoptCalc ),
    NTupleVariable("pt", lambda x: x.pt ),
    NTupleVariable("eta", lambda x: x.eta ),
    NTupleVariable("phi", lambda x: x.phi ),
    NTupleVariable("mass", lambda x: x.mass ),
    NTupleVariable("sjW1pt", lambda x: x.sjW1pt ),
    NTupleVariable("sjW1eta", lambda x: x.sjW1eta ),
    NTupleVariable("sjW1phi", lambda x: x.sjW1phi ),
    NTupleVariable("sjW1mass", lambda x: x.sjW1mass ),
    NTupleVariable("sjW1btag", lambda x: x.sjW1btag ),
    NTupleVariable("sjW2pt", lambda x: x.sjW2pt ),
    NTupleVariable("sjW2eta", lambda x: x.sjW2eta ),
    NTupleVariable("sjW2phi", lambda x: x.sjW2phi ),
    NTupleVariable("sjW2mass", lambda x: x.sjW2mass ),
    NTupleVariable("sjW2btag", lambda x: x.sjW2btag ),
    NTupleVariable("sjNonWpt", lambda x: x.sjNonWpt ),
    NTupleVariable("sjNonWeta", lambda x: x.sjNonWeta ),
    NTupleVariable("sjNonWphi", lambda x: x.sjNonWphi ),
    NTupleVariable("sjNonWmass", lambda x: x.sjNonWmass ),
    NTupleVariable("sjNonWbtag", lambda x: x.sjNonWbtag ),
    NTupleVariable("tau1", lambda x: x.tau1 ),   # Copied from matched fat jet
    NTupleVariable("tau2", lambda x: x.tau2 ),   # Copied from matched fat jet
    NTupleVariable("tau3", lambda x: x.tau3 ),   # Copied from matched fat jet
    NTupleVariable("bbtag", lambda x: x.bbtag ), # Copied from matched fat jet
    NTupleVariable("n_subjetiness", lambda x: x.n_subjetiness ), # Calculated
    NTupleVariable("delRopt", lambda x: x.delRopt ),             # Calculated
])

FatjetCA15ungroomedType = NTupleObjectType("FatjetCA15ungroomedType", variables = [
    NTupleVariable("pt", lambda x: x.pt ),
    NTupleVariable("eta", lambda x: x.eta ),
    NTupleVariable("phi", lambda x: x.phi ),
    NTupleVariable("mass", lambda x: x.mass ),
    NTupleVariable("tau1", lambda x: x.tau1 ),
    NTupleVariable("tau2", lambda x: x.tau2 ),
    NTupleVariable("tau3", lambda x: x.tau3 ),
    NTupleVariable("bbtag", lambda x: x.bbtag ),
])

FatjetCA15prunedType = NTupleObjectType("FatjetCA15prunedType", variables = [
    NTupleVariable("pt", lambda x: x.pt ),
    NTupleVariable("eta", lambda x: x.eta ),
    NTupleVariable("phi", lambda x: x.phi ),
    NTupleVariable("mass", lambda x: x.mass ),
])

SubjetCA15prunedType = NTupleObjectType("SubjetCA15prunedType", variables = [
    NTupleVariable("pt", lambda x: x.pt ),
    NTupleVariable("eta", lambda x: x.eta ),
    NTupleVariable("phi", lambda x: x.phi ),
    NTupleVariable("mass", lambda x: x.mass ),
    NTupleVariable("btag", lambda x: x.btag ),
])

# ==============================



def getTreeProducer(conf):
    #Create the output TTree writer
    #Here we define all the variables that we want to save in the output TTree
    treeProducer = cfg.Analyzer(
        class_object = AutoFillTreeProducer,
        verbose = False,
        vectorTree = True,
        globalVariables = [

            # Used by Subjet Analyzer

            NTupleVariable(
                "n_bjets",
                lambda ev: ev.n_bjets if hasattr(ev,'n_bjets') else -1,
                help="Number of selected bjets in event"
            ),

            NTupleVariable(
                "n_ljets",
                lambda ev: ev.n_ljets if hasattr(ev,'n_ljets') else -1,
                help="Number of selected ljets in event"
            ),

            NTupleVariable(
                "n_bjets_sj",
                lambda ev: ev.n_bjets_sj if hasattr(ev,'n_bjets_sj') else -1,
                help="Number of selected bjets in subjet-modified bjet list"
            ),

            NTupleVariable(
                "n_ljets_sj",
                lambda ev: ev.n_ljets_sj if hasattr(ev,'n_ljets_sj') else -1,
                help="Number of selected ljets in subjet-modified ljet list"
            ),


            NTupleVariable(
                "nhttCandidate",
                lambda ev: ev.nhttCandidate if hasattr(ev,'nhttCandidate') else -1,
                help="Number of original httCandidates in event"
            ),

            NTupleVariable(
                "nhttCandidate_aftercuts",
                lambda ev: ev.nhttCandidate_aftercuts \
                    if hasattr(ev,'nhttCandidate_aftercuts') else -1,
                help="Number of httCandidates that passed the cut"
            ),

            NTupleVariable(
                "Matching_subjet_bjet",
                lambda ev: ev.Matching_subjet_bjet \
                    if hasattr(ev, 'Matching_subjet_bjet') else -1,
                help="Number of subjets matched to btagged_jets"
            ),

            NTupleVariable(
                "Matching_subjet_ljet",
                lambda ev: ev.Matching_subjet_ljet \
                    if hasattr(ev, 'Matching_subjet_ljet') else -1,
                help="Number of subjets matched to wquark_candidate_jets"
            ),

            NTupleVariable(
                "Matching_event_type_number",
                lambda ev: ev.Matching_event_type_number \
                    if hasattr(ev, 'Matching_event_type_number') else -1,
                help="Type number of the event (see doc, todo)"
            ),

            NTupleVariable(
                "Matching_btag_disagreement",
                lambda ev: ev.Matching_btag_disagreement \
                    if hasattr(ev, 'Matching_btag_disagreement') else -1,
                help="Checks if there was a conflict between the b-tagged subjets and the b-tagged jets"
            ),

            # Quark matching: attempted or not
            NTupleVariable(
                "QMatching_t_attempted",
                lambda ev: ev.QMatching_t_attempted \
                    if hasattr(ev, 'QMatching_t_attempted') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_H_attempted",
                lambda ev: ev.QMatching_H_attempted \
                    if hasattr(ev, 'QMatching_H_attempted') else -1,
                help="" ),

            # Quark matching branches: subjets
            NTupleVariable(
                "QMatching_sj_hadr_bquark",
                lambda ev: ev.QMatching_sj_hadr_bquark \
                    if hasattr(ev, 'QMatching_sj_hadr_bquark') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_sj_lquark1",
                lambda ev: ev.QMatching_sj_lquark1 \
                    if hasattr(ev, 'QMatching_sj_lquark1') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_sj_lquark2",
                lambda ev: ev.QMatching_sj_lquark2 \
                    if hasattr(ev, 'QMatching_sj_lquark2') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_sj_lept_bquark",
                lambda ev: ev.QMatching_sj_lept_bquark \
                    if hasattr(ev, 'QMatching_sj_lept_bquark') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_sj_bquark_higgs1",
                lambda ev: ev.QMatching_sj_bquark_higgs1 \
                    if hasattr(ev, 'QMatching_sj_bquark_higgs1') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_sj_bquark_higgs2",
                lambda ev: ev.QMatching_sj_bquark_higgs2 \
                    if hasattr(ev, 'QMatching_sj_bquark_higgs2') else -1,
                help="" ),

            # Quark matching branches: subjets from other top
            NTupleVariable(
                "QMatching_sj_ot_hadr_bquark",
                lambda ev: ev.QMatching_sj_ot_hadr_bquark \
                    if hasattr(ev, 'QMatching_sj_ot_hadr_bquark') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_sj_ot_lquark1",
                lambda ev: ev.QMatching_sj_ot_lquark1 \
                    if hasattr(ev, 'QMatching_sj_ot_lquark1') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_sj_ot_lquark2",
                lambda ev: ev.QMatching_sj_ot_lquark2 \
                    if hasattr(ev, 'QMatching_sj_ot_lquark2') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_sj_ot_lept_bquark",
                lambda ev: ev.QMatching_sj_ot_lept_bquark \
                    if hasattr(ev, 'QMatching_sj_ot_lept_bquark') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_sj_ot_bquark_higgs1",
                lambda ev: ev.QMatching_sj_ot_bquark_higgs1 \
                    if hasattr(ev, 'QMatching_sj_ot_bquark_higgs1') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_sj_ot_bquark_higgs2",
                lambda ev: ev.QMatching_sj_ot_bquark_higgs2 \
                    if hasattr(ev, 'QMatching_sj_ot_bquark_higgs2') else -1,
                help="" ),

            # Quark matching branches: jets
            NTupleVariable(
                "QMatching_jet_hadr_bquark",
                lambda ev: ev.QMatching_jet_hadr_bquark \
                    if hasattr(ev, 'QMatching_jet_hadr_bquark') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_jet_lquark1",
                lambda ev: ev.QMatching_jet_lquark1 \
                    if hasattr(ev, 'QMatching_jet_lquark1') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_jet_lquark2",
                lambda ev: ev.QMatching_jet_lquark2 \
                    if hasattr(ev, 'QMatching_jet_lquark2') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_jet_lept_bquark",
                lambda ev: ev.QMatching_jet_lept_bquark \
                    if hasattr(ev, 'QMatching_jet_lept_bquark') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_jet_bquark_higgs1",
                lambda ev: ev.QMatching_jet_bquark_higgs1 \
                    if hasattr(ev, 'QMatching_jet_bquark_higgs1') else -1,
                help="" ),
            NTupleVariable(
                "QMatching_jet_bquark_higgs2",
                lambda ev: ev.QMatching_jet_bquark_higgs2 \
                    if hasattr(ev, 'QMatching_jet_bquark_higgs2') else -1,
                help="" ),
            #--END OF USED BY SUBJETANALYZER--#

            NTupleVariable(
                "Wmass", lambda ev: ev.Wmass,
                help="best W boson mass from untagged pair (untagged by CSVM)"
            ),
            NTupleVariable(
                "is_sl", lambda ev: ev.is_sl,
                help="event is single-lepton"
            ),
            NTupleVariable(
                "is_dl", lambda ev: ev.is_dl,
                help="event is di-lepton"
            ),

            NTupleVariable(
                "cat", lambda ev: ev.catn,
                type=int,
                help="ME category"
            ),

            NTupleVariable(
                "cat_btag", lambda ev: ev.cat_btag_n,
                type=int,
                help="ME category (b-tag)"
            ),

            NTupleVariable(
                "cat_gen", lambda ev: ev.n_cat_gen,
                type=int,
                help="top decay category (-1 unknown, 0 single-leptonic, 1 di-leptonic, 2 fully hadronic)"
            ),

            NTupleVariable(
                "nGenBHiggs", lambda ev: len(ev.b_quarks_h),
                type=int,
                help="Number of generated b from higgs"
            ),

            NTupleVariable(
                "nGenBTop", lambda ev: len(ev.b_quarks_t),
                type=int,
                help="Number of generated b from top"
            ),

            NTupleVariable(
                "nGenQW", lambda ev: len(ev.l_quarks_w),
                type=int,
                help="Number of generated quarks from W"
            ),

            NTupleVariable(
                "nGenNuTop", lambda ev: len(ev.nu_top),
                type=int,
                help="Number of generated nu from top"
            ),

            NTupleVariable(
                "nGenLepTop", lambda ev: len(ev.lep_top),
                type=int,
                help="Number of generated charged leptons from top"
            ),

            ###
            NTupleVariable(
                "btag_lr_2b_2c", lambda ev: ev.btag_lr_2b_2c,
                help="B-tagging likelihood ratio: 2b, 2c (13TeV CSV curves)"
            ),

            NTupleVariable(
                "btag_lr_2b_1c", lambda ev: ev.btag_lr_2b_1c,
                help="B-tagging likelihood ratio: 2b, 1c (13TeV CSV curves)"
            ),

            NTupleVariable(
                "btag_lr_4b_1c", lambda ev: ev.btag_lr_4b_1c,
                help="B-tagging likelihood ratio: 4b, 1c (13TeV CSV curves)"
            ),

            NTupleVariable(
                "btag_lr_4b", lambda ev: ev.btag_lr_4b,
                help="B-tagging likelihood ratio: 4b (13TeV CSV curves)"
            ),

            NTupleVariable(
                "btag_lr_2b", lambda ev: ev.btag_lr_2b,
                help="B-tagging likelihood ratio: 2b (13TeV CSV curves)"
            ),
            ###

            NTupleVariable(
                "btag_LR_4b_2b_old", lambda ev: ev.btag_LR_4b_2b_old,
                help="B-tagging likelihood ratio: 4b vs 2b (8TeV CSV curves)"
            ),
            NTupleVariable(
                "btag_LR_4b_2b", lambda ev: ev.btag_LR_4b_2b,
                help="B-tagging likelihood ratio: 4b vs 2b"
            ),
            NTupleVariable(
                "btag_LR_4b_2b_alt", lambda ev: ev.btag_LR_4b_2b_alt,
                help="B-tagging likelihood ratio: 4b vs 2b with multi-dimensional pt/eta binning for CSV"
            ),
            NTupleVariable(
                "nMatchSimB", lambda ev: ev.nMatchSimB if hasattr(ev, "nMatchSimB") else 0,
                type=int,
                help="number of gen B not matched to top decay"
            ),
            NTupleVariable(
                "nMatchSimC", lambda ev: ev.nMatchSimC if hasattr(ev, "nMatchSimC") else 0,
                type=int,
                help="number of gen C not matched to W decay"
            ),

            NTupleVariable(
                "nBCSVM", lambda ev: ev.nBCSVM if hasattr(ev, "nBCSVM") else 0,
                type=int,
                help="Number of good jets passing CSVM"
            ),
            NTupleVariable(
                "nBCSVT", lambda ev: ev.nBCSVT if hasattr(ev, "nBCSVT") else 0,
                type=int,
                help="Number of good jets passing CSVT"
            ),
            NTupleVariable(
                "nBCSVL", lambda ev: ev.nBCSVL if hasattr(ev, "nBCSVL") else 0,
                type=int,
                help="Number of good jets passing CSVL"
            ),

            NTupleVariable(
                "nTrueBTaggedCSVM", lambda ev: ev.n_tagwp_tagged_true_bjets if hasattr(ev, "n_tagwp_tagged_true_bjets") else 0,
                type=int,
                help=""
            ),

            NTupleVariable(
                "nTrueBTaggedLR", lambda ev: ev.n_lr_tagged_true_bjets if hasattr(ev, "n_lr_tagged_true_bjets") else 0,
                type=int,
                help=""
            ),

            NTupleVariable(
                "nMatch_wq", lambda ev: ev.nMatch_wq if hasattr(ev, "nMatch_wq") else 0,
                type=int,
                help="Number of jets matched to gen-level light quarks from W, without taking into account anti b-tagging"
            ),
            NTupleVariable(
                "nMatch_wq_btag", lambda ev: ev.nMatch_wq_btag if hasattr(ev, "nMatch_wq_btag") else 0,
                type=int,
                help="Number of jets matched to gen-level light quarks from W, taking into account anti b-tagging"
            ),

            NTupleVariable(
                "nMatch_tb", lambda ev: ev.nMatch_tb if hasattr(ev, "nMatch_tb") else 0,
                type=int,
                help="Number of jets matched to gen-level b quarks from top, without taking into account b-tagging"
            ),
            NTupleVariable(
                "nMatch_tb_btag", lambda ev: ev.nMatch_tb_btag if hasattr(ev, "nMatch_tb_btag") else 0,
                type=int,
                help="Number of jets matched to gen-level b quarks from top, taking into account b-tagging"
            ),

            NTupleVariable(
                "nMatch_hb", lambda ev: ev.nMatch_hb if hasattr(ev, "nMatch_hb") else 0,
                type=int,
                help="Number of jets matched to gen-level b quarks from higgs, without taking into account b-tagging"
            ),
            NTupleVariable(
                "nMatch_hb_btag", lambda ev: ev.nMatch_hb_btag if hasattr(ev, "nMatch_hb_btag") else 0,
                type=int,
                help="Number of jets matched to gen-level b quarks from higgs, taking into account b-tagging"
            ),

            NTupleVariable(
                "numJets", lambda ev: ev.numJets if hasattr(ev, "numJets") else 0,
                type=int,
                help="Number of jets passing jet selection"
            ),

            NTupleVariable(
                "lheNj", lambda ev: ev.input.lheNj if hasattr(ev.input, "lheNj") else 0,
                type=int,
                help=""
            ),
            NTupleVariable(
                "lheNb", lambda ev: ev.input.lheNb if hasattr(ev.input, "lheNb") else 0,
                type=int,
                help=""
            ),
            NTupleVariable(
                "lheNc", lambda ev: ev.input.lheNc if hasattr(ev.input, "lheNc") else 0,
                type=int,
                help=""
            ),
            NTupleVariable(
                "lheNg", lambda ev: ev.input.lheNg if hasattr(ev.input, "lheNg") else 0,
                type=int,
                help=""
            ),

            NTupleVariable(
                "n_mu_tight", lambda ev: ev.n_mu_tight if hasattr(ev, "n_mu_tight") else 0,
                type=int,
                help="Number of tight selected muons"
            ),

            NTupleVariable(
                "n_el_tight", lambda ev: ev.n_el_tight if hasattr(ev, "n_el_tight") else 0,
                type=int,
                help="Number of tight selected electrons"
            ),

            NTupleVariable(
                "n_mu_loose", lambda ev: ev.n_mu_loose if hasattr(ev, "n_mu_loose") else 0,
                type=int,
                help="Number of loose (DL) selected muons"
            ),

            NTupleVariable(
                "n_el_loose", lambda ev: ev.n_el_loose if hasattr(ev, "n_el_loose") else 0,
                type=int,
                help="Number of loose (DL) selected electrons"
            ),

            NTupleVariable(
                "tth_px_gen", lambda ev: ev.tth_px_gen if hasattr(ev, "tth_px_gen") else 0,
                help="generator-level ttH system px"
            ),
            NTupleVariable(
                "tth_py_gen", lambda ev: ev.tth_py_gen if hasattr(ev, "tth_py_gen") else 0,
                help="generator-level ttH system py"
            ),
            NTupleVariable(
                "tth_px_reco", lambda ev: ev.tth_px_reco if hasattr(ev, "tth_px_reco") else 0,
                help="reco-level ttH system px from matched jets and leptons"
            ),
            NTupleVariable(
                "tth_py_reco", lambda ev: ev.tth_py_reco if hasattr(ev, "tth_py_reco") else 0,
                help="reco-level ttH system py from matched jets and leptons"
            ),

            NTupleVariable(
                "tth_rho_px_reco", lambda ev: ev.tth_rho_px_reco if hasattr(ev, "tth_rho_px_reco") else 0,
                help="reco-level ttH system recoil px"
            ),
            NTupleVariable(
                "tth_rho_py_reco", lambda ev: ev.tth_rho_py_reco if hasattr(ev, "tth_rho_py_reco") else 0,
                help="reco-level ttH system recoil py"
            ),

            NTupleVariable(
                "tth_rho_px_gen", lambda ev: ev.tth_rho_px_gen if hasattr(ev, "tth_rho_px_gen") else 0,
                help="gen-level ttH system recoil px"
            ),
            NTupleVariable(
                "tth_rho_py_gen", lambda ev: ev.tth_rho_py_gen if hasattr(ev, "tth_rho_py_gen") else 0,
                help="gen-level ttH system recoil py"
            ),
        ],
        #FIXME: fill these from the VHbb ntuples
        globalObjects = {},
        collections = {
        #standard dumping of objects
            "met" : NTupleCollection("met", metType, 1, help="Reconstructed MET"),
            "met_gen" : NTupleCollection("met_gen", metType, 1, help="Generated MET"),
            "met_jetcorr" : NTupleCollection("met_jetcorr", metType, 1, help="Reconstructed MET, corrected to gen-level jets"),
            "tt_met" : NTupleCollection("met_ttbar_gen", metType, 1, help="Generated MET from nu(top)"),

            "b_quarks_gen" : NTupleCollection("b_quarks_gen", quarkType, 5, help=""),
            "l_quarks_gen" : NTupleCollection("l_quarks_gen", quarkType, 3, help=""),
            "b_quarks_t" : NTupleCollection("GenBFromTop", quarkType, 3, help=""),
            "b_quarks_h" : NTupleCollection("GenBFromHiggs", quarkType, 3, help=""),
            "l_quarks_w" : NTupleCollection("GenQFromW", quarkType, 5, help=""),
            "good_jets" : NTupleCollection("jets", jetType, 9, help="Selected jets"),
            "good_leptons" : NTupleCollection("leps", leptonType, 2, help="Selected leptons"),

            # V11 & V12
            # ==============================
            "httCandidate_AC" : NTupleCollection("httCandidate_AC", httCandidateType, 28, help=""),
            "FatjetCA15ungroomed" : NTupleCollection("FatjetCA15ungroomed", FatjetCA15ungroomedType, 8, help=""),
            "FatjetCA15pruned" : NTupleCollection("FatjetCA15pruned", FatjetCA15prunedType, 4, help=""),
            "SubjetCA15pruned" : NTupleCollection("SubjetCA15pruned", SubjetCA15prunedType, 5, help=""),
            # ==============================

            "mem_results_tth" : NTupleCollection("mem_tth", memType, len(conf.mem["methodsToRun"]), help="MEM tth"),
            "mem_results_ttbb" : NTupleCollection("mem_ttbb", memType, len(conf.mem["methodsToRun"]), help="MEM ttbb"),
        }
    )
    return treeProducer
