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
full_file_names["TTHOld"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GC1993e8a9d145/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root"
full_file_names["Matching"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/CheckMatching/GCca722c8c52be/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["TTHPerfect"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GCf2a8abfaa34b/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["TTHCheck"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GCc650435e7ba6/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["TTSLCheck"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GCc650435e7ba6/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"
full_file_names["TTDLCheck"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GCc650435e7ba6/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["TTHCheckH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GC2c178a899824/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["TTSLCheckH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GC2c178a899824/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"
full_file_names["TTDLCheckH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GC2c178a899824/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["StuffinFatjet"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/KinematicsSubjets/GC6c02ed00940b/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["MassCheck"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/Top_CheckTagger/GC4fb1ca542edd/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["CheckCatTTH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/VerifyCategorisation/GCf723cad014ff/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["CheckCatTTSL"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/VerifyCategorisation/GCf723cad014ff/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"
full_file_names["CheckCatTTDL"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/VerifyCategorisation/GCf723cad014ff/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["TTHKinematics"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GC26a07f96d7b8/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["TTSLKinematics"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GC26a07f96d7b8/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"
full_file_names["TTDLKinematics"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GC26a07f96d7b8/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root"


lumis = {}
lumis["TTH"] = 1428.0598 #In pb-1 Assuming XS of 0.5071*0.5824 = 0.2934045 pb and Ngen = 4189991.99109
lumis["TTSL"] = 7263.88959 #Assuming XS of 365.45736135 pb and Ngen = 26546419239.9
lumis["TTDL"] = 618.08568#In pb-1 Assuming XS of 88.341903326 pb and Ngen = 546028637.266

targetlumi = 49

output_dir = "../results/CheckForMEM_19062018/"

anc = ["SL_2w2h2t","SL_1w2h2t","SL_0w2h2t","DL_0w2h2t","SL_2w2h2t_sj","SL_1w2h2t_sj","SL_0w2h2t_sj","DL_0w2h2t_sj"]
resolved = anc[:4]
boosted = anc[4:]


########################################
# Create histograms, saved in file
########################################

combinedPlot("MEM_OldNew",
                 [plot( "New", "Difference_all", "", "TTH",color="kRed"),
                  plot( "Old", "Difference_all", "", "TTHOld",color="kBlack")],
                 50,-1,1,
                 label_x   =  "MEM_{boosted}-MEM_{resolved}",
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.55,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 2,
                 legend_text_size = 0.035,
                 get_ratio = False)


combinedPlot("MEM_MatchingTop",
                 [plot( "Top only - Resolved", "Matching_top_SL_2w2h2t", "", "Matching",color="kRed"),
                  plot( "Top only - Boosted", "Matching_top_SL_2w2h2t_sj", "", "Matching",color="kBlack"),
                  plot( "Top + Higgs - Resolved", "Matching_both_SL_2w2h2t", "", "Matching",color="kRed",linestyle = 7),
                  plot( "Top + Higgs - Boosted", "Matching_both_SL_2w2h2t_sj", "", "Matching",color="kBlack",linestyle = 7)],
                  10,0,10, 
                 label_x   =  "0: Unmatched, 1: Fully matched",
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.4,
                 legend_origin_y = 0.6,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 4,
                 legend_text_size = 0.035,
                 get_ratio = False)


combinedPlot("MEM_OldNewPerfect",
                 [plot( "New - all events", "Difference_all", "", "TTH",color="kRed"),
                  plot( "Old - all events", "Difference_all", "", "TTHOld",color="kBlack"),
                  plot( "New - top events", "Difference_top", "", "TTH",color="kRed", linestyle = 2),
                  plot( "New - only good events", "Difference_top", "", "TTHPerfect",color="kRed",linestyle = 7)],
                 50,-1,1,
                 label_x   =  "MEM_{boosted}-MEM_{resolved}",
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.55,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 4,
                 legend_text_size = 0.035,
                 get_ratio = False)


#Get ROC curves as well

f4 = ROOT.TFile.Open(full_file_names["StuffinFatjet"], "READ")

norm = {}

types = ["count_sl_CA15","count_sl_AK8","count_dl_CA15","count_dl_AK8"]
for a in types:
    norm[a] = f4.Get("{}".format(a))
    norm[a].Scale(1/norm[a].GetBinContent(2))

results = ROOT.TFile("./StuffinFatjet_Processed.root","recreate")
for a in types:
    norm[a].Write("{}".format(a))

full_file_names["StuffinFatjetProcessed"] = "./StuffinFatjet_Processed.root"


combinedPlot("MEM_ContentsJet",
                 [plot( "SL - CA15", "count_sl_CA15", "", "StuffinFatjetProcessed",color="kRed"),
                  plot( "SL - AK8", "count_sl_AK8", "", "StuffinFatjetProcessed",color="kRed",linestyle = 7),
                  plot( "DL - CA15", "count_dl_CA15", "", "StuffinFatjetProcessed",color="kBlack"),
                  plot( "DL - AK8", "count_dl_AK8", "", "StuffinFatjetProcessed",color="kBlack",linestyle = 7)],
                  10,0,10, 
                 label_x   =  "1: N_{FJ}, 2: N_{B from Top}, 3: N_{L from Top}, 4:N_{ISR}",
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = False,
                 legend_origin_x = 0.4,
                 legend_origin_y = 0.6,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 4,
                 legend_text_size = 0.035,
                 get_ratio = False)

combinedPlot("HTT_MassCheck",
                 [plot( "Mass", "sl_HTT_matched_mass", "", "MassCheck",color="kRed"),
                  plot( "Reco Mass", "sl_HTT_matched_massreco", "", "MassCheck",color="kBlack",),
                  plot( "Mass_{SD}", "sl_HTT_matched_softdropmass", "", "MassCheck",color="kOrange+7"),],
                  50,0,500, 
                 label_x   =  "Mass",
                 label_y   = "Fraction of events",  
                 axis_unit = "GeV",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.5,
                 legend_origin_y = 0.6,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = False)

names2 = ["TTHCheck","TTSLCheck","TTDLCheck"]
for s in names2:
    combinedPlot("MEM_Top_SL_2w2h2t_{}_Check".format(s),
                     [plot( "n light = 2", "CompareMEM_2l", "", s,color="kRed"),
                      plot( "n light > 2", "CompareMEM_m3l", "", s,color="kRed",linestyle = 7),
                      plot( "SubjetIDPassed = 1", "CompareMEM_sub2", "", s,color="kBlack"),
                      plot( "SubjetIDPassed = 0", "CompareMEM_sub1", "", s,color="kBlack",linestyle = 7),
                      plot( "n light = 2, ID = 1", "CompareMEM_sub1", "", s,color="kBlue"),
                      plot( "Combined", "MEM_top_SL_2w2h2t_sj", "", s,color="kOrange+7")],
                     50,-1,1,
                     label_x   =  "MEM",
                     label_y   = "Fraction of events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.4,
                     legend_origin_y = 0.6,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 6,
                     legend_text_size = 0.035,
                     get_ratio = False)

names3 = ["TTHCheckH","TTSLCheckH","TTDLCheckH"]
cats = ["SL_2w2h2t_sj","SL_1w2h2t_sj","SL_0w2h2t_sj","DL_0w2h2t_sj"]
for t in cats:
    for s in names3:
        combinedPlot("MEM_Higgs_SL_2w2h2t_{}_{}".format(s,t),
                          [plot( "SubjetIDPassed = 1", "CompareMEM_{}_sub2".format(t), "", s,color="kRed"),
                          plot( "SubjetIDPassed = 0", "CompareMEM_{}_sub1".format(t), "", s,color="kRed",linestyle = 7),
                          plot( "Combined", "MEM_higgs_{}".format(t), "", s,color="kBlack")],
                         50,-1,1,
                         label_x   =  "MEM",
                         label_y   = "Fraction of events",  
                         axis_unit = "",
                         #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                         log_y     = False,
                         normalize = True,
                         legend_origin_x = 0.4,
                         legend_origin_y = 0.6,
                         legend_size_x   = 0.25,
                         legend_size_y   = 0.05 * 3,
                         legend_text_size = 0.035,
                         get_ratio = False)


f5 = ROOT.TFile.Open(full_file_names["CheckCatTTH"], "READ")
f6 = ROOT.TFile.Open(full_file_names["CheckCatTTSL"], "READ")
f7 = ROOT.TFile.Open(full_file_names["CheckCatTTDL"], "READ")

norm = {}
nam = ["TTH","TTSL","TTDL"]

norm["TTH"] = f5.Get("Cat")
norm["TTSL"] = f6.Get("Cat")
norm["TTDL"] = f7.Get("Cat")
for a in nam:
    for i in range(1,4):
        totevents = norm[a].GetBinContent(i,1) + norm[a].GetBinContent(i,2) + norm[a].GetBinContent(i,3)
        if totevents > 0:
            for j in range(1,4):
                norm[a].SetBinContent(i,j,norm[a].GetBinContent(i,j)/totevents)


results = ROOT.TFile("./Categorisation_Processed.root","recreate")
for a in nam:
    norm[a].Write("{}".format(a))

full_file_names["Categorisation"] = "./Categorisation_Processed.root"

for s in nam:
    combinedPlot2D("Categorisation_{}".format(s),
        [plot( "", "{}".format(s), "", "Categorisation")],
        3,0,3,3,0,3,
        label_x   = "Generated category",
        label_y   = "Reconstructed category",                          
        axis_unit = "",
        log_y     = False,
        option    = "text")


names6 = ["TTHKinematics"]
for s in names6:
    combinedPlot("MEM_TopHiggs_SL_2w2h2t_{}".format(s),
                     [plot( "Res. All", "MEM_resolved_all", "", s,color="kRed"),
                      plot( "Res. Match", "MEM_resolved_allmatched", "", s,color="kBlack"),
                      plot( "Res. Match + Kin", "MEM_resolved_allmatchandkin", "", s,color="kOrange+7"),
                      plot( "Boos. All", "MEM_boosted_all", "", s,color="kRed",linestyle = 7),
                      plot( "Boos. Match", "MEM_boosted_allmatched", "", s,color="kBlack",linestyle = 7),
                      plot( "Boos. Match + Kin", "MEM_boosted_allmatchandkin", "", s,color="kOrange+7",linestyle = 7)],
                     50,-1,1,
                     label_x   =  "MEM",
                     label_y   = "Fraction of events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.4,
                     legend_origin_y = 0.6,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 6,
                     legend_text_size = 0.035,
                     get_ratio = False)




doWork(full_file_names, output_dir)

#Get ROC curves as well

f1 = ROOT.TFile.Open(full_file_names["TTHCheck"], "READ")
f2 = ROOT.TFile.Open(full_file_names["TTSLCheck"], "READ")
f3 = ROOT.TFile.Open(full_file_names["TTDLCheck"], "READ")

bkg = {}
bkg2 = {}

typ = ["CompareMEM_2l","CompareMEM_m3l","CompareMEM_sub1","CompareMEM_sub2","CompareMEM_2lsub2","MEM_top_SL_2w2h2t_sj","MEM_top_SL_2w2h2t"]
nicename = ["n light = 2","n light > 2","SubjetIDPassed = 0","SubjetIDPassed = 1","n light = 2, ID = 1","SL_2w2h2t_sj","SL_2w2h2t"]
for a in typ:
    bkg[a] = f2.Get("{}".format(a))
    bkg[a].Scale(targetlumi/lumis["TTSL"])
    bkg2[a] = f3.Get("{}".format(a))
    bkg2[a].Scale(targetlumi/lumis["TTDL"])
    bkg[a].Add(bkg2["{}".format(a)])


#Add backgrounds

ro = {}
for a in typ:
    ro[a] = ROOT.TGraph
    ro[a] = calc_roc(f1.Get("{}".format(a)),bkg["{}".format(a)])
 

results = ROOT.TFile("./MEMDistributions_processed.root","recreate")
for a in typ:
    ro[a].Write("ROC_{}".format(a))


f1.Close()
f2.Close()
f3.Close()
results.Close()

full_file_names["ROCs"] = "./MEMDistributions_processed.root"

f = ROOT.TFile.Open(full_file_names["ROCs"], "READ")
rocs = {}
for a in typ:
    rocs[a] = f.Get("ROC_{}".format(a))
f.Close()

colors = [ROOT.kGreen+1,ROOT.kGreen+1,ROOT.kCyan,ROOT.kCyan,ROOT.kRed,ROOT.kRed,ROOT.kBlack]
line = [1,7,1,7,1,7,1]

mu = ROOT.TMultiGraph()
for a in typ:
    m = typ.index(a)
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
for a in typ:
    m = typ.index(a)
    legend.AddEntry(rocs[a],"{}, AOC = {:0.2f}".format(nicename[m], 0.5-rocs[a].Integral()),"l")
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.Draw()
line = ROOT.TLine(0,0,1,1)
line.Draw()
#mu.GetYaxis().SetTitleOffset(1)
c.Print("{}pdf/ROCCurve_MEM.pdf".format(output_dir))
c.Print("{}png/ROCCurve_MEM.png".format(output_dir))
mu.Delete()