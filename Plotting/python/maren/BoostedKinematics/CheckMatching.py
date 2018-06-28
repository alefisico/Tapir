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
#SKIP_EVENTS = int(os.environ["SKIP_EVENTS"]) 
#MAX_EVENTS = int(os.environ["MAX_EVENTS"]) 



#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_168.root"
#full_file_names["TT"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_45.root"

########################################
# Create histograms, saved in file
########################################

cats = ["top","higgs","both"]
anc = ["SL_2w2h2t","SL_1w2h2t","SL_0w2h2t","DL_0w2h2t","SL_2w2h2t_sj","SL_1w2h2t_sj","SL_0w2h2t_sj","DL_0w2h2t_sj"]
resolved = anc[:4]
boosted = anc[4:]


Matching = {}

for i in anc:
    Matching[i] = {}
    for cat in cats:
        Matching[i][cat] = ROOT.TH1F("Matching_{}_{}".format(cat,i),"Matching_{}_{}".format(cat,i),10,0,10)


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


        catresolved = None
        if event.numJets == 4 and event.nBDeepCSVM == 4 and event.is_sl:
            catresolved = "SL_0w2h2t"
        elif event.numJets == 5 and event.nBDeepCSVM == 4 and event.is_sl:
            catresolved = "SL_1w2h2t"
        elif event.numJets >= 6 and event.nBDeepCSVM == 4 and event.is_sl:
            catresolved = "SL_2w2h2t"
        elif event.numJets == 4 and event.nBDeepCSVM == 4 and event.is_dl:
            catresolved = "DL_0w2h2t"

        catboosted = None
        if event.boosted == 1:
            if event.n_boosted_bjets == 4:
                if event.is_sl:
                    if event.n_boosted_ljets == 0:
                        catboosted = "SL_0w2h2t_sj"
                    elif event.n_boosted_ljets == 1:
                        catboosted = "SL_1w2h2t_sj"
                    elif event.n_boosted_ljets == 2:
                        catboosted = "SL_2w2h2t_sj"
                elif event.is_dl and event.n_boosted_ljets == 0:
                    catboosted  = "DL_0w2h2t_sj"



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

        if catboosted is not None:
            if typ == "top":
                Matching[catboosted][typ].Fill(1)
                if matchtop == 1:
                    Matching[catboosted][typ].Fill(2)
            if typ == "higgs":
                Matching[catboosted][typ].Fill(1)
                if matchhiggs == 1:
                    Matching[catboosted][typ].Fill(2)
            elif typ == "both":
                Matching[catboosted][typ].Fill(1)
                if matchtop == 1 and matchhiggs == 1:
                    Matching[catboosted][typ].Fill(2)

        if catresolved is not None:
            Matching[catresolved]["top"].Fill(1)
            Matching[catresolved]["higgs"].Fill(1)
            Matching[catresolved]["both"].Fill(1)
            if event.nMatch_hb == 2 and event.nMatch_wq == 2 and event.nMatch_tb >= 1:
                Matching[catresolved]["both"].Fill(2)
            elif event.nMatch_hb == 2:
                Matching[catresolved]["higgs"].Fill(2)
            elif event.nMatch_wq == 2 and event.nMatch_tb >= 1:
                Matching[catresolved]["top"].Fill(2)


results = ROOT.TFile("out.root","recreate")
for i in anc:
    for cat in cats:
        Matching[i][cat].Write()