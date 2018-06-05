#OK, Assume that I have found the target efficiency I want to find for my Higgs and top tagger. 
#Scan variables to find point with the efficiency I want and choose the one which also has the highest 
#background rejection rate.

#imports
########################################

import os
import pickle
import socket # to get the hostname
import math
import ROOT
from array import array


import TTH.MEAnalysis.nanoTreeClasses as nanoTreeClasses
import TTH.MEAnalysis.nanoTreeGenClasses as nanoTreeGenClasses
from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf


from TTH.Plotting.Helpers.CompareDistributionsPlots import *


########################################
# Define Input Files and
# output directory
########################################

full_file_names = {}
full_file_names["ttH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GetWPandCheck/GC510b027c7af4/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["tt"]  = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GetWPandCheck/GCd502ee15b1f9/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"

filename = "TaggerCuts_processed.root"

fi = ROOT.TFile.Open(filename, "READ")

sb = fi.Get("SB_sl")
ssb = fi.Get("SsB_sl")
effTH = fi.Get("effTH_sl")

sb.Scale(1/sb.GetEntries())
effTH.Scale(1/effTH.GetEntries())
ssb.Scale(1/ssb.GetEntries())

total = ssb.Clone()
total.Multiply(effTH)

total.GetXaxis().SetRangeUser(0.1,0.9)
total.GetYaxis().SetRangeUser(0.1,0.9)

print total.GetMaximum()

MaxBin = total.GetMaximumBin()
x, y, z = ROOT.Long(), ROOT.Long(), ROOT.Long()
total.GetBinXYZ(MaxBin, x, y, z)

print "The bin having the maximum value is",x," ", y
print "That corresponds to an Top efficiency of", float(x)/100
print "and a Higgs efficiency of", float(y)/100

results = ROOT.TFile("./GetWPandCheck2_processed.root","recreate")
total.Write("final")
sb.Write()
ssb.Write()
effTH.Write("efficiency")
results.Close()


full_file_names["SBs"] = "GetWPandCheck2_processed.root"

fil = ROOT.TFile.Open(full_file_names["SBs"], "READ")

combinedPlot2D("Final_discriminator",
    [plot( "", "final", "", "SBs")],
    102,0,1.01,102,0,1.01,
    label_x   = "Top BDT discrimator",
    label_y   = "Higgs BDT discrimator",                          
    axis_unit = "",
    log_y     = False,)

output_dir = "results/TaggerCutsOptimizer_04062018/"

doWork(full_file_names, output_dir)

fil.Close()


targetefficiencyTop = 0.39
targetefficiencyHiggs = 0.29
maxdeviance = 0.02

f1 = ROOT.TFile.Open(full_file_names["ttH"], "READ")
f2 = ROOT.TFile.Open(full_file_names["tt"], "READ")


pasH = {}
totH = {}
pasT = {}
totT = {}
pasH["tth"] = f1.Get("countH_pass") 
totH["tth"] = f1.Get("countH_total") 
pasT["tth"] = f1.Get("countT_pass") 
totT["tth"] = f1.Get("countT_total") 
pasH["ttjets"] = f2.Get("countH_pass") 
totH["ttjets"] = f2.Get("countH_total") 
pasT["ttjets"] = f2.Get("countT_pass") 
totT["ttjets"] = f2.Get("countT_total") 

goodWPH = []
goodWPT = []

#Do Higgs first
for t in range(0,100,5):
    print "t", t
    for bb in range(0,100,5):
        print "bb", bb
        for b in range(0,100,5):
            p = pasH["tth"].Integral(1,t,bb,100,b,100)
            es = p / pasH["tth"].Integral(1,100,1,100,1,100)
            q = totH["ttjets"].Integral(1,t,bb,100,b,100)
            eb = q / totH["ttjets"].Integral(1,100,1,100,1,100)
            if es > targetefficiencyHiggs - maxdeviance and es < targetefficiencyHiggs + maxdeviance:
                goodWPH.append((t,bb,b,es,eb))

goodWPH = sorted(goodWPH, key = lambda x: x[4])
cutnsub = float(goodWPH[0][0])/100
cutbbtag = float(goodWPH[0][1])/100
cutbtag = float(goodWPH[0][2])/100


print goodWPH

print "Optimization gave the following optimal working point for Higgs tagging:"
print "tau21SD < ", cutnsub
print "bbtag > ", cutbbtag
print "btagSL > ", cutbtag
print "Efficiency: " , goodWPH[0][3]
print "Background rejection rate: ", 1-goodWPH[0][4]

#And now for top
for m1 in range(0,100,5):
    print "m1", m1
    for m2 in range(m1,100,5):
        print "m2", m2
        for t in range(0,100,5):
            print "t", t
            for f in range(0,100,5):
                p = pasT["tth"].Integral(m1,m2,1,t,1,f)
                es = p / pasT["tth"].Integral(1,100,1,100,1,100)
                q = totT["ttjets"].Integral(m1,m2,1,t,1,f)
                eb = q / totT["ttjets"].Integral(1,100,1,100,1,100)
                if es > targetefficiencyTop - maxdeviance and es < targetefficiencyTop + maxdeviance:
                    goodWPT.append((m1,m2,t,f,es,eb))

goodWPT = sorted(goodWPT, key = lambda x: x[5])
cutmassinf = goodWPT[0][0]*4
cutmasssup = goodWPT[0][1]*4
cutnsub = float(goodWPT[0][2])/100
cutfrec = float(goodWPT[0][3])/100


print goodWPH

print "Optimization gave the following optimal working point for Top tagging:"
print "mass > ", cutmassinf, "<", cutmasssup
print "tau32SD < ", cutnsub
print "fRec < ", cutfrec
print "Efficiency: " , goodWPT[0][4]
print "Background rejection rate: ", 1-goodWPT[0][5]

f1.Close()
f2.Close()
