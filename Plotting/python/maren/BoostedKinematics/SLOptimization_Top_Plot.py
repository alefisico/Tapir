#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import pickle
import socket # to get the hostname
import numpy as np
import math

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.CompareDistributionsPlots import *
else:
    from TTH.Plotting.python.Helpers.CompareDistributionsPlots import *


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

full_file_names = {}
full_file_names["ttH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/SLOptimization_Top/GC0fa6b533bfef/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["tt"]  = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/SLOptimization_Top/GC9fa59a1156db/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8.root"
#full_file_names = ""

#output_dir = "results/JetCalibrations_Plots/"
output_dir = "results/SLOptimization_Top_09072018/"

lumis = {}
lumis["ttH"] = 4982.71007 #In pb-1 Assuming XS of 0.5071*0.5824 pb and Ngen = 2164706 
lumis["tt"] = 36.538208 #Assuming XS of 831.76 pb and Ngen = 30391020.0 

targetlumi = 40.0

li_colors = [ROOT.kRed,      ROOT.kBlue+1,     ROOT.kBlack, 
         ROOT.kOrange-1, ROOT.kViolet+1,   ROOT.kGreen+1,
         ROOT.kGray,     ROOT.kYellow]*10  

########################################
# Plots
########################################
categories = ["DL"]

var = ["pt","btag1","btag2","bbtag","DRl","mass","softdropmass","tau32","eta","fRec","Ropt","btag3"]
limits = [600,1,1,1,5,600,600,1,5,2,5,1]
limitsinf = [0,0,0,-1,0,0,0,0,-5,0,-5,0]
fatjets = ["Higgs","HiggsAK8","Top"]
prettyname = ["p_{T}","btagL","btagS","bbtag","#Delta R (l)","mass","mass_{SD}","#tau_{32}","|#eta|","f_{Rec}","R_{opt}","btagSSL"]

#Number of fatjets - cuts on pt and eta of fatjet
combinedPlot("SL_Nfatjets",
             [plot( "CA15 SD - ttHbb", "Nfatjets_sl_TCA15", "", "ttH"), 
              plot( "AK8 SD - ttHbb", "Nfatjets_sl_TAK8", "", "ttH"),
              plot( "HTT - ttHbb", "Nfatjets_sl_THTT", "", "ttH"),
              plot( "CA15 SD - TTbar", "Nfatjets_sl_TCA15", "", "tt"), 
              plot( "AK8 SD - TTbar", "Nfatjets_sl_TAK8", "", "tt"),
              plot( "HTT - TTbar", "Nfatjets_sl_THTT", "", "tt")],
             5,0,5, 
             label_x   =  "Nfatjets",
             label_y   = "N of events",  
             axis_unit = "",
             #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.6,
             legend_origin_y = 0.7,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 2,
             legend_text_size = 0.035,
             get_ratio = False)

#Matched means with DeltaR<1.0
combinedPlot("SL_Matchedfatjets",
             [plot( "Gen Top", "Count_sl", "", "ttH"), 
              plot( "Match to CA15 SD", "MatchedFatjet_sl_TCA15", "", "ttH"), 
              plot( "Match to AK8 SD", "MatchedFatjet_sl_TAK8", "", "ttH"),
              plot( "Match to HTT", "MatchedFatjet_sl_THTT", "", "ttH")],
             50,0,600, 
             label_x   =  "Gen Top p_{T}",
             label_y   = "N of events",  
             axis_unit = "GeV",
             #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
             log_y     = False,
             normalize = False,
             legend_origin_x = 0.6,
             legend_origin_y = 0.7,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 2,
             legend_text_size = 0.035,
             get_ratio = True,
             ratiomin = 0,
             ratiomax = 0.99)


for v in var:
    m = var.index(v)
    combinedPlot("SL_Jets_CA15_{}".format(v),
             [plot( "Matched", "sl_TCA15_matched_{}".format(v), "", "ttH"), 
              plot( "Unmatched ttHbb", "sl_TCA15_unmatched_{}".format(v), "", "ttH"), 
              plot( "Unmatched TTbar", "sl_TCA15_unmatched_{}".format(v), "", "tt")],
             50,limitsinf[m],limits[m], 
             label_x   =   prettyname[m],
             label_y   = "N of events",  
             #axis_unit = "GeV",
             axis_unit = "GeV" if "Mass" in v or v == "pt" else "",
             log_y     = False,
             normalize = True,
             scale = False,
             legend_origin_x = 0.6,
             legend_origin_y = 0.7,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 2,
             legend_text_size = 0.035,
             get_ratio = False,
             ratiomin = 0,
             ratiomax = 0.99) 

    combinedPlot("SL_Jets_AK8_{}".format(v),
             [plot( "Matched", "sl_TAK8_matched_{}".format(v), "", "ttH"), 
              plot( "Unmatched ttHbb", "sl_TAK8_unmatched_{}".format(v), "", "ttH"), 
              plot( "Unmatched TTbar", "sl_TAK8_unmatched_{}".format(v), "", "tt")],
             50,limitsinf[m],limits[m], 
             label_x   =  prettyname[m],
             label_y   = "N of events",  
             #axis_unit = "GeV",
             axis_unit = "GeV" if "Mass" in v or v == "pt" else "",
             log_y     = False,
             normalize = True,
             scale = False,
             legend_origin_x = 0.6,
             legend_origin_y = 0.7,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 2,
             legend_text_size = 0.035,
             get_ratio = False,
             ratiomin = 0,
             ratiomax = 0.99) 

    combinedPlot("SL_Jets_HTT_{}".format(v),
             [plot( "Matched", "sl_THTT_matched_{}".format(v), "", "ttH"), 
              plot( "Unmatched ttHbb", "sl_THTT_unmatched_{}".format(v), "", "ttH"), 
              plot( "Unmatched TTbar", "sl_THTT_unmatched_{}".format(v), "", "tt")],
             50,limitsinf[m],limits[m], 
             label_x   =  prettyname[m],
             label_y   = "N of events",  
             #axis_unit = "GeV",
             axis_unit = "GeV" if "Mass" in v or v == "pt" else "",
             log_y     = False,
             normalize = True,
             scale = False,
             legend_origin_x = 0.6,
             legend_origin_y = 0.7,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 2,
             legend_text_size = 0.035,
             get_ratio = False,
             ratiomin = 0,
             ratiomax = 0.99)

for k in ["CA15", "AK8","HTT"]:
    combinedPlot2D("DRCandidate_GenTop_Pt_{}".format(k),
        [plot( "", "DR_pt_sl_T{}".format(k), "", "ttH")],
        200, 0,1000,100,0,5,
        label_x   = "p_{T} gen Top",
        label_y   = "#Delta R (gen Top, Candidate)",                          
        axis_unit = "GeV",
        log_y     = False,)

 

f1 = ROOT.TFile.Open(full_file_names["ttH"], "READ")
f2 = ROOT.TFile.Open(full_file_names["tt"], "READ")

bkg = {"ttH","TTbar"}
ro = {}
for v in var:
    ro[v] = {}
    for b in bkg:
        ro[v][b] = ROOT.TGraph
        if b == "ttH":
            if "tau" in v:
                ro[v][b] = calc_roc(f1.Get("sl_TCA15_unmatched_{}".format(v)),f1.Get("sl_TCA15_matched_{}".format(v)))
            else:
                ro[v][b] = calc_roc(f1.Get("sl_TCA15_matched_{}".format(v)),f1.Get("sl_TCA15_unmatched_{}".format(v)))
        else:
            if "tau" in v:
                ro[v][b] = calc_roc(f2.Get("sl_TCA15_unmatched_{}".format(v)),f1.Get("sl_TCA15_matched_{}".format(v)))
            else:
                ro[v][b] = calc_roc(f1.Get("sl_TCA15_matched_{}".format(v)),f2.Get("sl_TCA15_unmatched_{}".format(v)))
ro2 = {}
for v in var:
    ro2[v] = {}
    for b in bkg:
        ro2[v][b] = ROOT.TGraph
        if b == "ttH":
            if "tau" in v:
                ro2[v][b] = calc_roc(f1.Get("sl_TAK8_unmatched_{}".format(v)),f1.Get("sl_TAK8_matched_{}".format(v)))
            else:
                ro2[v][b] = calc_roc(f1.Get("sl_TAK8_matched_{}".format(v)),f1.Get("sl_TAK8_unmatched_{}".format(v)))
        else:
            if "tau" in v:
                ro2[v][b] = calc_roc(f2.Get("sl_TAK8_unmatched_{}".format(v)),f1.Get("sl_TAK8_matched_{}".format(v)))
            else:
                ro2[v][b] = calc_roc(f1.Get("sl_TAK8_matched_{}".format(v)),f2.Get("sl_TAK8_unmatched_{}".format(v)))

ro3 = {}
for v in var:
    ro3[v] = {}
    for b in bkg:
        ro3[v][b] = ROOT.TGraph
        if b == "ttH":
            if "tau" in v:
                ro3[v][b] = calc_roc(f1.Get("sl_THTT_unmatched_{}".format(v)),f1.Get("sl_THTT_matched_{}".format(v)))
            else:
                ro3[v][b] = calc_roc(f1.Get("sl_THTT_matched_{}".format(v)),f1.Get("sl_THTT_unmatched_{}".format(v)))
        else:
            if "tau" in v:
                ro3[v][b] = calc_roc(f2.Get("sl_THTT_unmatched_{}".format(v)),f1.Get("sl_THTT_matched_{}".format(v)))
            else:
                ro3[v][b] = calc_roc(f1.Get("sl_THTT_matched_{}".format(v)),f2.Get("sl_THTT_unmatched_{}".format(v)))



results = ROOT.TFile("./SLOptimization_Top_processed.root","recreate")
for v in var:
    for b in bkg:
        ro[v][b].Write("ROC_{}_{}_CA15".format(v,b))
        ro2[v][b].Write("ROC_{}_{}_AK8".format(v,b))
        ro3[v][b].Write("ROC_{}_{}_HTT".format(v,b))


f1.Close()
f2.Close()
results.Close()

full_file_names["SBs"] = "./SLOptimization_Top_processed.root"


doWork(full_file_names, output_dir)


f = ROOT.TFile.Open(full_file_names["SBs"], "READ")
rocs = {}
for v in var:
    rocs[v] = {}
    for b in bkg:
        rocs[v][b] = f.Get("ROC_{}_{}_CA15".format(v,b))
rocs2 = {}
for v in var:
    rocs2[v] = {}
    for b in bkg:
        rocs2[v][b] = f.Get("ROC_{}_{}_AK8".format(v,b))
rocs3 = {}
for v in var:
    rocs3[v] = {}
    for b in bkg:
        rocs3[v][b] = f.Get("ROC_{}_{}_HTT".format(v,b))
f.Close()

mu = ROOT.TMultiGraph()
for k in rocs.keys():
    rocs[k]["ttH"].SetLineColor(li_colors[rocs.keys().index(k)])
    rocs[k]["ttH"].SetLineWidth(2)
    mu.Add(rocs[k]["ttH"])
    rocs[k]["TTbar"].SetLineColor(li_colors[rocs.keys().index(k)])
    rocs[k]["TTbar"].SetLineStyle(7)
    rocs[k]["TTbar"].SetLineWidth(2)
    mu.Add(rocs[k]["TTbar"])
c = ROOT.TCanvas("c","c",600,600)
c.SetLeftMargin(0.16)
mu.Draw("AL")
mu.GetXaxis().SetTitle("#varepsilon_{sig}")
mu.GetYaxis().SetTitle("#varepsilon_{bkg}")
mu.GetXaxis().SetLimits(0,1)
mu.GetYaxis().SetRangeUser(0,1)
legend = ROOT.TLegend(0.2,0.65,0.7,0.85)
for v in var:
    legend.AddEntry(rocs[v]["ttH"],"ttHbb, {}, AOC = {:0.2f}".format(v, 0.5-rocs[v]["ttH"].Integral()),"l")
    legend.AddEntry(rocs[v]["TTbar"],"TTbar, {}, AOC = {:0.2f}".format(v, 0.5-rocs[v]["TTbar"].Integral()),"l")
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.Draw()
line = ROOT.TLine(0,0,1,1)
line.Draw()
#mu.GetYaxis().SetTitleOffset(1)
c.Print("{}pdf/ROCCurve_TopVariables_SL.pdf".format(output_dir))
c.Print("{}png/ROCCurve_TopVariables_SL.png".format(output_dir))
mu.Delete()

mu2 = ROOT.TMultiGraph()
for k in rocs2.keys():
    rocs2[k]["ttH"].SetLineColor(li_colors[rocs2.keys().index(k)])
    rocs2[k]["ttH"].SetLineWidth(2)
    mu2.Add(rocs2[k]["ttH"])
    rocs2[k]["TTbar"].SetLineColor(li_colors[rocs2.keys().index(k)])
    rocs2[k]["TTbar"].SetLineStyle(7)
    rocs2[k]["TTbar"].SetLineWidth(2)
    mu2.Add(rocs2[k]["TTbar"])
c2 = ROOT.TCanvas("c2","c2",600,600)
c2.SetLeftMargin(0.16)
mu2.Draw("AL")
mu2.GetXaxis().SetTitle("#varepsilon_{sig}")
mu2.GetYaxis().SetTitle("#varepsilon_{bkg}")
mu2.GetXaxis().SetLimits(0,1)
mu2.GetYaxis().SetRangeUser(0,1)
legend = ROOT.TLegend(0.2,0.65,0.7,0.85)
for v in var:
    legend.AddEntry(rocs2[v]["ttH"],"ttHbb, {}, AOC = {:0.2f}".format(v, 0.5-rocs2[v]["ttH"].Integral()),"l")
    legend.AddEntry(rocs2[v]["TTbar"],"TTbar, {}, AOC = {:0.2f}".format(v, 0.5-rocs2[v]["TTbar"].Integral()),"l")
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.Draw()
line = ROOT.TLine(0,0,1,1)
line.Draw()
#mu.GetYaxis().SetTitleOffset(1)
c2.Print("{}pdf/ROCCurve_TopVariables_SL_AK8.pdf".format(output_dir))
c2.Print("{}png/ROCCurve_TopVariables_SL_AK8.png".format(output_dir))
mu2.Delete()

mu3 = ROOT.TMultiGraph()
for k in rocs3.keys():
    rocs3[k]["ttH"].SetLineColor(li_colors[rocs3.keys().index(k)])
    rocs3[k]["ttH"].SetLineWidth(2)
    mu3.Add(rocs3[k]["ttH"])
    rocs3[k]["TTbar"].SetLineColor(li_colors[rocs3.keys().index(k)])
    rocs3[k]["TTbar"].SetLineStyle(7)
    rocs3[k]["TTbar"].SetLineWidth(2)
    mu3.Add(rocs3[k]["TTbar"])
c3 = ROOT.TCanvas("c3","c3",600,600)
c3.SetLeftMargin(0.16)
mu3.Draw("AL")
mu3.GetXaxis().SetTitle("#varepsilon_{sig}")
mu3.GetYaxis().SetTitle("#varepsilon_{bkg}")
mu3.GetXaxis().SetLimits(0,1)
mu3.GetYaxis().SetRangeUser(0,1)
legend = ROOT.TLegend(0.2,0.65,0.7,0.85)
for v in var:
    legend.AddEntry(rocs3[v]["ttH"],"ttHbb, {}, AOC = {:0.2f}".format(v, 0.5-rocs3[v]["ttH"].Integral()),"l")
    legend.AddEntry(rocs3[v]["TTbar"],"TTbar, {}, AOC = {:0.2f}".format(v, 0.5-rocs3[v]["TTbar"].Integral()),"l")
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.Draw()
line = ROOT.TLine(0,0,1,1)
line.Draw()
#mu.GetYaxis().SetTitleOffset(1)
c3.Print("{}pdf/ROCCurve_TopVariables_SL_HTT.pdf".format(output_dir))
c3.Print("{}png/ROCCurve_TopVariables_SL_HTT.png".format(output_dir))
mu3.Delete()