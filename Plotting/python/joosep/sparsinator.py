from __future__ import print_function

import ROOT
ROOT.gSystem.Load("libTTHMEAnalysis")

import math

import os
from collections import OrderedDict
import logging
LOG_MODULE_NAME = logging.getLogger(__name__)
    
import numpy as np
from TTH.MEAnalysis.samples_base import getSitePrefix, get_prefix_sample, TRIGGERPATH_MAP
from TTH.Plotting.Datacards.sparse import add_hdict, save_hdict

from TTH.Plotting.Datacards.AnalysisSpecificationClasses import SystematicProcess, CategoryCut
from TTH.CommonClassifier.db import ClassifierDB

from VHbbAnalysis.Heppy.btagSF import btagSFhandle, get_event_SF, initBTagSF
from TTH.MEAnalysis.leptonSF import calc_lepton_SF

CvectorLorentz = getattr(ROOT, "std::vector<TLorentzVector>")
Cvectordouble = getattr(ROOT, "std::vector<double>")
CvectorJetType = getattr(ROOT, "std::vector<MEMClassifier::JetType>")


#Need to access this to initialize the library (?)
dummy = ROOT.TTH_MEAnalysis.TreeDescription

#From https://gitlab.cern.ch/jpata/tthbb13/blob/FH_systematics/Plotting/Daniel/Helper.py#L7
#Derived by Silvio in a manual fit to semileptonic differential top pt data: CMS-PAS-TOP-17-002
topPTreweight = lambda x,y: math.exp(0.5*((0.0843616-0.000743051*x)+(0.0843616-0.000743051*y)))
topPTreweightUp = lambda x,y: math.exp(0.5*((0.00160296-0.000411375*x)+(0.00160296-0.000411375*y)))
topPTreweightDown = lambda x,y: math.exp(0.5*((0.16712-0.00107473*x)+(0.16712-0.00107473*y)))

syst_pairs = OrderedDict([
    (x+d, ROOT.TTH_MEAnalysis.Systematic.make_id(
        getattr(ROOT.TTH_MEAnalysis.Systematic, x),
        getattr(ROOT.TTH_MEAnalysis.Systematic, d if d != "" else "None")
    ))
    for x in [
        #"CMS_scale_j",
        "CMS_res_j",
        "CMS_scaleSubTotalPileUp_j",
        "CMS_scaleAbsoluteStat_j",
        "CMS_scaleAbsoluteScale_j",
        "CMS_scaleAbsoluteFlavMap_j",
        "CMS_scaleAbsoluteMPFBias_j",
        "CMS_scaleFragmentation_j",
        "CMS_scaleSinglePionECAL_j",
        "CMS_scaleSinglePionHCAL_j",
        "CMS_scaleFlavorQCD_j",
        "CMS_scaleTimePtEta_j",
        "CMS_scaleRelativeJEREC1_j",
        "CMS_scaleRelativeJEREC2_j",
        "CMS_scaleRelativeJERHF_j",
        "CMS_scaleRelativePtBB_j",
        "CMS_scaleRelativePtEC1_j",
        "CMS_scaleRelativePtEC2_j",
        "CMS_scaleRelativePtHF_j",
        "CMS_scaleRelativeFSR_j",
        "CMS_scaleRelativeStatFSR_j",
        "CMS_scaleRelativeStatEC_j",
        "CMS_scaleRelativeStatHF_j",
        "CMS_scalePileUpDataMC_j",
        "CMS_scalePileUpPtRef_j",
        "CMS_scalePileUpPtBB_j",
        "CMS_scalePileUpPtEC1_j",
        "CMS_scalePileUpPtEC2_j",
        "CMS_scalePileUpPtHF_j",

        "CMS_ttH_CSVcferr1",
        "CMS_ttH_CSVcferr2",
        "CMS_ttH_CSVhf",
        "CMS_ttH_CSVhfstats1",
        "CMS_ttH_CSVhfstats2",
        "CMS_ttH_CSVjes",
#        "CMS_ttH_CSVjesAbsoluteMPFBias",
#        "CMS_ttH_CSVjesAbsoluteScale",
#        "CMS_ttH_CSVjesFlavorQCD",
#        "CMS_ttH_CSVjesPileUpDataMC",
#        "CMS_ttH_CSVjesPileUpPtBB",
#        "CMS_ttH_CSVjesPileUpPtEC1",
#        "CMS_ttH_CSVjesPileUpPtRef",
#        "CMS_ttH_CSVjesRelativeFSR",
#        "CMS_ttH_CSVjesSinglePionECAL",
#        "CMS_ttH_CSVjesSinglePionHCAL",
#        "CMS_ttH_CSVjesTimePtEta",
        "CMS_ttH_CSVlf",
        "CMS_ttH_CSVlfstats1",
        "CMS_ttH_CSVlfstats2",
        
        "CMS_ttH_scaleME",

        "CMS_pu"
    ]
    for d in ["Up", "Down", ""]
])
syst_pairs["nominal"] = ROOT.TTH_MEAnalysis.Systematic.make_id(ROOT.TTH_MEAnalysis.Systematic.Nominal, ROOT.TTH_MEAnalysis.Systematic.None)
syst_pairs["CMS_ttH_CSV"] = ROOT.TTH_MEAnalysis.Systematic.make_id(ROOT.TTH_MEAnalysis.Systematic.CMS_ttH_CSV, ROOT.TTH_MEAnalysis.Systematic.None)

def vec_from_list(vec_type, src):
    """
    Creates a std::vector<T> from a python list.
    vec_type (ROOT type): vector datatype, ex: std::vector<double>
    src (iterable): python list
    """
    v = vec_type()
    for item in src:
        v.push_back(item)
    return v

def l4p(pt, eta, phi, m):
    v = ROOT.TLorentzVector()
    v.SetPtEtaPhiM(pt, eta, phi, m)
    return v

def logit(x):
    return np.log(x/(1.0 - x))

def lv_p4s(pt, eta, phi, m, btagCSV=-100):
    ret = ROOT.TLorentzVector()
    ret.SetPtEtaPhiM(pt, eta, phi, m)
    ret.btagCSV = btagCSV
    return ret

def pass_HLT_sl_mu(event):
    pass_hlt = event.HLT_ttH_SL_mu
    return event.is_sl and pass_hlt and len(event.leps_pdgId)>=1 and int(abs(event.leps_pdgId[0])) == 13

def pass_HLT_sl_el(event):
    pass_hlt = event.HLT_ttH_SL_el
    return event.is_sl and pass_hlt and len(event.leps_pdgId)>=1 and int(abs(event.leps_pdgId[0])) == 11

def pass_HLT_dl_mumu(event):
    pass_hlt = (event.HLT_ttH_DL_mumu) or (not event.HLT_ttH_DL_mumu and event.HLT_ttH_SL_mu)
    st = sum(map(abs, event.leps_pdgId))
    return event.is_dl and pass_hlt and st == 26

def pass_HLT_dl_elmu(event):
    pass_hlt = event.HLT_ttH_DL_elmu
    pass_hlt = pass_hlt or (not event.HLT_ttH_DL_elmu and (event.HLT_ttH_SL_el and not event.HLT_ttH_SL_mu))
    pass_hlt = pass_hlt or (not event.HLT_ttH_DL_elmu and (event.HLT_ttH_SL_mu and not event.HLT_ttH_SL_el))
    st = sum(map(abs, event.leps_pdgId))
    return event.is_dl and pass_hlt and st == 24

def pass_HLT_dl_elel(event):
    pass_hlt = event.HLT_ttH_DL_elel or (not event.HLT_ttH_DL_elel and event.HLT_ttH_SL_el)
    st = sum(map(abs, event.leps_pdgId))
    return event.is_dl and pass_hlt and st == 22

def pass_HLT_fh(event):
    pass_hlt = event.HLT_ttH_FH
    return event.is_fh and pass_hlt ## FIXME add: st == ??

def triggerPath(event):
    if event.is_sl and pass_HLT_sl_mu(event):
        return TRIGGERPATH_MAP["m"]
    elif event.is_sl and pass_HLT_sl_el(event):
        return TRIGGERPATH_MAP["e"]
    elif event.is_dl and pass_HLT_dl_mumu(event):
        return TRIGGERPATH_MAP["mm"]
    elif event.is_dl and pass_HLT_dl_elmu(event):
        return TRIGGERPATH_MAP["em"]
    elif event.is_dl and pass_HLT_dl_elel(event):
        return TRIGGERPATH_MAP["ee"]
    return 0

def fillBase(matched_processes, event, syst, schema):
    for proc in matched_processes:
        for (k, histo_out) in proc.outdict_syst.get(syst, {}).items():
            weight = 1.0 
            if schema == "mc" or schema == "mc_syst":
                weight = event.weight_nominal * proc.xs_weight
                if weight <= 0:
                    LOG_MODULE_NAME.error("weight_nominal<=0")

            if histo_out.cut(event):
                histo_out.fill(event, weight)


def fillSystematic(matched_processes, event, systematic_weights, schema):
    #pre-compute the event weights 
    precomputed_weights = [
        (syst_weight, weightfunc(event))
        for (syst_weight, weightfunc) in systematic_weights
    ]

    for (syst_weight, _weight) in precomputed_weights:
        for proc in matched_processes:
            for (k, histo_out) in proc.outdict_syst[syst_weight].items():
                weight = _weight * proc.xs_weight
                if histo_out.cut(event):
                    histo_out.fill(event, weight)

def applyCuts(event, matched_processes):
    #check if this event falls into any category
    any_passes = False
    if not hasattr(event, "cuts"):
        event.cuts = {}
    for proc in matched_processes:
        check_proc = CategoryCut(proc.cuts).cut(event)
        if not check_proc:
            continue
        for cut_name, cut in proc.outdict_cuts.items():
            cut_result = cut.cut(event)
            any_passes = any_passes or cut_result
            event.cuts[cut_name] = cut_result
    return any_passes

class FakeJet:
    def __init__(self, pt, eta, hadronFlavour, csv):
        self._pt = pt
        self._eta = eta
        self._hadronFlavour = hadronFlavour
        self._csv = csv

    def pt(self):
        return self._pt
    
    def eta(self):
        return self._eta
    
    def hadronFlavour(self):
        return self._hadronFlavour
    
    def btag(self, algo):
        return self._csv

def recompute_btag_weights(event):
    p4 = [j.lv for j in event.jets]
    btag = [j.btag for j in event.jets]
    hadronFlavour = [hf for hf in event.jets_hadronFlavour]
    
    wrapped_jets = []
    for _p4, btag, hf in zip(p4, btag, hadronFlavour):
        jet = FakeJet(
            _p4.Pt(),
            _p4.Eta(),
            hf,
            btag
        )
        wrapped_jets += [jet]

    btag_weights = [
        "up_cferr1",
        "up_cferr2",
        "up_hf",
        "up_hfstats1",
        "up_hfstats2",
        "up_jes",
        "up_jesAbsoluteMPFBias",
        "up_jesAbsoluteScale",
        "up_jesFlavorQCD",
        "up_jesPileUpDataMC",
        "up_jesPileUpPtBB",
        "up_jesPileUpPtEC1",
        "up_jesPileUpPtRef",
        "up_jesRelativeFSR",
        "up_jesSinglePionECAL",
        "up_jesSinglePionHCAL",
        "up_jesTimePtEta",
        "up_lf",
        "up_lfstats1",
        "up_lfstats2",
    ]

    btag_weights_recomputed = {}
    for algo in ["CSV"]:
        for btag_syst in [
                "central",
            ] + btag_weights + [bw.replace("up_", "down_") for bw in btag_weights]:
            sf = get_event_SF(wrapped_jets, btag_syst, algo, btagSFhandle)
            btag_weights_recomputed[btag_syst] = sf
            if btag_syst == "central":
                LOG_MODULE_NAME.debug("replacing bweight {0} with {1}".format(event.weights[syst_pairs["CMS_ttH_CSV"]], btag_weights_recomputed[btag_syst]))
                event.weights[syst_pairs["CMS_ttH_CSV"]] = btag_weights_recomputed[btag_syst]
            else:
                sdir, syst_name = btag_syst.split("_")
                sp = syst_pairs["CMS_ttH_CSV{0}{1}".format(syst_name, sdir.capitalize())]
                LOG_MODULE_NAME.debug("replacing bweight {0} with {1} ({2})".format(event.weights[sp], btag_weights_recomputed[btag_syst], btag_syst))
                event.weights[sp] = btag_weights_recomputed[btag_syst]
 
def createEvent(
    events, syst, schema,
    matched_processes,
    cls_bdt_sl, cls_bdt_dl,
    calculate_bdt, do_recompute_btag_weights,
    sample
    ):

    event = events.create_event(syst_pairs[syst])
    if schema.startswith("mc"): 
        event.topPTweight = 1.0
        event.topPTweightUp = 1.0
        event.topPTweightDown = 1.0
        if event.is_sl and event.genTopLep_pt>0 and event.genTopHad_pt>0:
            event.topPTweight = topPTreweight(event.genTopLep_pt, event.genTopHad_pt)
            event.topPTweightUp = topPTreweightUp(event.genTopLep_pt, event.genTopHad_pt)
            event.topPTweightDown = topPTreweightDown(event.genTopLep_pt, event.genTopHad_pt)
    event.leps_pdgId = [x.pdgId for x in event.leptons]
    event.triggerPath = triggerPath(event)
    event.btag_LR_4b_2b_btagCSV_logit = logit(event.btag_LR_4b_2b_btagCSV)
    any_passes = applyCuts(event, matched_processes)
   
    #workaround for passall=False systematic migrations
    if any_passes and len(event.jets) == 0:
        LOG_MODULE_NAME.info("Event {0}:{1}:{2} has 0 reconstructed jets, likely a weird systematic migration".format(event.run, event.lumi, event.evt))
        return None
  
    if not any_passes:
        return None

    if do_recompute_btag_weights and syst == "nominal" and schema == "mc":
        recompute_btag_weights(event)
   
    #scaleME should be used only for some samples
    if not "scaleME" in sample.tags:
        event.weights[syst_pairs["CMS_ttH_scaleMEDown"]] = 1.0
        event.weights[syst_pairs["CMS_ttH_scaleMEUp"]] = 1.0
    else:
        #weight correction factors introduced here so that the scaleME weight would be normalized
        #to 1 in the inclusive phase space.
        #Extracted from the mean of the weight distribution in (is_sl || is_dl) && (numJets>=4 && nBCSVM>=2)
        event.weights[syst_pairs["CMS_ttH_scaleMEDown"]] = event.weights[syst_pairs["CMS_ttH_scaleMEDown"]]/1.13
        event.weights[syst_pairs["CMS_ttH_scaleMEUp"]] = event.weights[syst_pairs["CMS_ttH_scaleMEUp"]]/0.88

    event.weight_nominal = 1.0
    if schema == "mc" or schema == "mc_syst":
        event.lepton_weight = calc_lepton_SF(event)
        if syst == "nominal":
            event.lepton_weights_syst = {w: calc_lepton_SF(event, w) for w in [
                "CMS_effID_eUp", "CMS_effID_eDown",
                "CMS_effReco_eUp", "CMS_effReco_eDown",
                "CMS_effID_mUp", "CMS_effID_mDown",
                "CMS_effIso_mUp", "CMS_effIso_mDown",
                "CMS_effTracking_mUp", "CMS_effTracking_mDown",
                "CMS_effTrigger_eUp", "CMS_effTrigger_eDown",
                "CMS_effTrigger_mUp", "CMS_effTrigger_mDown",
                "CMS_effTrigger_eeUp", "CMS_effTrigger_eeDown",
                "CMS_effTrigger_emUp", "CMS_effTrigger_emDown",
                "CMS_effTrigger_mmUp", "CMS_effTrigger_mmDown",
            ]}
        event.weight_nominal *= event.weights.at(syst_pairs["CMS_pu"]) * event.weights.at(syst_pairs["CMS_ttH_CSV"]) * event.lepton_weight
   
    ##get MEM from the classifier database
    #ret["common_mem"] = -99
    #if do_classifier_db:
    #    syst_index = int(analysis.config.get(syst, "index"))
    #    db_key = int(event.run), int(event.lumi), int(event.evt), int(syst_index)
    #    if cls_db.data.has_key(db_key):
    #        classifiers = cls_db.get(db_key)
    #        if classifiers.mem_p_sig > 0:
    #            ret["common_mem"] = classifiers.mem_p_sig / (classifiers.mem_p_sig + float(MEM_SF) * classifiers.mem_p_bkg)
    #    else:
    #        ret["common_mem"] = -99
    
    event.common_bdt = 0

    #calculate BDT using the CommonClassifier
    if calculate_bdt:
        if event.is_sl:
            ret_bdt = cls_bdt_sl.GetBDTOutput(
                vec_from_list(CvectorLorentz, [x.lv for x in event.leptons]),
                vec_from_list(CvectorLorentz, [x.lv for x in event.jets]),
                vec_from_list(Cvectordouble, [x.btag for x in event.jets]),
                vec_from_list(CvectorLorentz, [x.lv for x in event.jets + event.loose_jets]),
                vec_from_list(Cvectordouble, [x.btag for x in event.jets + event.loose_jets]),
                l4p(event.met_pt, 0, event.met_phi, 0),
                event.btag_LR_4b_2b_btagCSV
            )
            event.common_bdt = ret_bdt
        elif event.is_dl:
            ret_bdt = cls_bdt_dl.GetBDTOutput(
                vec_from_list(CvectorLorentz, [x.lv for x in event.leptons]),
                vec_from_list(Cvectordouble, [x.charge for x in event.leptons]),
                vec_from_list(CvectorLorentz, [x.lv for x in event.jets]),
                vec_from_list(Cvectordouble, [x.btag for x in event.jets + event.loose_jets]),
                l4p(event.met_pt, 0, event.met_phi, 0),
            )
            event.common_bdt = ret_bdt
    return event

def main(analysis, file_names, sample_name, ofname, skip_events=0, max_events=-1, outfilter=None):
    """Summary
    
    Args:
        analysis (Analysis): The main Analysis object used to configure sparsinator
        file_names (list of string): the PFN of the files to process
        sample_name (string): Name of the current sample
        ofname (string): Name of the file
        skip_events (int, optional): Number of events to skip
        max_events (int, optional): Number of events to process
    
    Returns:
        nothing
    
    Raises:
        Exception: Description
    """

    #need to import here, not in base, because needs special ROOT libraries
    CvectorLorentz = getattr(ROOT, "std::vector<TLorentzVector>")
    Cvectordouble = getattr(ROOT, "std::vector<double>")
    CvectorJetType = getattr(ROOT, "std::vector<MEMClassifier::JetType>")

    # Create pairs of (systematic_name, weight function), which will be used on the
    # nominal event to create reweighted copies of the event. The systematic names
    # here will define the output histograms like
    # ttH/sl/sparse -> nominal event
    # ttH/sl/sparse_CMS_ttH_CSVJESUp -> event with btagWeight with JES up variation
    # ...
    
    systematic_weights = []

    systematics_event = []
    systematics_suffix_list = []

    btag_weights = []

    calculate_bdt = analysis.config.getboolean("sparsinator", "calculate_bdt")
    if calculate_bdt:
        cls_bdt_sl = ROOT.BlrBDTClassifier()
        cls_bdt_dl = ROOT.DLBDTClassifier()
    else:
        cls_bdt_sl = None
        cls_bdt_dl = None

    #Optionally add systematics
    if analysis.config.getboolean("sparsinator", "add_systematics"):

        #Get the list of systematics that modify the event topology
        systematics_event_nosdir = analysis.config.get("systematics", "event").split()
        #map the nice systematics names to a suffix in the ntuple
        for syst_event in systematics_event_nosdir:

            for sdir in ["Up", "Down"]:

                syst_event_sdir = syst_event + sdir
                systematics_event += [syst_event_sdir]
                if analysis.config.has_section(syst_event_sdir):
                    systematics_suffix_list += [(syst_event_sdir, analysis.config.get(syst_event_sdir, "suffix"))]
                else:
                    systematics_suffix_list += [(syst_event_sdir, syst_event_sdir.replace("CMS_scale", "").replace("_j", ""))]

        #systematics with weight
        systematics_weight_nosdir = analysis.config.get("systematics", "weight").split()
        
        ##create b-tagging systematics
        systematics_btag = [s.replace("CMS_ttH_CSV", "") for s in systematics_weight_nosdir if s.startswith("CMS_ttH_CSV")]
        for sdir in ["Up", "Down"]:
           for syst in systematics_btag:
               bweight = "CMS_ttH_CSV{0}{1}".format(syst, sdir)
               systematic_weights += [
                   (bweight, lambda ev, bweight=bweight, syst_pairs=syst_pairs:
                       ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs[bweight]) * ev.lepton_weight)
               ]
               btag_weights += [bweight]

        systematic_weights += [

                ("CMS_ttH_scaleMEUp", lambda ev, syst_pairs=syst_pairs:
                    (ev.weights.at(syst_pairs["CMS_pu"]) *
                    ev.weights.at(syst_pairs["CMS_ttH_CSV"]) *
                    ev.lepton_weight *
                    ev.weights.at(syst_pairs["CMS_ttH_scaleMEUp"]))),
                ("CMS_ttH_scaleMEDown", lambda ev, syst_pairs=syst_pairs:
                    (ev.weights.at(syst_pairs["CMS_pu"]) *
                    ev.weights.at(syst_pairs["CMS_ttH_CSV"]) *
                    ev.lepton_weight *
                    ev.weights.at(syst_pairs["CMS_ttH_scaleMEDown"]))
                ),
                ("CMS_puDown", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_puDown"]) * ev.weights.at(syst_pairs["CMS_ttH_CSV"]) * ev.lepton_weight ),
                ("CMS_puUp", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_puUp"]) * ev.weights.at(syst_pairs["CMS_ttH_CSV"]) * ev.lepton_weight ),
                ("CMS_puDown", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_puDown"]) * ev.weights.at(syst_pairs["CMS_ttH_CSV"]) * ev.lepton_weight ),
                #("CMS_topPTUp", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["CMS_ttH_CSV"]) * ev.lepton_weight ),
                #("CMS_topPTDown", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["CMS_ttH_CSV"]) * ev.lepton_weight ),
                ("unweighted", lambda ev: 1.0),
                ("pu_off", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_ttH_CSV"]) * ev.lepton_weight),
                ("lep_off", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["CMS_ttH_CSV"])),
                ("btag_off", lambda ev, syst_pairs=syst_pairs: ev.weights.at(syst_pairs["CMS_pu"]) * ev.lepton_weight)
        ]

        for lep_syst in ["CMS_effID_eUp", "CMS_effID_eDown",
                "CMS_effReco_eUp", "CMS_effReco_eDown",
                "CMS_effID_mUp", "CMS_effID_mDown",
                "CMS_effIso_mUp", "CMS_effIso_mDown",
                "CMS_effTracking_mUp", "CMS_effTracking_mDown",
                "CMS_effTrigger_eUp", "CMS_effTrigger_eDown",
                "CMS_effTrigger_mUp", "CMS_effTrigger_mDown",
                "CMS_effTrigger_eeUp", "CMS_effTrigger_eeDown",
                "CMS_effTrigger_emUp", "CMS_effTrigger_emDown",
                "CMS_effTrigger_mmUp", "CMS_effTrigger_mmDown",
        ]:
            systematic_weights += [
                (lep_syst, lambda ev, syst_pairs=syst_pairs, lep_syst=lep_syst: ev.weights.at(syst_pairs["CMS_pu"]) * ev.weights.at(syst_pairs["CMS_ttH_CSV"]) * ev.lepton_weights_syst[lep_syst])
            ]

    if len(file_names) == 0:
        raise Exception("No files specified")
    if max_events == 0:
        raise Exception("No events specified")

    sample = analysis.get_sample(sample_name)
    schema = sample.schema
    sample_systematic = False 

    #now we find which processes are matched to have this sample as an input
    #these processes are used to generate histograms
    matched_processes = [p for p in analysis.processes if p.input_name == sample.name]
   
    #Find the processes for which we have up/down variated samples
    systematics_sample = analysis.config.get("systematics", "sample").split()
    matched_procs_new = []
    for syst_sample in systematics_sample:
        procs_up = analysis.process_lists[analysis.config.get(syst_sample, "process_list_up")]
        procs_down = analysis.process_lists[analysis.config.get(syst_sample, "process_list_down")]
        for matched_proc in matched_processes:
            if matched_proc in procs_up:
                matched_proc_new = SystematicProcess(
                    input_name = matched_proc.input_name,
                    output_name = matched_proc.output_name,
                    cuts = matched_proc.cuts,
                    xs_weight = matched_proc.xs_weight,
                    systematic_name = syst_sample + "Up"
                )
                LOG_MODULE_NAME.info("replacing {0} with {1}".format(matched_proc.full_name, matched_proc_new.full_name))       
                matched_procs_new += [matched_proc_new]
            if matched_proc in procs_down:
                matched_proc_new = SystematicProcess(
                    input_name = matched_proc.input_name,
                    output_name = matched_proc.output_name,
                    cuts = matched_proc.cuts,
                    xs_weight = matched_proc.xs_weight,
                    systematic_name = syst_sample + "Down"
                )
                LOG_MODULE_NAME.info("replacing {0} with {1}".format(matched_proc.full_name, matched_proc_new.full_name))       
                matched_procs_new += [matched_proc_new]
  
    if len(matched_procs_new) > 0:
        if len(matched_procs_new) != len(matched_processes):
            raise Exception("Could not match each process to a systematic replacement!")
        matched_processes = matched_procs_new
        sample_systematic = True

    if len(matched_processes) == 0:
        LOG_MODULE_NAME.error("Could not match any processes to sample, will not generate histograms {0}".format(sample.name))
    for proc in matched_processes:
        LOG_MODULE_NAME.info("process: " + str(proc))
    LOG_MODULE_NAME.info("matched processes: {0}".format(len(matched_processes)))

    do_classifier_db = analysis.config.getboolean("sparsinator", "do_classifier_db")
    do_recompute_btag_weights = analysis.config.getboolean("sparsinator", "recompute_btag_weights")
    
    if do_recompute_btag_weights:
        LOG_MODULE_NAME.info("Initializing btag weights")
        initBTagSF()

    if do_classifier_db:
        cls_db = ClassifierDB(filename=sample.classifier_db_path)
    
    #configure systematic scenarios according to MC/Data
    if schema == "mc":
        systematics_event = ["nominal"] + systematics_event
        systematics_weight = [k[0] for k in systematic_weights]
    else:
        systematics_event = ["nominal"]
        systematics_weight = []
    LOG_MODULE_NAME.info("systematics_event: " + str(systematics_event))
    LOG_MODULE_NAME.info("systematics_weight: " + str(systematics_weight))

    all_systematics = systematics_event + systematics_weight
   
    outfile = ROOT.TFile(ofname, "RECREATE")
    outfile.cd()
    
    #pre-create output histograms
    for proc in matched_processes:
        LOG_MODULE_NAME.info("creating outputs for {0}, xsw={1}".format(proc.full_name, proc.xs_weight))
        outdict_syst, outdict_cuts = proc.createOutputs(outfile, analysis, all_systematics, outfilter)
        proc.outdict_syst = outdict_syst
        proc.outdict_cuts = outdict_cuts
    
    nevents = 0

    break_file_loop = False

    tf = None

    #Main loop
    for file_name in file_names:
        if break_file_loop:
            break
        LOG_MODULE_NAME.info("opening {0}".format(file_name))
        tf = ROOT.TFile.Open(file_name)
        treemodel = getattr(ROOT.TTH_MEAnalysis, sample.treemodel.split(".")[-1])
        LOG_MODULE_NAME.debug("treemodel {0}".format(treemodel))

        if schema == "mc" or schema == "mc_syst":
            events = treemodel(
                tf,
                ROOT.TTH_MEAnalysis.SampleDescription(
                    ROOT.TTH_MEAnalysis.SampleDescription.MC
                )
            )
        else:
             events = treemodel(
                tf,
                ROOT.TTH_MEAnalysis.SampleDescription(
                    ROOT.TTH_MEAnalysis.SampleDescription.DATA
                )
            )

        LOG_MODULE_NAME.info("looping over {0} events".format(events.reader.GetEntries(True)))
       
        iEv = 0
        
        #Loop over events
        while events.reader.Next():

            nevents += 1
            iEv += 1
            if skip_events > 0 and nevents < skip_events:
                continue
            if max_events > 0:
                if nevents > (skip_events + max_events):
                    LOG_MODULE_NAME.info("event loop: breaking due to MAX_EVENTS: {0} > {1} + {2}".format(
                        nevents, skip_events, max_events
                    ))
                    break_file_loop = True
                    break

            if nevents % 100 == 0:
                LOG_MODULE_NAME.info("processed {0} events".format(nevents))

            #apply some basic preselection that does not depend on jet systematics
            if not (events.is_sl or events.is_dl):
                continue

            #Loop over systematics that transform the event
            for iSyst, syst in enumerate(systematics_event):
                event = createEvent(
                    events, syst, schema,
                    matched_processes,
                    cls_bdt_sl, cls_bdt_dl,
                    calculate_bdt, do_recompute_btag_weights,
                    sample
                )
                if event is None:
                    continue
                
                #make sure data event is in golden JSON
                if schema == "data" and not event.json:
                    continue
                 
                #SL specific MET cut
                if event.is_sl:
                    if event.met_pt <= 20:
                        continue
                #dilepton specific cuts
                elif event.is_dl:
                    mll = (event.leptons.at(0).lv + event.leptons.at(1).lv).M()
                    #drell-yan
                    if mll < 20:
                        continue
                    #same sign
                    if math.copysign(1, event.leptons.at(0).pdgId * event.leptons.at(1).pdgId) == 1:
                        continue
                    #same flavour
                    if abs(event.leptons.at(0).pdgId) == abs(event.leptons.at(1).pdgId):
                        if event.met_pt <= 40 or abs(mll - 91) < 15:
                            continue

                fillBase(matched_processes, event, syst, schema)
                #Fill the base histogram
               
                #nominal event, fill also histograms with systematic weights
                if syst == "nominal" and schema == "mc" and not sample_systematic:
                    fillSystematic(matched_processes, event, systematic_weights, schema)

            #end of loop over event systematics
        #end of loop over events
        try:
            tf.Close()
        except Exception as e:
            print(e)
    #end of loop over file names

    outdict = {}
    for proc in matched_processes:
        for (syst, hists_syst) in proc.outdict_syst.items():
            outdict = add_hdict(outdict, {k: v.hist for (k, v) in hists_syst.items()})
   
    #put underflow and overflow entries into the first and last visible bin
    for k in sorted(outdict.keys()):
        v = outdict[k]
        print(k, v.GetEntries(), v.Integral())
        #b0 = v.GetBinContent(0)
        #e0 = v.GetBinError(0)
        #nb = v.GetNbinsX()
        #bn = v.GetBinContent(nb + 1)
        #en = v.GetBinError(nb + 1)

        #v.SetBinContent(0, 0)
        #v.SetBinContent(nb+1, 0)
        #v.SetBinError(0, 0)
        #v.SetBinError(nb+1, 0)

        #v.SetBinContent(1, v.GetBinContent(1) + b0)
        #v.SetBinError(1, math.sqrt(v.GetBinError(1)**2 + e0**2))
        #
        #v.SetBinContent(nb, v.GetBinContent(nb) + bn)
        #v.SetBinError(nb, math.sqrt(v.GetBinError(nb)**2 + en**2))
    
    
    LOG_MODULE_NAME.info("writing output")
    save_hdict(hdict=outdict, outfile=outfile, )
    

if __name__ == "__main__":
    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
    logging.basicConfig(level=logging.INFO)
    if os.environ.has_key("FILE_NAMES"):
        file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
        prefix, sample = get_prefix_sample(os.environ["DATASETPATH"])
        skip_events = int(os.environ.get("SKIP_EVENTS", -1))
        max_events = int(os.environ.get("MAX_EVENTS", -1))
        analysis = analysisFromConfig(os.environ.get("ANALYSIS_CONFIG",))

    else:
        #sample = "ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"
        sample = "TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"
        #sample = "TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"
        #sample = "TT_TuneCUETP8M2T4_13TeV-powheg-isrup-pythia8"
        #sample = "TT_TuneCUETP8M2T4_13TeV-powheg-isrdown-pythia8"
        #sample = "SingleMuon"
        #sample = "WW_TuneCUETP8M1_13TeV-pythia8"
        skip_events = 0
        max_events = 10000
        analysis = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/default.cfg")
        file_names = analysis.get_sample(sample).file_names
        #file_names = ["root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/tth/Aug3_syst/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Aug3_syst/170803_183651/0001/tree_1483.root"]

    outfilter = os.environ.get("OUTFILTER", None)
    main(analysis, file_names, sample, "out.root", skip_events, max_events, outfilter)
