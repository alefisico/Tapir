#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import pickle
import socket # to get the hostname
import math
import ROOT
import array
import numpy as np

from TTH.Plotting.Helpers.CompareDistributionsPlots import *


########################################
# Define Input Files and
# output directory
########################################

ROOT.gStyle.SetLegendBorderSize(0)

names = ["TTH","TTSL","TTDL"]
full_file_names = {}
#full_file_names["data"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/Distributions_TopSubjetsUncertainties/SingleMuon_May10/SingleMuon.root"
full_file_names["TTH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/KinematicsSubjets/GC9bd64777c67c/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"


output_dir = "../results/KinematicsSubjets_21062018/"

cat = ["sl","dl"]
var = ["pt","eta","phi","mass"]
prettynames = ["p_{T}-p_{T,gen Quark}","#eta-#eta_{T,gen Quark}","#phi-#phi_{T,gen Quark}","mass"]
liminf = [-100,-1,-1,0]
limsup = [100,1,1,100]

########################################
# Create histograms, saved in file
########################################

for a in cat:
    for v in var:
        m = var.index(v)
        combinedPlot("AK8_Higgs_bsubjet_{}_{}".format(a,v),
                     [plot( "Resolved jet", "count_AK8_{}_hb_jet_{}".format(a,v), "", "TTH",color="kRed"),
                      plot( "Subjet", "count_AK8_{}_hb_subjet_{}".format(a,v), "", "TTH",color="kBlack")],
                     50,liminf[m],limsup[m], 
                     label_x   =  prettynames[m],
                     label_y   = "Fraction of events",  
                     axis_unit = "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = True,
                     legend_origin_x = 0.65,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 3,
                     legend_text_size = 0.035,
                     get_ratio = False)
"""
for v in var:
    m = var.index(v)
    combinedPlot("Top_bsubjet_{}".format(v),
                 [plot( "Resolved jet", "count_sl_tb_jet_{}".format(v), "", "TTH",color="kRed"),
                  plot( "Subjet", "count_sl_tb_subjet_{}".format(v), "", "TTH",color="kBlack")],
                 50,liminf[m],limsup[m], 
                 label_x   =  prettynames[m],
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.65,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = False)

    combinedPlot("Top_lsubjet_{}".format(v),
                 [plot( "Resolved jet", "count_sl_tl_jet_{}".format(v), "", "TTH",color="kRed"),
                  plot( "Subjet", "count_sl_tl_subjet_{}".format(v), "", "TTH",color="kBlack")],
                 50,liminf[m],limsup[m], 
                 label_x   =  prettynames[m],
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.65,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = False)
"""

doWork(full_file_names, output_dir)