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
full_file_names["tth"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GenMatchJetStudies/GCcfdd14eb93ab/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["ttSL"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GenMatchJetStudies/GCcfdd14eb93ab/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8.root"
info = {}
info["tth"] = {}
info["ttSL"] = {}
info["tth"]["NGenEvents"] = 4140048.38588
info["tth"]["Xsection"] = 0.5071 #in pb, From LHCHXSWG, M_H = 125.0 Gev, sqrt(s) = 13 TeV, NLO QCD + NLO EW

info["ttSL"]["NGenEvents"] = 11965092718.8
info["ttSL"]["Xsection"] = 365.45736135 #831.76*2*0.6741*(1.0 - 0.6741) - XsectionTTbar * (proba for 1 hadronic top) * (proba for 1 hadronic top) * 2 (since it can be the other way around)

for jettype in ["CA15","AK8","HTT"]:
    print "Jet type:", jettype
    for l in full_file_names:
        f = ROOT.TFile.Open(full_file_names[l], "READ")
        h = getattr(f, "{}GenHiggspT".format(jettype))



        Luminosity = info[l]["NGenEvents"]/info[l]["Xsection"]*0.001
        print "Luminosity:", Luminosity

        targetlumi = [40,80,100]


        a = f.Get("{}GenHiggspT".format(jettype)) 
        b = f.Get("{}GenToppT".format(jettype))
        c = f.Get("{}GenHiggspTDR".format(jettype))
        c2 = f.Get("{}GenToppTDR".format(jettype))
        c3 = f.Get("{}GenToppTDR2".format(jettype))
        d = f.Get("{}GenHiggsDR".format(jettype)) 
        e = f.Get("{}GenTopHadpT".format(jettype)) 
        g = f.Get("{}GenTopHadHiggs".format(jettype))
        h = f.Get("{}GenTopHiggs".format(jettype))
        ik = f.Get("{}GenDRTopHiggs".format(jettype))
        j = f.Get("{}GenDRTopTop".format(jettype))
        kl = f.Get("{}GenDRHadTopHiggs".format(jettype))
        z = f.Get("{}GenWDR".format(jettype))
        mn = f.Get("{}GenWpTDR".format(jettype))
        no = f.Get("{}GenWpT".format(jettype))
        op = f.Get("{}GenHadWDR".format(jettype))
        pq = f.Get("{}GenHadWpTDR".format(jettype))
        qr = f.Get("{}GenHadWpT".format(jettype))
        rs = f.Get("{}GenNumbers".format(jettype))

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

        results = ROOT.TFile("/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GenMatchJetStudies/May14_{}_{}_processed.root".format(l,jettype),"recreate")
        f.GetList().Write() 
        for lumi in targetlumi:
            h1[targetlumi.index(lumi)].Write()
            h2[targetlumi.index(lumi)].Write()
            h3[targetlumi.index(lumi)].Write()
            h4[targetlumi.index(lumi)].Write()
    