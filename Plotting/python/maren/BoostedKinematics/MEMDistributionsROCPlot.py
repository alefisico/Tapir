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
full_file_names["TTH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GC8eefbad367bd/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["TTSL"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GC8eefbad367bd/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"
full_file_names["TTDL"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/MEMDistributions/GC8eefbad367bd/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root"


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

output_dir = "../results/MEMDistributions_17072018/"

pos = ["resolved","boosted","bothres","bothboo"]
cats = ["top","higgs","both","all"]
#anc = ["SL_2w2h2t","SL_1w2h2t","SL_0w2h2t","DL_0w2h2t","SL_2w2h2t_sj","SL_1w2h2t_sj","SL_0w2h2t_sj","DL_0w2h2t_sj"]
#resolved = anc[:4]
#boosted = anc[4:]

anc = ["SL_2w2h2t","SL_2w2h2t_sj"]
resolved = anc[:1]
boosted = anc[1:]

########################################
# Create histograms, saved in file
########################################

for a in cats:
    for b in pos:
        combinedPlot("MEM_{}_{}".format(a,b),
                     [plot( "t#bar{t}H", "MEM_{}_{}".format(a,b), "", "TTH",color="kRed"),
                      plot( "t#bar{t} - SL", "MEM_{}_{}".format(a,b), "", "TTSL",color="kOrange+7"),
                      plot( "t#bar{t} - DL", "MEM_{}_{}".format(a,b), "", "TTDL",color="kBlack")],
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


doWork(full_file_names, output_dir)


#Get ROC curves as well

prettynames2 = ["res ev.","boost ev.","res + boost - res MEM","res + boost - boost MEM"]


bkg = {}
bkg2 = {}
ro = {}
rocs = {}
for ca in cats:

    f1 = ROOT.TFile.Open(full_file_names["TTH"], "READ")
    f2 = ROOT.TFile.Open(full_file_names["TTSL"], "READ")
    f3 = ROOT.TFile.Open(full_file_names["TTDL"], "READ")

    bkg[ca] = {}
    bkg2[ca] = {}
    rocs[ca] = {}
    ro[ca] = {}

    for a in pos:
        bkg[ca]["MEM_{}_{}".format(ca,a)] = f2.Get("MEM_{}_{}".format(ca,a))
        bkg[ca]["MEM_{}_{}".format(ca,a)].Scale(targetlumi/lumis["TTSL"])
        bkg2[ca]["MEM_{}_{}".format(ca,a)] = f3.Get("MEM_{}_{}".format(ca,a))
        bkg2[ca]["MEM_{}_{}".format(ca,a)].Scale(targetlumi/lumis["TTDL"])
        bkg[ca]["MEM_{}_{}".format(ca,a)].Add(bkg2[ca]["MEM_{}_{}".format(ca,a)])


    #Add backgrounds

    for a in pos:
        ro[ca][a] = ROOT.TGraph
        ro[ca][a] = calc_roc(f1.Get("MEM_{}_{}".format(ca,a)),bkg[ca]["MEM_{}_{}".format(ca,a)])
     

    results = ROOT.TFile("./MEMDistributions_processed.root","recreate")
    for a in pos:
        ro[ca][a].Write("ROC_{}".format(a))


    f1.Close()
    f2.Close()
    f3.Close()
    results.Close()

    full_file_names["ROCs"] = "./MEMDistributions_processed.root"

    f = ROOT.TFile.Open(full_file_names["ROCs"], "READ")
    for a in pos:
        rocs[ca][a] = f.Get("ROC_{}".format(a))
    f.Close()

    colors = [ROOT.kBlack,ROOT.kRed,ROOT.kBlack,ROOT.kRed]
    line = [1,1,7,7]

    mu = ROOT.TMultiGraph()
    for a in pos:
        m = pos.index(a)
        rocs[ca][a].SetLineColor(colors[m])
        rocs[ca][a].SetLineStyle(line[m])
        rocs[ca][a].SetLineWidth(2)
        mu.Add(rocs[ca][a])
    c = ROOT.TCanvas("c","c",600,600)
    c.SetLeftMargin(0.16)
    mu.Draw("AL")
    mu.GetXaxis().SetTitle("#varepsilon_{sig}")
    mu.GetYaxis().SetTitle("#varepsilon_{bkg}")
    mu.GetXaxis().SetLimits(0,1)
    mu.GetYaxis().SetRangeUser(0,1)
    legend = ROOT.TLegend(0.2,0.65,0.7,0.85)
    for a in pos:
        n = pos.index(a)
        legend.AddEntry(rocs[ca][a],"{}, AOC = {:0.2f}".format(prettynames2[n], 0.5-rocs[ca][a].Integral()),"l")
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.Draw()
    line = ROOT.TLine(0,0,1,1)
    line.Draw()
    #mu.GetYaxis().SetTitleOffset(1)
    c.Print("{}pdf/ROCCurve_MEM_{}.pdf".format(output_dir,ca))
    c.Print("{}png/ROCCurve_MEM_{}.png".format(output_dir,ca))
    mu.Delete()
