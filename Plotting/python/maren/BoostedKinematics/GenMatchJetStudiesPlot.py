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
targetlumi = [40,80,100]

output_dir = "results/GenMatchJetStudies_20180515/"


def DoPlots(jettype,targetlumi,output_dir):
    print "Working on jet type:" , jettype
    full_file_names = {}
    full_file_names["ttH"] = None
    full_file_names["ttjets"] = None
    full_file_names["ttH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GenMatchJetStudies/May14_tth_{}_processed.root".format(jettype)
    full_file_names["ttjets"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GenMatchJetStudies/May14_ttSL_{}_processed.root".format(jettype)


    ########################################
    # Plots
    ########################################



    #for sample in full_file_names.keys():
    combinedPlot2D("GenParticleStudies_GenHiggspTDR_{}_{}".format("ttH",jettype),
                    [plot( "", "{}GenHiggspTDR".format(jettype), "", "ttH")],
                    200, 0,1000,100,0,5,
                    label_x   = "p_{T}",
                    label_y   = "#Delta R (b quarks)",                          
                    axis_unit = "GeV",
                    log_y     = False,)

    combinedPlot2D("GenParticleStudies_GenTopHiggs_{}_{}".format("ttH",jettype),
                    [plot( "", "{}GenTopHiggs".format(jettype), "", "ttH")],
                    200, 0,500,200, 0,500,
                    label_x   = "p_{T} (gen Top)",
                    label_y   = "p_{T} (gen Higgs)",                         
                    axis_unit = "GeV",
                    log_y     = False,)

    combinedPlot2D("GenParticleStudies_GenTopHadHiggs_{}_{}".format("ttH",jettype),
                    [plot( "", "{}GenTopHadHiggs".format(jettype), "", "ttH")],
                    200, 0,500,200, 0,500,
                    label_x   = "p_{T} (gen had Top)",
                    label_y   = "p_{T} (gen Higgs)",                          
                    axis_unit = "GeV",
                    log_y     = False,)

    combinedPlot("GenParticleStudies_GenHiggsDR_{}_{}".format("ttH",jettype),
                    [plot( "", "{}GenHiggsDR".format(jettype), "", "ttH")],
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

    combinedPlot("GenParticleStudies_GenHiggsHadTopDR_{}_{}".format("ttH",jettype),
                    [plot( "", "{}GenDRHadTopHiggs".format(jettype), "", "ttH")],
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


    combinedPlot("GenParticleStudies_GenHiggsTopDR_{}_{}".format("ttH",jettype),
                    [plot( "", "{}GenDRTopHiggs".format(jettype), "", "ttH")],
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

    combinedPlot("GenParticleStudies_GenTopTopDR_{}".format(jettype),
                    [plot( "ttH", "{}GenDRTopTop".format(jettype), "", "ttH"),
                    plot( "tt + jets", "{}GenDRTopTop".format(jettype), "", "ttjets")],
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

    combinedPlot("GenParticleStudies_GenHadWDR_{}".format(jettype),
                    [plot( "ttH", "{}GenHadWDR".format(jettype), "", "ttH"),
                    plot( "tt + jets", "{}GenHadWDR".format(jettype), "", "ttjets")],
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

    combinedPlot("GenParticleStudies_GenHadWpT_{}".format(jettype),
                    [plot( "ttH", "{}GenHadWpT".format(jettype), "", "ttH"),
                    plot( "tt + jets", "{}GenHadWpT".format(jettype), "", "ttjets")],
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

        combinedPlot2D("GenParticleStudies_GenToppTDR_{}_{}".format(s,jettype),
                        [plot( "", "{}GenToppTDR".format(jettype), "", s)],
                        200, 0,1000,100,0,5,
                        label_x   = "p_{T}",
                        label_y   = "#Delta R_{min}",                          
                        axis_unit = "GeV",
                        log_y     = False,)

        combinedPlot2D("GenParticleStudies_GenToppTDR2_{}_{}".format(s,jettype),
                        [plot( "", "{}GenToppTDR2".format(jettype), "", s)],
                        200, 0,1000,100,0,5,
                        label_x   = "p_{T}",
                        label_y   = "#Delta R_{bjj}",                          
                        axis_unit = "GeV",
                        log_y     = False,)

        combinedPlot2D("GenParticleStudies_GenWpTDR_{}_{}".format(s,jettype),
                        [plot( "", "{}GenWpTDR".format(jettype), "", s)],
                        200, 0,1000,100,0,5,
                        label_x   = "p_{T}",
                        label_y   = "#Delta R_{q_{1}q_{2}}",                          
                        axis_unit = "GeV",
                        log_y     = False,)

        combinedPlot2D("GenParticleStudies_GenHadWpTDR_{}_{}".format(s,jettype),
                        [plot( "", "{}GenHadWpTDR".format(jettype), "", s)],
                        200, 0,1000,100,0,5,
                        label_x   = "p_{T}",
                        label_y   = "#Delta R_{q_{1}q_{2}}",                          
                        axis_unit = "GeV",
                        log_y     = False,)




    for lumi in targetlumi:
        combinedPlot("GenParticleStudies_GenPart_pt_{0}_{1}fb_{2}".format(s,lumi,jettype),
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

def DoPlotsHTT(jettype,targetlumi,output_dir):
    print "Working on jet type:" , jettype
    full_file_names = {}
    full_file_names["ttH"] = None
    full_file_names["ttjets"] = None
    full_file_names["ttH"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GenMatchJetStudies/May14_tth_{}_processed.root".format(jettype)
    full_file_names["ttjets"] = "/mnt/t3nfs01/data01/shome/mameinha/tth/gc/GenMatchJetStudies/May14_ttSL_{}_processed.root".format(jettype)


    ########################################
    # Plots
    ########################################


    combinedPlot2D("GenParticleStudies_GenTopHiggs_{}_{}".format("ttH",jettype),
                    [plot( "", "{}GenTopHiggs".format("HTT"), "", "ttH")],
                    200, 0,500,200, 0,500,
                    label_x   = "p_{T} (gen Top)",
                    label_y   = "p_{T} (gen Higgs)",                         
                    axis_unit = "GeV",
                    log_y     = False,)

    combinedPlot2D("GenParticleStudies_GenTopHadHiggs_{}_{}".format("ttH",jettype),
                    [plot( "", "{}GenTopHadHiggs".format("HTT"), "", "ttH")],
                    200, 0,500,200, 0,500,
                    label_x   = "p_{T} (gen had Top)",
                    label_y   = "p_{T} (gen Higgs)",                          
                    axis_unit = "GeV",
                    log_y     = False,)

    combinedPlot("GenParticleStudies_GenHiggsHadTopDR_{}_{}".format("ttH",jettype),
                    [plot( "", "{}GenDRHadTopHiggs".format("HTT"), "", "ttH")],
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


    combinedPlot("GenParticleStudies_GenHiggsTopDR_{}_{}".format("ttH",jettype),
                    [plot( "", "{}GenDRTopHiggs".format("HTT"), "", "ttH")],
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

    combinedPlot("GenParticleStudies_GenTopTopDR_{}".format(jettype),
                    [plot( "ttH", "{}GenDRTopTop".format("HTT"), "", "ttH"),
                    plot( "tt + jets", "{}GenDRTopTop".format("HTT"), "", "ttjets")],
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

 
    for s in ["ttH","ttjets"]:

        combinedPlot2D("GenParticleStudies_GenToppTDR_{}_{}".format(s,jettype),
                        [plot( "", "{}GenToppTDR".format("HTT"), "", s)],
                        200, 0,1000,100,0,5,
                        label_x   = "p_{T}",
                        label_y   = "#Delta R_{min}",                          
                        axis_unit = "GeV",
                        log_y     = False,)

        combinedPlot2D("GenParticleStudies_GenToppTDR2_{}_{}".format(s,jettype),
                        [plot( "", "{}GenToppTDR2".format("HTT"), "", s)],
                        200, 0,1000,100,0,5,
                        label_x   = "p_{T}",
                        label_y   = "#Delta R_{bjj}",                          
                        axis_unit = "GeV",
                        log_y     = False,)


    for lumi in targetlumi:
        combinedPlot("GenParticleStudies_GenPart_pt_{0}_{1}fb_{2}".format(s,lumi,jettype),
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
                        draw_legend     = True,
                        legend_origin_x = 0.55,
                        legend_origin_y = 0.7,
                        legend_size_x   = 0.25,
                        legend_size_y   = 0.05 * 2,
                        legend_text_size = 0.035,
                        get_ratio = False)



    doWork(full_file_names, output_dir )

#DoPlots("CA15",targetlumi,output_dir)
#DoPlots("AK8",targetlumi,output_dir)
DoPlotsHTT("HTT",targetlumi,output_dir)