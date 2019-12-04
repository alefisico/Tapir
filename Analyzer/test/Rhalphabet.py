#!/usr/bin/env python
'''
File: BkgEstimation.py
Author: Alejandro Gomez Espinosa
Email: alejandro.gomez@cern.ch
Description: Bkg estimation. Check for options at the end.
'''

from ROOT import *
import rootpy.stl as stl
import time, os, math, sys, copy
from array import array
import argparse
from collections import OrderedDict
import subprocess
#from histoLabels import labels, labelAxis, finalLabels
import CMS_lumi as CMS_lumi
import tdrstyle as tdrstyle
#from commonFunctions import *
MapStrRootPtr = stl.map(stl.string, "TH1*")
StrHist = stl.pair(stl.string, "TH1*")

####gReset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)

xline = array('d', [0,2000])
yline = array('d', [1,1])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)

rhalPtList = [ '250', '300', '350', '400', '500', '2000' ]
#rhalPtList = [ '250','2000' ]

canvas = {}

def setSelection( listSel, xMin=0.65, yMax=0.65, align='right' ):

    for i in range( len( listSel ) ):
        textBox=TLatex()
        textBox.SetNDC()
        textBox.SetTextSize(0.04)
        if 'right' in align: textBox.SetTextAlign(31)
        textBox.SetTextFont(62) ### 62 is bold, 42 is normal
        textBox.DrawLatex(xMin, yMax, listSel[i])
        yMax = yMax -0.05


def buildPolynomialArray( iNVar0, iNVar1, iLabel0, iLabel1, iXMin0, iXMax0 ):

    iVars = []
    print "---- [buildPolynomialArray]"
    ## form of polynomial
    ## (p0r0 + p1r0 * pT + p2r0 * pT^2 + ...) +
    ## (p0r1 + p1r1 * pT + p2r1 * pT^2 + ...) * rho +
    ## (p0r2 + p1r2 * pT + p2r2 * pT^2 + ...) * rho^2 + ...

    for i0 in range(iNVar0+1):
       for i1 in range(iNVar1+1):
           pVar = iLabel1+str(i1)+iLabel0+str(i0);
           pXMin = iXMin0
           pXMax = iXMax0
           pVal  = math.pow(10,1-i1)
           pRooVar = RooRealVar(pVar,pVar,0.0,pXMin*pVal,pXMax*pVal)
           print pVar,pVal,"!!!!!!!!!!"
           iVars.append(pRooVar)
    return iVars
######################################################

def computeDDTMap(working_point,deepboosted_rho_pt):
    """docstring for computeDDTMap based on https://gitlab.cern.ch/abenecke/scripts/blob/master/diboson/taggerstudies/create_2D_decorrelation.py"""
    ddtMap= deepboosted_rho_pt.Project3D("yx");
#    ddtMap.SetName(ddtMapName);
    ddtMap.Reset();
    ddtMap.SetStats(0);
    ddtMap.SetDirectory(0);
    nbins_x = ddtMap.GetNbinsX();
    nbins_y = ddtMap.GetNbinsY();

    for xbin in range(1, nbins_x):
        for ybin in range(1,nbins_y):
            DeepBoostedproj = deepboosted_rho_pt.ProjectionZ("Rho2D", xbin, xbin, ybin, ybin);
            # Protection against default values
            # for bin in range(1,DeepBoostedproj.GetNbinsX()):
                # if DeepBoostedproj.GetBinCenter(bin)<0:
                #     DeepBoostedproj.SetBinContent(bin,0);

            if DeepBoostedproj.Integral() == 0:
                xval = deepboosted_rho_pt.GetXaxis().GetBinCenter(xbin)
                yval = deepboosted_rho_pt.GetYaxis().GetBinCenter(ybin)
#                print "Caution Integral 0!"
                ddtMap.SetBinContent(xbin,ybin,0)
                continue

            wp = array('d',[working_point])
            quantieles = array('d', [0.])
            DeepBoostedproj.GetQuantiles(1,quantieles , wp)
            ddtMap.SetBinContent(xbin,ybin,quantieles[0])

    return ddtMap;


######################################################
def massDecorrelation( name  ):
    """docstring for massDecorrelation based on https://gitlab.cern.ch/abenecke/scripts/blob/master/diboson/taggerstudies/create_2D_decorrelation.py"""

    bkgHistos = OrderedDict()
    for bkgSamples in bkgFiles:
        if not bkgSamples.startswith("TTToSemi"): continue
        newName = name# .replace('___', ivar+'_').replace('__', '_'+side+'_')
        bkgHistos[ bkgSamples+'3D' ] = bkgFiles[ bkgSamples ][0].Get( 'tthbb13/'+newName )
        #bkgHistos[ bkgSamples+'3D' ].SetTitle(bkgSamples+ivar+side)
        bkgHistos[ bkgSamples+'3D' ].Scale( bkgFiles[ bkgSamples ][1] )
        #try: bkgHistos[ ivar+side ].Add( bkgHistos[ bkgSamples+ivar+side ].Clone() )
        #except (KeyError, AttributeError) as e: bkgHistos[ ivar+side ] = bkgHistos[ bkgSamples+ivar+side ].Clone()

        #create 2D projections
        DeepBoosted_v_rho = TH2D("DeepBoosted_v_rho","DeepBoosted_v_rho",14,-7.0,0,40,0.,1.0);
        DeepBoosted_v_pt = TH2D("DeepBoosted_v_pt","DeepBoosted_v_pt",150,0,1500,40,0.,1.0);
        NBins_rho = bkgHistos[ bkgSamples+'3D' ].GetNbinsX();
        NBins_pt = bkgHistos[ bkgSamples+'3D' ].GetNbinsY();
        NBins_DeepBoosted = bkgHistos[ bkgSamples+'3D' ].GetNbinsZ();

        print "Bins(x,y,z): " + str(NBins_rho) + "  ,  " + str(NBins_pt) + "  ,  " + str(NBins_DeepBoosted)

        for rhoBin in range(1,NBins_rho):
            for ptBin in range(1,NBins_pt):
                for DeepBoostedBin in range(1,NBins_DeepBoosted):
                    rho = bkgHistos[ bkgSamples+'3D' ].GetXaxis().GetBinCenter(rhoBin)
                    pt = bkgHistos[ bkgSamples+'3D' ].GetYaxis().GetBinCenter(ptBin)
                    DeepBoosted = bkgHistos[ bkgSamples+'3D' ].GetZaxis().GetBinCenter(DeepBoostedBin)
                    DeepBoosted_v_rho.Fill(rho,DeepBoosted,bkgHistos[ bkgSamples+'3D' ].GetBinContent(rhoBin,ptBin,DeepBoostedBin));
                    DeepBoosted_v_pt.Fill(pt,DeepBoosted,bkgHistos[ bkgSamples+'3D' ].GetBinContent(rhoBin,ptBin,DeepBoostedBin));

        print "Done!"

        canvas['deepBoostedrho'] = TCanvas('deepBoostedrho', 'deepBoostedrho',  10, 10, 750, 750 )
        DeepBoosted_v_rho.Draw("colz")
        canvas['deepBoostedrho'].SaveAs('Plots/deepBoostedrho.png')

        canvas['deepBoostedpt'] = TCanvas('deepBoostedpt', 'deepBoostedpt',  10, 10, 750, 750 )
        DeepBoosted_v_pt.Draw("colz")
        canvas['deepBoostedpt'].SaveAs('Plots/deepBoostedpt.png')

        for xbin in range(1,DeepBoosted_v_rho.GetNbinsX()+1):
            proj = DeepBoosted_v_rho.ProjectionY("_y",xbin,xbin)
            if not proj.Integral() == 0:
                proj.Scale(1/proj.Integral())
            if not xbin%10:
                print "rho bin  " + str(DeepBoosted_v_rho.GetXaxis().GetBinCenter(xbin))
                c1 = TCanvas("c"+str(xbin), "c"+str(xbin), 600, 600);
                gStyle.SetOptStat(kFALSE);
                gStyle.SetPadTickY(1);
                gStyle.SetPadTickX(1);
                gStyle.SetLegendBorderSize(0);
                gPad.SetBottomMargin(.2);
                gPad.SetRightMargin(.2);

                leg=TLegend(0.2,0.7,0.4,0.9,"","brNDC")
                leg.SetHeader("#splitline{rho = " + str(DeepBoosted_v_rho.GetXaxis().GetBinCenter(xbin))+"}{averaged in pT}")
                leg.SetBorderSize(0);
                leg.SetTextSize(0.035);
                leg.SetFillColor(0);
                leg.SetLineColor(1);
                leg.SetTextFont(42);


                proj.GetXaxis().SetRangeUser(0,1)
                proj.GetXaxis().SetTitle("DeepBoosted")
                proj.GetYaxis().SetTitle("#Delta N /N")
                #proj.GetXaxis().SetLabelSize(ldsize)

                proj.Draw()

                txbin_0p02 = -99
                txbin_0p05 = -99
                first = True
                for bin in range(1,proj.GetNbinsX()+1):
                    inte = proj.Integral(0,bin)

                    if inte >= 0.98:
                        txbin_0p02 = proj.GetBinCenter(bin)
                        break
                    if inte >= 0.95 and first:
                        txbin_0p05 = proj.GetBinCenter(bin)
                        first = False


                line_0p02 = TLine(txbin_0p02,0,txbin_0p02,1)
                line_0p02.SetLineColor(kBlue)
                line_0p02.Draw("same")

                leg.AddEntry(line_0p02,"2% mistag rate","l")

                line_0p05 = TLine(txbin_0p05,0,txbin_0p05,1)
                line_0p05.SetLineColor(kRed)
                line_0p05.Draw("same")

                leg.AddEntry(line_0p05,"5% mistag rate","l")
                leg.Draw()
                c1.SetLogy()
                c1.SaveAs("Plots/Proj"+str(xbin)+".png");

        #calculated Map
        ddt_0p05= computeDDTMap(0.95,bkgHistos[ bkgSamples+'3D' ]);

        ddt_0p05.SetTitle("Simple DeepBoosted-DDT map");
        ddt_0p05.SetTitle("Rho2D");
        c1 = TCanvas("c1", "c1", 600, 600);
        gPad.SetRightMargin(0.2);
        ddt_0p05.GetXaxis().SetRangeUser(-6.0,-1);
        ddt_0p05.GetYaxis().SetRangeUser(0,2000);
        ddt_0p05.GetZaxis().SetRangeUser(0,1);
        ddt_0p05.Draw("colz");
        c1.SaveAs("Plots/DDT_0p05.png");
        ddt_0p05.GetZaxis().SetRangeUser(0.6,1);
        c1.SaveAs("Plots/DDT_0p05_scale.png");



######################################################
def BkgEstimation( name, xmin, xmax, rebinX, axisX='', axisY='', labX=0.92, labY=0.50, log=False, ext='png' ):
    """Bkg Estimation with rhalphabet method based on https://github.com/cmantill/ZPrimePlusJet/blob/56818fd461b549863ad56a2ed424c68c46fedff4/fitting/ZqqJet/resultsfeb20/buildRhalphabet.py"""

    ### Initializing RooFit variables
    MSD = RooRealVar( 'msd', 'msd', xmin, xmax )
    MSD.setBins( rebinX )
    PT = RooRealVar( 'pt', 'pt', 0, 1500 )
    PT.setBins( 1500 )
    #RHO = RooFormulaVar( "rho", "log(msd*msd/pt/pt)", RooArgList( MSD, PT ) )
    RHO = RooRealVar( "rho", "rho", -6., -4. )
    EFF = RooRealVar( "veff", "veff", 0.5, 0., 1.0)
    DM = RooRealVar("dm","dm", 0.,-10,10)
    SHIFT = RooFormulaVar( "shift", "msd-dm", RooArgList( MSD, DM ) )

    cats = RooCategory( "sample", "sample" )
    cats.defineType("mass") #,1)
    cats.defineType("rho") #,0)
    rooDict = OrderedDict()


#	if 'DATA' in args.process:
#		dataHistos = {}
#		dataHistos[ 'DATA' ] = dataFile.Get( nameInRoot+'_JetHT_Run2016'+tmpRegion if args.miniTree else args.boosted+'AnalysisPlots'+('' if 'pruned' in args.grooming else args.grooming)+'/'+nameInRoot  )
#		if 'massAve' in nameInRoot:
#			dataHistos[ 'DATA' ] = dataHistos[ 'DATA' ].Rebin( len( boostedMassAveBins )-1, dataHistos[ 'DATA' ].GetName(), boostedMassAveBins )
#			dataHistos[ 'DATA' ].Scale ( 1, 'width' )
#		elif rebinX > 1: dataHistos[ 'DATA' ] = dataHistos[ 'DATA' ].Rebin( rebinX )
#        legend.AddEntry( dataHistos[ 'DATA' ], 'Data', 'lep' )
#        if Norm: dataHistos[ 'DATA' ].Scale( 1 /dataHistos['DATA'].Integral() )


    ### Opening bkg plots
    bkgHistos = OrderedDict()
    for side in ['Fail', 'Pass']:
        for ivar in [ 'MassPt', 'RhoPt', 'RhoPtMass' ]:
            for bkgSamples in bkgFiles:
                newName = name.replace('___', ivar+'_').replace('__', '_'+side+'_')
                bkgHistos[ bkgSamples+ivar+side ] = bkgFiles[ bkgSamples ][0].Get( 'tthbb13/'+newName )
                bkgHistos[ bkgSamples+ivar+side ].SetTitle(bkgSamples+ivar+side)
                bkgHistos[ bkgSamples+ivar+side ].Scale( bkgFiles[ bkgSamples ][1] )
                try: bkgHistos[ ivar+side ].Add( bkgHistos[ bkgSamples+ivar+side ].Clone() )
                except (KeyError, AttributeError) as e: bkgHistos[ ivar+side ] = bkgHistos[ bkgSamples+ivar+side ].Clone()

            ### Making the 1D plots binned in Pt
            if ivar.endswith('Pt'):
                for ptbin in range(len(rhalPtList)-1):
                    bkgHistos[ ivar+side+rhalPtList[ptbin] ] = bkgHistos[ ivar+side ].ProjectionX( ivar+side+rhalPtList[ptbin], int(rhalPtList[ptbin]), int(rhalPtList[ptbin+1]) )
                    bkgHistos[ ivar+side+rhalPtList[ptbin] ].Rebin(2)
    ##############################

    ### Making simple ratio plots
    for ptbin in rhalPtList:
        if ptbin.endswith(rhalPtList[-1]): continue  ### last

        #### Making the ratio pass/fail
        bkgHistos[ 'RhoPt'+ptbin ] = TGraphAsymmErrors()
        tmpPass = bkgHistos[ 'RhoPtPass'+ptbin ].Clone()
        tmpFail = bkgHistos[ 'RhoPtFail'+ptbin ].Clone()
        binWidth = int(tmpPass.GetBinWidth(1))

        tmpPass.Scale( 1/tmpPass.Integral() )
        tmpFail.Scale( 1/tmpFail.Integral() )
        bkgHistos[ 'RhoPt'+ptbin ].Divide( tmpPass, tmpFail, 'pois')

        ### simple root fit
        bkgHistos[ 'FitRhoPt'+ptbin ] = TF1( 'fitRhoPt', 'pol1', -6, -1)
        bkgHistos[ 'RhoPt'+ptbin ].Fit( 'fitRhoPt', 'MIR' )
        bkgHistos[ 'RhoPt'+ptbin ].Fit( 'fitRhoPt', 'MIR' )
        #### bkg fail x fit
        BkgEst = tmpFail.Clone()
        BkgEst.Multiply(bkgHistos[ 'FitRhoPt'+ptbin ])

        #### simple plots
        legend=TLegend(0.65,0.65,0.90,0.83)
        legend.SetFillStyle(0)
        legend.SetTextSize(0.03)

        legend.AddEntry( tmpPass, 'Bkg pass ptbin('+ptbin+')', 'p'  )
        legend.AddEntry( tmpFail, 'Bkg fail ptbin('+ptbin+')', 'l'  )
        legend.AddEntry( BkgEst, 'Bkg fail x polynomial', 'l'  )

        tdrStyle.SetPadRightMargin(0.05)
        tdrStyle.SetPadLeftMargin(0.15)
        canvas['bkgEst'+ptbin] = TCanvas('c1bkgEst'+ptbin, 'c1bkgEst'+ptbin,  10, 10, 750, 750 )
        pad1 = TPad("pad1"+ptbin, "Fit"+ptbin, 0,0.207,1.00,1.00,-1)
        pad2 = TPad("pad2"+ptbin, "Pull"+ptbin, 0,0.00,1.00,0.30,-1);
        pad1.Draw()
        pad2.Draw()

        pad1.cd()
        tmpPass.SetMarkerStyle(8)
        tmpPass.GetXaxis().SetRangeUser( -10, 2 )
        tmpPass.GetYaxis().SetTitle( 'Normalized/'+str(binWidth)+' [GeV]' )
        tmpFail.SetLineColor(kBlue)
        BkgEst.SetLineColor(kRed)
        tmpPass.Draw()
        tmpFail.Draw("hist same")
        BkgEst.Draw("hist same")
        legend.Draw()

        CMS_lumi.cmsTextOffset = 0.0
        CMS_lumi.relPosX = 0.13
        CMS_lumi.CMS_lumi(pad1, 4, 0)

        pad2.cd()
        gStyle.SetOptFit(1)
        pad2.SetGrid()
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.3)
        tmpPad2= pad2.DrawFrame(-10, 0, 2, 2)

        tmpPad2.GetXaxis().SetTitle( 'Higgs candidate #rho' )
        tmpPad2.GetYaxis().SetTitle( "Pass/Fail" )
        tmpPad2.GetYaxis().SetTitleOffset( 0.5 )
        tmpPad2.GetYaxis().CenterTitle()
        tmpPad2.SetLabelSize(0.12, 'x')
        tmpPad2.SetTitleSize(0.12, 'x')
        tmpPad2.SetLabelSize(0.12, 'y')
        tmpPad2.SetTitleSize(0.12, 'y')
        tmpPad2.SetNdivisions(505, 'x')
        tmpPad2.SetNdivisions(505, 'y')
        pad2.Modified()
        bkgHistos[ 'RhoPt'+ptbin ].SetMarkerStyle(8)
        bkgHistos[ 'RhoPt'+ptbin ].Draw('P')
        bkgHistos[ 'FitRhoPt'+ptbin ].Draw("same")
        pad2.Update()
        st1 = bkgHistos[ 'RhoPt'+ptbin ].GetListOfFunctions().FindObject("stats")
        st1.SetX1NDC(.75)
        st1.SetX2NDC(.95)
        st1.SetY1NDC(.75)
        st1.SetY2NDC(.95)
        pad2.Modified()

        outputFileName = name.replace('__', '_RhoPt'+ptbin+'_')+'_PassFailPlots_'+args.version+'.'+ext
        if log: outputFileName = outputFileName.replace('Plots','Plots_Log')
        print('Processing.......', outputFileName)
        canvas['bkgEst'+ptbin].SaveAs( 'Plots/'+ outputFileName )

        #### Making the ratio pass/fail
        bkgHistos[ 'MassPt'+ptbin ] = TGraphAsymmErrors()
        tmpPass = bkgHistos[ 'MassPtPass'+ptbin ].Clone()
        tmpFail = bkgHistos[ 'MassPtFail'+ptbin ].Clone()
        for i in range(12,15):
            tmpPass.SetBinContent( i, 0 )
            tmpPass.SetBinError( i, 0 )
            tmpFail.SetBinContent( i, 0 )
            tmpFail.SetBinError( i, 0 )
        binWidth = int(tmpPass.GetBinWidth(1))

        #tmpPass.Scale( 1/tmpPass.Integral() )
        #tmpFail.Scale( 1/tmpFail.Integral() )
        bkgHistos[ 'MassPt'+ptbin ].Divide( tmpPass, tmpFail, 'pois')

        #### simple root fit
        fitLine = TF1( 'fitLine', 'pol4', xmin, 300)
        bkgHistos[ 'MassPt'+ptbin ].Fit( 'fitLine', 'MIR' )
        bkgHistos[ 'MassPt'+ptbin ].Fit( 'fitLine', 'MIR' )
        #### bkg fail x fit
        BkgEst = tmpFail.Clone()
        BkgEst.Multiply(fitLine)

        #### simple plots
        legend=TLegend(0.65,0.65,0.90,0.83)
        legend.SetFillStyle(0)
        legend.SetTextSize(0.03)

        legend.AddEntry( tmpPass, 'Bkg pass ptbin('+ptbin+')', 'p'  )
        legend.AddEntry( tmpFail, 'Bkg fail ptbin('+ptbin+')', 'l'  )
        legend.AddEntry( BkgEst, 'Bkg fail x polynomial', 'l'  )

        tdrStyle.SetPadRightMargin(0.05)
        tdrStyle.SetPadLeftMargin(0.15)
        canvas['bkgEstMassPt'+ptbin] = TCanvas('c1bkgEstMassPt'+ptbin, 'c1bkgEstMassPt'+ptbin,  10, 10, 750, 750 )
        pad1 = TPad("pad1"+ptbin, "Fit"+ptbin, 0,0.207,1.00,1.00,-1)
        pad2 = TPad("pad2"+ptbin, "Pull"+ptbin, 0,0.00,1.00,0.30,-1);
        pad1.Draw()
        pad2.Draw()

        pad1.cd()
        tmpPass.SetMarkerStyle(8)
        tmpPass.GetXaxis().SetRangeUser( xmin, xmax )
        tmpPass.SetMaximum( 1.1*max(tmpPass.GetMaximum(), tmpFail.GetMaximum()) )
        #tmpPass.GetYaxis().SetTitle( 'Normalized/'+str(binWidth)+' [GeV]' )
        tmpPass.GetYaxis().SetTitle( 'Events/'+str(binWidth)+' [GeV]' )
        tmpFail.SetLineColor(kBlue)
        BkgEst.SetLineColor(kRed)
        tmpPass.Draw()
        tmpFail.Draw("hist same")
        BkgEst.Draw("hist same")
        legend.Draw()

        CMS_lumi.cmsTextOffset = 0.0
        CMS_lumi.relPosX = 0.13
        CMS_lumi.CMS_lumi(pad1, 4, 0)

        pad2.cd()
        gStyle.SetOptFit(1)
        pad2.SetGrid()
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.3)
        tmpPad2= pad2.DrawFrame(xmin, 0, xmax, .2)

        tmpPad2.GetXaxis().SetTitle( 'Higgs candidate softdrop mass [GeV]' )
        tmpPad2.GetYaxis().SetTitle( "Pass/Fail" )
        tmpPad2.GetYaxis().SetTitleOffset( 0.5 )
        tmpPad2.GetYaxis().CenterTitle()
        tmpPad2.SetLabelSize(0.12, 'x')
        tmpPad2.SetTitleSize(0.12, 'x')
        tmpPad2.SetLabelSize(0.12, 'y')
        tmpPad2.SetTitleSize(0.12, 'y')
        tmpPad2.SetNdivisions(505, 'x')
        tmpPad2.SetNdivisions(505, 'y')
        pad2.Modified()
        bkgHistos[ 'MassPt'+ptbin ].SetMarkerStyle(8)
        bkgHistos[ 'MassPt'+ptbin ].Draw('P')
        fitLine.Draw("same")
        pad2.Update()
        st1 = bkgHistos[ 'MassPt'+ptbin ].GetListOfFunctions().FindObject("stats")
        st1.SetX1NDC(.75)
        st1.SetX2NDC(.95)
        st1.SetY1NDC(.75)
        st1.SetY2NDC(.95)
        pad2.Modified()

        outputFileName = name.replace('__', '_Pt'+ptbin+'_')+'_PassFailPlots_'+args.version+'.'+ext
        if log: outputFileName = outputFileName.replace('Plots','Plots_Log')
        print('Processing.......', outputFileName)
        canvas['bkgEstMassPt'+ptbin].SaveAs( 'Plots/'+ outputFileName )
        ##############################################

        ############# TEST
        #### bkg fail x fit
        BkgEst = bkgHistos[ 'MassPtFail'+ptbin ].Clone()
        #BkgEst.Multiply(bkgHistos[ 'FitRhoPt'+ptbin ])
        BkgEst.Multiply(fitLine)
        MCPass = bkgHistos[ 'MassPtPass'+ptbin ].Clone()
        Ratio = TGraphAsymmErrors()
        Ratio.Divide(MCPass.Clone(), BkgEst, 'pois')

        #### simple plots
        legend=TLegend(0.65,0.65,0.90,0.83)
        legend.SetFillStyle(0)
        legend.SetTextSize(0.03)

        legend.AddEntry( MCPass, 'Bkg pass ptbin('+ptbin+')', 'p'  )
        legend.AddEntry( BkgEst, 'Bkg fail x polynomial', 'l'  )

        tdrStyle.SetPadRightMargin(0.05)
        tdrStyle.SetPadLeftMargin(0.15)
        canvas['bkgEst'+ptbin] = TCanvas('c1bkgEst'+ptbin, 'c1bkgEst'+ptbin,  10, 10, 750, 750 )
        pad1 = TPad("pad1"+ptbin, "Fit"+ptbin, 0,0.207,1.00,1.00,-1)
        finalPad2 = TPad("finalPad2"+ptbin, "Pull"+ptbin, 0,0.00,1.00,0.30,-1);
        pad1.Draw()
        finalPad2.Draw()

        pad1.cd()
        MCPass.SetMarkerStyle(8)
        MCPass.GetXaxis().SetRangeUser( xmin, xmax )
        MCPass.GetYaxis().SetTitle( 'Events/'+str(binWidth)+' [GeV]' )
        BkgEst.SetLineColor(kRed)
        MCPass.Draw()
        BkgEst.Draw("histe same")
        legend.Draw()

        CMS_lumi.cmsTextOffset = 0.0
        CMS_lumi.relPosX = 0.13
        CMS_lumi.CMS_lumi(pad1, 4, 0)

        finalPad2.cd()
        finalPad2.SetGrid()
        finalPad2.SetTopMargin(0)
        finalPad2.SetBottomMargin(0.3)
        tmpfinalPad2= finalPad2.DrawFrame(xmin, 0, xmax, 2)

        tmpfinalPad2.GetXaxis().SetTitle( 'Higgs candidate softdrop mass [GeV]' )
        tmpfinalPad2.GetYaxis().SetTitle( "Pass/Fail" )
        tmpfinalPad2.GetYaxis().SetTitleOffset( 0.5 )
        tmpfinalPad2.GetYaxis().CenterTitle()
        tmpfinalPad2.SetLabelSize(0.12, 'x')
        tmpfinalPad2.SetTitleSize(0.12, 'x')
        tmpfinalPad2.SetLabelSize(0.12, 'y')
        tmpfinalPad2.SetTitleSize(0.12, 'y')
        tmpfinalPad2.SetNdivisions(505, 'x')
        tmpfinalPad2.SetNdivisions(505, 'y')
        finalPad2.Modified()
        Ratio.SetMarkerStyle(8)
        Ratio.Draw('P')
        finalPad2.Update()

        outputFileName = name.replace('__', '_Final'+ptbin+'_')+'_PassFailPlots_'+args.version+'.'+ext
        if log: outputFileName = outputFileName.replace('Plots','Plots_Log')
        print('Processing.......', outputFileName)
        canvas['bkgEst'+ptbin].SaveAs( 'Plots/'+ outputFileName )
        ######################

#        ### For Roofit creating Roorealvar, datasets, etc..
#        a0 = RooRealVar("a0", "a0", 0, -1, 1)
#        a1 = RooRealVar("a1", "a1", 0, -1, 1)
#        a2 = RooRealVar("a2", "a2", 0, -1, 1)
#        a3 = RooRealVar("a3", "a3", 0, -1, 1)
#        tmpRooArgListMass = RooArgList( a0, a1, a2, a3 )
#        rooDict[ 'BernsteinMass'+ptbin ] = RooBernstein( "bkgMass"+ptbin, "bkgMass"+ptbin, MSD, tmpRooArgListMass )
#        rooDict[ 'PassFailMass'+ptbin ] = RooDataHist( 'PassFailMass'+ptbin, 'PassFailMass'+ptbin, RooArgList(MSD), bkgHistos[ 'MassPt'+ptbin ].GetHistogram() )
#        b0 = RooRealVar("b0", "b0", 0, -1, 1)
#        b1 = RooRealVar("b1", "b1", 0, -1, 1)
#        b2 = RooRealVar("b2", "b2", 0, -1, 1)
#        b3 = RooRealVar("b3", "b3", 0, -1, 1)
#        tmpRooArgListRho = RooArgList( b0, b1, b2, b3 )
#        rooDict[ 'BernsteinRho'+ptbin ] = RooBernstein( "bkgRho"+ptbin, "bkgRho"+ptbin, MSD, tmpRooArgListRho )
#        rooDict[ 'PassFailRho'+ptbin ] = RooDataHist( 'PassFailRho'+ptbin, 'PassFailRho'+ptbin, RooArgList(RHO), bkgHistos[ 'RhoPt'+ptbin ].GetHistogram() )
#
#        histosMap = MapStrRootPtr()
#        histosMap.insert(StrHist("rho", bkgHistos[ 'MassPt'+ptbin ].GetHistogram()))
#        histosMap.insert(StrHist("mass", bkgHistos[ 'MassPt'+ptbin ].GetHistogram()))
#        #combData = RooDataHist("combdata", "combdata", RooArgSet(MSD), RooFit.Index(cats), RooFit.Import("mass", rooDict[ 'PassFailMass'+ptbin ]), RooFit.Import("rho", rooDict[ 'PassFailRho'+ptbin ]) )
#        combData = RooDataHist("combdata", "combdata", RooArgList(MSD), cats, histosMap )
#        rooDict[ 'lTot'+ptbin ] = RooSimultaneous( 'tot'+ptbin, 'tot'+ptbin, cats )
#        rooDict[ 'lTot'+ptbin ].addPdf( rooDict[ 'BernsteinMass'+ptbin ], "mass" )
#        rooDict[ 'lTot'+ptbin ].addPdf( rooDict[ 'BernsteinRho'+ptbin ], "rho" )
#        rooDict[ 'lTot'+ptbin ].Print()


        '''
        ## Normalization
        rooDict[ 'NTot'+ptbin ] = RooRealVar( 'norm'+ptbin, 'norm'+ptbin, (bkgHistos[ 'MassPtPass'+ptbin ].Integral()+bkgHistos[ 'MassPtFail'+ptbin ].Integral()), 0, 5*(bkgHistos[ 'MassPtPass'+ptbin ].Integral()+bkgHistos[ 'MassPtFail'+ptbin ].Integral()) )
        rooDict[ 'NPass'+ptbin ] = RooFormulaVar( 'fMassPtPass'+ptbin, 'norm'+ptbin+"*(veff)", RooArgList( rooDict[ 'NTot'+ptbin ], EFF ) )
        rooDict[ 'NFail'+ptbin ] = RooFormulaVar( 'fMassPtFail'+ptbin, 'norm'+ptbin+"*(1-veff)", RooArgList( rooDict[ 'NTot'+ptbin ], EFF ) )
        ## shapes
        rooDict[ 'PData'+ptbin ] = RooDataHist( 'MassPassDatahist'+ptbin, 'MassPassDatahist'+ptbin, RooArgList(MSD), bkgHistos[ 'MassPtPass'+ptbin ] )
        rooDict[ 'FData'+ptbin ] = RooDataHist( 'MassFailDatahist'+ptbin, 'MassFailDatahist'+ptbin, RooArgList(MSD), bkgHistos[ 'MassPtFail'+ptbin ] )
        rooDict[ 'P'+ptbin ] = RooHistPdf( 'MassPassRooHistPdf'+ptbin, 'MassPassRooHistPdf'+ptbin, RooArgList(SHIFT), RooArgList(MSD), rooDict[ 'PData'+ptbin ], 0 )
        rooDict[ 'F'+ptbin ] = RooHistPdf( 'MassFailRooHistPdf'+ptbin, 'MassFailRooHistPdf'+ptbin, RooArgList(SHIFT), RooArgList(MSD), rooDict[ 'FData'+ptbin ], 0 )
        ## extended likelihood from normalization and shape above
        rooDict[ 'EP'+ptbin ] = RooExtendPdf( 'MassPassExtPdf'+ptbin, 'MassPassExtPdf'+ptbin, rooDict[ 'P'+ptbin ], rooDict[ 'NFail'+ptbin ] )
        rooDict[ 'EF'+ptbin ] = RooExtendPdf( 'MassFailExtPdf'+ptbin, 'MassFailExtPdf'+ptbin, rooDict[ 'F'+ptbin ], rooDict[ 'NFail'+ptbin ] )

        rooDict[ 'TotP'+ptbin ] = RooAddPdf( 'tot_pass'+ptbin, 'tot_pass'+ptbin, RooArgList(rooDict[ 'P'+ptbin ]))
        rooDict[ 'TotF'+ptbin ] = RooAddPdf( 'tot_fail'+ptbin, 'tot_fail'+ptbin, RooArgList(rooDict[ 'F'+ptbin ]))

        rooDict[ 'lTot'+ptbin ] = RooSimultaneous( 'tot'+ptbin, 'tot'+ptbin, cats )
        rooDict[ 'lTot'+ptbin ].addPdf( rooDict[ 'TotP'+ptbin ], "pass" )
        rooDict[ 'lTot'+ptbin ].addPdf( rooDict[ 'TotF'+ptbin ], "fail" )

        #### make rhalphabet
        PT.setVal( int(ptbin) )
        rooDict[ 'polyArray' ] = buildPolynomialArray( 3, 4, "r", "p", -1.0, 1.0 )
        ##print rooDict[ 'polyArray' ]

        lPassBins = RooArgList()
        lFailBins = RooArgList()
        '''

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', dest='process', help='Process to draw, example: 1D, 2D, MC.' )
        parser.add_argument('-d', '--decay', action='store', default='SL', dest='ttbarDecay', help='ttbar decay channel: SL, DL' )
	parser.add_argument('-v', '--version', action='store', default='v0', help='Version: v01, v02.' )
	parser.add_argument('-c', '--cut', action='store', default='presel', help='cut, example: sl+presel' )
	parser.add_argument('-s', '--single', action='store', default='all', help='single histogram, example: massAve_cutDijet.' )
	parser.add_argument('-l', '--lumi', action='store', type=float, default=41530., help='Luminosity, example: 1.' )
	parser.add_argument('-e', '--ext', action='store', default='png', help='Extension of plots.' )
	parser.add_argument('-u', '--unc', action='store', default='JES', dest='unc',  help='Type of uncertainty' )
	parser.add_argument('-L', '--log', action='store_true', default=False, dest='log',  help='Plot in log scale (true) or not (false)' )
	parser.add_argument('-n', '--norm', action='store_true', default=False, dest='norm',  help='Normalized plot (true) or not (false)' )
	parser.add_argument('-f', '--final', action='store_true', default=False, dest='final',  help='If plot is final' )
	parser.add_argument('-F', '--addFit', action='store_true', default=False, dest='addFit',  help='Plot fit in ratio plot.' )
	parser.add_argument('-B', '--batchSys', action='store_true',  dest='batchSys', default=False, help='Process: all or single.' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

        if not os.path.exists('Plots/'): os.makedirs('Plots/')
	dataFiles = OrderedDict()
	bkgFiles = OrderedDict()
	signalFiles = OrderedDict()
	CMS_lumi.extraText = "Preliminary Simulation"
	#CMS_lumi.lumi_13TeV = str( round( (args.lumi/1000.), 2 ) )+" fb^{-1}, 13 TeV, 2017"
	CMS_lumi.lumi_13TeV = "13 TeV, 2017"


        tmp = 'noOrthogonal_' if '_' in args.version else ''
        VER = args.version.split('_')[1] if '_' in args.version else args.version
        bkgFiles["ST_s-channel"] = [ TFile('Rootfiles/'+VER+'/histograms_ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_'+tmp+'boosted.root'), args.lumi*10.3*.3259/9914948.,  40, 'Single top' ]
        bkgFiles["ST_t-channel"] = [ TFile('Rootfiles/'+VER+'/histograms_ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8_'+tmp+'boosted.root'), args.lumi*136.02/5982064.,  40, 'Single top' ]
        bkgFiles["ST_tW_antitop"] = [ TFile('Rootfiles/'+VER+'/histograms_ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*35.85/7745276., 40, 'Single top' ]
        bkgFiles["ST_tW_top"] = [ TFile('Rootfiles/'+VER+'/histograms_ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*35.85/7945242., 40, 'Single top' ]
        bkgFiles["TTTo2L2Nu"] = [ TFile('Rootfiles/'+VER+'/histograms_TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*88.342/283000430.596, 29, 'Dileptonic tt' ]
        ###bkgFiles["TTToHadronic"] = [ TFile('Rootfiles/'+VER+'/histograms_TTToHadronic_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*377.96/1647945788.34, 19 ]
        #bkgFiles["TTToSemiLeptonic"] = [ TFile('Rootfiles/'+VER+'/histograms_TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*365.46/720253370.04, 27 ]
        bkgFiles["TTToSemiLeptonic"] = [ TFile('Rootfiles/'+VER+'/histograms_TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*365.46/43732445., 27, 'Semileptonic tt' ]
#        bkgFiles["WW"] = [ TFile('Rootfiles/'+VER+'/histograms_WW_TuneCP5_13TeV-pythia8_'+tmp+'boosted.root'), args.lumi*118.7/7791498., 38, 'Dibosons' ]
#        bkgFiles["WZ"] = [ TFile('Rootfiles/'+VER+'/histograms_WZ_TuneCP5_13TeV-pythia8_'+tmp+'boosted.root'), args.lumi*27.6/73928630., 39, 'Dibosons' ]
#        bkgFiles["ZZ"] = [ TFile('Rootfiles/'+VER+'/histograms_ZZ_TuneCP5_13TeV-pythia8_'+tmp+'boosted.root'), args.lumi*12.14/1925931., 36, 'Dibosons' ]
    #    bkgFiles["QCD"] = [ TFile('Rootfiles/'+VER+'/histograms_QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8_'+tmp+'boosted.root'), args.lumi*1370000000./18455107., 6 ]
        bkgFiles["TTGJets"] = [ TFile('Rootfiles/'+VER+'/histograms_TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_'+tmp+'boosted.root'), args.lumi*3.697/7349100., 12, 'ttGluon' ]
        #bkgFiles["WJets"] = [ TFile('Rootfiles/'+VER+'/histograms_WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_'+tmp+'boosted.root'), args.lumi*52850.0/33073306., 33 ]
        bkgFiles["ttHToNonbb"] = [ TFile('Rootfiles/'+VER+'/histograms_ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*0.5071*(1-.5824)/5499293., kBlue, 'ttH, non-H(bb)' ]
        ##bkgFiles[""] = [ TFile('Rootfiles/'+VER+'/'), 1 ]
        ##bkgFiles[""] = [ TFile('Rootfiles/'+VER+'/'), 1 ]

        bkgFiles["TTWJetsToQQ"] = [ TFile('Rootfiles/'+VER+'/histograms_TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_'+tmp+'boosted.root'), args.lumi*0.3708/811306., 37, 'ttW'  ]
        bkgFiles["TTZToQQ"] = [ TFile('Rootfiles/'+VER+'/histograms_TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8_'+tmp+'boosted.root'),  args.lumi*0.6012/750000., 46, 'ttZ' ]
        signalFiles["THW"] = [ TFile('Rootfiles/'+VER+'/histograms_THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8_'+tmp+'boosted.root'), args.lumi*0.1475/4719999., 46, 'tHW' ]
        signalFiles["ttHTobb"] = [ TFile('Rootfiles/'+VER+'/histograms_ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*0.2934045/4216319.32, kRed, 'ttH(bb)' ]


	taulabX = 0.90
	taulabY = 0.85
	massMinX = 0
	massMaxX = 400

	plotList = [
                [ 'leadAK8Jet___2JdeltaR2WTau21DDT__boostedHiggs', 'Higgs candidate mass [GeV]', 50, 200, 2, False ],
                ]

        #massDecorrelation( 'leadAK8JetRhoPtHbb_2JdeltaR2WTau21DDT_boostedHiggs' )
	for i in plotList:
            BkgEstimation( i[0], i[2], i[3], i[4], log=args.log, axisX=i[1])
