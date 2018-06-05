#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import pickle
import socket # to get the hostname

import ROOT


########################################
# Define Input Files and
# output directory
########################################

full_file_names = {}
full_file_names["tth"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GenParticleStudies/GC6823d901cc8b/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["ttSL"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GenParticleStudies/GCdc91cdd43d31/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8.root"
info = {}
info["tth"] = {}
info["ttSL"] = {}
info["tth"]["NGenEvents"] = 4140048.38588
info["tth"]["Xsection"] = 0.5071 #in pb, From LHCHXSWG, M_H = 125.0 Gev, sqrt(s) = 13 TeV, NLO QCD + NLO EW

info["ttSL"]["NGenEvents"] = 11965092718.8
info["ttSL"]["Xsection"] = 365.45736135 #831.76*2*0.6741*(1.0 - 0.6741) - XsectionTTbar * (proba for 1 hadronic top) * (proba for 1 hadronic top) * 2 (since it can be the other way around)

for l in full_file_names:
    f = ROOT.TFile.Open(full_file_names[l], "READ")
    h = getattr(f, "GenHiggspT")



    Luminosity = info[l]["NGenEvents"]/info[l]["Xsection"]*0.001
    print "Luminosity:", Luminosity

    targetlumi = [40,80,100]


    a = f.Get("GenHiggspT") 
    b = f.Get("GenToppT")
    c = f.Get("GenHiggspTDR")
    c2 = f.Get("GenToppTDR")
    c3 = f.Get("GenToppTDR2")
    d = f.Get("GenHiggsDR") 
    e = f.Get("GenTopHadpT") 
    g = f.Get("GenTopHadHiggs")
    h = f.Get("GenTopHiggs")
    ik = f.Get("GenDRTopHiggs")
    j = f.Get("GenDRTopTop")
    kl = f.Get("GenDRHadTopHiggs")
    z = f.Get("GenWDR")
    mn = f.Get("GenWpTDR")
    no = f.Get("GenWpT")
    op = f.Get("GenHadWDR")
    pq = f.Get("GenHadWpTDR")
    qr = f.Get("GenHadWpT")
    rs = f.Get("GenNumbers")

    print "entries", a.GetEntries()

    h1 = {}
    h2 = {}
    h3 = {}
    h4 = {}

    for lumi in targetlumi:
        h1[targetlumi.index(lumi)] = ROOT.TH1F("GenHiggspT_{}fb".format(lumi),"GenHiggspT_{}fb".format(lumi),200,0,1000)
        h2[targetlumi.index(lumi)] = ROOT.TH1F("GenToppT_{}fb".format(lumi),"GenToppT_{}fb".format(lumi),200,0,1000)
        h3[targetlumi.index(lumi)] = ROOT.TH1F("GenTopHadpT_{}fb".format(lumi),"GenTopHadpT_{}fb".format(lumi),200,0,1000)
        h4[targetlumi.index(lumi)] = ROOT.TH1F("GenNumbers_{}fb".format(lumi),"GenNumbers_{}fb".format(lumi),100,0,100)
        for i in range (0,200):
            h1[targetlumi.index(lumi)].SetBinContent(i,a.GetBinContent(i)*(lumi/Luminosity))
            h2[targetlumi.index(lumi)].SetBinContent(i,b.GetBinContent(i)*(lumi/Luminosity))
            h3[targetlumi.index(lumi)].SetBinContent(i,e.GetBinContent(i)*(lumi/Luminosity))
            h4[targetlumi.index(lumi)].SetBinContent(i,rs.GetBinContent(i)*(lumi/Luminosity))

    for lumi in targetlumi:
        print h1[targetlumi.index(lumi)].Integral()
        print h2[targetlumi.index(lumi)].Integral()
        print h3[targetlumi.index(lumi)].Integral()
        print h4[targetlumi.index(lumi)].Integral()

        print "lumi ", lumi
        if lumi == 40:
            for bi in range(h4[targetlumi.index(lumi)].GetNbinsX()):
                print "numbers", bi, h4[targetlumi.index(lumi)].GetBinContent(bi)

    results = ROOT.TFile("/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GenParticleStudies/May14_{}_processed.root".format(l),"recreate")
    f.GetList().Write() 
    for lumi in targetlumi:
        h1[targetlumi.index(lumi)].Write()
        h2[targetlumi.index(lumi)].Write()
        h3[targetlumi.index(lumi)].Write()
        h4[targetlumi.index(lumi)].Write()
    