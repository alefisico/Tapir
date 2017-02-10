from __future__ import print_function

import ROOT
import math

import sys, os
from collections import OrderedDict
import logging
LOG_MODULE_NAME = logging.getLogger(__name__)
    
import numpy as np
from TTH.MEAnalysis.samples_base import getSitePrefix, samples_nick, get_prefix_sample, PROCESS_MAP, TRIGGERPATH_MAP
from TTH.Plotting.Datacards.sparse import add_hdict, save_hdict

from TTH.CommonClassifier.db import ClassifierDB

CvectorLorentz = getattr(ROOT, "std::vector<TLorentzVector>")
Cvectordouble = getattr(ROOT, "std::vector<double>")
CvectorJetType = getattr(ROOT, "std::vector<MEMClassifier::JetType>")

FUNCTION_TABLE = {
    "jetsByPt_0_pt": lambda ev: ev["jets_p4"][0].Pt(),
    "jetsByPt_0_eta": lambda ev: ev["jets_p4"][0].Eta(),
    "leps_0_pt": lambda ev: ev["leps_pt"][0],
    "btag_LR_4b_2b_btagCSV_logit": lambda ev: logit(ev["btag_LR_4b_2b_btagCSV"]) if ev["btag_LR_4b_2b_btagCSV"]>0.0 else -50,
    "common_mem": lambda ev: ev["common_mem"],
    "common_bdt": lambda ev: ev["common_bdt"],
    "mem_SL_2w2h2t_p": lambda ev: ev["mem_SL_2w2h2t_p"],
    "mem_SL_1w2h2t_p": lambda ev: ev["mem_SL_1w2h2t_p"],
}

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

class BufferedTree:
    """Class with buffered TTree access, so that using tree.branch does not load the entry twice
    
    Attributes:
        branches (dict string->branch): TTree branches
        buf (dict string->data): The buffer, according to branch name
        iEv (int): Current event
        maxEv (int): maximum number of events in the TTree
        tree (TTree): Underlying TTree
    """
    def __init__(self, tree):
        self.tree = tree
        self.tree.SetCacheSize(1*1024*1024)
        self.branches = {}
        for br in self.tree.GetListOfBranches():
            self.branches[br.GetName()] = br
        self.tree.AddBranchToCache("*")
        self.buf = {}
        self.iEv = 0
        self.maxEv = int(self.tree.GetEntries())
        
    def __getattr__(self, attr, defval=None):
        if self.__dict__["branches"].has_key(attr):
            if self.__dict__["buf"].has_key(attr):
                return self.__dict__["buf"][attr]
            else:
                val = getattr(self.__dict__["tree"], attr)
                self.__dict__["buf"][attr] = val
                return val
        else:
            if not defval is None:
                return defval
            raise Exception("Could not find branch with key: {0}".format(attr))
    
    def __iter__(self):
        return self
    
    def next(self):
        if self.iEv > self.maxEv:
            raise StopIteration
        self.buf = {}
        self.iEv += 1
        self.tree.GetEntry(self.iEv)
        return self

    def GetEntries(self):
        return self.tree.GetEntries()
    
    def GetEntry(self, idx):
        self.buf = {}
        self.iEv = idx
        return self.tree.GetEntry(idx)


def assign_process_label(process, event):
    """ In case the you need to decide which process an event falls into based on the event itself.

    Args:
        process (string): the input process
        event (dict string->data): the event data
    """
    if process == "ttbarUnsplit":
        ttCls = event["ttCls"]
        if ttCls == 51:
            _process = "ttbarPlusB"
        elif ttCls == 52:
            _process = "ttbarPlus2B"
        elif ttCls >= 53:
            _process = "ttbarPlusBBbar"
        elif ttCls in [41, 42, 43, 44, 45]:
            _process = "ttbarPlusCCbar"
        else:
            _process = "ttbarOther"
        return _process 
    elif samples_nick.has_key(process):
        return samples_nick[process]
    return process

def logit(x):
    return np.log(x/(1.0 - x))

class Func:
    """Describes a function that gets a value from a branch
    
    Attributes:
        branch (string): Name of the branch
        func (function TTree->value): Getter function
    """
    def __init__(self, branch, **kwargs):
        self.branch = branch
        self.func = kwargs.get("func",
            lambda ev, branch=self.branch: getattr(ev, branch)
        )

    def __call__(self, event):
        return self.func(event)

class Var:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.typ = kwargs.get("type")
        
        self.present = True

        #in case function not defined, just use variable name
        self.nominal_func = kwargs.get("nominal", Func(self.name))
        self.funcs_schema = kwargs.get("funcs_schema", {})

        self.systematics_funcs = kwargs.get("systematics", {})
        self.schema = kwargs.get("schema", ["mc", "data"])

    def fillSystematicsSuffix(self, systematics):
        """Fills the systematic function table with suffix lookup functions
        
        Args:
            systematics (list of string): Systematics to use
        
        Returns:
            nothing
        """
        self.systematics_funcs = {}
        for syst in systematics:
            for sdir in ["Up", "Down"]:
                suffix = syst + sdir
                self.systematics_funcs[suffix] = Func(
                    self.name + "_" + suffix,
                    func=lambda ev, suff=suffix, fallback=self.name: getattr(ev, suff, fallback)
                )

    def getValue(self, event, schema, systematic="nominal"):
                
        if self.present:
            try:
                if systematic == "nominal" or not self.systematics_funcs.has_key(systematic):
                    return self.funcs_schema.get(schema, self.nominal_func)(event)
                else:
                    return self.systematics_funcs[systematic](event)
            except:  
                print (self.name + " " + systematic + " DEACTIVATED")
                self.present = False
                return 0
        else:            
            return 0
                    

class Desc:
    """Event description with varying systematics
    
    Attributes:
        variables_dict (dict of string->Var): Variables in the event
    """

    def __init__(self, systematics, variables=[]):
        """Creates the event description based on a list of variables
        
        Args:
            systematics (list of string): systematics to use for variable lookup
            variables (list, optional): Variables to use
        """

        for v in variables:
            if v.systematics_funcs == "suffix":
                v.fillSystematicsSuffix(systematics)

        self.variables_dict = OrderedDict([(v.name, v) for v in variables])

    def getValue(self, event, schema="mc", systematic="nominal"):
        """Returns a dict with the values of all the variables given a systematic
        
        Args:
            event (TTree): The underlying data TTree
            schema (str, optional): The schema of the data, e.g. "mc", "data"
            systematic (str, optional): The systematic to use
        
        Returns:
            dict of string->data: The values of all the variables
        """
        ret = OrderedDict()
        for vname, v in self.variables_dict.items():
            if schema in v.schema:
                ret[vname] = v.getValue(event, schema, systematic)
        return ret

def lv_p4s(pt, eta, phi, m, btagCSV=-100):
    ret = ROOT.TLorentzVector()
    ret.SetPtEtaPhiM(pt, eta, phi, m)
    setattr(ret, "btagCSV", btagCSV)
    return ret


# Calculate lepton SF on the fly
# Currently only add muons
# TODO: Add electrons as well
def calc_lepton_SF(ev):
    
    weight = 1.

    # Leading muon
    if ev.nleps >= 1:
        if abs(ev.leps_pdgId[0] == 13):
            weight *= ev.leps_SF_IdCutTight[0]
            weight *= ev.leps_SF_IsoTight[0]
        
    # Subleading muon
    if ev.nleps >= 2:
        if abs(ev.leps_pdgId[1] == 13):
            weight *= ev.leps_SF_IdCutTight[1]
            weight *= ev.leps_SF_IsoTight[1]

    return weight

class HistogramOutput:
    def __init__(self, hist, func, cut_name):
        self.hist = hist
        self.func = func
        self.cut_name = cut_name

    def cut(self, event):
        return event[self.cut_name]

    def fill(self, event, weight = 1.0):
        self.hist.Fill(self.func(event), weight)

class CategoryCut:
    def __init__(self, cuts):
        self.cuts = cuts

    def cut(self, event):
        ret = True
        for cut in self.cuts:
            for cname, clow, chigh in cut.sparsinator:
                v = event[cname]
                ret = ret and (v >= clow and v < chigh)
        return ret

def get_schema(sample):
    process = samples_nick[sample]
    if "data" in process:
        schema = "data"
    else:
        schema = "mc"
    return schema

def createOutputs(outdir, analysis, process, systematics):
    """Creates an output dictionary with fillable objects in TDirectories based on categories and systematics. 
    
    Args:
        outdir (TYPE): Description
        analysis (TYPE): Description
        sample (TYPE): Description
        systematics (list of string): list of systematics for which to create outputs
    
    Returns:
        dict of string->output: Dictionary of fillable outputs
    """

    outdict_syst = {}
    outdict_cuts = {}

    ROOT.TH1.AddDirectory(False)

    for syst in systematics:
        outdict_syst[syst] = {} 
        syststr = ""
        if syst != "nominal":
            syststr = "__" + syst
        for k in analysis.groups.keys():
            for cat in analysis.groups[k]:
                if not outdict_cuts.has_key(cat.name):
                    outdict_cuts[(cat, process)] = CategoryCut(
                        cat.cuts + process.cuts
                    )

                name = "{proc}__{cat}__{discr}".format(
                    proc = process.output_name,
                    cat = cat.name,
                    discr = cat.discriminator.name
                ) + syststr
                if not outdict_syst[syst].has_key(name):
                    h = cat.discriminator.get_TH1(name)
                    outdict_syst[syst][name] = HistogramOutput(h, FUNCTION_TABLE[cat.discriminator.func], (cat, process))
    return outdict_syst, outdict_cuts

def pass_HLT_sl_mu(event):
    pass_hlt = event["HLT_ttH_SL_mu"]
    return event["is_sl"] and pass_hlt and int(abs(event["leps_pdgId"][0])) == 13

def pass_HLT_sl_el(event):
    pass_hlt = event["HLT_ttH_SL_el"]
    return event["is_sl"] and pass_hlt and int(abs(event["leps_pdgId"][0])) == 11

def pass_HLT_dl_mumu(event):
    pass_hlt = event["HLT_ttH_DL_mumu"]
    st = sum(map(abs, event["leps_pdgId"]))
    return event["is_dl"] and pass_hlt and st == 26

def pass_HLT_dl_elmu(event):
    pass_hlt = event["HLT_ttH_DL_elmu"]
    st = sum(map(abs, event["leps_pdgId"]))
    return event["is_dl"] and pass_hlt and st == 24

def pass_HLT_dl_elel(event):
    pass_hlt = event["HLT_ttH_DL_elel"]
    st = sum(map(abs, event["leps_pdgId"]))
    return event["is_dl"] and pass_hlt and st == 22

def pass_HLT_fh(event):
    pass_hlt = event["HLT_ttH_FH"]
    return event["is_fh"] and pass_hlt ## FIXME add: st == ??

def triggerPath(event):
    if event["is_sl"] and pass_HLT_sl_mu(event):
        return TRIGGERPATH_MAP["m"]
    elif event["is_sl"] and pass_HLT_sl_el(event):
        return TRIGGERPATH_MAP["e"]
    elif event["is_dl"] and pass_HLT_dl_mumu(event):
        return TRIGGERPATH_MAP["mm"]
    elif event["is_dl"] and pass_HLT_dl_elmu(event):
        return TRIGGERPATH_MAP["em"]
    elif event["is_dl"] and pass_HLT_dl_elel(event):
        return TRIGGERPATH_MAP["ee"]
    elif event["is_fh"] and pass_HLT_fh(event):
        return TRIGGERPATH_MAP["fh"]
    return 0

def main(analysis, file_names, sample_name, ofname, skip_events=0, max_events=-1):
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

    MEM_SF = analysis.config.getfloat("sparsinator", "mem_sf")

    # Create pairs of (systematic_name, weight function), which will be used on the
    # nominal event to create reweighted copies of the event. The systematic names
    # here will define the output histograms like
    # ttH/sl/sparse -> nominal event
    # ttH/sl/sparse_CMS_ttH_CSVJESUp -> event with btagWeight with JES up variation
    # ...
    
    systematic_weights = []
    btag_weights = []

    systematics_event = []

    calculate_bdt = analysis.config.getboolean("sparsinator", "calculate_bdt")
    if calculate_bdt:
        cls_bdt_sl = ROOT.BlrBDTClassifier()
        cls_bdt_dl = ROOT.DLBDTClassifier()

    #Optionally add systematics
    if analysis.config.get("sparsinator", "add_systematics"):

        systematics_event = analysis.config.get("systematics", "event").split()

        #systematics with weight

        ##create b-tagging systematics
        #for sdir in ["up", "down"]:
        #    for syst in ["cferr1", "cferr2", "hf", "hfstats1", "hfstats2", "jes", "lf", "lfstats1", "lfstats2"]:
        #        for tagger in ["CSV", "CMVAV2"]:
        #            bweight = "btagWeight{0}_{1}_{2}".format(tagger, sdir, syst)
        #            #make systematic outputs consistent in Up/Down naming
        #            sdir_cap = sdir.capitalize()
        #            systematic_weights += [
        #                ("CMS_ttH_{0}{1}{2}".format(tagger, syst, sdir_cap), lambda ev, bweight=bweight:
        #                    ev["puWeight"] * ev["triggerEmulationWeight"] * ev["lep_SF_weight"] * ev[bweight])
        #            ]
        #            btag_weights += [bweight]

        #systematic_weights += [
        #        ("puUp", lambda ev: ev["btagWeightCSV"] * ev["triggerEmulationWeight"] * ev["lep_SF_weight"] * ev["puWeightUp"]),
        #        ("puDown", lambda ev: ev["btagWeightCSV"] * ev["triggerEmulationWeight"] * ev["lep_SF_weight"] * ev["puWeightDown"]),
        #        ("unweighted", lambda ev: 1.0)
        #]


    extra_vars =  ["topCandidate_fRec",
                   "topCandidate_pt",
                   "topCandidate_ptcal",
                   "topCandidate_mass",
                   "topCandidate_masscal",
                   "topCandidate_n_subjettiness",
                   "topCandidate_n_subjettiness_groomed",
                
                   "higgsCandidate_secondbtag_subjetfiltered", 
                   "higgsCandidate_bbtag", 
                   "higgsCandidate_tau1", 
                   "higgsCandidate_tau2", 
                   "higgsCandidate_mass", 
                   "higgsCandidate_mass_softdropz2b1filt", 
                   "higgsCandidate_sj12massb_subjetfiltered", 
                   "higgsCandidate_sj12masspt_subjetfiltered", 
                
                   "multiclass_class",
                   "multiclass_proba_ttb",
                   "multiclass_proba_tt2b",
                   "multiclass_proba_ttbb",
                   "multiclass_proba_ttcc",
                   "multiclass_proba_ttll"]

    #create the event description
    desc = Desc(
        systematics_event,
        [
        Var(name="run"),
        Var(name="lumi"),
        Var(name="evt"),

        Var(name="is_sl"),
        Var(name="is_dl"),
        Var(name="is_fh"),

        Var(name="nfatjets"),
        Var(name="fatjets_pt"),
        Var(name="fatjets_eta"),
        Var(name="fatjets_mass"),

        Var(name="leps_pt"),
        Var(name="leps_eta"),

        Var(name="numJets", systematics="suffix"),
        Var(name="nBCSVM", systematics="suffix"),
        Var(name="nBCMVAM", systematics="suffix"),
        
        Var(name="Wmass", systematics="suffix"),

        Var(name="btag_LR_4b_2b_btagCSV",
            nominal=Func("blr_CSV", func=lambda ev: ev.btag_LR_4b_2b_btagCSV),
        ),

        Var(name="btag_LR_4b_2b_btagCSV_logit",
            nominal=Func("blr_CSV_logit", func=lambda ev: logit(ev.btag_LR_4b_2b_btagCSV)),
        ),
        Var(name="btag_LR_4b_2b_btagCMVA_logit",
            nominal=Func("blr_cMVA_logit", func=lambda ev: logit(ev.btag_LR_4b_2b_btagCMVA)),
        ),

        Var(name="leps_pdgId", nominal=Func("leps_pdgId", func=lambda ev: [int(ev.leps_pdgId[i]) for i in range(ev.nleps)])),
        Var(name="leps_charge", nominal=Func("leps_charge", func=lambda ev: [float(math.copysign(1.0, ev.leps_pdgId[i])) for i in range(ev.nleps)])),
        Var(name="leps_p4",
            nominal=Func(
                "leps_p4",
                func=lambda ev: [l4p(ev.leps_pt[i], ev.leps_eta[i], ev.leps_phi[i], ev.leps_mass[i]) for i in range(ev.nleps)]
            )
        ),

        Var(name="jets_p4",
            nominal=Func(
                "jets_p4",
                func=lambda ev: [lv_p4s(ev.jets_pt[i], ev.jets_eta[i], ev.jets_phi[i], ev.jets_mass[i], ev.jets_btagCSV[i]) for i in range(ev.njets)]
            ),
            systematics = {
                "CMS_scale_jUp": Func(
                    "jets_p4_JESUp",
                    func=lambda ev: [lv_p4s(ev.jets_pt[i]*float(ev.jets_corr_JESUp[i])/float(ev.jets_corr[i]), ev.jets_eta[i], ev.jets_phi[i], ev.jets_mass[i], ev.jets_btagCSV[i]) for i in range(ev.njets)]
                ),
                "CMS_scale_jDown": Func(
                    "jets_p4_JESDown",
                    func=lambda ev: [lv_p4s(ev.jets_pt[i]*float(ev.jets_corr_JESDown[i])/float(ev.jets_corr[i]), ev.jets_eta[i], ev.jets_phi[i], ev.jets_mass[i], ev.jets_btagCSV[i]) for i in range(ev.njets)]
                ),
                "CMS_res_jUp": Func(
                    "jets_p4_JERUp",
                    func=lambda ev: [lv_p4s(ev.jets_pt[i]*float(ev.jets_corr_JERUp[i])/float(ev.jets_corr_JER[i]) if ev.jets_corr_JER[i]>0 else 0.0, ev.jets_eta[i], ev.jets_phi[i], ev.jets_mass[i], ev.jets_btagCSV[i]) for i in range(ev.njets)]
                ),
                "CMS_res_jDown": Func(
                    "jets_p4_JERDown",
                    func=lambda ev: [lv_p4s(ev.jets_pt[i]*float(ev.jets_corr_JERDown[i])/float(ev.jets_corr_JER[i]) if ev.jets_corr_JER[i]>0 else 0.0, ev.jets_eta[i], ev.jets_phi[i], ev.jets_mass[i], ev.jets_btagCSV[i]) for i in range(ev.njets)]
                )
            }
        ),

        Var(name="loose_jets_p4",
            nominal=Func(
                "loose_jets_p4",
                func=lambda ev: [lv_p4s(ev.loose_jets_pt[i], ev.loose_jets_eta[i], ev.loose_jets_phi[i], ev.loose_jets_mass[i], ev.loose_jets_btagCSV[i]) for i in range(ev.nloose_jets)]
            ),
            systematics = {
                "CMS_scale_jUp": Func(
                    "loose_jets_p4_JESUp",
                    func=lambda ev: [lv_p4s(ev.loose_jets_pt[i]*float(ev.loose_jets_corr_JESUp[i])/float(ev.loose_jets_corr[i]), ev.loose_jets_eta[i], ev.loose_jets_phi[i], ev.loose_jets_mass[i], ev.loose_jets_btagCSV[i]) for i in range(ev.nloose_jets)]
                ),
                "CMS_scale_jDown": Func(
                    "loose_jets_p4_JESDown",
                    func=lambda ev: [lv_p4s(ev.loose_jets_pt[i]*float(ev.loose_jets_corr_JESDown[i])/float(ev.loose_jets_corr[i]), ev.loose_jets_eta[i], ev.loose_jets_phi[i], ev.loose_jets_mass[i], ev.loose_jets_btagCSV[i]) for i in range(ev.nloose_jets)]
                ),
                "CMS_res_jUp": Func(
                    "loose_jets_p4_JERUp",
                    func=lambda ev: [lv_p4s(ev.loose_jets_pt[i]*float(ev.loose_jets_corr_JERUp[i])/float(ev.loose_jets_corr_JER[i]) if ev.loose_jets_corr_JER[i]>0 else 0.0, ev.loose_jets_eta[i], ev.loose_jets_phi[i], ev.loose_jets_mass[i], ev.loose_jets_btagCSV[i]) for i in range(ev.nloose_jets)]
                ),
                "CMS_res_jDown": Func(
                    "loose_jets_p4_JERDown",
                    func=lambda ev: [lv_p4s(ev.loose_jets_pt[i]*float(ev.loose_jets_corr_JERDown[i])/float(ev.loose_jets_corr_JER[i]) if ev.loose_jets_corr_JER[i]>0 else 0.0, ev.loose_jets_eta[i], ev.loose_jets_phi[i], ev.loose_jets_mass[i], ev.loose_jets_btagCSV[i]) for i in range(ev.nloose_jets)]
                )
            }
        ),

        Var(name="mem_SL_0w2h2t_p",
            nominal=Func("mem_SL_0w2h2t_p", func=lambda ev, sf=MEM_SF: ev.mem_tth_SL_0w2h2t_p/(ev.mem_tth_SL_0w2h2t_p + sf*ev.mem_ttbb_SL_0w2h2t_p) if getattr(ev,"mem_tth_SL_0w2h2t_p",0)>0 else 0.0),
        ),
        Var(name="mem_SL_1w2h2t_p",
            nominal=Func("mem_SL_1w2h2t_p", func=lambda ev, sf=MEM_SF: ev.mem_tth_SL_1w2h2t_p/(ev.mem_tth_SL_1w2h2t_p + sf*ev.mem_ttbb_SL_1w2h2t_p) if getattr(ev,"mem_tth_SL_1w2h2t_p",0)>0 else 0.0),
        ),
        Var(name="mem_SL_2w2h2t_p",
            nominal=Func("mem_SL_2w2h2t_p", func=lambda ev, sf=MEM_SF: ev.mem_tth_SL_2w2h2t_p/(ev.mem_tth_SL_2w2h2t_p + sf*ev.mem_ttbb_SL_2w2h2t_p) if getattr(ev,"mem_tth_SL_2w2h2t_p",0)>0 else 0.0),
        ),
#        Var(name="mem_DL_0w2h2t_p",
#            nominal=Func("mem_p_DL_0w2h2t", func=lambda ev, sf=MEM_SF: ev.mem_tth_DL_0w2h2t_p/(ev.mem_tth_DL_0w2h2t_p + sf*ev.mem_ttbb_DL_0w2h2t_p) if getattr(ev,"mem_tth_DL_0w2h2t_p",0)>0 else 0.0),
#        ),
#        Var(name="mem_FH_4w2h2t_p",
#            nominal=Func("mem_p_FH_4w2h2t", func=lambda ev, sf=MEM_SF: ev.mem_tth_FH_4w2h2t_p/(ev.mem_tth_FH_4w2h2t_p + sf*ev.mem_ttbb_FH_4w2h2t_p) if getattr(ev,"mem_tth_FH_4w2h2t_p",0)>0 else 0.0),
#        ),
#        Var(name="mem_FH_3w2h2t_p",
#            nominal=Func("mem_p_FH_3w2h2t", func=lambda ev, sf=MEM_SF: ev.mem_tth_FH_3w2h2t_p/(ev.mem_tth_FH_3w2h2t_p + sf*ev.mem_ttbb_FH_3w2h2t_p) if getattr(ev,"mem_tth_FH_3w2h2t_p",0)>0 else 0.0),
#        ),
#        Var(name="mem_FH_4w2h1t_p",
#            nominal=Func("mem_p_FH_4w2h1t", func=lambda ev, sf=MEM_SF: ev.mem_tth_FH_4w2h1t_p/(ev.mem_tth_FH_4w2h1t_p + sf*ev.mem_ttbb_FH_4w2h1t_p) if getattr(ev,"mem_tth_FH_4w2h1t_p",0)>0 else 0.0),
#        ),
#        Var(name="mem_FH_0w0w2h2t_p",
#            nominal=Func("mem_p_FH_0w0w2h2t", func=lambda ev, sf=MEM_SF: ev.mem_tth_FH_0w0w2h2t_p/(ev.mem_tth_FH_0w0w2h2t_p + sf*ev.mem_ttbb_FH_0w0w2h2t_p) if getattr(ev,"mem_tth_FH_0w0w2h2t_p",0)>0 else 0.0),
#        ),
#        Var(name="mem_FH_0w0w2h1t_p",
#            nominal=Func("mem_p_FH_0w0w2h1t", func=lambda ev, sf=MEM_SF: ev.mem_tth_FH_0w0w2h1t_p/(ev.mem_tth_FH_0w0w2h1t_p + sf*ev.mem_ttbb_FH_0w0w2h1t_p) if getattr(ev,"mem_tth_FH_0w0w2h1t_p",0)>0 else 0.0),
#        ),

#        Var(name="HLT_ttH_DL_mumu", funcs_schema={"mc": lambda ev: 1.0, "data": lambda ev: ev.HLT_ttH_DL_mumu}),
#        Var(name="HLT_ttH_DL_elel", funcs_schema={"mc": lambda ev: 1.0, "data": lambda ev: ev.HLT_ttH_DL_elel}),
#        Var(name="HLT_ttH_DL_elmu", funcs_schema={"mc": lambda ev: 1.0, "data": lambda ev: ev.HLT_ttH_DL_elmu}),
#        Var(name="HLT_ttH_SL_el", funcs_schema={"mc": lambda ev: 1.0, "data": lambda ev: ev.HLT_ttH_SL_el}),
#        Var(name="HLT_ttH_SL_mu", funcs_schema={"mc": lambda ev: 1.0, "data": lambda ev: ev.HLT_ttH_SL_mu}),
#        Var(name="HLT_ttH_FH", funcs_schema={"mc": lambda ev: 1.0, "data": lambda ev: ev.HLT_ttH_FH}),

#        Var(name="lep_SF_weight", 
#            funcs_schema={"mc": lambda ev: calc_lepton_SF(ev), 
#                          "data": lambda ev: 1.0}),


    #MC-only branches
        Var(name="ttCls", schema=["mc"]),
        Var(name="puWeight", schema=["mc"]),
        Var(name="puWeightUp", schema=["mc"]),
        Var(name="puWeightDown", schema=["mc"]),
        Var(name="triggerEmulationWeight", schema=["mc"]),

        #nominal b-tag weight, systematic weights added later
        Var(name="btagWeightCSV", schema=["mc"]),
        Var(name="btagWeightCMVAV2", schema=["mc"]),
        ]
        #[Var(name=bw, schema=["mc"]) for bw in btag_weights] + [Var(name=br) for br in extra_vars]
    )

    if len(file_names) == 0:
        raise Exception("No files specified, probably a mistake")
    if max_events == 0:
        raise Exception("No events specified, probably a mistake")

    sample = analysis.get_sample(sample_name)
    schema = sample.schema
    process = sample.process

    #now we find which processes are matched to have this sample as an input
    #these processes are used to generate histograms
    matched_processes = [p for p in analysis.processes if p.input_name == sample.name]
    if len(matched_processes) == 0:
        LOG_MODULE_NAME.error("Could not match any processes to sample, will not generate histograms {0}".format(sample.name))

    do_classifier_db = analysis.config.getboolean("sparsinator", "do_classifier_db")
    if do_classifier_db:
        cls_db = ClassifierDB(filename=sample.classifier_db_path)
    
    #configure systematic scenarios according to MC/Data
    if schema == "mc":
        systematics_event = ["nominal"] + systematics_event
        systematics_weight = [k[0] for k in systematic_weights]
    elif schema == "data":
        systematics_event = ["nominal"]
        systematics_weight = []

    all_systematics = systematics_event+systematics_weight
   
    outfile = ROOT.TFile(ofname, "RECREATE")
    outfile.cd()

    outtree = ROOT.TTree("tree", "tree")
    bufs = {}
    bufs["event"] = np.zeros(1, dtype=np.int64)
    bufs["run"] = np.zeros(1, dtype=np.int64)
    bufs["lumi"] = np.zeros(1, dtype=np.int64)
    bufs["systematic"] = np.zeros(1, dtype=np.int64)
    bufs["mem"] = np.zeros(1, dtype=np.float32)
    bufs["bdt"] = np.zeros(1, dtype=np.float32)
    bufs["is_sl"] = np.zeros(1, dtype=np.int32)
    bufs["is_dl"] = np.zeros(1, dtype=np.int32)
    bufs["is_fh"] = np.zeros(1, dtype=np.int32)
    bufs["ttCls"] = np.zeros(1, dtype=np.int32)
    bufs["btag_LR_4b_2b"] = np.zeros(1, dtype=np.float32)
    bufs["numJets"] = np.zeros(1, dtype=np.int32)
    bufs["nBCSVM"] = np.zeros(1, dtype=np.int32)
    
    outtree.Branch("event", bufs["event"], "event/L")
    outtree.Branch("run", bufs["run"], "run/L")
    outtree.Branch("lumi", bufs["lumi"], "lumi/L")
    outtree.Branch("systematic", bufs["systematic"], "systematic/L")
    outtree.Branch("mem", bufs["mem"], "mem/F")
    outtree.Branch("bdt", bufs["bdt"], "bdt/F")
    outtree.Branch("numJets", bufs["numJets"], "numJets/I")
    outtree.Branch("nBCSVM", bufs["nBCSVM"], "nBCSVM/I")
    outtree.Branch("is_sl", bufs["is_sl"], "is_sl/I")
    outtree.Branch("is_dl", bufs["is_dl"], "is_dl/I")
    outtree.Branch("is_fh", bufs["is_fh"], "is_fh/I")
    outtree.Branch("btag_LR_4b_2b", bufs["btag_LR_4b_2b"], "btag_LR_4b_2b/F")
    outtree.Branch("ttCls", bufs["ttCls"], "ttCls/I")
    
    #pre-create output histograms
    for proc in matched_processes:
        outdict_syst, outdict_cuts = createOutputs(outfile, analysis, proc, all_systematics)
        proc.outdict_syst = outdict_syst
        proc.outdict_cuts = outdict_cuts

    nevents = 0

    break_file_loop = False

    #Main loop
    for file_name in file_names:
        if break_file_loop:
            break
        print("opening {0}".format(file_name))
        tf = ROOT.TFile.Open(file_name)
        events = BufferedTree(tf.Get("tree"))
        print("looping over {0} events".format(events.GetEntries()))
       
        iEv = 0

        #Loop over events
        for event in events:
            if nevents < skip_events:
                continue
            if max_events > 0:
                if nevents > (skip_events + max_events):
                    LOG_MODULE_NAME.info("event loop: breaking due to MAX_EVENTS: {0} > {1} + {2}".format(
                        nevents, skip_events, max_events
                    ))
                    break_file_loop = True
                    break

            #apply some basic preselection
            if not (event.is_sl or event.is_dl or event.is_fh):
                continue
            if not event.numJets >= 4:
                continue
            if not (event.nBCSVM>=3 or event.nBCMVAM>=3):
                continue
            if schema == "data" and not event.json:
                continue
            #print(nevents)

            #Found a monster event in ttH (bug?)
            if event.jets_pt[0] > 10000:
                LOG_MODULE_NAME.error("ANOMALOUS MEGAPT EVENT: {0}:{1}:{2}".format(event.run, event.lumi, event.evt))
                continue

            for iSyst, syst in enumerate(systematics_event):
                ret = desc.getValue(event, schema, syst)
                ret["process"] = PROCESS_MAP[assign_process_label(sample.process, ret)]
                ret["syst"] = syst
                ret["counting"] = 0
                ret["leptonFlavour"] = 0
                #ret["triggerPath"] = triggerPath(ret)

                ret["weight_nominal"] = 1.0
                #if schema == "mc":
                #    ret["weight_nominal"] *= ret["puWeight"] * ret["btagWeightCSV"]# * ret["triggerEmulationWeight"] * ret["lep_SF_weight"]
           
                #get MEM
                ret["common_mem"] = -99
                if do_classifier_db:
                    syst_index = int(analysis.config.get(syst, "index"))
                    db_key = int(event.run), int(event.lumi), int(event.evt), int(syst_index)
                    if cls_db.data.has_key(db_key):
                        classifiers = cls_db.get(db_key)
                        if classifiers.mem_p_sig > 0:
                            ret["common_mem"] = classifiers.mem_p_sig / (classifiers.mem_p_sig + float(MEM_SF) * classifiers.mem_p_bkg)
                    else:
                        ret["common_mem"] = -99
                
                ret["common_bdt"] = 0

                #calculate BDT using the CommonClassifier
                if calculate_bdt:
                    if ret["is_sl"]:
                        ret_bdt = cls_bdt_sl.GetBDTOutput(
                            vec_from_list(CvectorLorentz, ret["leps_p4"]),
                            vec_from_list(CvectorLorentz, ret["jets_p4"]),
                            vec_from_list(Cvectordouble, [v.btagCSV for v in ret["jets_p4"]]),
                            vec_from_list(CvectorLorentz, ret["loose_jets_p4"]),
                            vec_from_list(Cvectordouble, [v.btagCSV for v in ret["loose_jets_p4"]]),
                            l4p(event.met_pt, 0, event.met_phi, 0),
                            ret["btag_LR_4b_2b_btagCSV"]
                        )
                        ret["common_bdt"] = ret_bdt
                    elif ret["is_dl"]:
                        ret_bdt = cls_bdt_dl.GetBDTOutput(
                            vec_from_list(CvectorLorentz, ret["leps_p4"]),
                            vec_from_list(Cvectordouble, ret["leps_charge"]),
                            vec_from_list(CvectorLorentz, ret["jets_p4"]),
                            vec_from_list(Cvectordouble, [v.btagCSV for v in ret["jets_p4"]]),
                            l4p(event.met_pt, 0, event.met_phi, 0),
                        )
                        ret["common_bdt"] = ret_bdt
               
                bufs["event"][0] = event.evt
                bufs["run"][0] = event.run
                bufs["lumi"][0] = event.lumi
                bufs["systematic"][0] = iSyst
                bufs["mem"][0] = ret["common_mem"]
                bufs["bdt"][0] = ret["common_bdt"]
                bufs["is_sl"][0] = event.is_sl
                bufs["is_dl"][0] = event.is_dl
                bufs["is_fh"][0] = event.is_fh
                bufs["numJets"][0] = event.numJets
                bufs["nBCSVM"][0] = event.nBCSVM
                bufs["btag_LR_4b_2b"][0] = ret["btag_LR_4b_2b_btagCSV_logit"]

                outtree.Fill()

                #pre-calculate all category cuts
                for proc in matched_processes:
                    for (cat, process), cut in proc.outdict_cuts.items():
                        #print("cut", cat.name, proc.input_name, proc.output_name)
                        ret[(cat, process)] = cut.cut(ret)

                #Fill the base histogram
                for proc in matched_processes:
                    for (k, v) in proc.outdict_syst[syst].items():
                        #weight = ret["weight_nominal"] * proc.xs_weight
                        weight = ret["weight_nominal"]
                        if v.cut(ret):
                            v.fill(ret, weight)
                
                #nominal event, fill also histograms with systematic weights
                if syst == "nominal" and schema == "mc":
                    for (syst_weight, weightfunc) in systematic_weights:
                        weight = weightfunc(ret)
                        for proc in matched_processes:
                            for (k, v) in proc.outdict_syst[syst_weight].items():
                                if v.cut(ret):
                                    v.fill(ret, weight * proc.xs_weight)

            #end of loop over event systematics
            nevents += 1
            iEv += 1
        #end of loop over events
        tf.Close()
    #end of loop over file names

    outdict = {}
    for proc in matched_processes:
        for (syst, hists_syst) in proc.outdict_syst.items():
            outdict = add_hdict(outdict, {k: v.hist for (k, v) in hists_syst.items()})
    save_hdict(hdict=outdict, outfile=outfile, )

    print("processed {0} events".format(nevents))
    print("writing output")

if __name__ == "__main__":
    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

    if os.environ.has_key("FILE_NAMES"):
        file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
        prefix, sample = get_prefix_sample(os.environ["DATASETPATH"])
        skip_events = int(os.environ.get("SKIP_EVENTS", 0))
        max_events = int(os.environ.get("MAX_EVENTS", 0))
        analysis = analysisFromConfig(os.environ.get("ANALYSIS_CONFIG",))

    else:
        file_names = [
            #'root://t3dcachedb03.psi.ch/pnfs/psi.ch/cms/trivcat/store/user/jpata/tth/Feb1_leptonic_nome/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/Feb1_leptonic_nome/170201_171753/0000/tree_100.root'
            'file:///mnt/t3nfs01/data01/shome/jpata/tth/sw/CMSSW/src/TTH/tth_reopt2.root'
        ] 
        prefix = ""
        sample = "ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"
        skip_events = 0
        max_events = 10000
        analysis = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/Plotting/python/Datacards/config_sldl.cfg")
    main(analysis, file_names, sample, "out.root", skip_events, max_events)
