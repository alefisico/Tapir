#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import pickle
import socket # to get the hostname
import numpy as np
import math

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.CompareDistributionsPlots import *
else:
    from TTH.Plotting.python.Helpers.CompareDistributionsPlots import *


def calc_roc(h1, h2, rebin=1):
    h1 = h1.Clone()
    h2 = h2.Clone()
    h1.Rebin(rebin)
    h2.Rebin(rebin)

    if h1.Integral()>0:
        h1.Scale(1.0 / h1.Integral())
    if h2.Integral()>0:
        h2.Scale(1.0 / h2.Integral())
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

########################################
# Define Input Files and
# output directory
########################################

full_file_names = {}
full_file_names["ttH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/BasicTaggerStudies/GCbfc411e5cabd/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["tt"]  = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/BasicTaggerStudies/GCbfc411e5cabd/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8.root"
#full_file_names = ""

#output_dir = "results/JetCalibrations_Plots/"
output_dir = "results/BasicTaggerStudies_09072018/"

lumis = {}
lumis["ttH"] = 4982.71007 #In pb-1 Assuming XS of 0.5071*0.5824 pb and Ngen = 2164706 
lumis["tt"] = 36.538208 #Assuming XS of 831.76 pb and Ngen = 30391020.0 

targetlumi = 40.0

li_colors = [ROOT.kRed,      ROOT.kBlue+1,     ROOT.kBlack, 
         ROOT.kOrange-1, ROOT.kViolet+1,   ROOT.kGreen+1,
         ROOT.kGray,     ROOT.kYellow]*10  

########################################
# Plots
########################################
categories = ["DL"]

variables = ["pt","eta","btag1","btag2","btag3","bbtag","DRl","mass","softdropmass","tau32","tau21","tau31","fRec","Ropt"]
limits = [0,-5,0,0,0,-1,0,0,0,0,0,0,0,-5]
limitsinf = [600,5,1,1,1,1,5,600,600,1,1,1,5,5]
fatjets = ["Higgs","HiggsAK8","Top"]
prettyname = ["p_{T}","|#eta|","btagL","btagS","btagSSL","bbtag","#Delta R (l)","mass","mass_{SD}","#tau_{32}","#tau_{21}","#tau_{31}","f_{Rec}","R_{opt}"]


for cat in ["sl","dl"]:
    #Number of fatjets - cuts on pt and eta of fatjet
    combinedPlot("Nfatjets_{}".format(cat),
                 [plot( "CA15 SD - ttHbb", "nJet_{}_CA15".format(cat), "", "ttH"), 
                  plot( "AK8 SD - ttHbb", "nJet_{}_AK8".format(cat), "", "ttH"),
                  plot( "HTT - ttHbb", "nJet_{}_HTT".format(cat), "", "ttH"),
                  plot( "CA15 SD - TTbar", "nJet_{}_CA15".format(cat), "", "tt"), 
                  plot( "AK8 SD - TTbar", "nJet_{}_AK8".format(cat), "", "tt"),
                  plot( "HTT - TTbar", "nJet_{}_HTT".format(cat), "", "tt")],
                 5,0,5, 
                 label_x   =  "Nfatjets",
                 label_y   = "N of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.6,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 2,
                 legend_text_size = 0.035,
                 get_ratio = False)


    combinedPlot("Njets_{}".format(cat),
                 [plot( "AK4 - ttHbb", "nJet_{}_AK4".format(cat), "", "ttH"), 
                  plot( "AK4 btag - ttHbb", "nJet_{}_AK4b".format(cat), "", "ttH"),
                  plot( "AK4 wo FJ - ttHbb", "nJet_{}_AK4woFJ".format(cat), "", "ttH"),
                  plot( "AK4 wo FJ btag - ttHbb", "nJet_{}_AK4woFJb".format(cat), "", "ttH"),
                  plot( "AK4 wo SJ - ttHbb", "nJet_{}_AK4woSJ".format(cat), "", "ttH"),
                  plot( "AK4 wo SJ btag - ttHbb", "nJet_{}_AK4woSJb".format(cat), "", "ttH"),
                  plot( "AK4 - TTbar", "nJet_{}_AK4".format(cat), "", "tt"), 
                  plot( "AK4 btag - TTbar", "nJet_{}_AK4b".format(cat), "", "tt"),
                  plot( "AK4 wo FJ - TTbar", "nJet_{}_AK4woFJ".format(cat), "", "tt"),
                  plot( "AK4 wo FJ btag - TTbar", "nJet_{}_AK4woFJb".format(cat), "", "tt"),
                  plot( "AK4 wo SJ - TTbar", "nJet_{}_AK4woSJ".format(cat), "", "tt"),
                  plot( "AK4 wo SJ btag - TTbar", "nJet_{}_AK4woSJb".format(cat), "", "tt"),],
                 20,0,20, 
                 label_x   =  "Njets",
                 label_y   = "N of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.5,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 8,
                 legend_text_size = 0.035,
                 get_ratio = False)

    for jettype in ["CA15","AK8"]:
        for v in variables:
            m = variables.index(v)
            combinedPlot("Jets_{}_{}_{}".format(cat,jettype,v),
                     [plot( "Matched top - ttHbb", "Distribution_{}_{}_matchedT_{}".format(cat,jettype,v), "", "ttH"), 
                      plot( "Matched Higgs  - ttHbb", "Distribution_{}_{}_matchedH_{}".format(cat,jettype,v), "", "ttH"),
                      plot( "Unmatched  - ttHbb", "Distribution_{}_{}_unmatched_{}".format(cat,jettype,v), "", "ttH"),
                      plot( "All - ttHbb", "Distribution_{}_{}_all_{}".format(cat,jettype,v), "", "ttH"),
                      plot( "Matched top - TTbar", "Distribution_{}_{}_matchedT_{}".format(cat,jettype,v), "", "tt"),
                      plot( "Unmatched - TTbar", "Distribution_{}_{}_unmatched_{}".format(cat,jettype,v), "", "tt"),
                      plot( "All - TTbar", "Distribution_{}_{}_all_{}".format(cat,jettype,v), "", "tt"),],
                     50,limitsinf[m],limits[m], 
                     label_x   =   prettyname[m],
                     label_y   = "N of events",  
                     #axis_unit = "GeV",
                     axis_unit = "GeV" if "Mass" in v or v == "pt" else "",
                     log_y     = False,
                     normalize = True,
                     scale = False,
                     legend_origin_x = 0.5,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 6,
                     legend_text_size = 0.035,
                     get_ratio = False,
                     ratiomin = 0,
                     ratiomax = 0.99) 


    for jettype in ["HTT"]:
        for v in variables:
            m = variables.index(v)
            combinedPlot("Jets_{}_{}_{}".format(cat,jettype,v),
                     [plot( "Matched top - ttHbb", "Distribution_{}_{}_matchedT_{}".format(cat,jettype,v), "", "ttH"), 
                      plot( "Unmatched  - ttHbb", "Distribution_{}_{}_unmatched_{}".format(cat,jettype,v), "", "ttH"),
                      plot( "All - ttHbb", "Distribution_{}_{}_all_{}".format(cat,jettype,v), "", "ttH"),
                      plot( "Matched top - TTbar", "Distribution_{}_{}_matchedT_{}".format(cat,jettype,v), "", "tt"),
                      plot( "Unmatched - TTbar", "Distribution_{}_{}_unmatched_{}".format(cat,jettype,v), "", "tt"),
                      plot( "All - TTbar", "Distribution_{}_{}_all_{}".format(cat,jettype,v), "", "tt"),],
                     50,limitsinf[m],limits[m], 
                     label_x   =   prettyname[m],
                     label_y   = "N of events",  
                     #axis_unit = "GeV",
                     axis_unit = "GeV" if "Mass" in v or v == "pt" else "",
                     log_y     = False,
                     normalize = True,
                     scale = False,
                     legend_origin_x = 0.5,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 6,
                     legend_text_size = 0.035,
                     get_ratio = False,
                     ratiomin = 0,
                     ratiomax = 0.99) 


    for v in variables:
        m = variables.index(v)
        combinedPlot("Jets_{}_AK4_{}".format(cat,v),
                 [plot( "All - ttHbb", "Distribution_{}_AK4_all_{}".format(cat,v), "", "ttH"),
                  plot( "Btag - ttHbb", "Distribution_{}_AK4b_all_{}".format(cat,v), "", "ttH"),
                  plot( "All - TTbar", "Distribution_{}_AK4_all_{}".format(cat,v), "", "tt"),
                  plot( "Btag - TTbar", "Distribution_{}_AK4b_all_{}".format(cat,v), "", "tt"),],
                 50,limitsinf[m],limits[m], 
                 label_x   =   prettyname[m],
                 label_y   = "N of events",  
                 #axis_unit = "GeV",
                 axis_unit = "GeV" if "Mass" in v or v == "pt" else "",
                 log_y     = False,
                 normalize = True,
                 scale = False,
                 legend_origin_x = 0.5,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 6,
                 legend_text_size = 0.035,
                 get_ratio = False,
                 ratiomin = 0,
                 ratiomax = 0.99) 



doWork(full_file_names, output_dir)