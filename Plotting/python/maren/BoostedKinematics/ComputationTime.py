#!/usr/bin/env python

########################################
# Imports
########################################

import math
import os
import pickle
import socket # to get the hostname

import ROOT

from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf
import TTH.MEAnalysis.nanoTreeClasses as nanoTreeClasses
import TTH.MEAnalysis.nanoTreeGenClasses as nanoTreeGenClasses


from TTH.Plotting.maren.BDTStudies.BasicBoostedFunctions import *
from TTH.MEAnalysis.vhbb_utils import lvec, autolog


########################################
# Define Input Files and
# output directory
########################################


# for the filename: basepath + filename + .root
full_file_names = {}
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v



#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/Jul04_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/Jul04_withME/180704_113841/0000/tree_39.root"
#full_file_names["TT"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_45.root"

########################################
# Create histograms, saved in file
########################################

noperm = ["SL_2w2h2t","SL_1w2h2t","SL_0w2h2t","DL_0w2h2t","SL_2w2h2t_sj","SL_1w2h2t_sj","SL_0w2h2t_sj","DL_0w2h2t_sj"]
perm = ["SL_2w2h2t_sj_perm_top","SL_2w2h2t_sj_perm_higgs","SL_2w2h2t_sj_perm_tophiggs","SL_1w2h2t_sj_perm_higgs","SL_0w2h2t_sj_perm_higgs","DL_0w2h2t_sj_perm_higgs"]

anc = perm+noperm
#anc = noperm


Time = {}
Times = {}
Timeb = {}

for cat in anc:
    Time[cat] = ROOT.TH1F("Time_{}".format(cat),"Time_{}".format(cat),2000,0,200)
    Time[cat].Sumw2()
    Times[cat] = ROOT.TH1F("Times_{}".format(cat),"Times_{}".format(cat),2000,0,200)
    Times[cat].Sumw2()
    Timeb[cat] = ROOT.TH1F("Timeb_{}".format(cat),"Timeb_{}".format(cat),2000,0,200)
    Timeb[cat].Sumw2()


######################################
# Run code
########################################

for l in full_file_names:
    f = ROOT.TFile.Open(full_file_names[l], "READ")
    ttree = f.Get("tree")

    print full_file_names[l]

    sample = ""
    if "ttH" in full_file_names[l]:
        sample = "ttH"
    elif "TT" in full_file_names[l]:
        sample = "ttjets"


    counter  = 0 

    for event in ttree :
        counter += 1

        #if counter > 10000:
        #    break

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.evt

        for a in anc:
            if getattr(event,"mem_{}_p".format(a)) > 0:
                times =  getattr(event,"mem_tth_{}_time".format(a))*0.001
                timeb =  getattr(event,"mem_ttbb_{}_time".format(a))*0.001
                time = times + timeb
                Time[a].Fill(time)
                Times[a].Fill(times)
                Timeb[a].Fill(timeb)


results = ROOT.TFile("out.root","recreate")
for cat in anc:
    Time[cat].Write()
    Times[cat].Write()
    Timeb[cat].Write()