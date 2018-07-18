#!/usr/bin/env python

########################################
# Imports
########################################

import math
import os
import pickle
import socket # to get the hostname

import ROOT

import TTH.MEAnalysis.nanoTreeClasses as nanoTreeClasses
import TTH.MEAnalysis.nanoTreeGenClasses as nanoTreeGenClasses


from TTH.Plotting.maren.BDTStudies.BasicBoostedFunctions import *
from TTH.MEAnalysis.vhbb_utils import lvec, autolog


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

cats = ["res","boo","both"]
anc = ["SL_2w2h2t","SL_1w2h2t","SL_0w2h2t","DL_0w2h2t","SL_2w2h2t_sj","SL_1w2h2t_sj","SL_0w2h2t_sj","DL_0w2h2t_sj"]
perm = ["SL_2w2h2t_sj_perm_top","SL_2w2h2t_sj_perm_higgs","SL_2w2h2t_sj_perm_tophiggs","SL_1w2h2t_sj_perm_higgs","SL_0w2h2t_sj_perm_higgs","DL_0w2h2t_sj_perm_higgs"]
resolved = anc[:4]
boosted = anc[4:]
pos = ["top","higgs"]


MEM = {}
MEM2 = {}

for cat in cats:
    MEM[cat] = {}
    MEM2[cat] = {}
    for i in pos:
        MEM[cat][i] = ROOT.TH1F("pt_{}_{}".format(cat,i),"pt_{}_{}".format(cat,i),50,0,600)
        MEM[cat][i].Sumw2()
        MEM2[cat][i] = ROOT.TH1F("pt2_{}_{}".format(cat,i),"pt2_{}_{}".format(cat,i),50,0,600)
        MEM2[cat][i].Sumw2()


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
                typ = "both"
            elif event.nhiggsCandidate > 0 and event.ntopCandidate == 0:
                typ = "higgs"
            elif event.nhiggsCandidate == 0 and event.ntopCandidate > 0:
                typ = "top"
            if event.nhiggsCandidate > 0 and event.nMatch_b_higgs == 2:
                matchhiggs = 1
            if event.ntopCandidate > 0 and event.nMatch_b_htt == 1 and event.nMatch_q_htt == 2:
                matchtop = 1

        event.mem_resolved = 0
        event.mem_boosted = 0
        event.cat_resolved = None
        event.cat_boosted = None
        for m in resolved:
            if getattr(event,"mem_{}_p".format(m)) > 0:
                event.mem_resolved = getattr(event,"mem_{}_p".format(m))
                event.cat_resolved = m
        for m in boosted:
            if getattr(event,"mem_{}_p".format(m)) > 0:
                event.mem_boosted = getattr(event,"mem_{}_p".format(m))
                event.cat_boosted = m

        event.higgspt = event.genHiggs_pt[0]
        event.toppt = -1
        if event.ngenTopHad > 0:
            event.toppt = event.genTopHad_pt[0]


        if event.cat_resolved is not None and event.cat_boosted is not None:
            MEM["both"]["top"].Fill(event.toppt)
            MEM["both"]["higgs"].Fill(event.higgspt)
            if event.nhiggsCandidate > 0 and event.higgsCandidate_dr_genHiggs[0]<0.6:
                MEM2["both"]["higgs"].Fill(event.higgspt)
        elif event.cat_resolved is None and event.cat_boosted is not None:
            MEM["boo"]["top"].Fill(event.toppt)
            MEM["boo"]["higgs"].Fill(event.higgspt)
            if event.nhiggsCandidate > 0 and event.higgsCandidate_dr_genHiggs[0]<0.6:
                MEM2["boo"]["higgs"].Fill(event.higgspt)
        elif event.cat_resolved is not None and event.cat_boosted is None:
            MEM["res"]["top"].Fill(event.toppt)
            MEM["res"]["higgs"].Fill(event.higgspt)


 
results = ROOT.TFile("out.root","recreate")

for cat in cats:
    for i in pos:
        MEM[cat][i].Write()
        MEM2[cat][i].Write()
