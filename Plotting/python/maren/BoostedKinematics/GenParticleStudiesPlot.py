#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import pickle
import socket # to get the hostname

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.CompareDistributionsPlots import *
else:
    from TTH.Plotting.python.Helpers.CompareDistributionsPlots import *

########################################
# Define Input Files and
# output directory
########################################

full_file_names = {}
full_file_names["ttH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GenParticleStudies/May14_tth_processed.root"
full_file_names["ttjets"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GenParticleStudies/May14_ttSL_processed.root"
#full_file_names = "/mnt/t3nfs01/data01/shome/mameinha/TTH/CMSSW_8_0_25/CMSSW/src/TTH/Plotting/python/maren/SubjetMatching.root"

#output_dir = "results/JetCalibrations_Plots/"
output_dir = "results/GenParticleStudies_20180514/"

targetlumi = [40,80,100]

########################################
# Plots
########################################

#for sample in full_file_names.keys():
combinedPlot2D("GenParticleStudies_GenHiggspTDR_{}".format("ttH"),
                [plot( "", "GenHiggspTDR", "", "ttH")],
                200, 0,1000,100,0,5,
                label_x   = "p_{T}",
                label_y   = "#Delta R (b quarks)",                          
                axis_unit = "GeV",
                log_y     = False,)

combinedPlot2D("GenParticleStudies_GenTopHiggs_{}".format("ttH"),
                [plot( "", "GenTopHiggs", "", "ttH")],
                200, 0,500,200, 0,500,
                label_x   = "p_{T} (gen Top)",
                label_y   = "p_{T} (gen Higgs)",                         
                axis_unit = "GeV",
                log_y     = False,)

combinedPlot2D("GenParticleStudies_GenTopHadHiggs_{}".format("ttH"),
                [plot( "", "GenTopHadHiggs", "", "ttH")],
                200, 0,500,200, 0,500,
                label_x   = "p_{T} (gen had Top)",
                label_y   = "p_{T} (gen Higgs)",                          
                axis_unit = "GeV",
                log_y     = False,)

combinedPlot("GenParticleStudies_GenHiggsDR_{}".format("ttH"),
                [plot( "", "GenHiggsDR", "", "ttH")],
                100,0,5,
                label_x   = "#Delta R (b quarks)",
                label_y   = "# events",                          
                axis_unit = "",
                log_y     = False,
                normalize = False,
                draw_legend     = False,
                legend_origin_x = 0.15,
                legend_origin_y = 0.7,
                legend_size_x   = 0.25,
                legend_size_y   = 0.05 * 2,
                legend_text_size = 0.035,
                get_ratio = False)

combinedPlot("GenParticleStudies_GenHiggsHadTopDR_{}".format("ttH"),
                [plot( "", "GenDRHadTopHiggs", "", "ttH")],
                100,0,5,
                label_x   = "#Delta R (Higgs, Had Top)",
                label_y   = "# events",                          
                axis_unit = "",
                log_y     = False,
                normalize = False,
                draw_legend     = False,
                legend_origin_x = 0.15,
                legend_origin_y = 0.7,
                legend_size_x   = 0.25,
                legend_size_y   = 0.05 * 2,
                legend_text_size = 0.035,
                get_ratio = False)


combinedPlot("GenParticleStudies_GenHiggsTopDR_{}".format("ttH"),
                [plot( "", "GenDRTopHiggs", "", "ttH")],
                100,0,5,
                label_x   = "#Delta R (Higgs, Top)",
                label_y   = "# events",                          
                axis_unit = "",
                log_y     = False,
                normalize = False,
                draw_legend     = False,
                legend_origin_x = 0.15,
                legend_origin_y = 0.7,
                legend_size_x   = 0.25,
                legend_size_y   = 0.05 * 2,
                legend_text_size = 0.035,
                get_ratio = False)

combinedPlot("GenParticleStudies_GenTopTopDR",
                [plot( "ttH", "GenDRTopTop", "", "ttH"),
                plot( "tt + jets", "GenDRTopTop", "", "ttjets")],
                100,0,5,
                label_x   = "#Delta R (Top, Top)",
                label_y   = "# events",                          
                axis_unit = "",
                log_y     = False,
                normalize = True,
                draw_legend     = True,
                legend_origin_x = 0.15,
                legend_origin_y = 0.7,
                legend_size_x   = 0.25,
                legend_size_y   = 0.05 * 2,
                legend_text_size = 0.035,
                get_ratio = False)

combinedPlot("GenParticleStudies_GenHadWDR",
                [plot( "ttH", "GenHadWDR", "", "ttH"),
                plot( "tt + jets", "GenHadWDR", "", "ttjets")],
                100,0,5,
                label_x   = "#Delta R (W_{q1},W_{q2})",
                label_y   = "# events",                          
                axis_unit = "",
                log_y     = False,
                normalize = True,
                draw_legend     = True,
                legend_origin_x = 0.70,
                legend_origin_y = 0.7,
                legend_size_x   = 0.25,
                legend_size_y   = 0.05 * 2,
                legend_text_size = 0.035,
                get_ratio = False)

combinedPlot("GenParticleStudies_GenHadWpT",
                [plot( "ttH", "GenHadWpT", "", "ttH"),
                plot( "tt + jets", "GenHadWpT", "", "ttjets")],
                100,0,500,
                label_x   = "p_{T}",
                label_y   = "# events",                          
                axis_unit = "",
                log_y     = False,
                normalize = True,
                draw_legend     = True,
                legend_origin_x = 0.70,
                legend_origin_y = 0.7,
                legend_size_x   = 0.25,
                legend_size_y   = 0.05 * 2,
                legend_text_size = 0.035,
                get_ratio = False)

for s in ["ttH","ttjets"]:

    combinedPlot2D("GenParticleStudies_GenToppTDR_{}".format(s),
                    [plot( "", "GenToppTDR", "", s)],
                    200, 0,1000,100,0,5,
                    label_x   = "p_{T}",
                    label_y   = "#Delta R_{min}",                          
                    axis_unit = "GeV",
                    log_y     = False,)

    combinedPlot2D("GenParticleStudies_GenToppTDR2_{}".format(s),
                    [plot( "", "GenToppTDR2", "", s)],
                    200, 0,1000,100,0,5,
                    label_x   = "p_{T}",
                    label_y   = "#Delta R_{bjj}",                          
                    axis_unit = "GeV",
                    log_y     = False,)

    combinedPlot2D("GenParticleStudies_GenWpTDR_{}".format(s),
                    [plot( "", "GenWpTDR", "", s)],
                    200, 0,1000,100,0,5,
                    label_x   = "p_{T}",
                    label_y   = "#Delta R_{q_{1}q_{2}}",                          
                    axis_unit = "GeV",
                    log_y     = False,)

    combinedPlot2D("GenParticleStudies_GenHadWpTDR_{}".format(s),
                    [plot( "", "GenHadWpTDR", "", s)],
                    200, 0,1000,100,0,5,
                    label_x   = "p_{T}",
                    label_y   = "#Delta R_{q_{1}q_{2}}",                          
                    axis_unit = "GeV",
                    log_y     = False,)




for lumi in targetlumi:
    combinedPlot("GenParticleStudies_GenPart_pt_{0}_{1}fb".format(s,lumi),
                    [plot( "Gen Higgs - ttH", "GenHiggspT_{}fb".format(lumi), "", "ttH"),
                    #plot( "Gen Top", "GenToppT_{}fb".format(lumi), "", sample),
                    plot( "Gen Had Top - ttH", "GenTopHadpT_{}fb".format(lumi), "", "ttH"),
                    plot( "Gen Had Top - tt+jets", "GenTopHadpT_{}fb".format(lumi), "", "ttjets")],
                    200,0,1000, 
                    label_x   = "p_{T}",
                    label_y   = "# events",                          
                    axis_unit = "",
                    log_y     = False,
                    normalize = True,
                    scale = 2,
                    draw_legend     = True,
                    legend_origin_x = 0.55,
                    legend_origin_y = 0.7,
                    legend_size_x   = 0.25,
                    legend_size_y   = 0.05 * 2,
                    legend_text_size = 0.035,
                    get_ratio = False)



doWork(full_file_names, output_dir )