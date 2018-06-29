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
import ROOT
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

full_file_names = {}
#full_file_names["ttH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/TaggerCuts/GCa5c93e589b69/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
#full_file_names["tt"]  = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/TaggerCuts/GC0bf2a57c0367/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"
full_file_names["ttH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/TaggerCuts/GC33bbcd5193a5/ttHTobb_afterBDT.root"
full_file_names["tt"]  = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/TaggerCuts/GC04d2c320f0ca/TTToSemiLeptonic_afterBDT.root"


#output_dir = "results/JetCalibrations_Plots/"
output_dir = "results/TaggerCuts_27062018/"

ngen = {}
ngen["ttH"] = 3425244.0
ngen["tt"] = 5811679408.0

xsection = {}
xsection["ttH"] = 0.2934045
xsection["tt"] = 365.45736135

lumis = {} #These will be in fb-1
lumis["ttH"] = ngen["ttH"] / xsection["ttH"] * 0.001
lumis["tt"] = ngen["tt"] / xsection["tt"] * 0.001
print lumis["ttH"], lumis["tt"]
#lumis["ttH"] = 945.6877 #In pb-1 Assuming XS of 0.5071*0.5824 pb and Ngen = 2774696.04521
#lumis["tt"] = 8930.38 #Assuming XS of 365.45736135 pb and Ngen = 31280689575.4 

targetlumi = 49.0

f1 = ROOT.TFile.Open(full_file_names["ttH"], "READ")
f2 = ROOT.TFile.Open(full_file_names["tt"], "READ")


S = {}
SH = {}
ST = {}
Stot = {}
eff = {}
SB = {}
SsB = {}
SsSB = {}
es = {}
eb = {}
D = {}
De = {}
effTH = {}
effH = {}
effT = {}
effH2 = {}
effT2 = {}
for m in ["tth","ttjets"]:
    S[m] = {}
    Stot[m] = {}
    eff[m] = {}
    De[m] = {}
    D[m] = {}
    effH2[m] = {}
    effT2[m] = {}
    ST[m] = {}
    SH[m] = {}
for k in ["sl","dl"]:
    S["tth"][k] = f1.Get("count_{}_S_HT".format(k)) 
    S["tth"][k].Scale(targetlumi/lumis["ttH"])
    SH["tth"][k] = f1.Get("count_{}_S_H".format(k)) 
    SH["tth"][k].Scale(targetlumi/lumis["ttH"])
    ST["tth"][k] = f1.Get("count_{}_S_T".format(k))
    #for i in range(ST["tth"][k].GetNbinsX()):
    #    print ST["tth"][k].GetBinContent(i,1) 
    ST["tth"][k].Scale(targetlumi/lumis["ttH"])
    Stot["tth"][k] = f1.Get("count_{}_Stot_HT".format(k))
    Stot["tth"][k].Scale(targetlumi/lumis["ttH"])
    eff["tth"][k] = f1.Get("count_{}_effHT_HT".format(k))
    eff["tth"][k].Scale(targetlumi/lumis["ttH"])
    effH2["tth"][k] = f1.Get("count_{}_effH_H".format(k))
    effH2["tth"][k].Scale(targetlumi/lumis["ttH"])
    effT2["tth"][k] = f1.Get("count_{}_effT_T".format(k))
    #for i in range(effT2["tth"][k].GetNbinsX()):
    #    print effT2["tth"][k].GetBinContent(i,1) 
    effT2["tth"][k].Scale(targetlumi/lumis["ttH"])
    S["ttjets"][k] = f2.Get("count_{}_S_HT".format(k)) 
    S["ttjets"][k].Scale(targetlumi/lumis["tt"])
    SH["ttjets"][k] = f2.Get("count_{}_S_H".format(k)) 
    SH["ttjets"][k].Scale(targetlumi/lumis["tt"])
    ST["ttjets"][k] = f2.Get("count_{}_S_T".format(k)) 
    ST["ttjets"][k].Scale(targetlumi/lumis["tt"])
    Stot["ttjets"][k] = f2.Get("count_{}_Stot_HT".format(k))
    Stot["ttjets"][k].Scale(targetlumi/lumis["tt"])
    eff["ttjets"][k] = f2.Get("count_{}_effHT_HT".format(k))
    eff["ttjets"][k].Scale(targetlumi/lumis["tt"])
    effH2["ttjets"][k] = f2.Get("count_{}_effH_H".format(k))
    effH2["ttjets"][k].Scale(targetlumi/lumis["tt"])
    effT2["ttjets"][k] = f2.Get("count_{}_effT_T".format(k))
    effT2["ttjets"][k].Scale(targetlumi/lumis["tt"])

for k in ["sl","dl"]:
    SB[k] = S["tth"][k].Clone()
    SsB[k] = S["tth"][k].Clone()
    SsSB[k] = S["tth"][k].Clone()
    SB[k].Divide(S["ttjets"][k])
    De["ttjets"][k] = S["ttjets"][k].Clone()
    for i in range(De["ttjets"][k].GetNbinsX()):
        for j in range(De["ttjets"][k].GetNbinsY()):
            De["ttjets"][k].SetBinContent(i,j,math.sqrt(De["ttjets"][k].GetBinContent(i,j)))
    SsB[k].Divide(De["ttjets"][k])
    D["ttjets"][k] = S["ttjets"][k].Clone()
    D["ttjets"][k].Add(S["tth"][k].Clone())
    for i in range(D["ttjets"][k].GetNbinsX()):
        for j in range(D["ttjets"][k].GetNbinsY()):
            D["ttjets"][k].SetBinContent(i,j,math.sqrt(D["ttjets"][k].GetBinContent(i,j)))
    SsSB[k].Divide(D["ttjets"][k])
    es[k] = S["tth"][k].Clone()
    es[k].Divide(Stot["tth"][k])
    eb[k] = S["ttjets"][k].Clone()
    eb[k].Divide(Stot["ttjets"][k])
    effTH[k] = eff["tth"][k].Clone()
    effTH[k].Divide(S["tth"][k])
    effT[k] = effT2["tth"][k].Clone()
    effT[k].Divide(ST["tth"][k])
    effH[k] = effH2["tth"][k].Clone()
    effH[k].Divide(SH["tth"][k])

    #Also here define how to best select WP and then transfer them to next part of the code - 
    #Means that this code needs to be run twice, but who cares, its fast anyway.


    #Get efficiency and background rejection rate from BDT output score:

    WPH = 0.9
    WPT = 0.47
    efficiencyH = effH["sl"].GetBinContent(effH["sl"].FindBin(0,WPH))
    efficiencyT = effT["sl"].GetBinContent(effT["sl"].FindBin(WPT,0))

    print efficiencyH, efficiencyT
            


results = ROOT.TFile("./TaggerCuts_processed.root","recreate")
for v in ["sl","dl"]:
    S["tth"][v].Write("S_tth_{}".format(v))
    SH["tth"][v].Write("SH_tth_{}".format(v))
    ST["tth"][v].Write("ST_tth_{}".format(v))
    Stot["tth"][v].Write("Stot_tth_{}".format(v)) 
    eff["tth"][v].Write("eff_tth_{}".format(v))
    effH2["tth"][v].Write("effH2_tth_{}".format(v))
    effT2["tth"][v].Write("effT2_tth_{}".format(v))
    eff["tth"][v].Write("eff_tth_{}".format(v))
    S["ttjets"][v].Write("S_ttjets_{}".format(v))
    Stot["ttjets"][v].Write("Stot_ttjets_{}".format(v)) 
    eff["ttjets"][v].Write("eff_ttjets_{}".format(v))
    SB[v].Write("SB_{}".format(v))
    SsB[v].Write("SsB_{}".format(v))
    SsSB[v].Write("SsSB_{}".format(v))
    es[v].Write("es_{}".format(v))
    eb[v].Write("eb_{}".format(v))
    D["ttjets"][v].Write("D_{}".format(v))
    De["ttjets"][v].Write("De_{}".format(v))
    effTH[v].Write("effTH_{}".format(v))
    effT[v].Write("effT_{}".format(v))
    effH[v].Write("effH_{}".format(v))

f1.Close()
f2.Close()
results.Close()





li_colors = [ROOT.kRed,      ROOT.kBlue+1,     ROOT.kBlack, 
         ROOT.kOrange-1, ROOT.kViolet+1,   ROOT.kGreen+1,
         ROOT.kGray,     ROOT.kYellow]*10  

########################################
# Plots
########################################
categories = ["sl","dl"]


full_file_names["SBs"] = "TaggerCuts_processed.root"

f = ROOT.TFile.Open(full_file_names["SBs"], "READ")

for cat in ["sl","dl"]:
    for pl in ["SB","SsB","SsSB","es","eb","effTH"]:
        print "{}_{}".format(pl,cat)
        combinedPlot2D("{}_{}".format(pl,cat),
            [plot( "", "{}_{}".format(pl,cat), "", "SBs")],
            102,0,1.01,102,0,1.01,
            label_x   = "Top BDT discrimator",
            label_y   = "Higgs BDT discrimator",                          
            axis_unit = "GeV",
            log_y     = False,)




doWork(full_file_names, output_dir)
