#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import pickle
import socket # to get the hostname
import math
import ROOT
import array
import numpy as np

from TTH.Plotting.Helpers.CompareDistributionsPlots import *


def calc_roc(h1, h2, rebin=1):
    h1 = h1.Clone()
    h2 = h2.Clone()
    h1.Rebin(rebin)
    h2.Rebin(rebin)

    if h1.Integral()>0:
        h1.Scale(1.0 / h1.Integral())
    if h2.Integral()>0:
        h2.Scale(1.0 / h2.Integral())
    roc = np.zeros((h1.GetNbinsX()+2, 2))
    e1 = ROOT.Double(0)
    e2 = ROOT.Double(0)


    rc = ROOT.TGraph(h1.GetNbinsX()+2)
    for i in range(0, h1.GetNbinsX()+2):
        I1 = h1.Integral(0, h1.GetNbinsX()+2)
        I2 = h2.Integral(0, h2.GetNbinsX()+2)
        if I1>0 and I2>0:
            esig = float(h1.Integral(i, h1.GetNbinsX()+2)) / I1
            ebkg = float(h2.Integral(i, h2.GetNbinsX()+2)) / I2
            rc.SetPoint(i,esig,ebkg)
    rc.SetPoint(h1.GetNbinsX()+3,0,0)
    return rc



########################################
# Define Input Files and
# output directory
########################################

ROOT.gStyle.SetLegendBorderSize(0)

names = ["TTH","TTSL","TTDL"]
full_file_names = {}
#full_file_names["data"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/Distributions_TopSubjetsUncertainties/SingleMuon_May10/SingleMuon.root"
full_file_names["TTH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GC236a7e8fb997/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["TTSL"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GC236a7e8fb997/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"
full_file_names["TTDL"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GCf2b0287b9af6/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root"

lumis = {}
lumis["TTH"] = 1428.0598 #In pb-1 Assuming XS of 0.5071*0.5824 = 0.2934045 pb and Ngen = 4189991.99109
lumis["TTSL"] = 7263.88959 #Assuming XS of 365.45736135 pb and Ngen = 26546419239.9
lumis["TTDL"] = 618.08568#In pb-1 Assuming XS of 88.341903326 pb and Ngen = 546028637.266

targetlumi = 49

output_dir = "../results/MEMDistributions_14062018/"

anc = ["SL_2w2h2t","SL_1w2h2t","SL_0w2h2t","DL_0w2h2t","SL_2w2h2t_sj","SL_1w2h2t_sj","SL_0w2h2t_sj","DL_0w2h2t_sj"]
resolved = anc[:4]
boosted = anc[4:]


########################################
# Create histograms, saved in file
########################################

for a in anc:
    combinedPlot("MEM_{}".format(a),
                 [plot( "t#bar{t}H", "MEM_all_{}".format(a), "", "TTH",color="kRed"),
                  plot( "t#bar{t} - SL", "MEM_all_{}".format(a), "", "TTSL",color="kOrange+7"),
                  plot( "t#bar{t} - DL", "MEM_all_{}".format(a), "", "TTDL",color="kBlack")],
                 50,0,1, 
                 label_x   =  "MEM",
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.55,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = False)


for a in boosted:
    combinedPlot("MEM_{}_TTH".format(a),
                 [plot( "Boosted Higgs", "MEM_higgs_{}".format(a), "", "TTH",color="kRed"),
                  plot( "Boosted Top", "MEM_top_{}".format(a), "", "TTH",color="kOrange+7"),
                  plot( "Boosted Higgs & Top", "MEM_both_{}".format(a), "", "TTH",color="kBlack")],
                 50,0,1, 
                 label_x   =  "MEM",
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.45,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = False)

    combinedPlot("MEM_{}_TTSL".format(a),
                 [plot( "Boosted Higgs", "MEM_higgs_{}".format(a), "", "TTSL",color="kRed"),
                  plot( "Boosted Top", "MEM_top_{}".format(a), "", "TTSL",color="kOrange+7"),
                  plot( "Boosted Higgs & Top", "MEM_both_{}".format(a), "", "TTSL",color="kBlack")],
                 50,0,1, 
                 label_x   =  "MEM",
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.45,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = False)

    combinedPlot("MEM_{}_TTDL".format(a),
                 [plot( "Boosted Higgs", "MEM_higgs_{}".format(a), "", "TTDL",color="kRed"),
                  plot( "Boosted Top", "MEM_top_{}".format(a), "", "TTDL",color="kOrange+7"),
                  plot( "Boosted Higgs & Top", "MEM_both_{}".format(a), "", "TTDL",color="kBlack")],
                 50,0,1, 
                 label_x   =  "MEM",
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.45,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = False)

    combinedPlot("MEM_Newevents_all_{}".format(a),
                 [plot( "t#bar{t}H", "MEMnew_all_{}".format(a), "", "TTH",color="kRed"),
                  plot( "t#bar{t} - SL", "MEMnew_all_{}".format(a), "", "TTSL",color="kOrange+7"),
                  plot( "t#bar{t} - DL", "MEMnew_all_{}".format(a), "", "TTDL",color="kBlack")],
                 50,0,1, 
                 label_x   =  "MEM",
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.55,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = False)

    for n in ["top","higgs","both"]:
        combinedPlot("MEM_Matched_all_{}_{}".format(a,n),
                     [plot( "t#bar{t}H", "Matched_{}_{}".format(n,a), "", "TTH",color="kRed"),
                      plot( "t#bar{t} - SL", "Matched_{}_{}".format(n,a), "", "TTSL",color="kOrange+7"),
                      plot( "t#bar{t} - DL", "Matched_{}_{}".format(n,a), "", "TTDL",color="kBlack")],
                     50,0,1, 
                     label_x   =  "MEM",
                     label_y   = "Fraction of events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.55,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 3,
                     legend_text_size = 0.035,
                     get_ratio = False)


for i in names:
    combinedPlot("MEM_Difference_{}".format(i),
                     [plot( "Boosted Higgs", "Difference_higgs", "", i,color="kRed"),
                      plot( "Boosted Top", "Difference_top", "", i,color="kOrange+7"),
                      plot( "Boosted Higgs & Top", "Difference_both", "", i,color="kBlack")],
                     50,-1,1, 
                     label_x   =  "MEM_{boosted}-MEM_{resolved}",
                     label_y   = "Fraction of events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.45,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 3,
                     legend_text_size = 0.035,
                     get_ratio = False)

    combinedPlot("MEM_DifferenceMatched_{}".format(i),
                     [plot( "Boosted Higgs", "MatchedDiff_higgs", "", i,color="kRed"),
                      plot( "Boosted Top", "MatchedDiff_top", "", i,color="kOrange+7"),
                      plot( "Boosted Higgs & Top", "MatchedDiff_both", "", i,color="kBlack")],
                     50,-1,1, 
                     label_x   =  "MEM_{boosted}-MEM_{resolved}",
                     label_y   = "Fraction of events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.45,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 3,
                     legend_text_size = 0.035,
                     get_ratio = False)

    combinedPlot("MEM_Difference_all_{}".format(i),
                     [plot( "Boosted Higgs", "Difference2_higgs", "", i,color="kRed"),
                      plot( "Boosted Top", "Difference2_top", "", i,color="kOrange+7"),
                      plot( "Boosted Higgs & Top", "Difference2_both", "", i,color="kBlack")],
                     50,-1,1, 
                     label_x   =  "MEM_{boosted}-MEM_{resolved}",
                     label_y   = "Fraction of events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.45,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 3,
                     legend_text_size = 0.035,
                     get_ratio = False)

    for pos in ["tth","ttbb"]:
        combinedPlot("MEM_Difference_{}_{}".format(i,pos),
                     [plot( "Boosted Higgs", "Checks2_higgs_{}".format(pos), "", i,color="kRed"),
                      plot( "Boosted Top", "Checks2_top_{}".format(pos), "", i,color="kOrange+7"),
                      plot( "Boosted Higgs & Top", "Checks2_both_{}".format(pos), "", i,color="kBlack")],
                     100,-100,100, 
                     label_x   =  "log(prob_{boosted,pos})-log(prob_{resolved,pos})",
                     label_y   = "Fraction of events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.45,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 3,
                     legend_text_size = 0.035,
                     get_ratio = False)

        if i is not "TTDL":
            combinedPlot2D("MEM_Probability_{}_{}".format(i,pos),
                    [plot( "", "Prob1_all_{}".format(pos), "", i)],
                    200, 0,1000,100,0,5,
                    label_x   = "log(boosted probability)",
                    label_y   = "log(resolved probability)",                          
                    axis_unit = "",
                    log_y     = False,)
            
            combinedPlot2D("MEM_Probability2_{}_{}".format(i,pos),
                    [plot( "", "Prob2_all_{}".format(pos), "", i)],
                    200, 0,1000,100,0,5,
                    label_x   = "log(boosted probability)",
                    label_y   = "log(resolved probability)",                          
                    axis_unit = "",
                    log_y     = False,)

        combinedPlot("MEM_Difference2_{}_{}".format(i,pos),
                     [plot( "Boosted Higgs", "Checks3_higgs_{}".format(pos), "", i,color="kRed"),
                      plot( "Boosted Top", "Checks3_top_{}".format(pos), "", i,color="kOrange+7"),
                      plot( "Boosted Higgs & Top", "Checks3_both_{}".format(pos), "", i,color="kBlack")],
                     100,-100,100, 
                     label_x   =  "log(prob_{boosted,pos})-log(prob_{resolved,pos})",
                     label_y   = "Fraction of events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.45,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 3,
                     legend_text_size = 0.035,
                     get_ratio = False)

    combinedPlot("MEM_Newevents_{}".format(i),
                     [plot( "Boosted Higgs", "Newevents_higgs", "", i,color="kRed"),
                      plot( "Boosted Top", "Newevents_top", "", i,color="kOrange+7"),
                      plot( "Boosted Higgs & Top", "Newevents_both", "", i,color="kBlack")],
                     50,0,1, 
                     label_x   =  "MEM",
                     label_y   = "Fraction of events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.45,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 3,
                     legend_text_size = 0.035,
                     get_ratio = False)

for m in resolved:
    combinedPlot("MEM_BoostedeventsinResolved_{}".format(m),
                     [plot( "t#bar{t}H", "Checks_{}_sj_1".format(m), "", "TTH",color="kRed"),
                      plot( "t#bar{t} - SL", "Checks_{}_sj_1".format(m), "", "TTSL",color="kOrange+7"),
                      plot( "t#bar{t} - DL", "Checks_{}_sj_1".format(m), "", "TTDL",color="kBlack")],
                     50,0,1, 
                     label_x   =  "MEM",
                     label_y   = "Fraction of events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.45,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 3,
                     legend_text_size = 0.035,
                     get_ratio = False)

    combinedPlot("MEM_GoodResolvedinBoosted_{}".format(m),
                 [plot( "t#bar{t}H", "Checks_{}_sj_2".format(m), "", "TTH",color="kRed"),
                  plot( "t#bar{t} - SL", "Checks_{}_sj_2".format(m), "", "TTSL",color="kOrange+7"),
                  plot( "t#bar{t} - DL", "Checks_{}_sj_2".format(m), "", "TTDL",color="kBlack")],
                 50,0,1, 
                 label_x   =  "MEM",
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.45,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = False)

    for pos in ["s","b"]:
        if m == "DL_0w2h2t":
            continue
        combinedPlot("MEM_BoostedeventsinResolved_{}_{}".format(m,pos),
                     [plot( "t#bar{t}H", "Checks_{}_sj_1_{}".format(m,pos), "", "TTH",color="kRed"),
                      plot( "t#bar{t} - SL", "Checks_{}_sj_1_{}".format(m,pos), "", "TTSL",color="kOrange+7"),
                      plot( "t#bar{t} - DL", "Checks_{}_sj_1_{}".format(m,pos), "", "TTDL",color="kBlack")],
                     100,-60,20, 
                     label_x   =  "log(prob_{pos})",
                     label_y   = "Fraction of events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.45,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 3,
                     legend_text_size = 0.035,
                     get_ratio = False)

        combinedPlot("MEM_GoodResolvedinBoosted_{}_{}".format(m,pos),
                     [plot( "t#bar{t}H", "Checks_{}_sj_2_{}".format(m,pos), "", "TTH",color="kRed"),
                      plot( "t#bar{t} - SL", "Checks_{}_sj_2_{}".format(m,pos), "", "TTSL",color="kOrange+7"),
                      plot( "t#bar{t} - DL", "Checks_{}_sj_2_{}".format(m,pos), "", "TTDL",color="kBlack")],
                     100,-60,20, 
                     label_x   =  "log(prob_{pos})",
                     label_y   = "Fraction of events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.45,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 3,
                     legend_text_size = 0.035,
                     get_ratio = False)

for pos in ["s","b"]:
    combinedPlot("MEM_BoostedeventsinResolved_DL_0w2h2t_{}".format(pos),
                         [plot( "t#bar{t}H", "Checks_DL_0w2h2t_sj_1_{}".format(pos), "", "TTH",color="kRed"),
                          plot( "t#bar{t} - SL", "Checks_DL_0w2h2t_sj_1_{}".format(pos), "", "TTSL",color="kOrange+7"),
                          plot( "t#bar{t} - DL", "Checks_DL_0w2h2t_sj_1_{}".format(pos), "", "TTDL",color="kBlack")],
                         100,-60,20, 
                         label_x   =  "log(prob_{pos})",
                         label_y   = "Fraction of events",  
                         axis_unit = "",
                         #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                         log_y     = False,
                         normalize = True,
                         legend_origin_x = 0.45,
                         legend_origin_y = 0.7,
                         legend_size_x   = 0.25,
                         legend_size_y   = 0.05 * 3,
                         legend_text_size = 0.035,
                         get_ratio = False)

    combinedPlot("MEM_GoodResolvedinBoosted_DL_0w2h2t_{}".format(pos),
                         [plot( "t#bar{t}H", "Checks_DL_0w2h2t_sj_2_{}".format(pos), "", "TTH",color="kRed"),
                          plot( "t#bar{t} - SL", "Checks_DL_0w2h2t_sj_2_{}".format(pos), "", "TTSL",color="kOrange+7"),
                          plot( "t#bar{t} - DL", "Checks_DL_0w2h2t_sj_2_{}".format(pos), "", "TTDL",color="kBlack")],
                         100,-60,20, 
                         label_x   =  "log(prob_{pos})",
                         label_y   = "Fraction of events",  
                         axis_unit = "",
                         #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                         log_y     = False,
                         normalize = True,
                         legend_origin_x = 0.45,
                         legend_origin_y = 0.7,
                         legend_size_x   = 0.25,
                         legend_size_y   = 0.05 * 3,
                         legend_text_size = 0.035,
                         get_ratio = False)

for i in resolved:
    combinedPlot("MEM_Migrations_{}".format(i),
                         [plot( "t#bar{t}H", "Migrations_{}".format(i), "", "TTH",color="kRed"),
                          plot( "t#bar{t} - SL", "Migrations_{}".format(i), "", "TTSL",color="kOrange+7"),
                          plot( "t#bar{t} - DL", "Migrations_{}".format(i), "", "TTDL",color="kBlack")],
                         7,0,7, 
                         label_x   =  "Migrations",
                         label_y   = "Fraction of events",  
                         axis_unit = "",
                         #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                         log_y     = False,
                         normalize = True,
                         legend_origin_x = 0.45,
                         legend_origin_y = 0.7,
                         legend_size_x   = 0.25,
                         legend_size_y   = 0.05 * 3,
                         legend_text_size = 0.035,
                         get_ratio = False)

doWork(full_file_names, output_dir)

#Get ROC curves as well

f1 = ROOT.TFile.Open(full_file_names["TTH"], "READ")
f2 = ROOT.TFile.Open(full_file_names["TTSL"], "READ")
f3 = ROOT.TFile.Open(full_file_names["TTDL"], "READ")

bkg = {}
bkg2 = {}
for a in anc:
    bkg["MEM_all_{}".format(a)] = f2.Get("MEM_all_{}".format(a))
    bkg["MEM_all_{}".format(a)].Scale(targetlumi/lumis["TTSL"])
    bkg2["MEM_all_{}".format(a)] = f3.Get("MEM_all_{}".format(a))
    bkg2["MEM_all_{}".format(a)].Scale(targetlumi/lumis["TTDL"])
    bkg["MEM_all_{}".format(a)].Add(bkg2["MEM_all_{}".format(a)])


#Add backgrounds

ro = {}
for a in anc:
    ro[a] = ROOT.TGraph
    ro[a] = calc_roc(f1.Get("MEM_all_{}".format(a)),bkg["MEM_all_{}".format(a)])
 

results = ROOT.TFile("./MEMDistributions_processed.root","recreate")
for a in anc:
    ro[a].Write("ROC_{}".format(a))


f1.Close()
f2.Close()
f3.Close()
results.Close()

full_file_names["ROCs"] = "./MEMDistributions_processed.root"

f = ROOT.TFile.Open(full_file_names["ROCs"], "READ")
rocs = {}
for a in anc:
    rocs[a] = f.Get("ROC_{}".format(a))
f.Close()

colors = [ROOT.kRed,ROOT.kBlack,ROOT.kGreen+1,ROOT.kCyan,ROOT.kRed,ROOT.kBlack,ROOT.kGreen+1,ROOT.kCyan]
line = [1,1,1,1,7,7,7,7]

mu = ROOT.TMultiGraph()
for a in anc:
    m = anc.index(a)
    rocs[a].SetLineColor(colors[m])
    rocs[a].SetLineStyle(line[m])
    rocs[a].SetLineWidth(2)
    mu.Add(rocs[a])
c = ROOT.TCanvas("c","c",600,600)
c.SetLeftMargin(0.16)
mu.Draw("AL")
mu.GetXaxis().SetTitle("#varepsilon_{sig}")
mu.GetYaxis().SetTitle("#varepsilon_{bkg}")
mu.GetXaxis().SetLimits(0,1)
mu.GetYaxis().SetRangeUser(0,1)
legend = ROOT.TLegend(0.2,0.65,0.7,0.85)
for a in anc:
    legend.AddEntry(rocs[a],"{}, AOC = {:0.2f}".format(a, 0.5-rocs[a].Integral()),"l")
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.Draw()
line = ROOT.TLine(0,0,1,1)
line.Draw()
#mu.GetYaxis().SetTitleOffset(1)
c.Print("{}pdf/ROCCurve_MEM.pdf".format(output_dir))
c.Print("{}png/ROCCurve_MEM.png".format(output_dir))
mu.Delete()