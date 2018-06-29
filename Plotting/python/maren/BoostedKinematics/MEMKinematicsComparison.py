#!/usr/bin/env python

########################################
# Imports
########################################

import math
import os
import pickle
import socket # to get the hostname

import ROOT

from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf
import TTH.MEAnalysis.nanoTreeClasses as nanoTreeClasses
import TTH.MEAnalysis.nanoTreeGenClasses as nanoTreeGenClasses

from TTH.Plotting.maren.BDTStudies.BasicBoostedFunctions import *
from TTH.MEAnalysis.vhbb_utils import lvec, autolog

#Define cuts for taggers
class Conf:
    boost = {
        "top": {
            #Cuts set by "default"
            "pt":   200,
            "eta":  2.4,
            "drl": 1.0, #In SL events distance to lepton candidate
            "btagL": "DeepCSVL",
            #Cuts optained by optimization procedure
            "mass_inf": 160,
            "mass_sup": 280,
            "tau32SD": 0.8,
            "frec": 0.3,
        },
        "higgs": {
            #Cuts set by "default"
            "pt":   200,
            "eta":  2.4,
            "msoft": 50,
            #Cuts optained by optimization procedure
            "bbtag": 0.4,
            "btagSL": 0.7,
            "tau21SD": 0.7,
        },
    }

class JetCollection:
    def __init__(self, tree, n,name):
        self.pt = getattr(tree,"{}_pt".format(name))[n]
        self.eta = getattr(tree,"{}_eta".format(name))[n]
        self.phi = getattr(tree,"{}_phi".format(name))[n]
        self.mass = getattr(tree,"{}_mass".format(name))[n]
        pass
    @staticmethod
    def make_array(input,name):
        if "boosted" in name:
            return [JetCollection(input, i, name) for i in range(int(getattr(input,"n_{}".format(name))))]
        else:
            return [JetCollection(input, i, name) for i in range(getattr(input,"n{}".format(name)))]


class SubjetCollection:
    def __init__(self, tree, n,name):
        self.pt = getattr(tree,"{}pt".format(name))[n]
        self.eta = getattr(tree,"{}eta".format(name))[n]
        self.phi = getattr(tree,"{}phi".format(name))[n]
        self.mass = getattr(tree,"{}mass".format(name))[n]
        pass
    @staticmethod
    def make_array(input,name):
        if "top" in name:
            return [SubjetCollection(input, i, name) for i in range(int(getattr(input,"ntopCandidate")))]
        elif "higgs" in name:
            return [SubjetCollection(input, i, name) for i in range(int(getattr(input,"nhiggsCandidate")))]

########################################
# Define Input Files and
# output directory
########################################


# for the filename: basepath + filename + .root
full_file_names = {}
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v



#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_290.root"
#full_file_names["TT"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_45.root"

########################################
# Create histograms, saved in file
########################################

cats = ["both"]
anc = ["resolved","boosted"]
scenarios = ["all","allmatched","allmatchandkin"]
resolved = anc[:1]
boosted = anc[1:]


MEM = {}


for i in anc:
    MEM[i] = {}
    for j in scenarios:
        MEM[i][j] = ROOT.TH1F("MEM_{}_{}".format(i,j),"MEM_{}_{}".format(i,j),50,0,1)
        MEM[i][j].Sumw2()


######################################
# Run code
########################################

for l in full_file_names:
    f = ROOT.TFile.Open(full_file_names[l], "READ")
    ttree = f.Get("tree")

    print full_file_names[l]

    sample = ""
    if "ttH" in full_file_names[l]:
        sample = "ttH"
    elif "TT" in full_file_names[l]:
        sample = "ttjets"


    counter  = 0 

    for event in ttree :
        counter += 1

        #if counter > 10000:
        #    break

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.evt

        event.GenBQuarkFromHiggs = JetCollection.make_array(ttree,"GenBFromHiggs")
        event.GenWZQuark = JetCollection.make_array(ttree,"GenQFromW")
        event.GenBQuarkFromTop = JetCollection.make_array(ttree,"GenBFromTop")
        #event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
        #event.GenTop = nanoTreeGenClasses.GenTop.make_array(event.GenParticle)
        #event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)
        #event.boosted_ljets = JetCollection.make_array(ttree,"boosted_ljets")
        #event.boosted_bjets = JetCollection.make_array(ttree,"boosted_bjets")
        event.Jet = JetCollection.make_array(ttree,"jets")

        QuarksToMatch = event.GenBQuarkFromHiggs + event.GenBQuarkFromTop + event.GenWZQuark


 
        #Let's only consider SL events for top tagging
        cat = None
        if event.is_sl:
            cat = "sl"
        else:
            continue


        #Look at resolved case first.
        if event.numJets >= 6 and event.nBDeepCSVM == 4 and event.is_sl:
            if getattr(event,"mem_SL_2w2h2t_p") > 0:
                MEM["resolved"]["all"].Fill(getattr(event,"mem_SL_2w2h2t_p"),event.genWeight)
                if event.nMatch_hb == 2 and event.nMatch_wq == 2 and event.nMatch_tb== 2:
                    MEM["resolved"]["allmatched"].Fill(getattr(event,"mem_SL_2w2h2t_p"),event.genWeight)
                    matched_resolved = Match_two_lists(
                    event.Jet, 'Jet',
                    QuarksToMatch, 'Quark',0.3)
                    nkinmatch = 0
                    for i in event.Jet:
                        if hasattr(i, "matched_Quark") and abs(i.pt-i.matched_Quark.pt) < 20:
                            nkinmatch += 1
                    if nkinmatch >= 6:
                        MEM["resolved"]["allmatchandkin"].Fill(getattr(event,"mem_SL_2w2h2t_p"),event.genWeight)



        #And here comes the boosted stuff

        typ = "None"
        matchtop = -1
        matchhiggs = -1
    


        if event.boosted == 1:
            if event.nhiggsCandidate > 0 and event.ntopCandidate > 0:
                typ = "both"
            elif event.nhiggsCandidate > 0 and event.ntopCandidate == 0:
                typ = "higgs"
            elif event.nhiggsCandidate == 0 and event.ntopCandidate > 0:
                typ = "top"


        if event.boosted == 0:
            continue
        if event.nhiggsCandidate == 0:
            continue
        if event.ntopCandidate == 0:
            continue
        if event.topCandidate_subjetIDPassed[0] < 0.5:
            continue
        if event.n_boosted_ljets > 2:
            continue
        if typ is not "both":
            continue

        event.T1 = SubjetCollection.make_array(ttree,"topCandidate_sj1")
        event.T2 = SubjetCollection.make_array(ttree,"topCandidate_sj2")
        event.T3 = SubjetCollection.make_array(ttree,"topCandidate_sj3")

        event.H1 = SubjetCollection.make_array(ttree,"higgsCandidate_sj1")
        event.H2 = SubjetCollection.make_array(ttree,"higgsCandidate_sj2")

        if event.nhiggsCandidate > 0 and event.nMatch_b_higgs == 2:
            matchhiggs = 1
        if event.ntopCandidate > 0 and event.nMatch_b_htt == 1 and event.nMatch_q_htt == 2:
            matchtop = 1

        JetsToMatch = event.T1 + event.T2 + event.T3 + event.H1 + event.H2
        matched_boosted = Match_two_lists(
            JetsToMatch, 'Subjet',
            QuarksToMatch, 'Quark',0.3)
        nkinmatchb = 0
        for i in JetsToMatch:
            if hasattr(i, "matched_Quark") and abs(i.pt-i.matched_Quark.pt) < 20:
                nkinmatchb += 1


        if getattr(event,"mem_SL_2w2h2t_sj_p") > 0:
            MEM["boosted"]["all"].Fill(getattr(event,"mem_SL_2w2h2t_sj_p"),event.genWeight)
            if matched_boosted >= 5:
                MEM["boosted"]["allmatched"].Fill(getattr(event,"mem_SL_2w2h2t_sj_p"),event.genWeight)
                if nkinmatchb >= 5:
                    MEM["boosted"]["allmatchandkin"].Fill(getattr(event,"mem_SL_2w2h2t_sj_p"),event.genWeight)



results = ROOT.TFile("out.root","recreate")

for i in anc:
    for j in scenarios:
        MEM[i][j].Write()