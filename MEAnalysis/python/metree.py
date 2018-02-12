import PhysicsTools.HeppyCore.framework.config as cfg
import os
from PhysicsTools.Heppy.physicsutils.BTagWeightCalculator import BTagWeightCalculator
from TTH.MEAnalysis.MEMAnalyzer import MEMPermutation
from TTH.MEAnalysis.vhbb_utils import *

#Defines the output TTree branch structures
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer import *

#Override the default fillCoreVariables function, which
#by default looks for FWLite variables
#FIXME: this is a hack to run heppy on non-EDM formats. Better to propagate it to heppy
def fillCoreVariables(self, tr, event, isMC):
    if isMC:
        for x in ["run", "lumi", "evt", "genWeight"]: # Removed "xsec",  "puWeight"
            if x == "lumi" or x == "evt":
                tr.fill(x, getattr(event, x))
            else:
                tr.fill(x, getattr(event.input, x))
    else:
        for x in ["run", "lumi", "evt"]:
            if x == "lumi" or x == "evt":
                tr.fill(x, getattr(event, x))
            else:
                tr.fill(x, getattr(event.input, x))

AutoFillTreeProducer.fillCoreVariables = fillCoreVariables

lepton_sf_kind = [
    "SF_HLT_RunD4p2",
    "SF_HLT_RunD4p3",
    "SF_IdCutLoose",
    "SF_IdCutTight",
    "SF_IdMVALoose",
    "SF_IdMVATight",
    "SF_IsoLoose",
    "SF_IsoTight",
    "SF_trk_eta",
]

lepton_sf_kind_err = [x.replace("SF", "SFerr") for x in lepton_sf_kind]

#Specifies what to save for leptons
leptonType = NTupleObjectType("leptonType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("etaSc", lambda x : getattr(x, "etaSc", -99)),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("pdgId", lambda x : x.pdgId),
    NTupleVariable("iso", lambda x : x.iso),
    #NTupleVariable("ele_mva_id", lambda x : x.eleMVAIdSpring15Trig),
    NTupleVariable("mu_id", lambda x : 1*getattr(x, "looseIdPOG", 0) + 2*getattr(x, "tightId", 0)),
] + [NTupleVariable(sf, lambda x, sf=sf : getattr(x, sf, -1.0))
    for sf in lepton_sf_kind + lepton_sf_kind_err
])

p4type = NTupleObjectType("p4Type", variables = [
    NTupleVariable("pt", lambda x : x.Pt()),
    NTupleVariable("eta", lambda x : x.Eta()),
    NTupleVariable("phi", lambda x : x.Phi()),
    NTupleVariable("mass", lambda x : x.M()),
])

LHE_weights_type = NTupleObjectType("LHE_type", variables = [
    NTupleVariable("id", lambda x : x.id),
    NTupleVariable("wgt", lambda x : x.wgt),
])

#Specifies what to save for leptons
pvType = NTupleObjectType("pvType", variables = [
    NTupleVariable("z", lambda x : x.z),
    NTupleVariable("rho", lambda x : x.Rho),
    NTupleVariable("ndof", lambda x : x.ndof),
    NTupleVariable("isFake", lambda x : x.isFake),
])

quarkType = NTupleObjectType("quarkType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("pdgId", lambda x : x.pdgId),
])

genTopType = NTupleObjectType("genTopType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("decayMode", lambda x : x.decayMode),
])

metType = NTupleObjectType("metType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("px", lambda x : x.px),
    NTupleVariable("py", lambda x : x.py),
    NTupleVariable("sumEt", lambda x : x.sumEt),
    NTupleVariable("genPt", lambda x : x.genPt, mcOnly=True),
    NTupleVariable("genPhi", lambda x : x.genPhi, mcOnly=True),
])


perm_vars = [
    NTupleVariable("perm_{0}".format(i), lambda x : getattr(x, "perm_{0}".format(i)))
    for i in range(MEMPermutation.MAXOBJECTS)
]
memPermType = NTupleObjectType("memPermType", variables = [
    NTupleVariable("idx", lambda x : x.idx, type=int),
    NTupleVariable("p_mean", lambda x : x.p_mean),
    NTupleVariable("p_std", lambda x : x.p_std),
    NTupleVariable("p_tf_mean", lambda x : x.p_tf_mean),
    NTupleVariable("p_tf_std", lambda x : x.p_tf_std),
    NTupleVariable("p_me_mean", lambda x : x.p_me_mean),
    NTupleVariable("p_me_std", lambda x : x.p_me_std),
] + perm_vars)


FoxWolframType = NTupleObjectType("FoxWolframType", variables = [
    NTupleVariable("v", lambda x : x),
])

quarkType = NTupleObjectType("quarkType", variables = [
    NTupleVariable("pt", lambda x : x.pt),
    NTupleVariable("eta", lambda x : x.eta),
    NTupleVariable("phi", lambda x : x.phi),
    NTupleVariable("mass", lambda x : x.mass),
    NTupleVariable("id", lambda x : x.pdgId),
])

def makeGlobalVariable(vtype, systematic="nominal", mcOnly=False):
    name = vtype[0]
    typ = vtype[1]
    hlp = vtype[2]

    if len(vtype) == 3:
        func = lambda ev, systematic=systematic, name=name: \
            getattr(ev.systResults[systematic], name, -9999)
    elif len(vtype) == 4:
        if isinstance(vtype[3], str):
            func = lambda ev, systematic=systematic, name=vtype[3]: \
                getattr(ev.systResults[systematic], name, -9999)
        else:
            func = vtype[4]
    syst_suffix = "_" + systematic
    if systematic == "nominal":
        syst_suffix = ""
    return NTupleVariable(
        name + syst_suffix, func, type=typ, help=hlp, mcOnly=mcOnly
    )

topCandidateType = NTupleObjectType("topCandidateType", variables = [
    NTupleVariable("fRec", lambda x: x.fRec ),
    NTupleVariable("Ropt", lambda x: x.Ropt ),
    NTupleVariable("RoptCalc", lambda x: x.RoptCalc ),
    NTupleVariable("ptForRoptCalc", lambda x: x.ptForRoptCalc ),
    NTupleVariable("pt", lambda x: x.pt ),
    NTupleVariable("ptcal", lambda x: x.ptcal ),
    NTupleVariable("eta", lambda x: x.eta ),
    NTupleVariable("etacal", lambda x: x.etacal ),
    NTupleVariable("phi", lambda x: x.phi ),
    NTupleVariable("phical", lambda x: x.phical ),
    NTupleVariable("mass", lambda x: x.mass ),
    NTupleVariable("masscal", lambda x: x.masscal ),
    NTupleVariable("sjW1pt", lambda x: x.sjW1pt ),
    NTupleVariable("sjW1ptcal", lambda x: x.sjW1ptcal ),
    NTupleVariable("sjW1eta", lambda x: x.sjW1eta ),
    NTupleVariable("sjW1phi", lambda x: x.sjW1phi ),
    NTupleVariable("sjW1mass", lambda x: x.sjW1mass ),
    NTupleVariable("sjW1masscal", lambda x: x.sjW1masscal ),
    NTupleVariable("sjW1btag", lambda x: x.sjW1btag ),
    NTupleVariable("sjW2pt", lambda x: x.sjW2pt ),
    NTupleVariable("sjW2ptcal", lambda x: x.sjW2ptcal ),
    NTupleVariable("sjW2eta", lambda x: x.sjW2eta ),
    NTupleVariable("sjW2phi", lambda x: x.sjW2phi ),
    NTupleVariable("sjW2mass", lambda x: x.sjW2mass ),
    NTupleVariable("sjW2masscal", lambda x: x.sjW2masscal ),
    NTupleVariable("sjW2btag", lambda x: x.sjW2btag ),
    NTupleVariable("sjNonWpt", lambda x: x.sjNonWpt ),
    NTupleVariable("sjNonWptcal", lambda x: x.sjNonWptcal ),
    NTupleVariable("sjNonWeta", lambda x: x.sjNonWeta ),
    NTupleVariable("sjNonWphi", lambda x: x.sjNonWphi ),
    NTupleVariable("sjNonWmass", lambda x: x.sjNonWmass ),
    NTupleVariable("sjNonWmasscal", lambda x: x.sjNonWmasscal ),
    NTupleVariable("sjNonWbtag", lambda x: x.sjNonWbtag ),
    NTupleVariable("tau1", lambda x: x.tau1 ),   # Copied from matched fat jet
    NTupleVariable("tau2", lambda x: x.tau2 ),   # Copied from matched fat jet
    NTupleVariable("tau3", lambda x: x.tau3 ),   # Copied from matched fat jet
    NTupleVariable("bbtag", lambda x: x.bbtag ), # Copied from matched fat jet
    NTupleVariable("n_subjettiness", lambda x: x.n_subjettiness ), # Calculated
    NTupleVariable("n_subjettiness_groomed", lambda x: x.n_subjettiness_groomed ), # Calculated
    NTupleVariable("delRopt", lambda x: x.delRopt ),             # Calculated
    NTupleVariable("genTopHad_dr", lambda x: getattr(x, "genTopHad_dr", -1), help="DeltaR to the closest hadronic gen top" ),
    #NTupleVariable("genTopHad_index", lambda x: getattr(x, "genTopHad_index", -1), type=int, help="Index of the matched genTopHad" ),
])

higgsCandidateType = NTupleObjectType("higgsCandidateType", variables = [
    NTupleVariable("pt", lambda x: x.pt ),
    NTupleVariable("eta", lambda x: x.eta ),
    NTupleVariable("phi", lambda x: x.phi ),
    NTupleVariable("mass", lambda x: x.mass ),
    NTupleVariable("tau1", lambda x: x.tau1 ),
    NTupleVariable("tau2", lambda x: x.tau2 ),
    NTupleVariable("tau3", lambda x: x.tau3 ),
    NTupleVariable("bbtag", lambda x: x.bbtag ),

    NTupleVariable("nallsubjets_softdrop", lambda x: x.nallsubjets_softdrop ),
    NTupleVariable("nallsubjets_softdropz2b1", lambda x: x.nallsubjets_softdropz2b1 ),
    NTupleVariable("nallsubjets_softdropfilt", lambda x: x.nallsubjets_softdropfilt ),
    NTupleVariable("nallsubjets_softdropz2b1filt", lambda x: x.nallsubjets_softdropz2b1filt ),
    NTupleVariable("nallsubjets_pruned", lambda x: x.nallsubjets_pruned ),
    NTupleVariable("nallsubjets_subjetfiltered", lambda x: x.nallsubjets_subjetfiltered ),

    NTupleVariable("sj1pt_softdrop",   lambda x: x.sj1pt_softdrop ),
    NTupleVariable("sj1eta_softdrop",  lambda x: x.sj1eta_softdrop ),
    NTupleVariable("sj1phi_softdrop",  lambda x: x.sj1phi_softdrop ),
    NTupleVariable("sj1mass_softdrop", lambda x: x.sj1mass_softdrop ),
    NTupleVariable("sj1btag_softdrop", lambda x: x.sj1btag_softdrop ),
    NTupleVariable("sj2pt_softdrop",   lambda x: x.sj2pt_softdrop ),
    NTupleVariable("sj2eta_softdrop",  lambda x: x.sj2eta_softdrop ),
    NTupleVariable("sj2phi_softdrop",  lambda x: x.sj2phi_softdrop ),
    NTupleVariable("sj2mass_softdrop", lambda x: x.sj2mass_softdrop ),
    NTupleVariable("sj2btag_softdrop", lambda x: x.sj2btag_softdrop ),

    NTupleVariable("sj1pt_softdropz2b1",   lambda x: x.sj1pt_softdropz2b1 ),
    NTupleVariable("sj1eta_softdropz2b1",  lambda x: x.sj1eta_softdropz2b1 ),
    NTupleVariable("sj1phi_softdropz2b1",  lambda x: x.sj1phi_softdropz2b1 ),
    NTupleVariable("sj1mass_softdropz2b1", lambda x: x.sj1mass_softdropz2b1 ),
    NTupleVariable("sj1btag_softdropz2b1", lambda x: x.sj1btag_softdropz2b1 ),
    NTupleVariable("sj2pt_softdropz2b1",   lambda x: x.sj2pt_softdropz2b1 ),
    NTupleVariable("sj2eta_softdropz2b1",  lambda x: x.sj2eta_softdropz2b1 ),
    NTupleVariable("sj2phi_softdropz2b1",  lambda x: x.sj2phi_softdropz2b1 ),
    NTupleVariable("sj2mass_softdropz2b1", lambda x: x.sj2mass_softdropz2b1 ),
    NTupleVariable("sj2btag_softdropz2b1", lambda x: x.sj2btag_softdropz2b1 ),

    NTupleVariable("sj1pt_softdropfilt",   lambda x: x.sj1pt_softdropfilt ),
    NTupleVariable("sj1eta_softdropfilt",  lambda x: x.sj1eta_softdropfilt ),
    NTupleVariable("sj1phi_softdropfilt",  lambda x: x.sj1phi_softdropfilt ),
    NTupleVariable("sj1mass_softdropfilt", lambda x: x.sj1mass_softdropfilt ),
    NTupleVariable("sj1btag_softdropfilt", lambda x: x.sj1btag_softdropfilt ),
    NTupleVariable("sj2pt_softdropfilt",   lambda x: x.sj2pt_softdropfilt ),
    NTupleVariable("sj2eta_softdropfilt",  lambda x: x.sj2eta_softdropfilt ),
    NTupleVariable("sj2phi_softdropfilt",  lambda x: x.sj2phi_softdropfilt ),
    NTupleVariable("sj2mass_softdropfilt", lambda x: x.sj2mass_softdropfilt ),
    NTupleVariable("sj2btag_softdropfilt", lambda x: x.sj2btag_softdropfilt ),

    NTupleVariable("sj1pt_softdropz2b1filt",   lambda x: x.sj1pt_softdropz2b1filt ),
    NTupleVariable("sj1eta_softdropz2b1filt",  lambda x: x.sj1eta_softdropz2b1filt ),
    NTupleVariable("sj1phi_softdropz2b1filt",  lambda x: x.sj1phi_softdropz2b1filt ),
    NTupleVariable("sj1mass_softdropz2b1filt", lambda x: x.sj1mass_softdropz2b1filt ),
    NTupleVariable("sj1btag_softdropz2b1filt", lambda x: x.sj1btag_softdropz2b1filt ),
    NTupleVariable("sj2pt_softdropz2b1filt",   lambda x: x.sj2pt_softdropz2b1filt ),
    NTupleVariable("sj2eta_softdropz2b1filt",  lambda x: x.sj2eta_softdropz2b1filt ),
    NTupleVariable("sj2phi_softdropz2b1filt",  lambda x: x.sj2phi_softdropz2b1filt ),
    NTupleVariable("sj2mass_softdropz2b1filt", lambda x: x.sj2mass_softdropz2b1filt ),
    NTupleVariable("sj2btag_softdropz2b1filt", lambda x: x.sj2btag_softdropz2b1filt ),

    NTupleVariable("sj1pt_pruned",   lambda x: x.sj1pt_pruned ),
    NTupleVariable("sj1eta_pruned",  lambda x: x.sj1eta_pruned ),
    NTupleVariable("sj1phi_pruned",  lambda x: x.sj1phi_pruned ),
    NTupleVariable("sj1mass_pruned", lambda x: x.sj1mass_pruned ),
    NTupleVariable("sj1btag_pruned", lambda x: x.sj1btag_pruned ),
    NTupleVariable("sj2pt_pruned",   lambda x: x.sj2pt_pruned ),
    NTupleVariable("sj2eta_pruned",  lambda x: x.sj2eta_pruned ),
    NTupleVariable("sj2phi_pruned",  lambda x: x.sj2phi_pruned ),
    NTupleVariable("sj2mass_pruned", lambda x: x.sj2mass_pruned ),
    NTupleVariable("sj2btag_pruned", lambda x: x.sj2btag_pruned ),

    NTupleVariable("sj1pt_subjetfiltered",   lambda x: x.sj1pt_subjetfiltered ),
    NTupleVariable("sj1eta_subjetfiltered",  lambda x: x.sj1eta_subjetfiltered ),
    NTupleVariable("sj1phi_subjetfiltered",  lambda x: x.sj1phi_subjetfiltered ),
    NTupleVariable("sj1mass_subjetfiltered", lambda x: x.sj1mass_subjetfiltered ),
    NTupleVariable("sj1btag_subjetfiltered", lambda x: x.sj1btag_subjetfiltered ),
    NTupleVariable("sj2pt_subjetfiltered",   lambda x: x.sj2pt_subjetfiltered ),
    NTupleVariable("sj2eta_subjetfiltered",  lambda x: x.sj2eta_subjetfiltered ),
    NTupleVariable("sj2phi_subjetfiltered",  lambda x: x.sj2phi_subjetfiltered ),
    NTupleVariable("sj2mass_subjetfiltered", lambda x: x.sj2mass_subjetfiltered ),
    NTupleVariable("sj2btag_subjetfiltered", lambda x: x.sj2btag_subjetfiltered ),
    NTupleVariable("sj12masspt_subjetfiltered", lambda x: x.sj12masspt_subjetfiltered ), # take leading two pt subjets for mass
    NTupleVariable("sj12massb_subjetfiltered", lambda x: x.sj12massb_subjetfiltered ), # take leading two bjet from leading three pt subjets
    NTupleVariable("sj123masspt_subjetfiltered", lambda x: x.sj123masspt_subjetfiltered ), # take leading three pt subjets for mass
    NTupleVariable("secondbtag_subjetfiltered", lambda x: x.secondbtag_subjetfiltered ), 

    NTupleVariable("sj3pt_subjetfiltered",   lambda x: x.sj3pt_subjetfiltered ),
    NTupleVariable("sj3eta_subjetfiltered",  lambda x: x.sj3eta_subjetfiltered ),
    NTupleVariable("sj3phi_subjetfiltered",  lambda x: x.sj3phi_subjetfiltered ),
    NTupleVariable("sj3mass_subjetfiltered", lambda x: x.sj3mass_subjetfiltered ),
    NTupleVariable("sj3btag_subjetfiltered", lambda x: x.sj3btag_subjetfiltered ),

    NTupleVariable("mass_softdrop", lambda x: x.mass_softdrop, help="mass of the matched softdrop jet" ),
    NTupleVariable("mass_softdropz2b1", lambda x: x.mass_softdropz2b1, help="mass of the matched softdropz2b1 jet" ),

    NTupleVariable("mass_softdropfilt", lambda x: x.mass_softdropfilt, help="mass of the matched softdropfilt jet" ),
    NTupleVariable("mass_softdropz2b1filt", lambda x: x.mass_softdropz2b1filt, help="mass of the matched softdropz2b1filt jet" ),
    NTupleVariable("mass_pruned", lambda x: x.mass_pruned, help="mass of the matched pruned jet" ),
    NTupleVariable("n_subjettiness", lambda x: x.n_subjettiness ),
    NTupleVariable("dr_top", lambda x: getattr(x, "dr_top", -1), help="deltaR to the best HTT candidate"),
    NTupleVariable("dr_genHiggs", lambda x: getattr(x, "dr_genHiggs", -1), help="deltaR to gen higgs"),
    NTupleVariable("dr_genTop", lambda x: getattr(x, "dr_genTop", -1), help="deltaR to closest gen top"),
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

def getTreeProducer(conf):
    factorized_dw_vars = [
        NTupleVariable("dw_" + fc, lambda x,fc=fc : getattr(x, "dw", {}).get(fc, 0.0), type=float)
        for fc in conf.mem["jet_corrections"]
    ]
    
    variated_vars = [
        NTupleVariable("var_" + fc, lambda x,i=i : x.variated.at(i) if x.variated.size()>i else 0.0, type=float)
        for (i, fc) in enumerate(conf.mem["jet_corrections"])
    ]
    
    memType_nominal = NTupleObjectType("memType", variables = [
        NTupleVariable("p", lambda x : x.p),
        NTupleVariable("p_err", lambda x : x.p_err),
        #NTupleVariable("chi2", lambda x : x.chi2),
        NTupleVariable("time", lambda x : x.time),
        #NTupleVariable("error_code", lambda x : x.error_code, type=int),
        #NTupleVariable("efficiency", lambda x : x.efficiency),
        NTupleVariable("nperm", lambda x : x.num_perm, type=int),
    ] + factorized_dw_vars + variated_vars)
    
    memType_syst = NTupleObjectType("memType", variables = [
        NTupleVariable("p", lambda x : x.p),
        NTupleVariable("p_err", lambda x : x.p_err),
        #NTupleVariable("chi2", lambda x : x.chi2),
        #NTupleVariable("time", lambda x : x.time),
        #NTupleVariable("error_code", lambda x : x.error_code, type=int),
        #NTupleVariable("efficiency", lambda x : x.efficiency),
        #NTupleVariable("nperm", lambda x : x.num_perm, type=int),
    ])
   
    #create jet up/down variations
    corrs = [NTupleVariable(
            "corr_"+c,
            lambda x,c="corr_"+c : getattr(x, c),
            mcOnly=True,
            the_type=float,
        ) for c in conf.mem["jet_corrections"]
    ]

    #Specifies what to save for jets
    jetType = NTupleObjectType("jetType", variables = [
        NTupleVariable("pt", lambda x : x.pt),
        NTupleVariable("eta", lambda x : x.eta),
        NTupleVariable("phi", lambda x : x.phi),
        NTupleVariable("mass", lambda x : x.mass),
        NTupleVariable("id", lambda x : x.jetId),  
        NTupleVariable("qgl", lambda x : x.qgl),
        NTupleVariable("btagCSV", lambda x : x.btagCSV),
        NTupleVariable("btagDeepCSV", lambda x : x.btagDeepCSV),
        NTupleVariable("btagCMVA", lambda x : x.btagCMVA),
        #NTupleVariable("btagCMVA_log", lambda x : getattr(x, "btagCMVA_log", -20), help="log-transformed btagCMVA"),
        NTupleVariable("btagFlag", lambda x : getattr(x, "btagFlag", -1), help="Jet was considered to be a b in MEM according to the algo"),
        NTupleVariable("qg_sf", lambda x : getattr(x,"qg_sf",1.), type=float, mcOnly=True),
        NTupleVariable("partonFlavour", lambda x : x.partonFlavour, type=int, mcOnly=True),
        NTupleVariable("hadronFlavour", lambda x : x.hadronFlavour, type=int, mcOnly=True),
        NTupleVariable("matchFlag",
            lambda x : getattr(x, "tth_match_label_numeric", -1),
            type=int,
            mcOnly=True,
            help="0 - matched to light quark from W, 1 - matched to b form top, 2 - matched to b from higgs"
        ),
        NTupleVariable("matchBfromHadT", lambda x : getattr(x, "tth_match_label_bfromhadt", -1), type=int, mcOnly=True),
        NTupleVariable("mcPt", lambda x : x.mcPt, mcOnly=True),
        NTupleVariable("mcEta", lambda x : x.mcEta, mcOnly=True),
        NTupleVariable("mcPhi", lambda x : x.mcPhi, mcOnly=True),
        NTupleVariable("mcM", lambda x : x.mcM, mcOnly=True),
        NTupleVariable("mcMatchIdx", lambda x : x.mcMatchIdx, mcOnly=True),
        #NTupleVariable("mcNumBHadrons", lambda x : x.genjet.numBHadrons if hasattr(x, "genjet") else -1, mcOnly=True),
        #NTupleVariable("mcNumCHadrons", lambda x : x.genjet.numCHadrons if hasattr(x, "genjet") else -1, mcOnly=True),
        NTupleVariable("corr_JEC", lambda x : x.corr, mcOnly=True),
        #NTupleVariable("corr_JER", lambda x : x.corr_JER, mcOnly=True),
        NTupleVariable("puId", lambda x : x.puId),
    ] + corrs)

    #Create the output TTree writer
    #Here we define all the variables that we want to save in the output TTree
    treeProducer = cfg.Analyzer(
        class_object = AutoFillTreeProducer,
        defaultFloatType = "F",
        verbose = False,
        vectorTree = True,
        globalVariables = [

            # Used by Subjet Analyzer
            #NTupleVariable(
            #    "n_bjets",
            #    lambda ev: getattr(ev, "n_bjets_nominal", -1),
            #    help="Number of selected bjets in event"
            #),

            #NTupleVariable(
            #    "n_ljets",
            #    lambda ev: getattr(ev, "n_ljets_nominal", -1),
            #    help="Number of selected ljets in event"
            #),

            #NTupleVariable(
            #    "n_boosted_bjets",
            #    lambda ev: getattr(ev, "n_boosted_bjets_nominal", -1),
            #    help="Number of selected bjets in subjet-modified bjet list"
            #),

            #NTupleVariable(
            #    "n_boosted_ljets",
            #    lambda ev: getattr(ev, "n_boosted_ljets_nominal", -1),
            #    help="Number of selected ljets in subjet-modified ljet list"
            #),

            #NTupleVariable(
            #    "n_excluded_bjets",
            #    lambda ev: getattr(ev, "n_excluded_bjets_nominal", -1),
            #    help="Number of excluded bjets: reco resolved b-jets that match a subjet in the HTT-candidate"
            #),

            #NTupleVariable(
            #    "n_excluded_ljets",
            #    lambda ev: getattr(ev, "n_excluded_ljets_nominal", -1),
            #    help="Number of excluded ljets: "
            #),
            #--END OF USED BY SUBJETANALYZER--#

            NTupleVariable(
               "nGenBHiggs", lambda ev: len(getattr(ev, "b_quarks_h_nominal", [])),
               type=int,
               help="Number of generated b from higgs", mcOnly=True
            ),

            NTupleVariable(
               "nGenBTop", lambda ev: len(getattr(ev, "b_quarks_t_nominal", [])),
               type=int,
               help="Number of generated b from top", mcOnly=True
            ),

            NTupleVariable(
               "nGenQW", lambda ev: len(getattr(ev, "l_quarks_w_nominal", [])),
               type=int,
               help="Number of generated quarks from W", mcOnly=True
            ),
            
            NTupleVariable(
               "passPV", lambda ev: getattr(ev, "passPV", -1),
               type=int,
               help="First PV passes selection"
            ),

            NTupleVariable(
               "triggerDecision", lambda ev: getattr(ev, "triggerDecision", -1),
               type=int,
               help="Trigger selection"
            ),
            NTupleVariable(
               "triggerBitmask", lambda ev: getattr(ev, "triggerBitmask", -1),
               type=int,
               help="Bitmask of trigger decisions"
            ),
            NTupleVariable(
               "is_sl", lambda ev: ev.is_sl,
               type=int,
               help="is single-leptonic"
            ),
            NTupleVariable(
               "is_dl", lambda ev: ev.is_dl,
               type=int,
               help="is di-leptonic"
            ),
            NTupleVariable(
               "is_fh", lambda ev: ev.is_fh,
               type=int,
               help="is fully hadronic"
            ),
            #NTupleVariable("ht40", lambda ev: getattr(ev, "ht40", -9999), type=float, help="ht considering only jets with pT>40"),
            NTupleVariable("csv1", lambda ev: getattr(ev, "csv1", -9999), type=float, help="highest jet csv value"),
            NTupleVariable("csv2", lambda ev: getattr(ev, "csv2", -9999), type=float, help="2nd highest jet csv value"),

        ],
        globalObjects = {
           "MET" : NTupleObject("met", metType, help="Reconstructed MET"),
           #"MET_gen_nominal" : NTupleObject("met_gen", metType, help="Generated MET", mcOnly=True),
           #"MET_jetcorr_nominal" : NTupleObject("met_jetcorr", metType, help="Reconstructed MET, corrected to gen-level jets"),
           #"MET_tt_nominal" : NTupleObject("met_ttbar_gen", metType, help="Generated MET from nu(top)"),
           "primaryVertex" : NTupleObject("pv", pvType, help="First PV"),
           "dilepton_p4" : NTupleObject("ll", p4type, help="Dilepton system"),
        },
        collections = {
        #standard dumping of objects
        #These are collections which are not variated
            #"b_quarks_gen_nominal" : NTupleCollection("b_quarks_gen", quarkType, 5, help="generated b quarks", mcOnly=True),
            #"l_quarks_gen_nominal" : NTupleCollection("l_quarks_gen", quarkType, 3, help="generated light quarks", mcOnly=True),
            "b_quarks_t_nominal" : NTupleCollection("GenBFromTop", quarkType, 3, help="generated b quarks from top", mcOnly=True),
            "b_quarks_h_nominal" : NTupleCollection("GenBFromHiggs", quarkType, 3, help="generated b quarks from higgs", mcOnly=True),
            "l_quarks_w_nominal" : NTupleCollection("GenQFromW", quarkType, 5, help="generated light quarks from W", mcOnly=True),
            "GenHiggsBoson" : NTupleCollection("genHiggs", quarkType, 2, help="Generated Higgs boson", mcOnly=True),
            "genTopLep" : NTupleCollection("genTopLep", genTopType, 2, help="Generated top quark (leptonic)", mcOnly=True),
            "genTopHad" : NTupleCollection("genTopHad", genTopType, 2, help="Generated top quark (hadronic)", mcOnly=True),
            #"LHE_weights_scale" : NTupleCollection("LHE_weights_scale", LHE_weights_type, 6, help="LHE weights scale", mcOnly=True),
            #"LHE_weights_pdf" : NTupleCollection("LHE_weights_pdf", LHE_weights_type, 102, help="LHE weights pdf", mcOnly=True),

            #"FatjetCA15ungroomed" : NTupleCollection("fatjets", FatjetCA15ungroomedType, 4, help="Ungroomed CA 1.5 fat jets"),
            "good_jets_nominal" : NTupleCollection("jets", jetType, 16, help="Selected resolved jets, pt ordered"),
            "good_leptons_nominal" : NTupleCollection("leps", leptonType, 2, help="Selected leptons"),
            
            "loose_jets_nominal" : NTupleCollection("loose_jets", jetType, 6, help="Additional jets with 20<pt<30"),
            
            #"topCandidate_nominal": NTupleCollection("topCandidate" , topCandidateType, 1, help="Best top candidate in event. Currently chosen by max deltaR wrt. lepton"),

            #"othertopCandidate_nominal": NTupleCollection("othertopCandidate", topCandidateType, 4, help="All other top candidates that pass HTTv2 cuts"),
            #"topCandidatesSync_nominal": NTupleCollection("topCandidatesSync" , topCandidateType, 4, help=""),
            #"higgsCandidate_nominal": NTupleCollection("higgsCandidate", higgsCandidateType, 4, help="Boosted Higgs candidates"),

        }
    )
    
    #add HLT bits to final tree
    trignames = []
    for pathname, trigs in list(conf.trigger["trigTable"].items()) + list(conf.trigger["trigTableData"].items()):
        for pref in ["HLT"]:
            #add trigger path (combination of trigger)
            _pathname = "_".join([pref, pathname])
            print _pathname
            if not _pathname in trignames:
                trignames += [_pathname]

            #add individual trigger bits
            for tn in trigs:
                #strip the star
                tn = pref + "_BIT_" + tn[:-1]
                if not tn in trignames:
                    trignames += [tn]
    print trignames

    for trig in trignames:
        treeProducer.globalVariables += [NTupleVariable(
            trig, lambda ev, name=trig: getattr(ev, name, -1), type=int, mcOnly=False
        )]

    
    #MET filter flags added in VHBB
    #According to https://gitlab.cern.ch/ttH/reference/blob/master/definitions/Moriond17.md#42-met-filters
    metfilter_flags = [
        "Flag_goodVertices", 
        #"Flag_GlobalTightHalo2016Filter", #Not in nanoAOD
        "Flag_HBHENoiseFilter",
        "Flag_HBHENoiseIsoFilter",
        "Flag_EcalDeadCellTriggerPrimitiveFilter",
        "Flag_eeBadScFilter",

        #TODO: These need to be added to VHBB somehow
        # "Flag_BadPFMuonFilter",
        # "Flag_BadChargedCandidateFilter",
        # "badGlobalMuonTagger",
        # "cloneGlobalMuonTagger",
    ]
    for metfilter in metfilter_flags:
        treeProducer.globalVariables += [NTupleVariable(
            trig, lambda ev, name=metfilter: getattr(ev.input, name, -1), type=int, mcOnly=False
        )]
       
    #Add systematically variated quantities
    for systematic in conf.general["systematics"]:

        #scalar variables that have systematic variations
        for vtype in [
            ("Wmass",               float,      "Best reconstructed W candidate mass"),
            ("mbb_closest",          float,      "Mass of geometrically closest bb pair"),
            ("cat",                 int,        "ME category", "catn"),
            ("cat_btag",            int,        "ME category (b-tag)", "cat_btag_n"),
            ("cat_gen",             int,        "top decay category (-1 unknown, 0 single-leptonic, 1 di-leptonic, 2 fully hadronic)", "cat_gen_n"),
            ("fh_region",           int,        "FH region for QCD estimation"), #DS
            #("btag_lr_4b",          float,      "4b, N-4 light, probability, 3D binning"),
            #("btag_lr_3b",          float,      "3b, N-3 light, probability, 3D binning"),
            #("btag_lr_2b",          float,      "2b, N-2 Nlight probability, 3D binning"),
            #("btag_lr_1b",          float,      "1b, N-1 Nlight probability, 3D binning"),
            #("btag_lr_0b",          float,      "0b, N   Nlight probability, 3D binning"),
            #("btag_LR_4b_2b_btagCMVA_log",   float,      ""),
            ("btag_LR_4b_2b_btagCMVA",        float,      "4b vs 2b b-tag likelihood ratio using the cMVA tagger"),
            ("btag_LR_4b_2b_btagCSV",        float,      "4b vs 2b b-tag likelihood ratio using the CSV tagger"),
            #("htt_mass",        float,      "HEPTopTagger candidate mass"),
            #("htt_frec",        float,      "HEPTopTagger candidate mass"),
            ("higgs_mass",      float,      "Higgs candidate mass"),
            #("btag_LR_4b_3b_btagCMVA_log",   float,      ""),
            ("btag_LR_4b_3b_btagCMVA",       float,      ""),
            ("btag_LR_4b_3b_btagCSV",        float,      ""),
            #("btag_LR_3b_2b_btagCMVA_log",   float,      ""),
            ("btag_LR_3b_2b_btagCMVA",       float,      ""),
            ("btag_LR_3b_2b_btagCSV",        float,      ""),
            #("btag_LR_geq2b_leq1b_btagCMVA_log",   float,   ""),
            ("btag_LR_geq2b_leq1b_btagCMVA",       float,   ""),
            ("btag_LR_geq2b_leq1b_btagCSV",        float,   ""),
            ("qg_LR_4b_flavour_3q_0q", float,      ""),
            #("qg_LR_4b_flavour_3q_2q", float,      ""),
            ("qg_LR_4b_flavour_4q_0q", float,      ""),
            #("qg_LR_4b_flavour_4q_3q", float,      ""),
            ("qg_LR_4b_flavour_5q_0q", float,      ""),
            #("qg_LR_3b_flavour_3q_0q", float,      ""),
            #("qg_LR_3b_flavour_3q_2q", float,      ""),
            ("qg_LR_3b_flavour_4q_0q", float,      ""),
            #("qg_LR_3b_flavour_4q_3q", float,      ""),
            ("qg_LR_3b_flavour_5q_0q", float,      ""),
            #("qg_LR_3b_flavour_5q_4q", float,      ""),

            ("nBCSVM",              int,      "Number of good jets that pass the CSV Medium WP"),
            ("nBCSVT",              int,      "Number of good jets that pass the DeepCSV Tight WP"),
            ("nBCSVL",              int,      "Number of good jets that pass the DeepCSV Loose WP"),
            ("nBDeepCSVM",          int,      "Number of good jets that pass the DeepCSV Medium WP"),
            #("nCSVv2IVFM",              int,      ""),                
            ("nBCMVAM",             int,      "Number of good jets that pass cMVAv2 Medium WP"),
            ("numJets",             int,        "Total number of good jets that pass jet ID"),
            #("ht",                  float,      ""),
            ("changes_jet_category",int,        "Jet category changed on systematic"),
            ("ht30",                float,      ""),
        ]:

            is_mc_only = False

            #only define the nominal values for data
            if systematic != "nominal":
                is_mc_only = True

            treeProducer.globalVariables += [makeGlobalVariable(vtype, systematic, mcOnly=is_mc_only)]
        #end of loop over syst variables 
        
        syst_suffix = "_" + systematic
        syst_suffix2 = syst_suffix
        if systematic == "nominal":
            syst_suffix2 = ""
       
        #add nominal and systematically variated final MEM ratios
        #these are simple scalars already
        for hypo in conf.mem["methodsToRun"]:
            treeProducer.globalVariables.append(
                NTupleVariable(
                    "mem_" + hypo + "_p" + syst_suffix2,
                    lambda ev, s="mem_" + hypo + "_p" + syst_suffix: getattr(ev, s, 0.0),
                    mcOnly = False,
                ),
            )
    #add full MEM output struct for nominal and the systematic case where we
    #explicitly recomputed the MEM
    for systematic in conf.general["systematics"]:
        syst_suffix = "_" + systematic
        syst_suffix2 = syst_suffix
        memType = memType_syst
        if systematic == "nominal":
            syst_suffix2 = ""
            memType = memType_nominal
        for hypo in conf.mem["methodsToRun"]:
            for proc in ["tth", "ttbb"]:
                name = "mem_{0}_{1}".format(proc, hypo) 
                treeProducer.globalObjects.update({
                    name + syst_suffix: NTupleObject(
                        name + syst_suffix2, memType ,
                        help="MEM result for proc={0} hypo={1} syst={2}".format(proc, hypo, systematic),
                        mcOnly = False if systematic == "nominal" else True
                    ),
                })

    #MC-only global variables
    for vtype in [
        ("nMatch_wq",               int,    ""),
        ("nMatch_wq_btag",          int,    ""),
        ("nMatch_tb",               int,    ""),
        ("nMatch_tb_btag",          int,    ""),
        ("nMatch_hb",               int,    ""),
        ("nMatch_hb_btag",          int,    ""),
        #("nMatch_q_htt",            int,    "number of light quarks matched to HEPTopTagger subjets"),
        #("nMatch_b_htt",            int,    "number of b-quarks matched to HEPTopTagger subjets"),
        #("nMatch_b_higgs",          int,    "number of b-quarks matched to HiggsTagger subjets"),
        ("ttCls",                   int,    "ttbar classification from GenHFHadronMatcher"),
        ("genHiggsDecayMode",       int,    ""),
        ("puWeightUp",              float,    ""),
        ("puWeightDown",            float,    ""),
        ("qgWeight",                float,  ""),
        ("nPU0",                    float,  ""),
        ("nTrueInt",                int,  ""),
        ("trigtrigTablegerEmulationWeight",  float,  ""),
        ("tth_rho_px_gen",  float,  ""),
        ("tth_rho_py_gen",  float,  ""),
        ("tth_rho_px_reco",  float,  ""),
        ("tth_rho_py_reco",  float,  ""),
    ]:
        treeProducer.globalVariables += [makeGlobalVariable(vtype, "nominal", mcOnly=True)]
   
    #for bweight in bweights:
    #    treeProducer.globalVariables += [
    #        makeGlobalVariable((bweight, float, ""), "nominal", mcOnly=True)
    #    ]

    for vtype in [
        ("rho",                     float,  ""),
        ("json",                    int,  ""),
        ("runrange",                int,  "integer index of the run range (A-F)"),
        ("nPVs",                    float,  ""),
    ]:
        treeProducer.globalVariables += [makeGlobalVariable(vtype, "nominal", mcOnly=False)]
    return treeProducer
