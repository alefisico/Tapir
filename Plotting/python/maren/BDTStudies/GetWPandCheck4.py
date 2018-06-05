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

########################################
# Define helper functions
########################################


                                         
# for the filename: basepath + filename + .root
full_file_names = {}


full_file_names["ttH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GetWPandCheck3/GC79477ba7e7a5/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["tt"]  = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GetWPandCheck3/GC79477ba7e7a5/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"
#full_file_names = ""

#output_dir = "results/JetCalibrations_Plots/"
output_dir = "results/TaggerCutsTesting_04062018/"

lumis = {}
lumis["ttH"] = 945.6877 #In pb-1 Assuming XS of 0.5071*0.5824 pb and Ngen = 2774696.04521
lumis["tt"] = 8930.38 #Assuming XS of 365.45736135 pb and Ngen = 31280689575.4 

targetlumi = 49.0

f1 = ROOT.TFile.Open(full_file_names["ttH"], "READ")
f2 = ROOT.TFile.Open(full_file_names["tt"], "READ")



cats = ["sl","dl"]
cases = ["H","T","HT"]

for cat in cats:
    print "{} category:".format(cat)
    H = f1.Get("numbers_{}_H".format(cat)) 
    T = f1.Get("numbers_{}_T".format(cat)) 
    HT = f1.Get("numbers_{}_HT".format(cat)) 
    HB = f2.Get("numbers_{}_H".format(cat)) 
    TB = f2.Get("numbers_{}_T".format(cat)) 
    HTB = f2.Get("numbers_{}_HT".format(cat)) 
    SB = H.GetBinContent(3)/HB.GetBinContent(3)
    SsB = H.GetBinContent(3)/math.sqrt(HB.GetBinContent(3))
    SsSB = H.GetBinContent(3)/math.sqrt(HB.GetBinContent(3)+H.GetBinContent(3))
    eS = H.GetBinContent(3)/H.GetBinContent(2)
    eB = HB.GetBinContent(3)/HB.GetBinContent(2)
    eH = H.GetBinContent(4)/H.GetBinContent(3)
    eHB = HB.GetBinContent(4)/HB.GetBinContent(3)
    print "Higgs only:"
    print "S/B:", SB
    print "S/sqrt(B):", SsB
    print "S/sqrt(S+B):", SsSB
    print "e_Signal", eS
    print "e_Bkg", eB
    print "e_Higgs,S", eH
    print "e_Higgs,B", eHB
    if cat == "sl":
        SB2 = T.GetBinContent(3)/TB.GetBinContent(3)
        print T.GetBinContent(3), TB.GetBinContent(3), H.GetBinContent(3), HB.GetBinContent(3)
        SsB2 = T.GetBinContent(3)/math.sqrt(TB.GetBinContent(3))
        SsSB2 = T.GetBinContent(3)/math.sqrt(TB.GetBinContent(3)+T.GetBinContent(3))
        eS2 = T.GetBinContent(3)/T.GetBinContent(2)
        eB2 = TB.GetBinContent(3)/TB.GetBinContent(2)
        eT2 = T.GetBinContent(4)/T.GetBinContent(3)
        eTB2 = TB.GetBinContent(4)/TB.GetBinContent(3)
        print "Top only:"
        print "S/B:", SB2
        print "S/sqrt(B):", SsB2
        print "S/sqrt(S+B):", SsSB2
        print "e_Signal", eS2
        print "e_Bkg", eB2
        print "e_Top,S", eT2
        print "e_Top,B", eTB2
        SB3 = HT.GetBinContent(3)/HTB.GetBinContent(3)
        SsB3 = HT.GetBinContent(3)/math.sqrt(HTB.GetBinContent(3))
        SsSB3 = HT.GetBinContent(3)/math.sqrt(HTB.GetBinContent(3)+HT.GetBinContent(3))
        eS3 = HT.GetBinContent(3)/HT.GetBinContent(2)
        eB3 = HTB.GetBinContent(3)/HTB.GetBinContent(2)
        eT3 = HT.GetBinContent(4)/HT.GetBinContent(3)
        eTB3 = HTB.GetBinContent(4)/HTB.GetBinContent(3)
        print "Top and Higgs:"
        print "S/B:", SB3
        print "S/sqrt(B):", SsB3
        print "S/sqrt(S+B):", SsSB3
        print "e_Signal", eS3
        print "e_Bkg", eB3
        print "e_Top,Higgs,S", eT3
        print "e_Top,Higgs,B", eTB3