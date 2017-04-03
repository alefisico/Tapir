from __future__ import print_function

import ROOT
import math
import time

import sys, os
from collections import OrderedDict
import logging
LOG_MODULE_NAME = logging.getLogger(__name__)
    
import numpy as np
from TTH.MEAnalysis.samples_base import getSitePrefix, get_prefix_sample, TRIGGERPATH_MAP
from TTH.Plotting.Datacards.sparse import add_hdict, save_hdict

from TTH.Plotting.Datacards.AnalysisSpecificationClasses import SystematicProcess, CategoryCut
from TTH.CommonClassifier.db import ClassifierDB

CvectorLorentz = getattr(ROOT, "std::vector<TLorentzVector>")
Cvectordouble = getattr(ROOT, "std::vector<double>")
CvectorJetType = getattr(ROOT, "std::vector<MEMClassifier::JetType>")

#Generates accessor functions for systematically variated values
def generateSystematicsSuffix(base, sources, func=lambda x, ev: x):
    ret = {}
    for name, src in sources:
        v = "_".join([base, src])
        ret[name] = Func(v, func=lambda ev, v=v, f=func: f(getattr(ev, v), ev))
    return ret

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
        self.tree.SetCacheSize(10*1024*1024)
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
        bytes = self.tree.GetEntry(self.iEv)
        if bytes < 0:
            raise Exception("Could not read entry {0}".format(self.iEv))
        return self

    def GetEntries(self):
        return self.tree.GetEntries()
    
    def GetEntry(self, idx):
        self.buf = {}
        self.iEv = idx
        return self.tree.GetEntry(idx)

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

        #in case function not defined, just use variable name
        self.nominal_func = kwargs.get("nominal", Func(self.name))
        self.funcs_schema = kwargs.get("funcs_schema", {})

        self.systematics_funcs = kwargs.get("systematics", {})
        self.schema = kwargs.get("schema", ["mc", "data"])

        self.present_syst = {}

    def getValue(self, event, schema, systematic="nominal", base_data={}):
    
        #check if this branch was present with this systematic
        if self.present_syst.get(systematic, True):
            if systematic == "nominal":
                return self.funcs_schema.get(schema, self.nominal_func)(event)
            elif self.systematics_funcs.has_key(systematic):
                return self.systematics_funcs[systematic](event)
            else:
                if base_data.has_key(self.name):
                    return base_data[self.name]
                else:
                    return self.funcs_schema.get(schema, self.nominal_func)(event) 

class EventDescription:
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
        self.variables_dict = OrderedDict([(v.name, v) for v in variables])

    def getValue(self, event, schema="mc", systematic="nominal", base_data={}):
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
                ret[vname] = v.getValue(event, schema, systematic, base_data)
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

def fillBase(matched_processes, ret, syst, schema):
    for proc in matched_processes:
        for (k, histo_out) in proc.outdict_syst.get(syst, {}).items():
            weight = 1.0 
            if schema == "mc":
                weight = ret["weight_nominal"] * proc.xs_weight
            if histo_out.cut(ret):
                histo_out.fill(ret, weight)


def fillSystematic(matched_processes, ret, systematic_weights, schema):
    for (syst_weight, weightfunc) in systematic_weights:
        for proc in matched_processes:
            for (k, histo_out) in proc.outdict_syst[syst_weight].items():
                weight = weightfunc(ret) * proc.xs_weight
                if histo_out.cut(ret):
                    histo_out.fill(ret, weight)

def applyCuts(ret, matched_processes):
    #check if this event falls into any category
    any_passes = False
    for proc in matched_processes:
        check_proc = CategoryCut(proc.cuts).cut(ret)
        if not check_proc:
            continue
        for cut_name, cut in proc.outdict_cuts.items():
            cut_result = cut.cut(ret)
            any_passes = any_passes or cut_result
            ret[cut_name] = cut_result
    return any_passes

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
        ##create b-tagging systematics
        for sdir in ["up", "down"]:
           for syst in ["cferr1", "cferr2", "hf", "hfstats1", "hfstats2", "jes", "lf", "lfstats1", "lfstats2"]:
               for tagger in ["CSV", "CMVAV2"]:
                   bweight = "btagWeight{0}_{1}_{2}".format(tagger, sdir, syst)
                   #make systematic outputs consistent in Up/Down naming
                   sdir_cap = sdir.capitalize()
                   systematic_weights += [
                       ("CMS_ttH_{0}{1}{2}".format(tagger, syst, sdir_cap), lambda ev, bweight=bweight:
                           ev["puWeight"] * ev[bweight])
                   ]
                   btag_weights += [bweight]

        systematic_weights += [
                ("CMS_puUp", lambda ev: ev["puWeightUp"] * ev["btagWeightCSV"] ),
                ("CMS_puDown", lambda ev: ev["puWeightDown"] * ev["btagWeightCSV"]),
                ("unweighted", lambda ev: 1.0)
        ]

    
    #create the event description

    desc_cut = EventDescription(
        systematics_event,
        [
        Var(name="is_sl"),
        Var(name="is_dl"),
        Var(name="is_fh"),
        
        Var(name="leps_pdgId", nominal=Func("leps_pdgId", func=lambda ev: [int(ev.leps_pdgId[i]) for i in range(ev.nleps)])),

        Var(name="numJets", systematics = generateSystematicsSuffix("numJets", systematics_suffix_list)),
        Var(name="nBCSVM", systematics = generateSystematicsSuffix("nBCSVM", systematics_suffix_list)),
        Var(name="HLT_ttH_DL_mumu", funcs_schema={
            "mc": lambda ev: ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v or ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v or ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v or ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v,
            "data": lambda ev: ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v or ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v or ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v or ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v
        }),
        Var(name="HLT_ttH_DL_elel", funcs_schema={
            "mc": lambda ev: ev.HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v,
            "data": lambda ev: ev.HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v
        }),
        Var(name="HLT_ttH_DL_elmu", funcs_schema={
            "mc": lambda ev: ev.HLT_BIT_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v or ev.HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v or ev.HLT_BIT_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v or ev.HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v,
            "data": lambda ev: ev.HLT_BIT_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v or ev.HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v or ev.HLT_BIT_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v or ev.HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v
        }),
        Var(name="HLT_ttH_SL_el", funcs_schema={
            "mc": lambda ev: ev.HLT_BIT_HLT_Ele27_WPTight_Gsf_v,
            "data": lambda ev: ev.HLT_BIT_HLT_Ele27_WPTight_Gsf_v
        }),
        Var(name="HLT_ttH_SL_mu", funcs_schema={
            "mc": lambda ev: ev.HLT_BIT_HLT_IsoMu24_v or ev.HLT_BIT_HLT_IsoTkMu24_v,
            "data": lambda ev: ev.HLT_BIT_HLT_IsoMu24_v or ev.HLT_BIT_HLT_IsoTkMu24_v
        }),
        Var(name="ttCls", schema=["mc"]),
        ]
    )
    desc = EventDescription(
        systematics_event,
        [
        Var(name="run"),
        Var(name="lumi"),
        Var(name="evt"),

        Var(name="leps_pt"),
        Var(name="leps_eta"),

        Var(name="Wmass", systematics = generateSystematicsSuffix("Wmass", systematics_suffix_list)),
            
        Var(name="btag_LR_4b_2b_btagCSV", systematics = generateSystematicsSuffix("btag_LR_4b_2b_btagCSV", systematics_suffix_list)),

        Var(name="btag_LR_4b_2b_btagCSV_logit",
            nominal=Func("btag_LR_4b_2b_btagCSV",
            func=lambda ev: logit(ev.btag_LR_4b_2b_btagCSV)),
            systematics = generateSystematicsSuffix("btag_LR_4b_2b_btagCSV", systematics_suffix_list, func=lambda x, ev: logit(x))
        ),

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
            systematics = generateSystematicsSuffix(
                "jets_corr",
                systematics_suffix_list,
                func=lambda x, ev: [
                    lv_p4s(
                        ev.jets_pt[i]*float(x[i])/float(ev.jets_corr[i]),
                        ev.jets_eta[i],
                        ev.jets_phi[i],
                        ev.jets_mass[i],
                        ev.jets_btagCSV[i]
                    ) for i in range(ev.njets)
                ])
        ),

        Var(name="loose_jets_p4",
            nominal=Func(
                "loose_jets_p4",
                func=lambda ev: [lv_p4s(ev.loose_jets_pt[i], ev.loose_jets_eta[i], ev.loose_jets_phi[i], ev.loose_jets_mass[i], ev.loose_jets_btagCSV[i]) for i in range(ev.nloose_jets)]
            ),
            systematics = generateSystematicsSuffix("loose_jets_corr", systematics_suffix_list, func=lambda x, ev: [lv_p4s(ev.loose_jets_pt[i]*float(x[i])/float(ev.loose_jets_corr[i]), ev.loose_jets_eta[i], ev.loose_jets_phi[i], ev.loose_jets_mass[i], ev.loose_jets_btagCSV[i]) for i in range(ev.nloose_jets)])
        ),

        Var(name="mem_DL_0w2h2t_p",
            nominal=Func("mem_DL_0w2h2t_p", func=lambda ev: ev.mem_DL_0w2h2t_p),
            systematics = generateSystematicsSuffix("mem_DL_0w2h2t_p", systematics_suffix_list)
        ),
        Var(name="mem_SL_0w2h2t_p",
            nominal=Func("mem_SL_0w2h2t_p", func=lambda ev: ev.mem_SL_0w2h2t_p),
            systematics = generateSystematicsSuffix("mem_SL_0w2h2t_p", systematics_suffix_list)

        ),
        Var(name="mem_SL_1w2h2t_p",
            nominal=Func("mem_SL_1w2h2t_p", func=lambda ev: ev.mem_SL_1w2h2t_p),
            systematics = generateSystematicsSuffix("mem_SL_1w2h2t_p", systematics_suffix_list)
        ),
        Var(name="mem_SL_2w2h2t_p",
            nominal=Func("mem_SL_2w2h2t_p", func=lambda ev: ev.mem_SL_2w2h2t_p),
            systematics = generateSystematicsSuffix("mem_SL_2w2h2t_p", systematics_suffix_list)
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

#        Var(name="lep_SF_weight", 
#            funcs_schema={"mc": lambda ev: calc_lepton_SF(ev), 
#                          "data": lambda ev: 1.0}),


    #MC-only branches
        Var(name="puWeight", schema=["mc"]),
        Var(name="puWeightUp", schema=["mc"]),
        Var(name="puWeightDown", schema=["mc"]),

        #nominal b-tag weight, systematic weights added later
        Var(name="btagWeightCSV", schema=["mc"]),
        Var(name="btagWeightCMVAV2", schema=["mc"]),
        ] + [Var(name=n, schema=["mc"]) for n in btag_weights]
    )

    if len(file_names) == 0:
        raise Exception("No files specified")
    if max_events == 0:
        raise Exception("No events specified")

    sample = analysis.get_sample(sample_name)
    schema = sample.schema
    sample_systematic = False 
    #process = sample.process

    #now we find which processes are matched to have this sample as an input
    #these processes are used to generate histograms
    matched_processes = [p for p in analysis.processes if p.input_name == sample.name]
    
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
                matched_procs_new += [matched_proc_new]
            if matched_proc in procs_down:
                matched_proc_new = SystematicProcess(
                    input_name = matched_proc.input_name,
                    output_name = matched_proc.output_name,
                    cuts = matched_proc.cuts,
                    xs_weight = matched_proc.xs_weight,
                    systematic_name = syst_sample + "Down"
                )
                matched_procs_new += [matched_proc_new]
  
    if len(matched_procs_new) > 0:
        if len(matched_procs_new) != len(matched_processes):
            raise Exception("Could not match each process to a systematic replacement!")
        matched_processes = matched_procs_new
        sample_systematic = True

    if len(matched_processes) == 0:
        LOG_MODULE_NAME.error("Could not match any processes to sample, will not generate histograms {0}".format(sample.name))
    for proc in matched_processes:
        print(proc.input_name, proc.output_name, ",".join([c.name for c in proc.cuts]), proc.xs_weight)
    LOG_MODULE_NAME.info("matched processes: {0}".format(len(matched_processes)))

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
    LOG_MODULE_NAME.info("systematics_event: " + str(systematics_event))
    LOG_MODULE_NAME.info("systematics_weight: " + str(systematics_weight))

    all_systematics = systematics_event + systematics_weight
   
    outfile = ROOT.TFile(ofname, "RECREATE")
    outfile.cd()
    
    #pre-create output histograms
    for proc in matched_processes:
        outdict_syst, outdict_cuts = proc.createOutputs(outfile, analysis, all_systematics)
        proc.outdict_syst = outdict_syst
        proc.outdict_cuts = outdict_cuts

    nevents = 0

    break_file_loop = False

    tf = None

    #Main loop
    for file_name in file_names:
        if break_file_loop:
            if tf:
                tf.Close()
            break
        LOG_MODULE_NAME.info("opening {0}".format(file_name))
        try:
            tf = ROOT.TFile.Open(file_name)
            if not tf or tf.IsZombie():
                raise Exception("Could not open file")
        except Exception as e:
            LOG_MODULE_NAME.error("error opening file {0} {1}".format(file_name, e))
            continue
        events = BufferedTree(tf.Get("tree"))
        LOG_MODULE_NAME.info("looping over {0} events".format(events.GetEntries()))
       
        iEv = 0

        #Loop over events
        for event in events:

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

            if nevents % 1000 == 0:
                LOG_MODULE_NAME.info("processed {0} events".format(nevents))

            #apply some basic preselection
            if not (event.is_sl or event.is_dl):
                continue
            if schema == "data" and not event.json:
                continue

            ##Found a monster event in ttH (bug?)
            #if event.jets_pt[0] > 10000:
            #    LOG_MODULE_NAME.error("ANOMALOUS MEGAPT EVENT: {0}:{1}:{2}".format(event.run, event.lumi, event.evt))
            #    continue

            #Loop over systematics that transform the event
            ret_nominal = {}
            for iSyst, syst in enumerate(systematics_event):
                ret = desc_cut.getValue(event, schema, syst, ret_nominal)

                ret["syst"] = syst
                ret["counting"] = 0
                ret["leptonFlavour"] = 0
                ret["triggerPath"] = triggerPath(ret)

                any_passes = applyCuts(ret, matched_processes)
                if not any_passes:
                    continue
               
                #now load the full event
                ret.update(desc.getValue(event, schema, syst, ret_nominal))
                
                ret["weight_nominal"] = 1.0
                if schema == "mc":
                    ret["weight_nominal"] *= ret["puWeight"] * ret["btagWeightCSV"]# * ret["triggerEmulationWeight"] * ret["lep_SF_weight"]
               
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


                fillBase(matched_processes, ret, syst, schema)
                #Fill the base histogram
               
                #nominal event, fill also histograms with systematic weights
                if syst == "nominal" and schema == "mc" and not sample_systematic:
                    fillSystematic(matched_processes, ret, systematic_weights, schema)

            #end of loop over event systematics
        #end of loop over events
        tf.Close()
    #end of loop over file names

    outdict = {}
    for proc in matched_processes:
        for (syst, hists_syst) in proc.outdict_syst.items():
            outdict = add_hdict(outdict, {k: v.hist for (k, v) in hists_syst.items()})
   
    #put underflow and overflow entries into the first and last visible bin
    for k in sorted(outdict.keys()):
        v = outdict[k]
        b0 = v.GetBinContent(0)
        e0 = v.GetBinError(0)
        nb = v.GetNbinsX()
        bn = v.GetBinContent(nb + 1)
        en = v.GetBinError(nb + 1)

        v.SetBinContent(0, 0)
        v.SetBinContent(nb+1, 0)
        v.SetBinError(0, 0)
        v.SetBinError(nb+1, 0)

        v.SetBinContent(1, v.GetBinContent(1) + b0)
        v.SetBinError(1, math.sqrt(v.GetBinError(1)**2 + e0**2))
        
        v.SetBinContent(nb, v.GetBinContent(nb) + bn)
        v.SetBinError(nb, math.sqrt(v.GetBinError(nb)**2 + en**2))
        print(k, v.Integral(), v.GetEntries())
    
    
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
        sample = "ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"
        skip_events = 0
        max_events = 1000
        analysis = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/data/default.cfg")
        file_names = analysis.get_sample(sample).file_names

    main(analysis, file_names, sample, "out.root", skip_events, max_events)
