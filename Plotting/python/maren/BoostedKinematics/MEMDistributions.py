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
#SKIP_EVENTS = int(os.environ["SKIP_EVENTS"]) 
#MAX_EVENTS = int(os.environ["MAX_EVENTS"]) 



#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_127.root"
#full_file_names["TT"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_45.root"

########################################
# Create histograms, saved in file
########################################

cats = ["top","higgs","both","all","None"]
anc = ["SL_2w2h2t","SL_1w2h2t","SL_0w2h2t","DL_0w2h2t","SL_2w2h2t_sj","SL_1w2h2t_sj","SL_0w2h2t_sj","DL_0w2h2t_sj"]
resolved = anc[:4]
boosted = anc[4:]
checks = ["1","2","1_s","1_b","2_s","2_b"]
mems = ["tth","ttbb"]


MEM = {}
MEMnew = {}
Difference = {}
Difference2 = {}
Newevents = {}
Checks = {}
Checks2 = {}
Checks3 = {}
Migrations = {}
Matched = {}
MatchedDiff = {}
Prob1 = {}
Prob2 = {}

for cat in cats:
    MEM[cat] = {}
    MEMnew[cat] = {}
    Matched[cat] = {}
    for i in anc:
        MEM[cat][i] = ROOT.TH1F("MEM_{}_{}".format(cat,i),"MEM_{}_{}".format(cat,i),50,0,1)
        MEM[cat][i].Sumw2()
    for i in boosted:
        MEMnew[cat][i] = ROOT.TH1F("MEMnew_{}_{}".format(cat,i),"MEMnew_{}_{}".format(cat,i),50,0,1)
        MEMnew[cat][i].Sumw2()
        Matched[cat][i] = ROOT.TH1F("Matched_{}_{}".format(cat,i),"Matched_{}_{}".format(cat,i),50,0,1)
        Matched[cat][i].Sumw2()

    Difference[cat] = ROOT.TH1F("Difference_{}".format(cat),"Difference_{}".format(cat),50,-1,1)
    Difference[cat].Sumw2()
    MatchedDiff[cat] = ROOT.TH1F("MatchedDiff_{}".format(cat),"MatchedDiff_{}".format(cat),50,-1,1)
    MatchedDiff[cat].Sumw2()
    Difference2[cat] = ROOT.TH1F("Difference2_{}".format(cat),"Difference2_{}".format(cat),50,-1,1)
    Difference2[cat].Sumw2()
    Newevents[cat] = ROOT.TH1F("Newevents_{}".format(cat),"Newevents_{}".format(cat),50,0,1)
    Newevents[cat].Sumw2()

for b in boosted:
    Checks[b] = {}
    for c in checks:
        if "_" in c:
            Checks[b][c] = ROOT.TH1F("Checks_{}_{}".format(b,c),"Checks_{}_{}".format(b,c),100,-60,-20)
        else:
            Checks[b][c] = ROOT.TH1F("Checks_{}_{}".format(b,c),"Checks_{}_{}".format(b,c),50,0,1)
        Checks[b][c].Sumw2()
for c in cats:
    Checks2[c] = {}
    Checks3[c] = {}
    Prob1[c] = {}
    Prob2[c] = {}
    for b in mems:
        Checks2[c][b] = ROOT.TH1F("Checks2_{}_{}".format(c,b),"Checks2_{}_{}".format(c,b),100,-100,100)
        Checks3[c][b] = ROOT.TH1F("Checks3_{}_{}".format(c,b),"Checks3_{}_{}".format(c,b),100,-100,100)
        Prob1[c][b] = ROOT.TH2F("Prob1_{}_{}".format(c,b),"Prob1".format(c,b),100,-100,-20,100,-100,-20)
        Prob2[c][b] = ROOT.TH2F("Prob2_{}_{}".format(c,b),"Prob2".format(c,b),100,-100,-20,100,-100,-20)
        Checks2[c][b].Sumw2()
        Checks3[c][b].Sumw2()
for c in resolved:
    Migrations[c] = ROOT.TH1F("Migrations_{}".format(c),"Migrations_{}".format(c),10,0,10)
    Migrations[c].Sumw2()

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
            if event.ntopCandidate > 0 and event.topCandidate_subjetIDPassed[0] < 0.5:
                continue


        #Now have a look at some MEM distributions
        for m in resolved:
            if getattr(event,"mem_{}_p".format(m)) > 0:
                MEM["all"][m].Fill(getattr(event,"mem_{}_p".format(m)), event.genWeight)
        for m in boosted:
            if getattr(event,"mem_{}_p".format(m)) > 0:
                if event.ntopCandidate == 0:
                    continue
                MEM["all"][m].Fill(getattr(event,"mem_{}_p".format(m)), event.genWeight)
                MEM[typ][m].Fill(getattr(event,"mem_{}_p".format(m)), event.genWeight)

        res = 0
        ress = 0
        resb = 0
        boo = 0
        boos = 0
        boob = 0
        diff = 0
        for m in resolved:
            if getattr(event,"mem_{}_p".format(m)) > 0:
                res = getattr(event,"mem_{}_p".format(m))
                if getattr(event,"mem_tth_{}_p".format(m)) > 0 and getattr(event,"mem_ttbb_{}_p".format(m)) > 0:
                    ress = math.log(getattr(event,"mem_tth_{}_p".format(m)))
                    resb = math.log(getattr(event,"mem_ttbb_{}_p".format(m)))
        for m in boosted:
            if getattr(event,"mem_{}_p".format(m)) > 0:
                boo = getattr(event,"mem_{}_p".format(m))
                if getattr(event,"mem_tth_{}_p".format(m)) > 0 and getattr(event,"mem_ttbb_{}_p".format(m)) > 0:
                    boos = math.log(getattr(event,"mem_tth_{}_p".format(m)))
                    boob = math.log(getattr(event,"mem_ttbb_{}_p".format(m)))
                if res == 0:
                    MEMnew["all"][m].Fill(getattr(event,"mem_{}_p".format(m)), event.genWeight)
                    MEMnew[typ][m].Fill(getattr(event,"mem_{}_p".format(m)), event.genWeight)
            if typ == "higgs" and matchhiggs == 1:
                Matched[typ][m].Fill(getattr(event,"mem_{}_p".format(m)), event.genWeight)
            if typ == "top" and matchtop == 1:
                Matched[typ][m].Fill(getattr(event,"mem_{}_p".format(m)), event.genWeight)
            if typ == "both" and matchhiggs == 1 and matchtop == 1:
                Matched[typ][m].Fill(getattr(event,"mem_{}_p".format(m)), event.genWeight)    

        if res > 0 and boo > 0:
            diff = boo-res
            Difference["all"].Fill(diff, event.genWeight)
            Difference[typ].Fill(diff, event.genWeight)

            Checks2["all"]["tth"].Fill(boos-ress, event.genWeight)
            Checks2[typ]["tth"].Fill(boos-ress, event.genWeight)
            Checks2["all"]["ttbb"].Fill(boob-resb, event.genWeight)
            Checks2[typ]["ttbb"].Fill(boob-resb, event.genWeight)

            Prob1["all"]["tth"].Fill(boos,ress, event.genWeight)
            Prob1[typ]["tth"].Fill(boos,ress, event.genWeight)
            Prob1["all"]["ttbb"].Fill(boob,resb, event.genWeight)
            Prob1[typ]["ttbb"].Fill(boob,resb, event.genWeight)

            if typ == "higgs" and matchhiggs == 1:
                MatchedDiff[typ].Fill(diff, event.genWeight)
            if typ == "top" and matchtop == 1:
                MatchedDiff[typ].Fill(diff, event.genWeight)
            if typ == "both" and matchhiggs == 1 and matchtop == 1:
                MatchedDiff[typ].Fill(diff, event.genWeight)          

        diff = boo-res
        Difference2["all"].Fill(diff, event.genWeight)
        Difference2[typ].Fill(diff, event.genWeight)

        Checks3["all"]["tth"].Fill(boos-ress, event.genWeight)
        Checks3[typ]["tth"].Fill(boos-ress, event.genWeight)
        Checks3["all"]["ttbb"].Fill(boob-resb, event.genWeight)
        Checks3[typ]["ttbb"].Fill(boob-resb, event.genWeight)

        Prob2["all"]["tth"].Fill(boos,ress, event.genWeight)
        Prob2[typ]["tth"].Fill(boos,ress, event.genWeight)
        Prob2["all"]["ttbb"].Fill(boob,resb, event.genWeight)
        Prob2[typ]["ttbb"].Fill(boob,resb, event.genWeight)


        if res == 0 and boo > 0:
            Newevents["all"].Fill(boo, event.genWeight)
            Newevents[typ].Fill(boo, event.genWeight)

        #### Investigations - Work on SL1w2h2t category
        for m in resolved:
            if getattr(event,"mem_{}_sj_p".format(m)) > 0:
                Checks["{}_sj".format(m)]["1"].Fill(getattr(event,"mem_{}_p".format(m)), event.genWeight)
                if getattr(event,"mem_tth_{}_sj_p".format(m)) > 0 and getattr(event,"mem_ttbb_{}_sj_p".format(m)) > 0:
                    Checks["{}_sj".format(m)]["1_s"].Fill(math.log(getattr(event,"mem_tth_{}_sj_p".format(m))), event.genWeight)
                    Checks["{}_sj".format(m)]["1_b"].Fill(math.log(getattr(event,"mem_ttbb_{}_sj_p".format(m))), event.genWeight)

            if getattr(event,"mem_{}_p".format(m)) > 0.7:
                if getattr(event,"mem_{}_sj_p".format(m)) > 0:
                    Checks["{}_sj".format(m)]["2"].Fill(getattr(event,"mem_{}_sj_p".format(m)), event.genWeight)
                    if getattr(event,"mem_tth_{}_sj_p".format(m)) > 0 and getattr(event,"mem_ttbb_{}_sj_p".format(m)) > 0:
                        Checks["{}_sj".format(m)]["2_s"].Fill(math.log(getattr(event,"mem_tth_{}_sj_p".format(m))), event.genWeight)
                        Checks["{}_sj".format(m)]["2_b"].Fill(math.log(getattr(event,"mem_ttbb_{}_sj_p".format(m))), event.genWeight)

        for m in resolved:
            if getattr(event,"mem_{}_p".format(m)) > 0:
                Migrations[m].Fill(1,event.genWeight)
            if getattr(event,"mem_{}_sj_p".format(m)) > 0:
                Migrations[m].Fill(2,event.genWeight)
            if getattr(event,"mem_{}_p".format(m)) > 0:
                existsb = 0
                for n in boosted:
                    if getattr(event,"mem_{}_p".format(n)) > 0:
                        existsb = 1
                        if m not in n:
                            Migrations[m].Fill(5,event.genWeight)
                if existsb == 0:
                    Migrations[m].Fill(6,event.genWeight)

            #New boosted events, boosted events from other resolved category
            if getattr(event,"mem_{}_sj_p".format(m)) > 0:
                exists = 0
                own = 0
                for o in resolved:
                    if getattr(event,"mem_{}_p".format(m)) > 0:
                        exists = 1
                        if o == m:
                            own = 1
                if exists == 0:
                    Migrations[m].Fill(3,event.genWeight)
                if exists == 1 and own == 0:
                    Migrations[m].Fill(4,event.genWeight)




results = ROOT.TFile("out.root","recreate")
for b in boosted:
    for c in checks:
        Checks[b][c].Write()
for c in cats:
    for b in mems:
        Checks2[c][b].Write()
        Checks3[c][b].Write()
        Prob1[c][b].Write()
        Prob2[c][b].Write()
for c in resolved:
    Migrations[c].Write()

for cat in cats:
    for i in anc:
        MEM[cat][i].Write()
    for i in boosted:
        MEMnew[cat][i].Write()
        Matched[cat][i].Write()
    Difference[cat].Write()
    Difference2[cat].Write()
    MatchedDiff[cat].Write()
    Newevents[cat].Write()