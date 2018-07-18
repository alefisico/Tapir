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
#######################################

full_file_names = {}

#full_file_names["TTH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/ComputationTime/GC760701b1543d/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["TTH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/ComputationTime/GC7a71f62f1930/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"

########################################
# Create histograms, saved in file
########################################

noperm = ["SL_2w2h2t","SL_1w2h2t","SL_0w2h2t","DL_0w2h2t","SL_2w2h2t_sj","SL_1w2h2t_sj","SL_0w2h2t_sj","DL_0w2h2t_sj"]
perm = ["SL_2w2h2t_sj_perm_top","SL_2w2h2t_sj_perm_higgs","SL_2w2h2t_sj_perm_tophiggs","SL_1w2h2t_sj_perm_higgs","SL_0w2h2t_sj_perm_higgs","DL_0w2h2t_sj_perm_higgs"]

anc = noperm+perm

f1 = ROOT.TFile.Open(full_file_names["TTH"], "READ")
t = {}
ts = {}
tb = {}

for a in anc:
    t["{}".format(a)] = f1.Get("Time_{}".format(a))
    ts["{}".format(a)] = f1.Get("Times_{}".format(a))
    tb["{}".format(a)] = f1.Get("Timeb_{}".format(a))
    print a,  t["{}".format(a)].GetMean(), ts["{}".format(a)].GetMean(), tb["{}".format(a)].GetMean()
    print a,  t["{}".format(a)].GetRMS(), ts["{}".format(a)].GetRMS(), tb["{}".format(a)].GetRMS()