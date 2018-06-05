#imports
########################################

import os
import pickle
import socket # to get the hostname
import math
import ROOT
import numpy as np
from array import array

########################################
# Define Input Files and
# output directory
########################################

def calc_roc(h1, h2, rebin=1):
    h1 = h1.Clone()
    h2 = h2.Clone()
    h1.Rebin(rebin)
    h2.Rebin(rebin)

    #if h1.Integral()>0:
    #    h1.Scale(1.0 / h1.Integral())
    #if h2.Integral()>0:
    #    h2.Scale(1.0 / h2.Integral())
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

full_file_names = {}
full_file_names["r"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/DL_Selection/GCf736058bdf91/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root"

samples = ["SL","DL"]
npassing = ["0","1","2"]

h1 = {}
h2 = {}
h3 = {}
h4 = {}
h5 = {}


for l in full_file_names: 

    f = ROOT.TFile.Open(full_file_names[l], "READ")

    for p in samples:
        a = f.Get("GenHiggsCndHiggsDR_{0}".format(p)) 
        b = f.Get("Total_{0}".format(p)) 
        c = f.Get("TotalSubjetsMatching_{0}".format(p)) 
        d = f.Get("TotalQuarksMatching_{0}".format(p))

        h1[p] = {}
        h2[p] = {}
        h3[p] = {}
        h4[p] = {}
        h5[p] = {}

        for r in npassing:
            e = f.Get("HiggsCandMatch_{0}_{1}".format(p,r)) 
            g = f.Get("HiggsResMatch_{0}_{1}".format(p,r)) 
            h = f.Get("HiggsResBtagMatch_{0}_{1}".format(p,r)) 
            j = f.Get("HiggsSubjetsMatching_{0}_{1}".format(p,r)) 
            k = f.Get("HiggsQuarksMatching_{0}_{1}".format(p,r))

            h1[p][r] = ROOT.TH1F("HiggsCandMatch_{}_{}".format(r,p),"HiggsCandMatch_{}_{}".format(r,p),60,0,600)
            h2[p][r] = ROOT.TH1F("HiggsResMatch_{}_{}".format(r,p),"HiggsResMatch_{}_{}".format(r,p),60,0,600)
            h3[p][r] = ROOT.TH1F("HiggsResBtagMatch_{}_{}".format(r,p),"HiggsResBtagMatch_{}_{}".format(r,p),60,0,600)
            h4[p][r] = ROOT.TH1F("HiggsSubjetsMatching_{}_{}".format(r,p),"HiggsSubjetsMatching_{}_{}".format(r,p),60,0,5)
            h5[p][r] = ROOT.TH1F("HiggsQuarksMatching_{}_{}".format(r,p),"HiggsQuarksMatching_{}_{}".format(r,p),60,0,5)
            h1[p][r].Divide(e,b)
            h2[p][r].Divide(g,b)
            h3[p][r].Divide(h,b)
            h4[p][r].Divide(j,c)
            h5[p][r].Divide(k,d)

    var = ["Mass","Nsub","Bbtag","Pt","Eta","NSubjets","BtagF","BtagS","SBSF"]

    ro = {}
    for s in samples:
        ro[s] = {}
        for p in var:
            ro[s][p] = ROOT.TGraph
            ro[s][p] = calc_roc(f.Get("Higgs{}_{}".format(p,s)),f.Get("Higgs{}2_{}".format(p,s)))
            if p == "Nsub":
                ro[s][p] = calc_roc(f.Get("Higgs{}2_{}".format(p,s)),f.Get("Higgs{}_{}".format(p,s)))
            
        results = ROOT.TFile("/mnt/t3nfs01/data01/shome/mameinha/tth/gc/HiggsStudiesDL/Nov16_processed_ptcut.root","recreate")
        f.GetList().Write() 

for p in samples:
    for r in npassing:
        h1[p][r].Write()
        h2[p][r].Write()
        h3[p][r].Write()
        h4[p][r].Write()
        h5[p][r].Write()

    for v in var:
        ro[p][v].Write("ROC_{}_{}".format(v,p))






