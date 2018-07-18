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


########################################
# Define Input Files and
# output directory
########################################


# for the filename: basepath + filename + .root
full_file_names = {}
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v



#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/Jul04_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/Jul04_withME/180704_113841/0000/tree_45.root"
#full_file_names["TT"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_45.root"

########################################
# Create histograms, saved in file
########################################

pos = ["resolved","boosted","boostedperm","bothres","bothboo","bothbooperm"]
cats = ["top","higgs","both","all","None"]
anc = ["SL_2w2h2t","SL_1w2h2t","SL_0w2h2t","DL_0w2h2t","SL_2w2h2t_sj","SL_1w2h2t_sj","SL_0w2h2t_sj","DL_0w2h2t_sj"]
perm = ["SL_2w2h2t_sj_perm_top","SL_2w2h2t_sj_perm_higgs","SL_2w2h2t_sj_perm_tophiggs","SL_1w2h2t_sj_perm_higgs","SL_0w2h2t_sj_perm_higgs","DL_0w2h2t_sj_perm_higgs"]
resolved = anc[:4]
boosted = anc[4:]


MEM = {}

for cat in cats:
    MEM[cat] = {}
    for i in pos:
        MEM[cat][i] = ROOT.TH1F("MEM_{}_{}".format(cat,i),"MEM_{}_{}".format(cat,i),50,0,1)
        MEM[cat][i].Sumw2()


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


 
        #Let's only consider SL events for top tagging
        cat = None
        if event.is_sl:
            cat = "sl"
        elif event.is_dl:
            cat = "dl"
        else:
            continue

        typ = "None"
        matchtop = -1
        matchhiggs = -1


    


        if event.boosted == 1:
            if event.nhiggsCandidate > 0 and event.ntopCandidate > 0:
                if event.ngenHiggs > 0 and event.ngenTopHad > 0:
                    if Get_DeltaR_two_objects_coord(event.topCandidate_eta[0],event.topCandidate_phi[0],event.genTopHad_eta[0],event.genTopHad_phi[0]) < 0.6:
                        if Get_DeltaR_two_objects_coord(event.higgsCandidate_eta[0],event.higgsCandidate_phi[0],event.genHiggs_eta[0],event.genHiggs_phi[0]) < 0.6:
                            typ = "both"
            elif event.nhiggsCandidate > 0 and event.ntopCandidate == 0:
                if event.ngenHiggs > 0:
                    if Get_DeltaR_two_objects_coord(event.higgsCandidate_eta[0],event.higgsCandidate_phi[0],event.genHiggs_eta[0],event.genHiggs_phi[0]) < 0.6:
                        typ = "higgs"
            elif event.nhiggsCandidate == 0 and event.ntopCandidate > 0:
                if event.ngenTopHad > 0:
                    if Get_DeltaR_two_objects_coord(event.topCandidate_eta[0],event.topCandidate_phi[0],event.genTopHad_eta[0],event.genTopHad_phi[0]) < 0.6:
                        typ = "top"
            if event.nhiggsCandidate > 0 and event.nMatch_b_higgs == 2:
                matchhiggs = 1
            if event.ntopCandidate > 0 and event.nMatch_b_htt == 1 and event.nMatch_q_htt == 2:
                matchtop = 1

        event.mem_resolved = 0
        event.mem_boosted = 0
        event.mem_boostedperm = 0
        event.cat_resolved = None
        event.cat_boosted = None
        event.cat_boostedperm = None
        for m in resolved:
        	if getattr(event,"mem_{}_p".format(m)) > 0:
        		event.mem_resolved = getattr(event,"mem_{}_p".format(m))
       			event.cat_resolved = m
       	for m in boosted:
        	if getattr(event,"mem_{}_p".format(m)) > 0:
        		event.mem_boosted = getattr(event,"mem_{}_p".format(m))
       			event.cat_boosted = m
        for m in perm:
            if getattr(event,"mem_{}_p".format(m)) > 0:
                event.mem_boostedperm = getattr(event,"mem_{}_p".format(m))
                event.cat_boostedperm = m


        if event.cat_resolved is not None and event.cat_boosted is not None:
            MEM["all"]["bothres"].Fill(event.mem_resolved)
            MEM[typ]["bothres"].Fill(event.mem_resolved)
            MEM["all"]["bothboo"].Fill(event.mem_boosted)
            MEM[typ]["bothbooperm"].Fill(event.mem_boostedperm)
            MEM["all"]["bothbooperm"].Fill(event.mem_boostedperm)
            MEM[typ]["bothboo"].Fill(event.mem_boosted)
        elif event.cat_resolved is None and event.cat_boosted is not None:
            MEM["all"]["boosted"].Fill(event.mem_boosted)
            MEM[typ]["boosted"].Fill(event.mem_boosted)
            MEM["all"]["boostedperm"].Fill(event.mem_boostedperm)
            MEM[typ]["boostedperm"].Fill(event.mem_boostedperm)
        elif event.cat_resolved is not None and event.cat_boosted is None:
            MEM["all"]["resolved"].Fill(event.mem_resolved)


 
results = ROOT.TFile("out.root","recreate")

for cat in cats:
    for i in pos:
        MEM[cat][i].Write()
