import os
from collections import OrderedDict
from TTH.MEAnalysis.MEMConfig import MEMConfig
import ROOT
from ROOT import MEM
#import VHbbAnalysis.Heppy.TriggerTableData as trigData
#import VHbbAnalysis.Heppy.TriggerTable as trig
import TTH.MEAnalysis.TriggerTable as trig

def jet_baseline(jet):
    #Require that jet must have at least loose POG_PFID
    #Look in Heppy autophobj.py and Jet.py
    return (jet.jetId >= 1)

# LB: in fact,  mu.tightId should contain all the other cuts
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Tight_Muon
# nanoAOD is using CMSSW definiton: https://github.com/cms-sw/cmssw/blob/master/DataFormats/MuonReco/src/MuonSelectors.cc#L854
def mu_baseline_tight(mu):
    return (
        mu.tightId == 1 
    )

def print_mu(mu):
    print "Muon: (pt=%s, eta=%s, tight=%s, dxy=%s, dz=%s, nhits=%s, stat=%s)" % (mu.pt, mu.eta, mu.tightId, mu.dxy , mu.dz, (getattr(mu, "nMuonHits", 0) > 0 or getattr(mu, "nChamberHits", 0) > 0) , mu.nStations)

factorizedJetCorrections = []

def el_baseline_loose(el):
    sca = abs(el.etaSc)
    ret = ( el.eleCutId == 2 and
            not ( sca >= 1.4442 and
                  sca < 1.5669 )
    )

    return ret

def el_baseline_medium(el):
    sca = abs(el.etaSc)
    ret = ( el.eleCutId == 3 and
            not ( sca >= 1.4442 and
                  sca < 1.5669 )
    )

    return ret

def el_baseline_tight(el):
    
    # Taken from https://gitlab.cern.ch/ttH/reference/blob/master/definitions/Moriond17.md#22-electron
    #  --> Usage of VID tools. Should also contain isolation cut
    sca = abs(el.etaSc)
    ret = ( el.eleCutId == 4 and
            not ( sca >= 1.4442 and
                  sca < 1.5669 )
    )
            
    return ret

def print_el(el):
    print "Electron: (pt=%s, eta=%s, convVeto=%s, etaSc=%s, dEta=%s, dPhi=%s, sieie=%s, HoE=%s, dxy=%s, dz=%s, nhits=%s, eOp=%s VIDID=%s)" % (
        el.pt, el.eta, el.convVeto, abs(el.etaSc), abs(el.DEta),
        abs(el.DPhi), el.sieie, el.hoe, abs(el.dxy),
        abs(el.dz), getattr(el, "eleExpMissingInnerHits", 0),
        getattr(el, "eleooEmooP", 0),
        getattr(el, "eleCutId",0)
    )

class Conf:
    leptons = {
        "mu": {

            #SL
            "SL": {
                "pt": 26,
                "eta":2.1,
                "iso": 0.15,
                "idcut": mu_baseline_tight,
            },
            "DL": {
                "iso": 0.25,
                "eta": 2.4,
                "idcut": mu_baseline_tight,
            },
            "veto": {
                "pt": 15.0,
                "eta": 2.4,
                "iso": 0.25,
                "idcut": mu_baseline_tight,
            },
            "isotype": "PFIso04_all", #pfRelIso - delta-beta, relIso - rho
            "debug" : print_mu
        },

        "el": {
            "SL": {
                "pt": 30,
                "eta": 2.1,
                "idcut": lambda el: el_baseline_tight(el),
            },
            "DL": {
                "eta": 2.4,
                "idcut": el_baseline_tight,
            },
            "veto": {
                "pt": 15.0,
                "eta": 2.4,
                "idcut": lambda el: el_baseline_loose(el),
            },
            #Isolation applied directly in el_baseline_tight using combIsoAreaCorr as cutoff
            "isotype": "relIso03", #KS: changed for nanoAOD.
            "debug" : print_el
        },
        "DL": {
            "pt_leading": 25,
            "pt_subleading": 15,
        },
        "selection": lambda event: event.is_sl or event.is_dl,
    }

    jets = {
        # pt, |eta| thresholds for **leading two jets** (common between sl and dl channel)
        "pt":   30,
        "eta":  2.4,

        # pt, |eta| thresholds for **leading jets** specific to sl channel
        "pt_sl":  30,
        "eta_sl": 2.4,

        # pt, |eta| thresholds for **trailing jets** specific to dl channel
        "pt_dl":  20,
        "eta_dl": 2.4,

        # pt threshold for leading jets in fh channel
        "pt_fh": 40,

        # nhard'th jet is used for pt threshold
        "nhard_fh": 6,

        # minimum number of jets to save event in tree
        "minjets_fh": 6,

        #The default b-tagging algorithm (branch name)
        "btagAlgo": "btagCSV",

        #The default b-tagging WP
        "btagWP": "CSVM",

        #The loose b-tag WP for QCD data estimation
        "looseBWP": "CSVL",


        #These working points are evaluated and stored in the trees as nB* - number of jets passing the WP
        #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation94X
        "btagWPs": {
            "CSVL": ("btagCSV", 0.5803),
            "CSVM": ("btagCSV", 0.8838),
            "CSVT": ("btagCSV", 0.9693),

            "DeepCSVL": ("btagDeepCSV", 0.1522),
            "DeepCSVM": ("btagDeepCSV", 0.4641),
            "DeepCSVT": ("btagDeepCSV", 0.8001),

            #Removed CMVA since not supported (at least in the BtagRecommendation94X
        },

        #if btagCSV, untagged/tagged selection for W mass and MEM is done by CSVM cut
        #if btagLR, selection is done by the btag likelihood ratio permutation
        #"untaggedSelection": "btagCMVA",
        "untaggedSelection": "btagCSV",

        #how many jets to consider for the btag LR permutations
        "NJetsForBTagLR": 15, #DS

        #base jet selection
        "selection": jet_baseline
    }

    trigger = {

        "filter": False,
        #Change to trig.triggerTable for 2017 menu (starting from 92X samples)
        "trigTable": trig.triggerTable2016,
        "trigTableData": trig.triggerTable2016,
    }

    general = {
        "passall": True,
        "boosted": False,
        "QGLtoDo": {
         #3:[(3,0)] => "evalute qg LR of 3q vs 0q(+3g), considering only light jets, in events with 3 b-jets"
            3:[(3,0),(3,2),(4,0),(4,3),(5,0),(5,4)], 
            4:[(3,0),(3,2),(4,0),(4,3),(5,0)] },
        "controlPlotsFile": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/3Dplots.root",
        #"QGLPlotsFile_flavour": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/Histos_QGL_flavour.root",
        "QGLPlotsFile_flavour": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/QGL_3dPlot.root",
        "sampleFile": os.environ["CMSSW_BASE"]+"/python/TTH/MEAnalysis/samples.py",
        "transferFunctionsPickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions.pickle",
        #"transferFunctionsPickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions_ttbar.pickle",
        "transferFunctions_sj_Pickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions_sj.pickle",
        #"transferFunctions_sj_Pickle": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/data/transfer_functions_sj_ttbar.pickle",
        "systematics": [
            "nominal",
        ] + [fj+sdir for fj in factorizedJetCorrections for sdir in ["Up", "Down"]],


        #If the list contains:
        # "gen" - print out the ttH gen-level particles (b from top, b form higgs, q from W, leptons
        # "reco" - print out the reco-level selected particles
        # "matching" - print out the association between gen and reco objects
        "verbosity": [
            #"eventboundary", #print run:lumi:event
            #"trigger", #print trigger bits
            #"input", #print input particles
            #"gen", #print out gen-level info
            #"matching", 
            #"debug", #very high-level debug info
            #"reco", #info about reconstructed final state
            #"meminput", #info about particles used for MEM input
            #"commoninput", #print out inputs for CommonClassifier
            #"commonclassifier",
        ],

        # "eventWhitelist": [
        #    # (1, 8471, 1181605),
        #    # (1, 10785, 1504514),
        #    # (1, 11359, 1584590),
        #    (1, 4034, 562719),
        # ]
    }

    #multiclass = {
    #    "bdtPickleFile": os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/BDT.pickle"
    #}

    #tth_mva = {
    #    "filename": os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/root/tth_bdt.pkl",
    #    "varlist": [
    #        "is_sl",
    #        "is_dl",
    #        "lep0_pt",
    #        "lep0_aeta",
    #        "lep1_pt",
    #        "lep1_aeta",
    #        "jet0_pt",
    #        "jet0_btag",
    #        "jet0_aeta",
    #        "jet1_pt",
    #        "jet1_btag",
    #        "jet1_aeta",
    #        "jet2_pt",
    #        "jet2_btag",
    #        "jet2_aeta",
    #        "mean_bdisc",
    #        "mean_bdisc_btag",
    #        "min_dr_btag",
    #        "mean_dr_btag",
    #        "std_dr_btag",
    #        "momentum_eig0",
    #        "momentum_eig1",
    #        "momentum_eig2",
    #        "fw_h0",
    #        "fw_h1",
    #        "fw_h2",
    #        "aplanarity",
    #        "isotropy",
    #        "numJets",
    #        "nBCSVM",
    #        "Wmass"
    #    ]
    #}

    mem = {

        #Actually run the ME calculation
        #If False, all ME values will be 0
        "calcME": True,
        "n_integration_points_mult": 1.0,
        "factorized_sources": factorizedJetCorrections,
        #compute MEM variations for these sources in the nominal case
        "jet_corrections": ["{0}{1}".format(corr, direction) for corr in factorizedJetCorrections for direction in ["Up", "Down"]],
        #compute MEM from scratch with these variations
        "enabled_systematics": [
            "nominal",
        #    "TotalUp",
        #    "TotalDown",
        ],

        "weight": 0.10, #k in Psb = Ps/(Ps+k*Pb)

        "blr_cuts": {
            "sl_j4_t2": 20,
            "sl_j4_t3": -20,
            "sl_j4_tge4": -20,

            "sl_j5_t2": 20,
            "sl_j5_t3": -20,
            "sl_j5_tge4": -20,

            "sl_jge6_t2": 20,
            "sl_jge6_t3": -20,
            "sl_jge6_tge4": -20,

            "dl_j3_t2": 20,
            "dl_j3_t3": -20,
            "dl_jge4_t2": 20,
            "dl_jge4_t3": -20,
            "dl_jge4_tge4": -20,

            ##[CHECK-ME]
            "fh_j9_t4": -20,
            "fh_j8_t3": -20,
            "fh_j8_t4": -20,
            "fh_j7_t4": -20,
            "fh_j7_t3": -20,
            "fh_jge6_t4": -20,
            "fh_jge6_t3": -20,
        },

        #Generic event-dependent selection function applied
        #just before the MEM. If False, MEM is skipped for all hypos
        #note that we set hypothesis-specific cuts below
        "selection": lambda event: (
                ((event.is_sl or event.is_dl) and
                (event.numJets>=4 and event.nBCSVM >= 4))
            #(event.is_fh and event.cat in ["cat7","cat8"]
            #and event.btag_LR_4b_2b > 0.95)
        ),

        #This configures the MEMs to actually run, the rest will be set to 0
        "methodsToRun": [
            "SL_0w2h2t",
            "DL_0w2h2t",
            "SL_1w2h2t",
            #"SL_2w2h1t_l",
            #"SL_2w2h1t_h",
            "SL_2w2h2t",
            #"SL_2w2h2t_1j",
            #"SL_2w2h2t_sj",
            #"SL_0w2h2t_sj",
            #"SL_2w2h2t_memLR",
            #"SL_0w2h2t_memLR",
            #"FH_4w2h2t", #8j,4b
            #"FH_3w2h2t", #7j,4b
            #"FH_4w2h1t", #7j,3b & 8j,3b
            #"FH_4w1h2t", #7j,3b & 8j,3b
            #"FH_3w2h1t", #7j,3b & 8j,3b (int. 1 jet)
            #"FH_0w2w2h2t", #all 4b cats
            #"FH_1w1w2h2t", #all 4b cats
            #"FH_0w0w2h2t", #all 4b cats
            #"FH_0w0w2h1t", #all cats
            #"FH_0w0w1h2t"  #all cats
        ],
        # btag LR cuts for FH MEM categories
        "FH_bLR_3b_SR": 0.94,
        "FH_bLR_4b_SR": 0.99,
        "FH_bLR_3b_excl": 1.96,
        "FH_bLR_4b_excl": 0.998,       
        "FH_bLR_3b_CR_lo": 0.60,
        "FH_bLR_3b_CR_hi": 0.94,
        "FH_bLR_4b_CR_lo": 0.80,
        "FH_bLR_4b_CR_hi": 0.99,
    }

    mem_configs = OrderedDict()

CvectorPermutations = getattr(ROOT, "std::vector<MEM::Permutations::Permutations>")
CvectorPSVar = getattr(ROOT, "std::vector<MEM::PSVar::PSVar>")

###
### SL_2w2h2t
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 2
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t"] = c

###
### SL_2w2h2t Sudakov
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
c.cfg.int_code |= MEM.IntegrandType.Sudakov
Conf.mem_configs["SL_2w2h2t_sudakov"] = c

###
### SL_2w2h2t Recoil
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
c.cfg.int_code |= MEM.IntegrandType.Recoil
Conf.mem_configs["SL_2w2h2t_recoil"] = c

###
### SL_2w2h2t No Tag
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t_notag"] = c

###
### SL_2w2h2t No Sym
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t_nosym"] = c


###
### SL_2w2h2t_1j
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 3
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
c.cfg.int_code += ROOT.MEM.IntegrandType.AdditionalRadiation
Conf.mem_configs["SL_2w2h2t_1j"] = c

###
### SL_1w2h2t
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 1 and
    ev.numJets == 5
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("1qW")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_1w2h2t"] = c

###
### SL_2w2h1t_l
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 3 and
    len(mcfg.l_quark_candidates(ev)) >= 1
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("2w2h1t_l")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h1t_l"] = c

###
### SL_2w2h1t_h
###
c = MEMConfig(Conf)
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 3 and
    len(mcfg.l_quark_candidates(ev)) >= 1
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("2w2h1t_h")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h1t_h"] = c

###
### SL_0w2h2t
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda ev: []
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    ev.numJets == 4
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("0qW")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
#c.cfg.int_code = 0
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_0w2h2t"] = c

###
### DL_0w2h2t
###
c = MEMConfig(Conf)
#c.b_quark_candidates = lambda ev: ev.good_jets
c.l_quark_candidates = lambda ev: []
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 2 and
    len(mcfg.b_quark_candidates(ev)) >= 4
    #(len(mcfg.l_quark_candidates(ev)) + len(mcfg.b_quark_candidates(ev))) >= 4
)
c.maxLJets = 4
c.mem_assumptions.add("dl")
strat = CvectorPermutations()
#FIXME: are we sure about these assumptions?
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.FirstRankedByBTAG)
c.cfg.perm_pruning = strat
Conf.mem_configs["DL_0w2h2t"] = c


#Subjet configurations#
#######################

#SL_2w2h2t_sj
c = MEMConfig(Conf)
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.l_quark_candidates = lambda event: \
                                     event.boosted_ljets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) == 4 and
    len(mcfg.l_quark_candidates(ev)) == 2 and
    ev.PassedSubjetAnalyzer == True
)
c.mem_assumptions.add("sl")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_2w2h2t_sj"] = c

#SL_0w2h2t_sj
c = MEMConfig(Conf)
# Select the custom jet lists
c.b_quark_candidates = lambda event: \
                                     event.boosted_bjets
c.l_quark_candidates = lambda event: \
                                     event.boosted_ljets
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 1 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    len(mcfg.l_quark_candidates(ev)) >= 0
)
c.mem_assumptions.add("sl")
c.mem_assumptions.add("0w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["SL_0w2h2t_sj"] = c

##SL_2w2h2t_sj_perm
#c = MEMConfig(Conf)
#c.do_calculate = lambda ev, mcfg: (
#    len(mcfg.lepton_candidates(ev)) == 1 and
#    len(mcfg.b_quark_candidates(ev)) >= 4 and
#    len(mcfg.l_quark_candidates(ev)) == 2
#)
#c.mem_assumptions.add("sl")
##FIXME: Thomas, why this is not required?
##strat.push_back(MEM.Permutations.QQbarBBbarSymmetry)
#strat = CvectorPermutations()
#strat.push_back(MEM.Permutations.HEPTopTagged)
#strat.push_back(MEM.Permutations.QUntagged)
#strat.push_back(MEM.Permutations.BTagged)
#c.cfg.perm_pruning = strat
#Conf.mem_configs["SL_2w2h2t_sj_perm"] = c

# apply btag LR cuts for FH MEM categories only if using btagLR
# must allow for overlapping 3b and 4b regions (both hypos run)
bLR = False
if Conf.jets["untaggedSelection"] == "btagLR":
    bLR = True

# btag LR cuts for FH MEM categories
FH_bLR_3b_SR = Conf.mem["FH_bLR_3b_SR"]
FH_bLR_4b_SR = Conf.mem["FH_bLR_4b_SR"]
FH_bLR_3b_excl = Conf.mem["FH_bLR_3b_excl"]
FH_bLR_4b_excl = Conf.mem["FH_bLR_4b_excl"]
FH_bLR_3b_CR_lo = Conf.mem["FH_bLR_3b_CR_lo"]
FH_bLR_3b_CR_hi = Conf.mem["FH_bLR_3b_CR_hi"]
FH_bLR_4b_CR_lo = Conf.mem["FH_bLR_4b_CR_lo"]
FH_bLR_4b_CR_hi = Conf.mem["FH_bLR_4b_CR_hi"]

###
### FH_4w2h2t #only 9j,4b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low #DS adds 5th,6th,... btags
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and #although from BTagLRAnalyzer there are max 4 candidates
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or 
     (ev.btag_LR_3b_2b < FH_bLR_3b_excl and ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) ) and
    ( #(len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))>=9 ) #DS do not consider 10 jet events
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("4w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry, but then add _l,_h for all missing-q methods
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_4w2h2t"] = c

###
### FH_3w2h2t #7j,4b & 8j,4b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or 
     (ev.btag_LR_3b_2b < FH_bLR_3b_excl and ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) ) and
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 ) #run two methods for 8j,4b category
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("3w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_3w2h2t"] = c

###
### FH_4w2h1t #7j,3b, 8j,3b (9j,3b) #do not need _l,_h if not imposing t-tbar symmetry
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_3b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_3b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    (bLR or len(mcfg.b_quark_candidates(ev)) == 3 ) and
    (not bLR or (ev.btag_LR_4b_2b < FH_bLR_4b_excl and (ev.btag_LR_3b_2b > FH_bLR_3b_SR or 
     (ev.btag_LR_3b_2b > FH_bLR_3b_CR_lo and ev.btag_LR_3b_2b < FH_bLR_3b_CR_hi) ) ) ) and
    ( len(mcfg.l_quark_candidates(ev)) >= 4 ) #max 9 jets considered in bLR, but only 5 light q for MEM
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("4w2h1t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_4w2h1t"] = c

###
### FH_4w1h2t #7j,3b, 8j,3b (9j,3b as drop 6th l jet) #DS
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_3b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_3b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    (bLR or len(mcfg.b_quark_candidates(ev)) == 3 ) and
    (not bLR or (ev.btag_LR_4b_2b < FH_bLR_4b_excl and (ev.btag_LR_3b_2b > FH_bLR_3b_SR or 
     (ev.btag_LR_3b_2b > FH_bLR_3b_CR_lo and ev.btag_LR_3b_2b < FH_bLR_3b_CR_hi) ) ) ) and
    ( len(mcfg.l_quark_candidates(ev)) == 4 or len(mcfg.l_quark_candidates(ev)) == 5
      or len(mcfg.l_quark_candidates(ev)) == 6 ) #DS
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("4w1h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_4w1h2t"] = c

###
### FH_3w2h1t #7j,3b, 8j,3b (int. 1 light jet)
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_3b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_3b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    (bLR or len(mcfg.b_quark_candidates(ev)) == 3 ) and
    (not bLR or (ev.btag_LR_4b_2b < FH_bLR_4b_excl and (ev.btag_LR_3b_2b > FH_bLR_3b_SR or 
     (ev.btag_LR_3b_2b > FH_bLR_3b_CR_lo and ev.btag_LR_3b_2b < FH_bLR_3b_CR_hi) ) ) ) and
    ( len(mcfg.l_quark_candidates(ev)) == 4 or len(mcfg.l_quark_candidates(ev)) == 5 )
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("3w2h1t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_3w2h1t"] = c

###
### FH_0w2w2h2t #all 4b categories: 7j,4b, 8j,4b, 9j,4b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or 
     (ev.btag_LR_3b_2b < FH_bLR_3b_excl and ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) ) and
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 ) 
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("0w2w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_0w2w2h2t"] = c

###
### FH_1w1w2h2t #all 4b categories: 7j,4b, 8j,4b, 9j,4b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or 
     (ev.btag_LR_3b_2b < FH_bLR_3b_excl and ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) ) and
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 ) 
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("1w1w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_1w1w2h2t"] = c

###
### FH_0w0w2h2t #all 4b categories: 7j,4b, 8j,4b, 9j,4b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 4 and
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or 
     (ev.btag_LR_3b_2b < FH_bLR_3b_excl and ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) ) and
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 )
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("0w0w2h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_0w0w2h2t"] = c

###
### FH_0w0w2h1t #all FH categories: 7j,4b, 8j,4b, 9j,4b, 7j,3b, 8j,3b, 9j,3b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b if (event.btag_LR_4b_2b > FH_bLR_4b_SR or (ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi)) else event.buntagged_jets_maxLikelihood_3b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b if (event.btag_LR_4b_2b > FH_bLR_4b_SR or (ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi)) else event.btagged_jets_maxLikelihood_3b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 3 and
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or ev.btag_LR_3b_2b > FH_bLR_3b_SR or
     (ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) or
     (ev.btag_LR_3b_2b > FH_bLR_3b_CR_lo and ev.btag_LR_3b_2b < FH_bLR_3b_CR_hi) ) and
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 )
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("0w0w2h1t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_0w0w2h1t"] = c

###
### FH_0w0w1h2t #all FH categories: 7j,4b, 8j,4b, 9j,4b, 7j,3b, 8j,3b, 9j,3b
###
c = MEMConfig(Conf)
c.l_quark_candidates = lambda event: event.buntagged_jets + event.selected_btagged_jets_low
if bLR:
    c.l_quark_candidates = lambda event: event.buntagged_jets_maxLikelihood_4b if (event.btag_LR_4b_2b > FH_bLR_4b_SR or (ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi)) else event.buntagged_jets_maxLikelihood_3b
    c.b_quark_candidates = lambda event: event.btagged_jets_maxLikelihood_4b if (event.btag_LR_4b_2b > FH_bLR_4b_SR or (ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi)) else event.btagged_jets_maxLikelihood_3b
c.do_calculate = lambda ev, mcfg: (
    len(mcfg.lepton_candidates(ev)) == 0 and
    len(mcfg.b_quark_candidates(ev)) >= 3 and
    (not bLR or ev.btag_LR_4b_2b > FH_bLR_4b_SR or ev.btag_LR_3b_2b > FH_bLR_3b_SR or
     (ev.btag_LR_4b_2b > FH_bLR_4b_CR_lo and ev.btag_LR_4b_2b < FH_bLR_4b_CR_hi) or
     (ev.btag_LR_3b_2b > FH_bLR_3b_CR_lo and ev.btag_LR_3b_2b < FH_bLR_3b_CR_hi) ) and
    ( (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==7 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==8 or
      (len(mcfg.l_quark_candidates(ev))+len(mcfg.b_quark_candidates(ev)))==9 )
)
c.mem_assumptions.add("fh")
c.mem_assumptions.add("0w0w1h2t")
strat = CvectorPermutations()
strat.push_back(MEM.Permutations.QQbarBBbarSymmetry) #FIXME: add t-tbar symmetry
strat.push_back(MEM.Permutations.QUntagged)
strat.push_back(MEM.Permutations.BTagged)
c.cfg.perm_pruning = strat
Conf.mem_configs["FH_0w0w1h2t"] = c

import inspect
def print_dict(d):
    s = "(\n"
    for k, v in sorted(d.items(), key=lambda x: x[0]):
        if callable(v) and not isinstance(v, ROOT.TF1):
            v = inspect.getsource(v).strip()
        elif isinstance(v, dict):
            s += print_dict(v)
        s += "  {0}: {1},\n".format(k, v)
    s += ")"
    return s

def conf_to_str(Conf):
    s = "Conf (\n"
    for k, v in sorted(Conf.__dict__.items(), key=lambda x: x[0]):
        s += "{0}: ".format(k)
        if isinstance(v, dict):
            s += print_dict(v) + ",\n"
        elif isinstance(v, ROOT.TF1):
            s += "ROOT.TF1({0}, {1})".format(v.GetName(), v.GetTitle()) + ",\n"
        else:
            s += str(v) + ",\n"
    s += "\n"
    return s
