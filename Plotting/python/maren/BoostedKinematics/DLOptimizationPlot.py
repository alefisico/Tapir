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
full_file_names["ttH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/DLOptimization/GC856cf8aae257/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root"
full_file_names["tt"]  = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/DLOptimization/GC856cf8aae257/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root"
#full_file_names = ""

#output_dir = "results/JetCalibrations_Plots/"
output_dir = "results/DLOptimization_13032018/"

lumis = {}
lumis["ttH"] = 4982.71007 #In pb-1 Assuming XS of 0.5071*0.5824 pb and Ngen = 1461927.13478 
lumis["tt"] = 36.538208 #Assuming XS of 831.76 pb and Ngen = 30391020.0 

targetlumi = 40.0

li_colors = [ROOT.kRed,      ROOT.kBlue+1,     ROOT.kBlack, 
         ROOT.kOrange-1, ROOT.kViolet+1,   ROOT.kGreen+1,
         ROOT.kGray,     ROOT.kYellow]*10  

########################################
# Plots
########################################
categories = ["DL"]

var = ["pt","btag1","btag2","bbtag","mass","softdropmass","tau21"]
limits = [600,1,1,1,600,600,1]
limitsinf = [0,0,0,-1,0,0,0]
fatjets = ["Higgs","HiggsAK8","Top"]
prettyname = ["p_{T}","btagL","btagS","bbtag","mass","mass_{SD}","#tau_{21}"]

#Number of fatjets - cuts on pt and eta of fatjet
combinedPlot("DL_Nfatjets",
             [plot( "CA15 SD - ttHbb", "Nfatjets_dl_HCA15", "", "ttH"), 
              plot( "AK8 SD - ttHbb", "Nfatjets_dl_HAK8", "", "ttH"),
              plot( "CA15 SD - TTbar", "Nfatjets_dl_HCA15", "", "tt"), 
              plot( "AK8 SD - TTbar", "Nfatjets_dl_HAK8", "", "tt")],
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
combinedPlot("DL_Matchedfatjets",
             [plot( "Gen Higgs", "Count_dl", "", "ttH"), 
              plot( "Match to CA15 SD", "MatchedFatjet_dl_HCA15", "", "ttH"), 
              plot( "Match to AK8 SD", "MatchedFatjet_dl_HAK8", "", "ttH")],
             50,0,600, 
             label_x   =  "Gen Higgs p_{T}",
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
    combinedPlot("DL_Jets_CA15_{}".format(v),
             [plot( "Matched", "dl_HCA15_matched_{}".format(v), "", "ttH"), 
              plot( "Unmatched ttHbb", "dl_HCA15_unmatched_{}".format(v), "", "ttH"), 
              plot( "Unmatched TTbar", "dl_HCA15_unmatched_{}".format(v), "", "tt")],
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

    combinedPlot("DL_Jets_AK8_{}".format(v),
             [plot( "Matched", "dl_HAK8_matched_{}".format(v), "", "ttH"), 
              plot( "Unmatched ttHbb", "dl_HAK8_unmatched_{}".format(v), "", "ttH"), 
              plot( "Unmatched TTbar", "dl_HAK8_unmatched_{}".format(v), "", "tt")],
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

for k in ["CA15", "AK8"]:
    combinedPlot2D("DRCandidate_GenHiggs_Pt_{}".format(k),
        [plot( "", "DR_pt_dl_H{}".format(k), "", "ttH")],
        200, 0,1000,100,0,5,
        label_x   = "p_{T} gen Higgs",
        label_y   = "#Delta R (gen Higgs, Candidate)",                          
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
                ro[v][b] = calc_roc(f1.Get("dl_HCA15_unmatched_{}".format(v)),f1.Get("dl_HCA15_matched_{}".format(v)))
            else:
                ro[v][b] = calc_roc(f1.Get("dl_HCA15_matched_{}".format(v)),f1.Get("dl_HCA15_unmatched_{}".format(v)))
        else:
            if "tau" in v:
                ro[v][b] = calc_roc(f2.Get("dl_HCA15_unmatched_{}".format(v)),f1.Get("dl_HCA15_matched_{}".format(v)))
            else:
                ro[v][b] = calc_roc(f1.Get("dl_HCA15_matched_{}".format(v)),f2.Get("dl_HCA15_unmatched_{}".format(v)))
ro2 = {}
for v in var:
    ro2[v] = {}
    for b in bkg:
        ro2[v][b] = ROOT.TGraph
        if b == "ttH":
            if "tau" in v:
                ro2[v][b] = calc_roc(f1.Get("dl_HAK8_unmatched_{}".format(v)),f1.Get("dl_HAK8_matched_{}".format(v)))
            else:
                ro2[v][b] = calc_roc(f1.Get("dl_HAK8_matched_{}".format(v)),f1.Get("dl_HAK8_unmatched_{}".format(v)))
        else:
            if "tau" in v:
                ro2[v][b] = calc_roc(f2.Get("dl_HAK8_unmatched_{}".format(v)),f1.Get("dl_HAK8_matched_{}".format(v)))
            else:
                ro2[v][b] = calc_roc(f1.Get("dl_HAK8_matched_{}".format(v)),f2.Get("dl_HAK8_unmatched_{}".format(v)))


S = {}
B1 = {}
B2 = {}
SB1 = {}
SB2 = {}
N = {}
M = {}
D = {}
De = {}
for k in ["CA15","AK8"]:
    S[k] = {}
    B1[k] = {}
    B2[k] = {}
    SB1[k] = {}
    SB2[k] = {}
    De[k] = {}
for v in ["btag1","btag2","bbtag"]:

    S["CA15"][v] = f1.Get("dl_HCA15_S1_{}".format(v)) 
    S["CA15"][v].Scale(targetlumi/lumis["ttH"])
    B1["CA15"][v] = f1.Get("dl_HCA15_S2_{}".format(v))
    B1["CA15"][v].Scale(targetlumi/lumis["ttH"])
    B2["CA15"][v] = f2.Get("dl_HCA15_B_{}".format(v))
    B2["CA15"][v].Scale(targetlumi/lumis["tt"])
    S["AK8"][v] = f1.Get("dl_HAK8_S1_{}".format(v))
    S["AK8"][v].Scale(targetlumi/lumis["ttH"])
    B1["AK8"][v] = f1.Get("dl_HAK8_S2_{}".format(v))
    B1["AK8"][v].Scale(targetlumi/lumis["ttH"])
    B2["AK8"][v] = f2.Get("dl_HAK8_B_{}".format(v))
    B2["AK8"][v].Scale(targetlumi/lumis["tt"])

for k in ["CA15","AK8"]:
    N[k] = S[k]["bbtag"].Clone()
    N[k].Add(B1[k]["bbtag"])
    M[k] = {}
    D[k] = {}
    for v in ["btag1","btag2","bbtag"]:
        M[k][v] = S[k][v].Clone()
        D[k][v] = S[k][v].Clone()
        D[k][v].Add(B1[k][v])
        M[k][v].Divide(D[k][v])

        SB1[k][v] = S[k][v].Clone()
        SB2[k][v] = S[k][v].Clone()
        SB1[k][v].Add(B1[k][v].Clone())
        SB2[k][v].Add(B1[k][v].Clone())
        SB1[k][v].Divide(B2[k][v])
        De[k][v] = B2[k][v].Clone()
        for i in range(De[k][v].GetNbinsX()):
            De[k][v].SetBinContent(i,math.sqrt(De[k][v].GetBinContent(i)))
        SB2[k][v].Divide(De[k][v])



results = ROOT.TFile("./DLOptimization_processed.root","recreate")
N["CA15"].Write("N_CA15")
N["AK8"].Write("N_AK8")
for v in var:
    for b in bkg:
        ro[v][b].Write("ROC_{}_{}_CA15".format(v,b))
        ro2[v][b].Write("ROC_{}_{}_AK8".format(v,b))
for k in ["CA15","AK8"]:
    for v in ["btag1","btag2","bbtag"]:
        S[k][v].Write("S_{}_{}".format(k,v))
        B1[k][v].Write("B1_{}_{}".format(k,v)) 
        B2[k][v].Write("B2_{}_{}".format(k,v))
        SB1[k][v].Write("SB1_{}_{}".format(k,v))
        SB2[k][v].Write("SB2_{}_{}".format(k,v))
        M[k][v].Write("Match_{}_{}".format(k,v))
        D[k][v].Write("Divisor_{}_{}".format(k,v))

f1.Close()
f2.Close()
results.Close()

full_file_names["SBs"] = "./DLOptimization_processed.root"


for k in ["CA15","AK8"]:
    combinedPlot("DL_Match_{}".format(k),
             [plot( "bbtag", "Match_{}_bbtag".format(k), "", "SBs"), 
              plot( "btag L", "Match_{}_btag1".format(k), "", "SBs"),
              plot( "btag SL", "Match_{}_btag2".format(k), "", "SBs")],
             30,0,16, 
             label_x   = "Cut",
             label_y   = "% Matched",  
             #axis_unit = "GeV",
             axis_unit = "",
             log_y     = False,
             normalize = False,
             scale = False,
             legend_origin_x = 0.6,
             legend_origin_y = 0.7,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 2,
             legend_text_size = 0.035,
             get_ratio = False,
             ratiomin = 0,
             ratiomax = 0.99)

    combinedPlot("DL_SB_{}".format(k),
         [plot( "bbtag", "SB1_{}_bbtag".format(k), "", "SBs"), 
         plot( "btag1", "SB1_{}_btag1".format(k), "", "SBs"),
         plot( "btag2", "SB1_{}_btag2".format(k), "", "SBs")],
         32,0,32, 
         label_x   = "Cut",
         label_y   = "S/B",  
         #axis_unit = "GeV",
         axis_unit = "",
         log_y     = False,
         normalize = False,
         scale = False,
         legend_origin_x = 0.6,
         legend_origin_y = 0.7,
         legend_size_x   = 0.25,
         legend_size_y   = 0.05 * 2,
         legend_text_size = 0.035,
         get_ratio = False,
         ratiomin = 0,
         ratiomax = 0.99)  

    combinedPlot("DL_SsB_{}".format(k),
         [plot( "bbtag", "SB2_{}_bbtag".format(k), "", "SBs"), 
         plot( "btag1", "SB2_{}_btag1".format(k), "", "SBs"),
         plot( "btag2", "SB2_{}_btag2".format(k), "", "SBs")],
         32,0,32, 
         label_x   = "Cut",
         label_y   = "S/#sqrt{B}",  
         #axis_unit = "GeV",
         axis_unit = "",
         log_y     = False,
         normalize = False,
         scale = False,
         legend_origin_x = 0.6,
         legend_origin_y = 0.7,
         legend_size_x   = 0.25,
         legend_size_y   = 0.05 * 2,
         legend_text_size = 0.035,
         get_ratio = False,
         ratiomin = 0,
         ratiomax = 0.99)  

combinedPlot("N_EventsWithFJ",
             [plot( "CA15", "N_CA15", "", "SBs"), 
              plot( "AK8", "N_AK8", "", "SBs")],
             30,0,16, 
             label_x   = "Cut",
             label_y   = "# Events",  
             #axis_unit = "GeV",
             axis_unit = "",
             log_y     = False,
             normalize = False,
             scale = False,
             legend_origin_x = 0.6,
             legend_origin_y = 0.7,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 2,
             legend_text_size = 0.035,
             get_ratio = False,
             ratiomin = 0,
             ratiomax = 0.99) 

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
c.Print("{}pdf/ROCCurve_HiggsVariables_DL.pdf".format(output_dir))
c.Print("{}png/ROCCurve_HiggsVariables_DL.png".format(output_dir))
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
c2.Print("{}pdf/ROCCurve_HiggsVariables_DL_AK8.pdf".format(output_dir))
c2.Print("{}png/ROCCurve_HiggsVariables_DL_AK8.png".format(output_dir))
mu2.Delete()