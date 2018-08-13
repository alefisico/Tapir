import os
from copy import copy, deepcopy
import ROOT
from array import array
import Helper


ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

def Slice3DHistoZ(h3, sliceAxisTitle = None, addTitle = None, identifier = None, plotSym = True, xTitle = None, yTitle = None, fillError = False, zTitle = None):
    thisSlices = []
    nZbins = h3.GetZaxis().GetNbins()
    nYbins = h3.GetYaxis().GetNbins()
    nXbins = h3.GetXaxis().GetNbins()
    xLowerBound = h3.GetXaxis().GetBinLowEdge(1)
    xUpperBound = h3.GetXaxis().GetBinUpEdge(nXbins)
    yLowerBound = h3.GetYaxis().GetBinLowEdge(1)
    yUpperBound = h3.GetYaxis().GetBinUpEdge(nYbins)

    if not plotSym:
        xEdges = []
        for xBin in range(nXbins+1):
            xEdges.append(h3.GetXaxis().GetBinUpEdge(xBin))
        yEdges = []
        for yBin in range(nYbins+1):
            yEdges.append(h3.GetYaxis().GetBinUpEdge(yBin))

    if identifier is not None:
        num = identifier
    else:
        num = ROOT.gRandom.Integer(1000)
    for z in range(1,nZbins+1):
        hName = "Slice_"+str(num)+"_zBin-"+str(z)

        if plotSym:
            hSlice = ROOT.TH2F(hName, hName, nXbins, 0, nXbins , nYbins,  0, nYbins)
            for x in range(1, nXbins+1):
                hSlice.GetXaxis().SetBinLabel(x,"{0:}-{1}".format(int(h3.GetXaxis().GetBinLowEdge(x)), int(h3.GetXaxis().GetBinUpEdge(x))))
            for y in range(1, nYbins+1):
                hSlice.GetYaxis().SetBinLabel(y,"{0:}-{1}".format(int(h3.GetYaxis().GetBinLowEdge(y)), int(h3.GetYaxis().GetBinUpEdge(y))))
        else:
            hSlice = ROOT.TH2F(hName, hName, nXbins, array("f", xEdges), nYbins, array("f", yEdges))

        if xTitle is None:
            hSlice.GetXaxis().SetTitle(h3.GetXaxis().GetTitle())
        else:
            hSlice.GetXaxis().SetTitle(xTitle)
        if yTitle is None:
            hSlice.GetYaxis().SetTitle(h3.GetYaxis().GetTitle())
        else:
            hSlice.GetYaxis().SetTitle(yTitle)
        if zTitle is not None:
            hSlice.GetZaxis().SetTitle(zTitle)
            hSlice.GetZaxis().SetTitleOffset(1.6)
        if sliceAxisTitle is not None:
            hTitle = sliceAxisTitle
        else:
            hTitle = h3.GetZaxis().GetTitle()
        if addTitle is not None:
            titlePrefix = addTitle
        else:
            titlePrefix = ""
        hSlice.SetTitle(titlePrefix+"{0} #leq {2} < {1}".format(h3.GetZaxis().GetBinLowEdge(z), h3.GetZaxis().GetBinUpEdge(z),hTitle))
        for x in range(1, nXbins+1):
            for y in range(1, nYbins+1):
                if not fillError:
                    val = h3.GetBinContent(x,y,z)
                    hSlice.SetBinContent(x,y, val)
                else:
                    val = h3.GetBinError(x,y,z)
                    hSlice.SetBinContent(x,y, val)
        thisSlices.append(hSlice)
    return thisSlices

def getSlices(inputfile, outputfile, h2slice, sliceTitle, h2slicepostfix = None, xTitle = None, yTitle = None, plotErrors = False, zTitle = None, is3DSF = False):
    rFile = ROOT.TFile(inputfile, "READ")
    SFHistos = []
    if h2slicepostfix is None:
        for key in rFile.GetListOfKeys():
            if h2slice in key.GetName():
                SFHistos.append(rFile.Get(key.GetName()))
    else:
        for key in rFile.GetListOfKeys():
            keyName = key.GetName()
            if keyName.startswith(h2slice) and keyName.endswith(h2slicepostfix):
                SFHistos.append(rFile.Get(key.GetName()))
    print SFHistos

    if is3DSF:
        bBins = { 0 : "" }
    else:
        bBins = { 0 : "- 2 #leq nBCSVM < 3",
                  1 : "- 3 #leq nBCSVM < 4",
                  2 : "- 4 #leq nBCSVM < 8",
        }
    SFHistos = sorted(SFHistos, key = lambda histo : histo.GetName())

    Slices = []
    for ih, hSF in enumerate(SFHistos):
        Slices.append(
            Slice3DHistoZ(
                hSF, sliceAxisTitle = sliceTitle, addTitle = "{0} ".format(bBins[ih]), identifier = ih,
                xTitle = xTitle, yTitle = yTitle, fillError = plotErrors, zTitle = zTitle
            )
        )
    """
    out = ROOT.TFile(outputfile+".root", "RECREATE")
    out.cd()
    for islice, slices in enumerate(Slices):        
        for sl in slices:
            sl.Write()
    out.Close()
    """
    return deepcopy(Slices)

def plotHistoList(hList, filename, folder):
    if not os.path.exists(folder):
        print "Making folder",folder
        os.mkdir(folder)

    lumi = Helper.luminosity
    box = Helper.create_paves(lumi, "DataWiP", CMSposX=0.155, CMSposY=0.82, 
                          prelimPosX=0.15, prelimPosY=0.77,
                          lumiPosX=0.977, lumiPosY=0.91, alignRight=False,
                          CMSsize=0.075*.75, prelimSize=0.057*.75, lumiSize=0.060*.75)

        
    for ihisto, histo in enumerate(hList):
        c = ROOT.TCanvas("c"+str(ihisto)+filename, "c"+str(ihisto)+filename, 1350, 1000)
        c.SetLeftMargin(0.115)
        c.SetRightMargin(0.16)
        c.cd()
        histo.Draw("colztext")
        box["CMS"].Draw("same")
        box["label"].Draw("same")
        if ihisto == 0:
            c.Print(folder+"/"+filename+".pdf(")
        elif ihisto == len(hList)-1:
            c.Print(folder+"/"+filename+".pdf)")
        else:
            c.Print(folder+"/"+filename+".pdf")

def main(SFFile, Plots4D, outPostFix):
    foldername = "TriggerSF_Slices_3D"
    #SFSlices = getSlices(SFFile, "SF_Slices_"+SFFile.split("/")[1], "scalefac")
    #EffMCSlices = getSlices(SFFile, "EffMC_Slices_"+SFFile.split("/")[1], "mc_eff")
    #EffDataSlices = getSlices(SFFile, "EffData_Slices_"+SFFile.split("/")[1], "data_eff")
    if Plots4D:
        SFSlices = getSlices(SFFile, "SF_Slices_"+SFFile.split(".")[0], "h3SF",  "p_{T,4}",
                             xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Scale Factor")
        SFErrSlices = getSlices(SFFile, "SFErr_Slices_"+SFFile.split(".")[0], "h3SF",  "p_{T,4}",
                                xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Scale Factor Error", plotErrors = True)

        EffMCSlices = getSlices(SFFile, "EffMC_Slices_"+SFFile.split(".")[0], "h3MC_eff", "p_{T,4}",
                                xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Efficiency")
        EffDataSlices = getSlices(SFFile, "EffData_Slices_"+SFFile.split(".")[0], "h3Data_eff", "p_{T,4}",
                                  xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Efficiency")

        EffErrMCSlices = getSlices(SFFile, "EffErrMC_Slices_"+SFFile.split(".")[0], "h3MC_eff", "p_{T,4}",
                                   xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", plotErrors = True, zTitle = "Efficiency Error")
        EffErrDataSlices = getSlices(SFFile, "EffErrData_Slices_"+SFFile.split(".")[0], "h3Data_eff", "p_{T,4}",
                                     xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", plotErrors = True, zTitle = "Efficiency Error")

        TotMCSlices = getSlices(SFFile, "TotMC_Slices_"+SFFile.split(".")[0], "h3MC_tot", "p_{T,4}",
                                xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Weighted Events")
        TotDataSlices = getSlices(SFFile, "TotData_Slices_"+SFFile.split(".")[0], "h3Data_tot", "p_{T,4}",
                                  xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Events")

        TrigMCSlices = getSlices(SFFile, "TrigMC_Slices_"+SFFile.split(".")[0], "h3MC_trig", "p_{T,4}",
                                 xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Weighted Events")
        TrigDataSlices = getSlices(SFFile, "TrigData_Slices_"+SFFile.split(".")[0], "h3Data_trig", "p_{T,4}",
                                   xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Events")
    else:
        SFSlices = getSlices(SFFile, "SF_Slices_"+SFFile.split(".")[0], "h3SF",  "nBCSVM",
                             xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Scale Factor", is3DSF = True)
        SFErrSlices = getSlices(SFFile, "SFErr_Slices_"+SFFile.split(".")[0], "h3SF",  "nBCSVM",
                                xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Scale Factor Error", plotErrors = True, is3DSF = True)

        EffMCSlices = getSlices(SFFile, "EffMC_Slices_"+SFFile.split(".")[0], "h3MC_eff", "nBCSVM",
                                xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Efficiency", is3DSF = True)
        EffDataSlices = getSlices(SFFile, "EffData_Slices_"+SFFile.split(".")[0], "h3Data_eff", "nBCSVM",
                                  xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Efficiency", is3DSF = True)

        EffErrMCSlices = getSlices(SFFile, "EffErrMC_Slices_"+SFFile.split(".")[0], "h3MC_eff", "nBCSVM",
                                   xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", plotErrors = True, zTitle = "Efficiency Error", is3DSF = True)
        EffErrDataSlices = getSlices(SFFile, "EffErrData_Slices_"+SFFile.split(".")[0], "h3Data_eff", "nBCSVM",
                                     xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", plotErrors = True, zTitle = "Efficiency Error", is3DSF = True)

        TotMCSlices = getSlices(SFFile, "TotMC_Slices_"+SFFile.split(".")[0], "h3MC_tot", "nBCSVM",
                                xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Weighted Denominator Events", is3DSF = True)
        TotDataSlices = getSlices(SFFile, "TotData_Slices_"+SFFile.split(".")[0], "h3Data_tot", "nBCSVM",
                                  xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Denominator Events", is3DSF = True)
        TotErrDataSlices = getSlices(SFFile, "TotData_Slices_"+SFFile.split(".")[0], "h3Data_tot", "nBCSVM", plotErrors = True,
                                  xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Denominator Events", is3DSF = True)

        TrigMCSlices = getSlices(SFFile, "TrigMC_Slices_"+SFFile.split(".")[0], "h3MC_trig", "nBCSVM",
                                 xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Weighted Numerator Events", is3DSF = True)
        TrigDataSlices = getSlices(SFFile, "TrigData_Slices_"+SFFile.split(".")[0], "h3Data_trig", "nBCSVM",
                                   xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Numerator Events", is3DSF = True)
        TrigErrDataSlices = getSlices(SFFile, "TrigData_Slices_"+SFFile.split(".")[0], "h3Data_trig", "nBCSVM", plotErrors = True,
                                   xTitle = "HT [GeV]", yTitle = "p_{T} of 6th jet", zTitle = "Numerator Events", is3DSF = True)

    print SFSlices
    plots = [
        ("SF", SFSlices), ("SFErr", SFErrSlices),
        ("EffMC", EffMCSlices), ("EffData", EffDataSlices),
        ("EffErrMC", EffErrMCSlices), ("EffErrData", EffErrDataSlices),
        ("TotMC", TotMCSlices), ("TotData", TotDataSlices),
        ("TotErrData", TotErrDataSlices), ("TrigErrData", TrigErrDataSlices),
        ("TrigMC", TrigMCSlices), ("TrigData", TrigDataSlices)
    ]
    for slName, slType in plots:
        for ih, slHisto in enumerate(slType):
            plotHistoList(slHisto, slName+"_"+str(ih)+outPostFix, foldername)
            
if __name__ == "__main__":
    #SFFile = "Trigger_plots/h3_sf_ttH_AH_v1_isSL_OverFlow_offlinecuts_RunCNoPre_RunD_RunE_RunF.root"
    SFFile = "Trigger_plots_v2/sf3d_out_3DSF_Finalv2_tightCutRunB-CNoPre-D-E-F_all_plusHTplusJet_wPuGenB_binningv2.root"
    #SFFile = "sf3d_out.root"
    main(SFFile, False, "finalv2")
