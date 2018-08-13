#!/usr/bin/env python
import ROOT
from array import array
import Helper
from copy import deepcopy
import os
import GetEfficiencyTH3F
#############################################################
############### Configure Logging
import logging
log_format = (
    '[%(asctime)s] %(levelname)-8s %(funcName)-20s %(message)s')
logging.basicConfig(
    filename='debug.log',
    format=log_format,
    level=logging.DEBUG,
)

formatter = logging.Formatter(log_format)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
#############################################################
#############################################################
 
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)
if True:
    ROOT.gErrorIgnoreLevel = ROOT.kWarning# kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal;

 
def moveOverUnderFlow(histo, moveOverFlow=True, moveUnderFlow=False):
    """
    Function for moving the overflow and (or) underflow bin to the first/last bin
    """
    nBins = histo.GetNbinsX()
    if moveUnderFlow:
        underflow = histo.GetBinContent(0)
        fistBinContent = histo.GetBinContent(1)
        histo.SetBinContent(1, fistBinContent+underflow)
        histo.SetBinContent(0, 0)
    if moveOverFlow:
        overflow = histo.GetBinContent(nBins+1)
        lastBinContent = histo.GetBinContent(nBins)
        histo.SetBinContent(nBins, lastBinContent+overflow)
        histo.SetBinContent(nBins+1, 0)


def makeBaseHisto(name, title, bins, Htype):
    """
    Function for making the base histograms that are used to initialize the plots

    Args:
        name (str) : Name of the histogram (internal ROOT name)
        title (str) : Histogram title --> Will be used as x-axis Title
        bins (list) : List of bin edges. Including Lower and upper edge of histo
        Htype (str) : Either Data or MC --> Used for setting style
       
    Returns:
        ROOT.TH1F Object
    """
    logging.debug("Making base histo for %s", name)
    htmp = ROOT.TH1F(name, title, len(bins)-1, array("d",bins))
    htmp.Sumw2()
    return htmp

def setStyle(histo, Htype):
    if Htype == "Data":
        color = ROOT.kBlack
        marker = 20
    elif Htype == "MC":
        color = ROOT.kRed
        marker = 23
    else:
        raise KeyError("Htype can be Data or MC. Your choice: {0}".format(hType))
    histo.SetLineColor(color)
    histo.SetLineWidth(2)
    histo.SetMarkerStyle(marker)
    histo.SetMarkerColor(color)
    histo.SetMarkerSize(0.8)

def make3DBaseHisto(name, title, xbinning, ybinning, zbinning):
    """
    Function for creating the 3D base histogram
    """
    logging.debug("Making 3D base histogram")
    h3 = ROOT.TH3F(name, title,
                   len(xbinning)-1, array("d",xbinning),
                   len(ybinning)-1, array("d",ybinning),
                   len(zbinning)-1, array("d",zbinning),
    )
    h3.Sumw2()
    return h3
            
def makeHistos(baseHistoVars, prefix, SFHisto = False):
    """
    Function to initialize all the histograms need.
    
    Args:
        baseHistosVars (list) : List of tuples with base TH1F and variable name (var, th1f)
        prefix (str) : will be used for Cloning and histoname
    Return:
        histoDict (dict) : Dictionary containing the total, triggered and efficiency histograms for each variable
    """
    if SFHisto:
        histoDict = { "ScaleFactor" : {}  }
    else:
        histoDict = { "Total" : {},
                      "Triggered" : {},
                      "Efficiency" : {},
        }
    for variable, histo in baseHistoVars:
        logging.debug("Cloning histograms for variable %s with new names %s", variable,"{0}_*_{1}".format(prefix, variable) )
        if SFHisto:
            histoDict["ScaleFactor"][variable] = histo.Clone("{0}_sf_{1}".format(prefix, variable))
        else:
            histoDict["Total"][variable] = histo.Clone("{0}_tot_{1}".format(prefix, variable))
            histoDict["Triggered"][variable] = histo.Clone("{0}_trig_{1}".format(prefix, variable))
            histoDict["Efficiency"][variable] = histo.Clone("{0}_eff_{1}".format(prefix, variable))
    return histoDict

def make3DHistos(base3DHisto, prefix, binning = None, SFHisto = False):
    """
    Function to initialize all 3d histograms. Will create binned histograms for specified in args
    
    Args:
        3dBaseHisto (ROOT.TH3F) : base 3D histogram
        prefix (str) : Will be used for cloning
        binName (str) : var name of the binning
        binning (list) : List of bin edges. Including Lower and upper edge
    
    Returns:
        histoDict (dict)
    """
    if SFHisto:
        histoDict = { "ScaleFactor" : {}  }
    else:
        histoDict = { "Total" : {},
                      "Triggered" : {},
                      "Efficiency" : {},
        }
    if binning is None:
        if SFHisto:
            histoDict["ScaleFactor"]["0"] = base3DHisto.Clone("{0}_tot".format(prefix))
        else:
            histoDict["Total"]["0"] = base3DHisto.Clone("{0}_tot".format(prefix))
            histoDict["Triggered"]["0"] = base3DHisto.Clone("{0}_trig".format(prefix))
            histoDict["Efficiency"]["0"] = base3DHisto.Clone("{0}_eff".format(prefix))
    else:
        logging.info("Initializing binned 3D histograms --> Will create %s histos", len(binning)-1)
        for ibin in range(len(binning)-1):
            if SFHisto:
                histoDict["ScaleFactor"][str(ibin)] = base3DHisto.Clone("{0}_sf_{1}".format(prefix, ibin))
            else:
                histoDict["Total"][str(ibin)] = base3DHisto.Clone("{0}_tot_{1}".format(prefix, ibin))
                histoDict["Triggered"][str(ibin)] = base3DHisto.Clone("{0}_trig_{1}".format(prefix, ibin))
                histoDict["Efficiency"][str(ibin)] = base3DHisto.Clone("{0}_eff_{1}".format(prefix, ibin))

    return histoDict
    

def FillDataHistos(tree, histos, treeVars, baseSelection, triggerSelection, dataSelection = "1"):
    """
    Funciton for filling the Data histograms
    
    Args:
       tree (ROOT.TTree) : Tree for projection
       histos (dict) : Dict with histos (see makeHistos function)
       treeVars (dict) : Dict with strings used for projection (corresonding to var names in makeHistos function)
       *Selection (str) : Selection for the projection
    """
    logging.info("Start filling data histos")
    if histos["Total"].keys() != treeVars.keys():
        raise RuntimeError("Keys of histos and treeVars do not match! Please check")

    logging.debug("Filling Total histos")
    for var in histos["Total"]:
        logging.debug("Projection Total for %s",var)
        tree.Project(
            histos["Total"][var].GetName(),
            treeVars[var],
            "({0} && {1} && {2})".format(baseSelection, "1", dataSelection)
        )
        moveOverUnderFlow(histos["Total"][var])
    logging.debug("Filling Triggerd histos")
    for var in histos["Triggered"]:
        logging.debug("Projection Triggerd for %s",var)
        tree.Project(
            histos["Triggered"][var].GetName(),
            treeVars[var],
            "({0} && {1} && {2})".format(baseSelection, triggerSelection, dataSelection)
        )
        moveOverUnderFlow(histos["Triggered"][var])
    logging.debug("Filling Efficienies")
    for var in histos["Efficiency"]:
        histos["Efficiency"][var].Divide(histos["Triggered"][var], histos["Total"][var], 1, 1, "cl=0.683 b(1,1) mode")

    for plottype in histos:
        for var in histos[plottype]:
            setStyle(histos[plottype][var], "Data")


            
def FillData3DHistos(tree, histos, xyzTreeVars, binTreeVar = None, binning = None, baseSelection = "1", triggerSelection = "1", dataSelection = "1", useEffFunc = True):
    """
    Function for filling the 3D histograms for data

    Args:
       tree (ROOT.TTree) : Tree for projection
       histos (dict) : Dict with histos (see make3DHistos function)
       xyzTreeVars (tuple) : the 3 variable that will be used for projection
       binTreeVar (str) : Variable for the binning of the histograms
       binning (list) : bin edges
       *Selection (str) : Selection for the projection
    """
    if not isinstance(xyzTreeVars, tuple) or not len(xyzTreeVars) == 3:
        raise RuntimeError("xyzTreeVars is required to be a type with 3 str but is {0}".format(xyzTreeVars))
    logging.info("Starting 3D projection of Data")
    if binTreeVar is None or binning is None:
        binloop = [("0" , "1")]
    else:
        binloop = []
        for ibin in range(len(binning)-1):
            binloop.append( (str(ibin) , "{0} >= {1} && {0} < {2}".format(binTreeVar, binning[ibin], binning[ibin+1])) )
    for ibin, binSel in binloop:
        logging.info("Projection 3D histo with sel: %s",binSel)
        nprojTot = tree.Project(
            histos["Total"][ibin].GetName(),
            "{0}:{1}:{2}".format(xyzTreeVars[2], xyzTreeVars[1], xyzTreeVars[0]),
            "({0} && {1} && {2} && {3})".format(baseSelection, "1", dataSelection, binSel),
        )
        trigSel = "({0} && {1} && {2} && {3})".format(baseSelection, triggerSelection, dataSelection, binSel)
        logging.debug("TriggerSel: %s", trigSel)
        logging.debug("Will project to %s",histos["Triggered"][ibin].GetName())
        logging.debug("Variable: %s","{0}:{1}:{2}".format(xyzTreeVars[2], xyzTreeVars[1], xyzTreeVars[0]))
        nprojTrig = tree.Project(
            histos["Triggered"][ibin].GetName(),
            "{0}:{1}:{2}".format(xyzTreeVars[2], xyzTreeVars[1], xyzTreeVars[0]),
            trigSel,
        )
        logging.debug("Projection yielded %s total events and %s triggered events", nprojTot, nprojTrig)
        if useEffFunc:
            logging.warning("Will calculate efficiency using GetEfficiencyTH3F module")
            name = histos["Efficiency"][ibin].GetName()
            histos["Efficiency"][ibin] = GetEfficiencyTH3F.GetEfficiencyTHNF(histos["Triggered"][ibin], histos["Total"][ibin])
            histos["Efficiency"][ibin].SetName(name)
        else:
            histos["Efficiency"][ibin].Divide(histos["Triggered"][ibin], histos["Total"][ibin],1,1,"cl=0.683 b(1,1) mode")
            
def FillMCHistos(trees, inhistos, outHistos, treeVars, baseSelection, triggerSelection, weight):
    """
    Function for filling the MC histos. This will also sum all the trees and put them into the outHistos

    Args:
       trees (list(ROOT.TTree)) : List of Tree for projection
       inhistos (list(dict)) : List Dict with histos (see makeHistos function)
       treeVars (dict) : Dict with strings used for projection (corresonding to var names in makeHistos function)
       *Selection (str) : Selection for the projection   
       weight (list(str)) : weight expression for the projection
    """
    logging.info("Starting MC projection")
    for histos in inhistos:
        if histos["Total"].keys() != treeVars.keys():
            raise RuntimeError("Keys of histos and treeVars do not match! Please check")
    if len(inhistos) != len(trees):
        raise AssertionError("Trees and inhisto list have different length")
    for ihistos, histos in enumerate(inhistos):
        logging.info("Processing MC sample %s", ihistos)
        for var in histos["Total"]:
            logging.debug("Projection Total for %s",var)
            trees[ihistos].Project(
                histos["Total"][var].GetName(),
                treeVars[var],
                "({0}) * {1}".format(baseSelection, weight[ihistos])
            )
            moveOverUnderFlow(histos["Total"][var])
        for var in histos["Triggered"]:
            logging.debug("Projection Triggerd for %s",var)
            trees[ihistos].Project(
                histos["Triggered"][var].GetName(),
                treeVars[var],
                "({0} && {1}) * {2}".format(baseSelection, triggerSelection, weight[ihistos])
            )
            moveOverUnderFlow(histos["Triggered"][var])
    logging.info("Making sum of MC")
    for histos in inhistos:
        for var in histos["Total"]:
            outHistos["Total"][var].Add( histos["Total"][var] )
        for var in histos["Triggered"]:
            outHistos["Triggered"][var].Add( histos["Triggered"][var] )

    logging.info("Calculating efficiency")
    for var in outHistos["Efficiency"]:
        outHistos["Efficiency"][var].Divide(outHistos["Triggered"][var], outHistos["Total"][var], 1, 1, "cl=0.683 b(1,1) mode")

    for plottype in outHistos:
        for var in outHistos[plottype]:
            setStyle(outHistos[plottype][var], "MC")

def FillMC3DHistos(trees, inhistos, outhistos, xyzTreeVars, binTreeVar = None, binning = None, baseSelection = "1", triggerSelection = "1", weights = ["1"], useEffFunc = True):
    """
    Function for filling the 3D histograms for data

    Args:
       tree (ROOT.TTree) : Tree for projection
       inhistos (list(dict)) : List Dict with histos (see make3DHistos function)
       xyzTreeVars (tuple) : the 3 variable that will be used for projection
       binTreeVar (str) : Variable for the binning of the histograms
       binning (list) : bin edges
       *Selection (str) : Selection for the projection
    """
    if not isinstance(xyzTreeVars, tuple) or not len(xyzTreeVars) == 3:
        raise RuntimeError("xyzTreeVars is required to be a type with 3 str but is {0}".format(xyzTreeVars))        
    logging.info("Starting 3D projection of MC")
    if binTreeVar is None or binning is None:
        binloop = [("0" , "1")]
    else:
        binloop = []
        for ibin in range(len(binning)-1):
            binloop.append( (str(ibin) , "{0} >= {1} && {0} < {2}".format(binTreeVar, binning[ibin], binning[ibin+1])) )
    for ihistos, histos in enumerate(inhistos):
        logging.debug("Processing MC sample %s", ihistos)
        for ibin, binSel in binloop:
            logging.info("Projection 3D histo with sel: %s",binSel)
            nprojTot = trees[ihistos].Project(
                histos["Total"][ibin].GetName(),
                "{0}:{1}:{2}".format(xyzTreeVars[2], xyzTreeVars[1], xyzTreeVars[0]),
                "({0} && {1} && {2}) * {3}".format(baseSelection, "1", binSel, weights[ihistos]),
            )
            nprojTrig = trees[ihistos].Project(
                histos["Triggered"][ibin].GetName(),
                "{0}:{1}:{2}".format(xyzTreeVars[2], xyzTreeVars[1], xyzTreeVars[0]),
                "({0} && {1} && {2}) * {3}".format(baseSelection, triggerSelection, binSel, weights[ihistos]),
            )
            histos["Efficiency"][ibin].Divide(histos["Triggered"][ibin], histos["Total"][ibin],1,1,"cl=0.683 b(1,1) mode")
            logging.debug("Projection yielded %s total events and %s triggered events", nprojTot, nprojTrig)
    for ihistos, histos in enumerate(inhistos):
        for ibin, binSel in binloop:
            outhistos["Total"][ibin].Add(histos["Total"][ibin])
            outhistos["Triggered"][ibin].Add(histos["Triggered"][ibin])
    for ibin, binSel in binloop:
        if useEffFunc:
            logging.warning("Will calculate efficiency using GetEfficiencyTH3F module")
            name = outhistos["Efficiency"][ibin].GetName()
            outhistos["Efficiency"][ibin] = GetEfficiencyTH3F.GetEfficiencyTHNF(outhistos["Triggered"][ibin], outhistos["Total"][ibin])
            outhistos["Efficiency"][ibin].SetName(name)
        else:
            outhistos["Efficiency"][ibin].Divide(outhistos["Triggered"][ibin], outhistos["Total"][ibin],1,1,"cl=0.683 b(1,1) mode")


def Make3DScaleFactors(dataHistos, mcHistos, sfHistos):
    """
    Function to make the 3SFs by dividing MC and Data efficiencies
    """
    bins = dataHistos["Efficiency"].keys()
    for b in bins:
        sfHistos["ScaleFactor"][str(b)].Divide(dataHistos["Efficiency"][b], mcHistos["Efficiency"][b], 1, 1)
        
def setEfficiencyStyle(histos, titles, xmin = 0.0, xmax = 1.2):
    """
    Function for setting the style of the efficiency plots:
    
    Args:
       histos (dict) : Dictonary with vars as keys and efficiency histograms
       titles (dict) : Dictonary with vars as keys and histograms titles
       xmin, xmax (float) : y range of efficiency plot
    """
    logging.debug("Setting Efficiency style")
    if histos["Efficiency"].keys() != titles.keys():
        raise RuntimeError("Keys of histos and titles do not match! Please check")

    for var in histos["Efficiency"]:
        histos["Efficiency"][var].SetTitle(titles[var])
        histos["Efficiency"][var].GetYaxis().SetTitleSize(0.069*0.69)
        histos["Efficiency"][var].GetYaxis().SetTitleOffset(0.98)
        histos["Efficiency"][var].GetYaxis().SetLabelSize(0.060*0.75)
        histos["Efficiency"][var].GetXaxis().SetTitleSize(0.069*0.75)
        histos["Efficiency"][var].GetXaxis().SetLabelSize(0.06*0.75)
        histos["Efficiency"][var].GetXaxis().SetDecimals(1)
        histos["Efficiency"][var].GetYaxis().SetDecimals(1)
        histos["Efficiency"][var].GetXaxis().SetNdivisions(20504)
        histos["Efficiency"][var].GetYaxis().SetNdivisions(505)
        histos["Efficiency"][var].GetYaxis().SetRangeUser(xmin,xmax)

def makePlots(dataHistos, mcHistos, plottype = "Efficiency", normalized = False):
    """
    Function for making the plots
    
    Returns:
        allCanvas (list) : List of canvases
    """
    lumi = Helper.lumi_Trigger
    box = Helper.create_paves(lumi, "DataWiP", CMSposX=0.155, CMSposY=0.84, 
                          prelimPosX=0.15, prelimPosY=0.79,
                          lumiPosX=0.977, lumiPosY=0.91, alignRight=False,
                          CMSsize=0.075*.75, prelimSize=0.057*.75, lumiSize=0.060*.75)
    
    logging.info("Starting to plot plottype %s", plottype)
    leg = ROOT.TLegend(0.4,0.4,0.7,0.6)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.05)
    onekey = dataHistos[plottype].keys()[0]
    leg.AddEntry(mcHistos[plottype][onekey], "t#bar{t} MC", "PLE")
    leg.AddEntry(dataHistos[plottype][onekey], "data", "PLE")
    

    line = ROOT.TF1("line","1",0.0,9000.0)
    line.SetLineColor(12) #Grey
    line.SetLineWidth(1)
    line.SetLineStyle(2) #Dashe
    
    allCanvas = []
    for var in dataHistos[plottype]:
        logging.debug("Drawing %s for %s", plottype, var)
        canvas = ROOT.TCanvas("c"+plottype+"_"+var,"c"+plottype+"_"+var, 5, 30, 640, 580)
        canvas.SetTopMargin(0.08*.75)
        canvas.SetRightMargin(0.04)
        canvas.SetLeftMargin(0.11)
        canvas.SetBottomMargin(0.12)
        canvas.SetTicks()
        canvas.cd()
        if normalized:
            dataHistos[plottype][var].GetYaxis().SetTitle("Normalized Units")
            dataHistos[plottype][var].DrawNormalized("PE")
            mcHistos[plottype][var].DrawNormalized("PESAME")
        else:
            dataHistos[plottype][var].Draw("PE")
            mcHistos[plottype][var].Draw("PESAME")
        leg.Draw("SAME")
        box["lumi"].Draw()
        box["CMS"].Draw()
        box["label"].Draw()
        canvas.Update()
        if plottype == "Efficiency":
            logging.info("Drawing line")
            line.Draw("SAME")

        canvas.Update()
        allCanvas.append(deepcopy(canvas))

    return allCanvas


def saveCanvasListAsPDF(listofCanvases, outputfilename, foldername):
    logging.info("Writing outputfile %s.pdf",outputfilename)
    for icanvas, canves in enumerate(listofCanvases):
        if icanvas == 0:
            canves.Print(foldername+"/"+outputfilename+".pdf(")
        elif icanvas == len(listofCanvases)-1:
            canves.Print(foldername+"/"+outputfilename+".pdf)")
        else:
            canves.Print(foldername+"/"+outputfilename+".pdf")

def saveHistosAsROOT(histosList, outfileName, foldername):
    logging.info("Writing outputfile %s.root",outfileName)
    out = ROOT.TFile(foldername+"/"+outfileName+".root", "RECREATE")
    out.cd()
    for obj in histosList:
        for plottype in obj.keys():
            for plot in obj[plottype].keys():
                obj[plottype][plot].Write()
    out.Close()


    
def TriggerSF(tag, offlinecuts):

    runcuts = ["RunB","RunCNoPre","RunD","RunE","RunF"]
    #runcuts = ["RunB","RunCNoPre","RunD"]
    #runcuts = ["RunC"]

    RunCuts = { "RunB": " (run>= 297020 && run<= 299329)",
                "RunC": " (run>= 299337 && run<= 302029)",
                "RunCPre": " (run>= 299337 && run<= 300999)",
                "RunCNoPre": " (run>= 301000 && run<= 302029)",
                "RunD": " (run>= 302030 && run<= 303434)",
                "RunE": " (run>= 303435 && run<= 304826)",
                "RunF": " (run>= 304911 && run<= 306462)",
    }

    tag += "_"+("tightCut" if offlinecuts else "looseCut")
    if runcuts:
        tag += "Run"
        for irun, run in enumerate(runcuts):
            if irun == 0:
                tag += run[len("Run"):]
            else:
                tag += "-"+run[len("Run"):]

    """ Old Binning
    if offlinecuts:
        htbins = [500,550,600,650,700,800,1000,1500,2000,2500]
        ptbins = [40,45,50,55,60,70,120,200]
        pt4bins = [40,50,60,80,100,120,200,300]
        nbbins = [2,3,4,8]
    else:
        htbins = [450,500,550,600,650,700,800,1000,1500,2000]
        ptbins = [35,40,45,50,55,60,70,120,200]
        pt4bins = [35,40,50,60,80,100,120,200,300]
        nbbins = [1,2,3,4,8]
    """

    #baseSel = "is_sl && abs(leps_pdgId[0]) == 13 && (HLT_BIT_HLT_IsoMu27)"
    baseSel = "is_sl && abs(leps_pdgId[0]) == 13 && (HLT_BIT_HLT_IsoMu27)"

    trigger = "(HLT_ttH_FH || HLT_BIT_HLT_PFJet500 || HLT_BIT_HLT_PFHT1050)"
    #trigger = "(HLT_ttH_FH)"
    triggerMC = trigger

    
    
    #trigger = "(HLT_BIT_HLT_HT300PT30_QuadJet_75_60_45_40_TripeCSV_p07|| HLT_BIT_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0)"
    #triggerMC = "(HLT_BIT_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0)"
    
    #trigger = "(HLT_BIT_HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 || HLT_BIT_HLT_PFHT430_SixJet40_BTagCSV_p080)"
    #triggerMC = "(HLT_BIT_HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5)"

    #trigger = "(HLT_BIT_HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 || HLT_BIT_HLT_PFHT430_SixJet40_BTagCSV_p080 || HLT_BIT_HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2 || HLT_BIT_HLT_PFHT380_SixJet32_DoubleBTagCSV_p075)"
    #triggerMC = "(HLT_BIT_HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5 || HLT_BIT_HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2)"

    #trigger = "(HLT_BIT_HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2 || HLT_BIT_HLT_PFHT380_SixJet32_DoubleBTagCSV_p075)"
    #triggerMC = "(HLT_BIT_HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2)"

    
    #trigger = "(HLT_BIT_HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2)"
    #trigger = "(HLT_BIT_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0)"
    #trigger = "(HLT_BIT_HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2 || HLT_BIT_HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0)"

    
    if offlinecuts:
        logging.warning("Will use tight offline cuts")
        baseSel += "&&(ht30>500 && jets_pt[5]> 40 && nBCSVM>=2)"
    else:
        logging.warning("Will use loose offline cuts")
        baseSel += "&&(ht30>450 && jets_pt[5]> 35 && nBCSVM>=1)"

    datacuts = ""
    if runcuts:
        datacuts = "&&(0"
        for run in runcuts:
            datacuts += "||"+RunCuts[run]
            logging.info("Adding run %s to datasel", run)
        datacuts += ")"

    logging.info("baseSel: %s", baseSel)
    logging.debug("datacuts: %s", datacuts)


    fdata = ROOT.TFile.Open("/mnt/t3nfs01/data01/shome/koschwei/scratch/ttH/skims/2017/ttH_AH_TriggerSF_v1p2/SingleMuon.root") 
    tdata = fdata.Get("tree")
        
    #MC files and stuff is WIP!!!
    mcFiles = { 
        "DL" : ROOT.TFile.Open("/mnt/t3nfs01/data01/shome/koschwei/scratch/ttH/skims/2017/ttH_AH_TriggerSF_v1p2/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root"),
        "SL" : ROOT.TFile.Open("/mnt/t3nfs01/data01/shome/koschwei/scratch/ttH/skims/2017/ttH_AH_TriggerSF_v1p2/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root"),
        "AH" : ROOT.TFile.Open("/mnt/t3nfs01/data01/shome/koschwei/scratch/ttH/skims/2017/ttH_AH_TriggerSF_v1p2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.root")
    }

    tag += "_all_plusHTplusJet_wPuGenB_binningv2"
    #tag += "_all_wPuGenB"
    foldername = "Trigger_plots_v2"

    if not os.path.exists(foldername):
        logging.warning("Creating folder: {0}".format(foldername))
        os.makedirs(foldername)
    
    scaleMCto = 1000*35.336
    mcWeight = "puWeight * (sign(genWeight)) * btagWeight_shape"
    mcInfo = { # (tree, xsec SF)
        "DL" : (mcFiles["DL"].Get("tree"), 90.578/float(8608726)),
        "SL" : (mcFiles["SL"].Get("tree"), 367.804/float(104846497)),
        "AH" : (mcFiles["SL"].Get("tree"), 373.3/float(40548871)),
    }

    logging.info("Will use **%s** as filename postfix",tag)
    make3DSFs(tag, tdata, mcInfo, scaleMCto, mcWeight, baseSel, trigger, triggerMC, datacuts, foldername, offlinecuts)

def make4DSFs(tdata, mcInfo, scaleMCto, mcWeight, baseSel, trigger, triggerMC, datacuts, foldername = ".", offlinecuts = True):
    logging.info("Making Base histos")
    treeVars = {
        "ht" : "ht30",
        "pt" : "jets_pt[5]",
        "pt4" : "jets_pt[3]",
        "nb" : "nBCSVM"
    }

    titles = {
        "ht" : ";#it{H}_{T} (GeV);Efficiency",
        "pt" : ";6th leading jet p_{T} (GeV);Efficiency",
        "pt4" : ";4th leading jet p_{T} (GeV);Efficiency",
        "nb" : ";Number of CSVM b tags;Efficiency",
    }
    
    binning = {
        "ht" :  [500,550,600,700,800,1000,1500,2000,2500],
        "pt" :  [40,45,50,60,70,120,200],
        "pt4" : [40,60,100,300],
        "nb" : [2,3,4,8],
    }
    
    BaseDataHistos = [
        ("ht", makeBaseHisto("hd_ht", ";HT[GeV];", binning["ht"], "Data")),
        ("pt", makeBaseHisto("hd_pt", ";6jpT[Gev];", binning["pt"], "Data")),
        ("pt4", makeBaseHisto("hd_pt4", ";4jpT[GeV];", binning["pt4"], "Data")),
        ("nb", makeBaseHisto("hd_nb", ";nBCSVM;", binning["nb"], "Data")),
    ]
    BaseMCHistos = [
        ("ht", makeBaseHisto("hm_ht", ";HT[GeV];", binning["ht"], "MC")),
        ("pt", makeBaseHisto("hm_pt", ";6jpT[Gev];", binning["pt"], "MC")),
        ("pt4", makeBaseHisto("hm_pt4", ";4jpT[GeV];", binning["pt4"], "MC")),
        ("nb", makeBaseHisto("hm_nb", ";nBCSVM;", binning["nb"], "MC")),
    ]

    Base3D = make3DBaseHisto(
        "h3", "h3",
        xbinning = binning["ht"],
        ybinning = binning["pt"],
        zbinning = binning["pt4"]
    )
    
    dataHistos = makeHistos(BaseDataHistos, "hData")
    mcSLHistos = {}
    for key in mcInfo:
        mcSLHistos[key] = makeHistos(BaseDataHistos, "hMC_"+key)
    mcHistos = makeHistos(BaseDataHistos, "hMC")

    data3DHistos = make3DHistos(Base3D, "h3Data", binning["nb"])
    mcSL3DHistos= {}
    for key in mcInfo:
        mcSL3DHistos[key] = make3DHistos(Base3D, "h3MC_"+key, binning["nb"])
    mc3DHistos = make3DHistos(Base3D, "h3MC", binning["nb"])
    sf3DHistos = make3DHistos(Base3D, "h3SF", binning["nb"], SFHisto = True)
    
    logging.info("Starting histogram filling")
    logging.info("Processing 2D histograms")
    hmcList = []
    h3mcList = []
    tmcList = []
    wmcList = []
    for key in mcInfo:
        hmcList.append(mcSLHistos[key])
        h3mcList.append(mcSL3DHistos[key])
        tmcList.append(mcInfo[key][0])
        wmcList.append(str(scaleMCto * mcInfo[key][1])+" * "+mcWeight)
        
    logging.info("MC samples:"+str(mcInfo.keys()))
    #FillMCHistos(tmcList, hmcList, mcHistos, treeVars, baseSel, triggerMC, wmcList)
    #FillDataHistos(tdata, dataHistos, treeVars, baseSel, trigger, "1"+datacuts)

    logging.info("Processing 3D histograms")
    FillData3DHistos(tdata, data3DHistos, (treeVars["ht"], treeVars["pt"], treeVars["pt4"]), treeVars["nb"], binning["nb"], baseSel, trigger, "1"+datacuts)
    FillMC3DHistos(tmcList, h3mcList, mc3DHistos, (treeVars["ht"], treeVars["pt"], treeVars["pt4"]), treeVars["nb"], binning["nb"], baseSel, triggerMC, wmcList)
    Make3DScaleFactors(data3DHistos, mc3DHistos, sf3DHistos)

    setEfficiencyStyle(dataHistos, titles)
    setEfficiencyStyle(mcHistos, titles)

    finalCEffs = makePlots(dataHistos, mcHistos)
    finalCTotals = makePlots(dataHistos, mcHistos,"Total", normalized = True)
    finalCTriggers = makePlots(dataHistos, mcHistos,"Triggered", normalized = True)

    
    saveCanvasListAsPDF(finalCEffs, "eff_out")
    saveCanvasListAsPDF(finalCTotals, "tot_out")
    saveCanvasListAsPDF(finalCTriggers, "trig_out")

    saveHistosAsROOT([data3DHistos, mc3DHistos, sf3DHistos], "sf3d_out")


def make3DSFs(tag, tdata, mcInfo, scaleMCto, mcWeight, baseSel, trigger, triggerMC, datacuts, foldername = ".", offlinecuts = True):
    logging.info("Making Base histos")
    treeVars = {
        "ht" : "ht30",
        "pt" : "jets_pt[5]",
        "pt4" : "jets_pt[3]",
        "nb" : "nBCSVM"
    }
    
    titles = {
        "ht" : ";#it{H}_{T} (GeV);Efficiency",
        "pt" : ";6th leading jet p_{T} (GeV);Efficiency",
        "pt4" : ";4th leading jet p_{T} (GeV);Efficiency",
        "nb" : ";Number of CSVM b tags;Efficiency",
    }

    if offlinecuts:
        binning = {
            "ht" :  [500,550,600,700,800,1000,1500,2500],
            #"ht" :  [500,550,600,700,800,1000,1500,2000,2500],
            "pt" :  [40,45,50,60,70,120,200],
            "pt4" : [40,60,100,300],
            "nb" : [2,3,4,8],
        }
        
    else:
        binning = {
            "ht" :  [450,500,550,600,700,800,1000,1500,2500],
            #"ht" :  [450,500,550,600,700,800,1000,1500,2000,2500],
            "pt" :  [35,40,45,50,60,70,120,200],
            "pt4" : [40,60,100,300],
            "nb" : [1,2,3,4,8],
        }
    
    BaseDataHistos = [
        ("ht", makeBaseHisto("hd_ht", ";HT[GeV];", binning["ht"], "Data")),
        ("pt", makeBaseHisto("hd_pt", ";6jpT[Gev];", binning["pt"], "Data")),
        ("pt4", makeBaseHisto("hd_pt4", ";4jpT[GeV];", binning["pt4"], "Data")),
        ("nb", makeBaseHisto("hd_nb", ";nBCSVM;", binning["nb"], "Data")),
    ]
    BaseMCHistos = [
        ("ht", makeBaseHisto("hm_ht", ";HT[GeV];", binning["ht"], "MC")),
        ("pt", makeBaseHisto("hm_pt", ";6jpT[Gev];", binning["pt"], "MC")),
        ("pt4", makeBaseHisto("hm_pt4", ";4jpT[GeV];", binning["pt4"], "MC")),
        ("nb", makeBaseHisto("hm_nb", ";nBCSVM;", binning["nb"], "MC")),
    ]

    Base3D = make3DBaseHisto(
        "h3", "h3",
        xbinning = binning["ht"],
        ybinning = binning["pt"],
        zbinning = binning["nb"]
    )
    
    dataHistos = makeHistos(BaseDataHistos, "hData")
    mcSLHistos = {}
    for key in mcInfo:
        mcSLHistos[key] = makeHistos(BaseDataHistos, "hMC_"+key)
    mcHistos = makeHistos(BaseDataHistos, "hMC")

    data3DHistos = make3DHistos(Base3D, "h3Data")
    mcSL3DHistos= {}
    for key in mcInfo:
        mcSL3DHistos[key] = make3DHistos(Base3D, "h3MC_"+key)
    mc3DHistos = make3DHistos(Base3D, "h3MC")
    sf3DHistos = make3DHistos(Base3D, "h3SF", SFHisto = True)
    
    logging.info("Starting histogram filling")
    logging.info("Processing 2D histograms")
    hmcList = []
    h3mcList = []
    tmcList = []
    wmcList = []
    for key in mcInfo:
        hmcList.append(mcSLHistos[key])
        h3mcList.append(mcSL3DHistos[key])
        tmcList.append(mcInfo[key][0])
        wmcList.append(str(scaleMCto * mcInfo[key][1])+" * "+mcWeight)
        
    logging.info("MC samples:"+str(mcInfo.keys()))
    FillMCHistos(tmcList, hmcList, mcHistos, treeVars, baseSel, triggerMC, wmcList)
    FillDataHistos(tdata, dataHistos, treeVars, baseSel, trigger, "1"+datacuts)

    logging.info("Processing 3D histograms")
    FillData3DHistos(tdata, data3DHistos, (treeVars["ht"], treeVars["pt"], treeVars["nb"]), None, None, baseSel, trigger, "1"+datacuts)
    FillMC3DHistos(tmcList, h3mcList, mc3DHistos, (treeVars["ht"], treeVars["pt"], treeVars["nb"]),  None, None, baseSel, triggerMC, wmcList)
    Make3DScaleFactors(data3DHistos, mc3DHistos, sf3DHistos)

    setEfficiencyStyle(dataHistos, titles)
    setEfficiencyStyle(mcHistos, titles)

    finalCEffs = makePlots(dataHistos, mcHistos)
    finalCTotals = makePlots(dataHistos, mcHistos,"Total", normalized = True)
    finalCTriggers = makePlots(dataHistos, mcHistos,"Triggered", normalized = True)

    
    saveCanvasListAsPDF(finalCEffs, "eff_out_3DSF_"+tag, foldername)
    saveCanvasListAsPDF(finalCTotals, "tot_out_3DSF_"+tag, foldername)
    saveCanvasListAsPDF(finalCTriggers, "trig_out_3DSF_"+tag, foldername)

    saveHistosAsROOT([data3DHistos, mc3DHistos, sf3DHistos], "sf3d_out_3DSF_"+tag, foldername)


if __name__ == "__main__":
    import argparse
    ##############################################################################################################
    ##############################################################################################################
    # Argument parser definitions:
    argumentparser = argparse.ArgumentParser(
        description='Description'
    )
    argumentparser.add_argument(
        "--tag",
        action = "store",
        required = True,
        type = str,
        help = "Set the tag used for the filename",
    )
    argumentparser.add_argument(
        "--looseOfflinecuts",
        action = "store_false",
        help = "If enabled, the loose offline cuts for SF measurement will be used",
    )
    args = argumentparser.parse_args()
    TriggerSF(tag = args.tag, offlinecuts = args.looseOfflinecuts)
