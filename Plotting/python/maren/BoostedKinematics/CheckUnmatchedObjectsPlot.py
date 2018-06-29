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


full_file_names = {}
#full_file_names["data"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/Distributions_TopSubjetsUncertainties/SingleMuon_May10/SingleMuon.root"
full_file_names["TTH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/CheckUnmatchedObjects/GC90f130c71dfd/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"


output_dir = "../results/CheckUnmatchedObjects_11062018/"

########################################
# Create histograms, saved in file
########################################


combinedPlot("Distances_Higgs_SL",
             [plot( "#Delta R(cand_{H},gen_{H})", "DistancesHiggs_sl_higgs", "", "TTH",color="kRed"),
              plot( "#Delta R(cand_{H},gen_{had T})", "DistancesHiggs_sl_top", "", "TTH",color="kBlack"),
              plot( "#Delta R(cand_{H},gen_{lep T})", "DistancesHiggs_sl_topl", "", "TTH",color="kBlack",linestyle = 7),],
             50,0,5, 
             label_x   =  "#Delta R",
             label_y   = "Fraction of events",  
             axis_unit = "",
             #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.45,
             legend_origin_y = 0.6,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 3,
             legend_text_size = 0.035,
             get_ratio = False)

combinedPlot("Distances_Higgs_DL",
             [plot( "#Delta R(cand_{H},gen_{H})", "DistancesHiggs_dl_higgs", "", "TTH",color="kRed"),
              plot( "#Delta R(cand_{H},gen_{had T})", "DistancesHiggs_dl_top", "", "TTH",color="kBlack"),
              plot( "#Delta R(cand_{H},gen_{lep T})", "DistancesHiggs_dl_topl", "", "TTH",color="kBlack",linestyle = 7),],
             50,0,5, 
             label_x   =  "#Delta R",
             label_y   = "Fraction of events",  
             axis_unit = "",
             #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.45,
             legend_origin_y = 0.6,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 3,
             legend_text_size = 0.035,
             get_ratio = False)

combinedPlot("Distances_Top",
             [plot( "#Delta R(cand_{T},gen_{had T})", "DistancesTop_sl_top", "", "TTH",color="kBlack"),
             plot( "#Delta R(cand_{T},gen_{lep T})", "DistancesTop_sl_topl", "", "TTH",color="kBlack",linestyle = 7),
              plot( "#Delta R(cand_{T},gen_{H})", "DistancesTop_sl_higgs", "", "TTH",color="kRed"),],
             50,0,5, 
             label_x   =  "#Delta R",
             label_y   = "Fraction of events",  
             axis_unit = "",
             #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.45,
             legend_origin_y = 0.6,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 3,
             legend_text_size = 0.035,
             get_ratio = False)

combinedPlot("Distances_TopHiggs",
             [plot( "#Delta R(c_{T},g_{h T}) - #Delta R(c_{T},g_{H}) - SL", "Distances_sl_top", "", "TTH",color="kRed"),
              plot( "#Delta R(c_{H},g_{H}) - #Delta R(c_{H},g_{h T}) - SL", "Distances_sl_higgs", "", "TTH",color="kRed",linestyle = 7),
              plot( "#Delta R(c_{H},g_{H}) - #Delta R(c_{H},g_{h T}) - DL", "Distances_dl_higgs", "", "TTH",color="kBlack",linestyle = 7)],
             50,-5,5, 
             label_x   =  "#Delta R",
             label_y   = "Fraction of events",  
             axis_unit = "",
             #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.2,
             legend_origin_y = 0.65,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 3,
             legend_text_size = 0.035,
             get_ratio = False)




doWork(full_file_names, output_dir)