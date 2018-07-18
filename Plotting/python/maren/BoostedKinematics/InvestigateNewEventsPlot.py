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
full_file_names["TTH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/InvestigateNewEvents/GC3b4c8dd53fcc/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["TTSL"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/InvestigateNewEvents/GCed2c8e045522/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"
full_file_names["TTDL"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/InvestigateNewEvents/GCed2c8e045522/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root"


ngen = {}
ngen["TTH"] = 3716693.80815
ngen["TTSL"] = 29187802179.8
ngen["TTDL"] = 438669330.543

xsection = {}
xsection["TTH"] = 0.2934045
xsection["TTSL"] = 365.45736135
xsection["TTDL"] = 88.341903326

lumis = {} #These will be in fb-1
lumis["TTH"] = ngen["TTH"] / xsection["TTH"] * 0.001
lumis["TTSL"] = ngen["TTSL"] / xsection["TTSL"] * 0.001
lumis["TTDL"] = ngen["TTDL"] / xsection["TTDL"] * 0.001
print lumis["TTH"], lumis["TTSL"],lumis["TTDL"]


targetlumi = 49

output_dir = "../results/InvestigateNewEvents_05072018/"

pos = ["resolved","boosted","bothres","bothboo"]
cats = ["top","higgs","both","all"]
anc = ["SL_2w2h2t","SL_1w2h2t","SL_0w2h2t","DL_0w2h2t","SL_2w2h2t_sj","SL_1w2h2t_sj","SL_0w2h2t_sj","DL_0w2h2t_sj"]
resolved = anc[:4]
boosted = anc[4:]

var = ["pt","eta","phi","mass"]
prettynames = ["p_{T}-p_{T,gen Quark}","#eta-#eta_{T,gen Quark}","#phi-#phi_{T,gen Quark}","mass"]
liminf = [-100,-1,-1,0]
limsup = [100,1,1,100]

########################################
# Create histograms, saved in file
########################################



for v in var:
    m = var.index(v)
    combinedPlot("NewEvents_Kinematics_hb_{}".format(v),
                 [plot( "New boosted events", "count_new_hb_{}".format(v), "", "TTH",color="kRed"),
                  plot( "Previous res. events", "count_old_hb_{}".format(v), "", "TTH",color="kBlack")],
                 50,liminf[m],limsup[m], 
                 label_x   =  prettynames[m],
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.65,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = False)

    combinedPlot("NewEvents_Kinematics_tb_{}".format(v),
                 [plot( "New boosted events", "count_new_tb_{}".format(v), "", "TTH",color="kRed"),
                  plot( "Previous res. events", "count_old_tb_{}".format(v), "", "TTH",color="kBlack")],
                 50,liminf[m],limsup[m], 
                 label_x   =  prettynames[m],
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.65,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = False)

    combinedPlot("NewEvents_Kinematics_tl_{}".format(v),
                 [plot( "New boosted events", "count_new_tl_{}".format(v), "", "TTH",color="kRed"),
                  plot( "Previous res. events", "count_old_tl_{}".format(v), "", "TTH",color="kBlack")],
                 50,liminf[m],limsup[m], 
                 label_x   =  prettynames[m],
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.65,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = False)

combinedPlot("Object_pt_withCandidate",
                     [plot( "New events, gen. Higgs", "pt_higgs_gen", "", "TTH",color="kRed"),
                      plot( "Res. events, gen. Higgs", "pt_ResEvents_higgs_gen", "", "TTH",color="kRed",linestyle = 7),
                      plot( "New events, gen. Top", "pt_top_gen", "", "TTH",color="kBlack"),
                      plot( "Res. events, gen. Top", "pt_ResEvents_top_gen", "", "TTH",color="kBlack",linestyle = 7)],
                     50,0,800, 
                     label_x   =  "p_{T,Higgs/Top}",
                     label_y   = "Fraction of events",  
                     axis_unit = "GeV",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.4,
                     legend_origin_y = 0.65,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 3,
                     legend_text_size = 0.035,
                     get_ratio = False)

combinedPlot("Njet",
                     [plot( "N boost. jet", "njet_njetsb", "", "TTH",color="kRed"),
                      plot( "N boost. bjet", "njet_nbjetsb", "", "TTH",color="kRed",linestyle = 7),
                      plot( "N res. jets", "njet_njets", "", "TTH",color="kBlack"),
                      plot( "N res. bjets", "njet_nbjets", "", "TTH",color="kBlack",linestyle = 7),],
                     20,0,10, 
                     label_x   =  "n_{Jet}",
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

combinedPlot("Njet_difference",
                     [plot( "N jet boost. - N jet res.", "njet_jetsdiff", "", "TTH",color="kRed"),
                      plot( "N bjet boost. - N bjet res.", "njet_jetsdiffb", "", "TTH",color="kRed",linestyle = 7)],
                     20,-10,10, 
                     label_x   =  "n_{Jet} difference",
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


combinedPlot("NonBjets_DistToBQuark",
                     [plot( "", "distbquark", "", "TTH",color="kRed"),],
                     100,0,5, 
                     label_x   =  "#Delta R (non b jet, nearest b quark)",
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



doWork(full_file_names, output_dir)

f1 = ROOT.TFile.Open(full_file_names["TTH"], "READ")
matchnew  = f1.Get("matching_new")
matchnew.Scale(targetlumi/lumis["TTH"])
print "Match new: "
print "Top:", matchnew.GetBinContent(2)/(matchnew.GetBinContent(2)+matchnew.GetBinContent(3))
print "Higgs:", matchnew.GetBinContent(3)/(matchnew.GetBinContent(3)+matchnew.GetBinContent(4))
matchold  = f1.Get("matching_old")
matchold.Scale(targetlumi/lumis["TTH"])
print "Match old: "
print "Top:", matchold.GetBinContent(2)/(matchold.GetBinContent(2)+matchold.GetBinContent(3))
print "Higgs:", matchold.GetBinContent(3)/(matchold.GetBinContent(3)+matchold.GetBinContent(4))
num = f1.Get("numNE")
num.Scale(targetlumi/lumis["TTH"])
for i in range(num.GetNbinsX()):
    print num.GetBinContent(i)
results = ROOT.TFile("./NewEvents_processed.root","recreate")
num.Write("num")
f1.Close()

full_file_names["num"] = "./NewEvents_processed.root"

combinedPlot("NumNewEvents",
                     [plot( "", "num", "", "num",color="kRed"),],
                     10,0,10, 
                     label_x   =  "Category",
                     label_y   = "# events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = False,
                     legend_origin_x = 0.55,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 3,
                     legend_text_size = 0.035,
                     get_ratio = False)

doWork(full_file_names, output_dir)





f2 = ROOT.TFile.Open(full_file_names["TTSL"], "READ")
f3 = ROOT.TFile.Open(full_file_names["TTDL"], "READ")
num2 = f2.Get("numNE")
num2.Scale(targetlumi/lumis["TTSL"])
print "------SL now"
for i in range(num2.GetNbinsX()):
    print num2.GetBinContent(i)

num3 = f3.Get("numNE")
num3.Scale(targetlumi/lumis["TTDL"])
print "------DL now"
for i in range(num3.GetNbinsX()):
    print num3.GetBinContent(i)

f2.Close()
f3.Close()