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

from TTH.Plotting.maren.BDTStudies.BasicBoostedFunctions import *


########################################
# Define Input Files and
# output directory
########################################

                                         
full_file_names = {}

outfile = "Train"

full_file_names["H_sig"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/TrainingSample/Train/tth.root"
full_file_names["H_bkg"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/TrainingSample/Train/ttjets.root"
full_file_names["T_sig"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/TrainingSampleTop/Train/tth.root"
full_file_names["T_bkg"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/TrainingSampleTop/Train/ttjets.root"

nevents = {}
nevents["H_sig"] = 765277/2
nevents["H_bkg"] = 8460240767/2
nevents["T_sig"] = 765277/2
nevents["T_bkg"] = 8460240767/2

crosssection = {}
crosssection["H_sig"] = 0.2934045
crosssection["H_bkg"] = 365.45736135
crosssection["T_sig"] = 0.2934045
crosssection["T_bkg"] = 365.45736135

lumi = {}
lumi["H_sig"] = nevents["H_sig"]/crosssection["H_sig"]
lumi["H_bkg"] = nevents["H_bkg"]/crosssection["H_bkg"]
lumi["T_sig"] = nevents["T_sig"]/crosssection["T_sig"]
lumi["T_bkg"] = nevents["T_bkg"]/crosssection["T_bkg"]

factorH = lumi["H_sig"]/lumi["H_bkg"]
factorT = lumi["T_sig"]/lumi["T_bkg"]


#factorH = 1
#factorT = 1
#Let's use the full ttH sample, and compute the number of bkg events to get from the background sample



#Higgs first
f = ROOT.TFile.Open(full_file_names["H_sig"], "READ")
ttree = f.Get("t2")
nentries = ttree.GetEntries()
f2 = ROOT.TFile.Open(full_file_names["H_bkg"], "READ")
ttree2 = f2.Get("t2")
nentries2 = ttree2.GetEntries()
maxH = ttree2.GetEntries() * factorH

#Create a new file + a clone of old tree in new file
out = ROOT.TFile("Higgs_BDT_{}.root".format(outfile),"recreate")
newtree = ttree.CloneTree(0)
counter = 0
for event in ttree :
    #print match, event.fromtop
    newtree.Fill()
    counter += 1

f.Close()

newtree2 = ttree2.CloneTree(0)
counter2 = 0
for event2 in ttree2:
    if counter2 > maxH:
        break
    newtree2.Fill()
    counter2 += 1

    #event->Clear();
lis = ROOT.TList()
lis.Add(newtree)
lis.Add(newtree2)
nt = ROOT.TTree.MergeTrees(lis)
nt.SetName("t2")
print newtree.GetEntries()
newtree.Print()

nt.AutoSave()
f2.Close()
out.Close()


#And now top
f3 = ROOT.TFile.Open(full_file_names["T_sig"], "READ")
ttree3 = f3.Get("t2")
nentries3 = ttree3.GetEntries()
f4 = ROOT.TFile.Open(full_file_names["T_bkg"], "READ")
ttree4 = f4.Get("t2")
nentries4 = ttree4.GetEntries()
maxT = ttree4.GetEntries() * factorT



#Create a new file + a clone of old tree in new file
out2 = ROOT.TFile("Top_BDT_{}.root".format(outfile),"recreate")
newtree3 = ttree3.CloneTree(0)
counter3 = 0
for event3 in ttree3:
    #if event3.fromtop == 1:
    newtree3.Fill()
    counter3 += 1


print ttree4.GetEntries()
newtree4 = ttree4.CloneTree(0)
counter4 = 0
for event4 in ttree4:
    #if counter4 > maxT:
    #    break
    counter4 += 1
    #if event4.fromtop == 0:
    newtree4.Fill()

    #event->Clear();
print newtree3.GetEntries()
lis2 = ROOT.TList()
#lis2.Add(newtree3)
lis2.Add(newtree4)
nt2 = ROOT.TTree.MergeTrees(lis2)
nt2.SetName("t2")
nt2.Print()
nt2.AutoSave()
f3.Close()
f4.Close()
out2.Close()