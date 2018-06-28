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
full_file_names["TopTTSL"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/Top_CheckTagger/GC5306fd17c14b/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"
full_file_names["TopTTH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/Top_CheckTagger/GC3deb631ebfed/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["HiggsTTSL"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/Higgs_CheckTagger/GCa4cb91de21dd/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"
full_file_names["HiggsTTDL"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/Higgs_CheckTagger/GC07999eb61e11/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root"
full_file_names["HiggsTTH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/Higgs_CheckTagger/GCcd9da63a15d4/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root"


output_dir = "../results/CheckTagger_28062018/"

########################################
# Create histograms, saved in file
########################################

criteria = ["pt","btag1","btag2","btag3","DRl","mass","softdropmass","tau32","tau32SD","eta","fRec","Ropt","ptsub","etasub","masssub"]
#criteriaH = ["pt","btag1","btag2","bbtag","bbtagSD","DRl","mass","softdropmass","tau21","tau21SD","eta","ptsub","etasub","masssub"]
#criteriaH = ["pt","btag1","btag2","bbtag","DRl","mass","softdropmass","tau21","eta","ptsub","etasub","masssub"]
criteriaH = ["pt","btag1","btag2","DRl","bbtag","mass","softdropmass","tau21","eta","ptsub","etasub","masssub"]
Categories = ["sl","dl"]

limitsinf = [0,0,0,0,0,0,0,0.2,0.2,-5,0,-5,0,-5,0]
limits = [600,1,1,1,5,400,600,1,1,5,2,5,600,5,100]
#limitsinfH = [0,0,0,-1,-1,0,0,0,0.2,0.2,-5,0,-5,0]
#limitsH = [600,1,1,1,1,5,600,600,1,1,5,600,5,200]
#limitsinfH = [0,0,0,-1,0,0,0,0,-5,0,-5,0]
#limitsH = [600,1,1,1,5,600,600,1,5,600,5,200]
limitsinfH = [0,0,0,0,-1,0,0,0,-5,0,-5,0]
limitsH = [800,1,1,5,1,400,400,1,5,600,5,200]

prettyname = ["p_{T}","btagL","btagSL","btagSSL","#Delta R (l)","mass","mass_{SD}","#tau_{32}","#tau_{32SD}","|#eta|","f_{Rec}","R_{opt}","p_{T,sub}","|#eta|_{sub}","mass_{T,sub}"]
#prettynameH = ["p_{T}","btagL","btagSL","bbtag","bbtag_{SD}","#Delta R (l)","mass","mass_{SD}","#tau_{21}","#tau_{21SD}","|#eta|","p_{T,sub}","|#eta|_{sub}","mass_{T,sub}"]
prettynameH = ["p_{T}","btagL","btagSL","#Delta R (l)","bbtag","mass","mass_{SD}","#tau_{21}","|#eta|","p_{T,sub}","|#eta|_{sub}","mass_{T,sub}"]

combinedPlot("SL_Nfatjets_Top",
             [plot( "All HTT - t#bar{t}H", "Nfatjets_sl_allHTT", "", "TopTTH",color="kRed"),
              plot( "Sel HTT - t#bar{t}H", "Nfatjets_sl_HTT", "", "TopTTH",color="kRed",linestyle = 7),
              plot( "All HTT - t#bar{t}", "Nfatjets_sl_allHTT", "", "TopTTSL",color="kBlack"),
              plot( "Sel HTT - t#bar{t}", "Nfatjets_sl_HTT", "", "TopTTSL",color="kBlack",linestyle = 7)],
             5,0,5, 
             label_x   =  "Nfatjets",
             label_y   = "Fraction of events",  
             axis_unit = "",
             #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
             log_y     = False,
             normalize = True,
             legend_origin_x = 0.55,
             legend_origin_y = 0.7,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 4,
             legend_text_size = 0.035,
             get_ratio = False)

combinedPlot("SL_Matchedfatjets_Top_TTH",
             [plot( "All Gen Top", "Count_sl", "", "TopTTH",0.001,color="kBlack"),
              plot( "Match to all HTT", "MatchedFatjet_sl_allHTT", "", "TopTTH",0.001,color="kOrange+7",linestyle = 7), 
              plot( "Match to sel HTT", "MatchedFatjet_sl_HTT", "", "TopTTH",0.001,color="kRed",linestyle = 2),             
              #plot( "All Gen Top", "Count_sl", "", "TopTTSL",color="kBlack"),
              #plot( "Match to all HTT", "MatchedFatjet_sl_allHTT", "", "TopTTSL",color="kBlack",linestyle = 7), 
              #plot( "Match to sel HTT", "MatchedFatjet_sl_HTT", "", "TopTTSL",color="kBlack",linestyle = 2),
              ],
             50,150,600, 
             label_x   =  "Gen Top p_{T}",
             label_y   = "A.U.",  
             axis_unit = "GeV",
             #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
             log_y     = False,
             normalize = False,
             legend_origin_x = 0.55,
             legend_origin_y = 0.7,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 3,
             legend_text_size = 0.035,
             get_ratio = True,
             ratiomin = 0,
             ratiomax = 1.1)

combinedPlot("SL_Matchedfatjets_Top_TT",
             [#plot( "All Gen Top", "Count_sl", "", "TopTTH",color="kRed"),
              #plot( "Match to all HTT", "MatchedFatjet_sl_allHTT", "", "TopTTH",color="kRed",linestyle = 7), 
              #plot( "Match to sel HTT", "MatchedFatjet_sl_HTT", "", "TopTTH",color="kRed",linestyle = 2),             
              plot( "All Gen Top", "Count_sl", "", "TopTTSL",0.0000001,color="kBlack"),
              plot( "Match to all HTT", "MatchedFatjet_sl_allHTT", "", "TopTTSL",0.0000001,color="kOrange+7",linestyle = 7), 
              plot( "Match to sel HTT", "MatchedFatjet_sl_HTT", "", "TopTTSL",0.0000001,color="kRed",linestyle = 2),
              ],
             50,150,600, 
             label_x   =  "Gen Top p_{T}",
             label_y   = "A.U.", 
             axis_unit = "GeV",
             #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
             log_y     = False,
             normalize = False,
             legend_origin_x = 0.55,
             legend_origin_y = 0.7,
             legend_size_x   = 0.25,
             legend_size_y   = 0.05 * 3,
             legend_text_size = 0.035,
             get_ratio = True,
             ratiomin = 0,
             ratiomax = 1.1)

for crit in criteria:
    m = criteria.index(crit)
    combinedPlot("SL_Top_{}_TT".format(crit),
                 [plot( "All HTT - um", "sl_allHTT_unmatched_{}".format(crit), "", "TopTTSL", 0.0000001,color="kBlack"),
                  plot( "All HTT - m", "sl_allHTT_matched_{}".format(crit), "", "TopTTSL", 0.0000001,color="kRed"),
                  plot( "Sel HTT - um", "sl_HTT_unmatched_{}".format(crit), "", "TopTTSL", 0.0000001,color="kBlack",linestyle = 7), 
                  plot( "Sel HTT - m", "sl_HTT_matched_{}".format(crit), "", "TopTTSL", 0.0000001,color="kRed",fillstyle = 3144),
                  ],
                 50,limitsinf[m],limits[m], 
                 label_x   = prettyname[m],
                 label_y   = "A.U.", 
                 axis_unit = "GeV" if "Mass" in crit or crit == "pt" else "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = False,
                 legend_origin_x = 0.55,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 4,
                 legend_text_size = 0.035,
                 get_ratio = False,
                 ratiomin = 0,
                 ratiomax = 0.99)

    combinedPlot("SL_Top_{}_TTH".format(crit),
                 [plot( "All HTT - um", "sl_allHTT_unmatched_{}".format(crit), "", "TopTTH", 0.001,color="kBlack"),
                  plot( "All HTT - m", "sl_allHTT_matched_{}".format(crit), "", "TopTTH", 0.001,color="kRed"),
                  plot( "Sel HTT - um", "sl_HTT_unmatched_{}".format(crit), "", "TopTTH", 0.001,color="kBlack",linestyle = 7), 
                  plot( "Sel HTT - m", "sl_HTT_matched_{}".format(crit), "", "TopTTH", 0.001,color="kRed",fillstyle = 3144),
                  ],
                 50,limitsinf[m],limits[m], 
                 label_x   = prettyname[m],
                 label_y   = "A.U.", 
                 axis_unit = "GeV" if "Mass" in crit or crit == "pt" else "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = False,
                 legend_origin_x = 0.55,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 4,
                 legend_text_size = 0.035,
                 get_ratio = False,
                 ratiomin = 0,
                 ratiomax = 0.99)

for cat in Categories:
    if cat == "sl":
        bkg = "HiggsTTSL"
        name = "SL"
    else:
        bkg = "HiggsTTDL"
        name = "DL"
    combinedPlot("{}_Nfatjets_Higgs".format(name),
                 [plot( "All Higgs - t#bar{t}H", "Nfatjets_{}_allHiggs".format(cat), "", "HiggsTTH",color="kRed"),
                  plot( "Sel Higgs - t#bar{t}H", "Nfatjets_{}_Higgs".format(cat), "", "HiggsTTH",color="kRed",linestyle = 7),
                  plot( "All Higgs - t#bar{t}", "Nfatjets_{}_allHiggs".format(cat), "", bkg,color="kBlack"),
                  plot( "Sel Higgs - t#bar{t}", "Nfatjets_{}_Higgs".format(cat), "", bkg,color="kBlack",linestyle = 7)],
                 5,0,5, 
                 label_x   =  "Nfatjets",
                 label_y   = "Fraction of events",  
                 axis_unit = "",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = True,
                 legend_origin_x = 0.55,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 4,
                 legend_text_size = 0.035,
                 get_ratio = False)

    combinedPlot("{}_Matchedfatjets_Higgs_TTH".format(name),
                 [plot( "All Gen Higgs", "Count_{}".format(cat), "", "HiggsTTH",0.001,color="kBlack"),
                  plot( "Match to all Higgs", "MatchedFatjet_{}_allHiggs".format(cat), "", "HiggsTTH",0.001,color="kOrange+7",linestyle = 7), 
                  plot( "Match to sel Higgs", "MatchedFatjet_{}_Higgs".format(cat), "", "HiggsTTH",0.001,color="kRed",linestyle = 2),             
                  #plot( "All Gen Top", "Count_sl", "", "TopTTSL",color="kBlack"),
                  #plot( "Match to all HTT", "MatchedFatjet_sl_allHTT", "", "TopTTSL",color="kBlack",linestyle = 7), 
                  #plot( "Match to sel HTT", "MatchedFatjet_sl_HTT", "", "TopTTSL",color="kBlack",linestyle = 2),
                  ],
                 50,150,600, 
                 label_x   =  "Gen Higgs p_{T}",
                 label_y   = "A.U.",  
                 axis_unit = "GeV",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = False,
                 legend_origin_x = 0.55,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = True,
                 ratiomin = 0,
                 ratiomax = 1.1)

    combinedPlot("{}_Matchedfatjets_Higgs_TT".format(name),
                 [#plot( "All Gen Top", "Count_sl", "", "TopTTH",color="kRed"),
                  #plot( "Match to all HTT", "MatchedFatjet_sl_allHTT", "", "TopTTH",color="kRed",linestyle = 7), 
                  #plot( "Match to sel HTT", "MatchedFatjet_sl_HTT", "", "TopTTH",color="kRed",linestyle = 2),             
                  plot( "All Gen Higgs", "Count_{}".format(cat), "", bkg,0.0000001,color="kBlack"),
                  plot( "Match to all Higgs", "MatchedFatjet_{}_allHiggs".format(cat), "", bkg,0.0000001,color="kOrange+7",linestyle = 7), 
                  plot( "Match to sel Higgs", "MatchedFatjet_{}_Higgs".format(cat), "", bkg,0.0000001,color="kRed",linestyle = 2),
                  ],
                 50,150,600, 
                 label_x   =  "Gen Higgs p_{T}",
                 label_y   = "A.U.", 
                 axis_unit = "GeV",
                 #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                 log_y     = False,
                 normalize = False,
                 legend_origin_x = 0.55,
                 legend_origin_y = 0.7,
                 legend_size_x   = 0.25,
                 legend_size_y   = 0.05 * 3,
                 legend_text_size = 0.035,
                 get_ratio = True,
                 ratiomin = 0,
                 ratiomax = 1.1)

    for crit in criteriaH:
        m = criteriaH.index(crit)
        combinedPlot("{}_Higgs_{}_TT".format(name,crit),
                     [plot( "All Higgs - um", "{}_allHiggs_unmatched_{}".format(cat,crit), "", bkg, 0.0000001,color="kBlack"),
                      plot( "All Higgs - m", "{}_allHiggs_matched_{}".format(cat,crit), "", bkg, 0.0000001,color="kRed"),
                      plot( "Sel Higgs - um", "{}_Higgs_unmatched_{}".format(cat,crit), "", bkg, 0.0000001,color="kBlack",linestyle = 7), 
                      plot( "Sel Higgs - m", "{}_Higgs_matched_{}".format(cat,crit), "", bkg, 0.0000001,color="kRed",fillstyle = 3144),
                      ],
                     50,limitsinfH[m],limitsH[m], 
                     label_x   = prettynameH[m],
                     label_y   = "A.U.", 
                     axis_unit = "GeV" if "Mass" in crit or crit == "pt" else "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = False,
                     legend_origin_x = 0.55,
                     legend_origin_y = 0.7,
                     legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 4,
                     legend_text_size = 0.035,
                     get_ratio = False,
                     ratiomin = 0,
                     ratiomax = 0.99)


        combinedPlot("{}_Higgs_{}_TTH".format(name,crit),
                     [plot( "All Higgs - um", "{}_allHiggs_unmatched_{}".format(cat,crit), "", "HiggsTTH", 0.001,color="kBlack"),
                      plot( "All Higgs - m", "{}_allHiggs_matched_{}".format(cat,crit), "", "HiggsTTH", 0.001,color="kRed"),
                      plot( "Sel Higgs - um", "{}_Higgs_unmatched_{}".format(cat,crit), "", "HiggsTTH", 0.001,color="kBlack",linestyle = 7), 
                      plot( "Sel Higgs - m", "{}_Higgs_matched_{}".format(cat,crit), "", "HiggsTTH", 0.001,color="kRed",fillstyle = 3144),
                      ],
                     50,limitsinfH[m],limitsH[m], 
                     label_x   = prettynameH[m],
                     label_y   = "A.U.", 
                     axis_unit = "GeV" if "Mass" in crit or crit == "pt" else "",
                     #axis_unit = "GeV" if v == "Mass" or v == "Pt" else "",
                     log_y     = False,
                     normalize = False,
                     legend_origin_x = 0.55,
                     legend_origin_y = 0.7,
                    legend_size_x   = 0.25,
                     legend_size_y   = 0.05 * 4,
                     legend_text_size = 0.035,
                     get_ratio = False,
                     ratiomin = 0,
                     ratiomax = 0.99)




doWork(full_file_names, output_dir)