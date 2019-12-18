#!/usr/bin/env python
'''
File: BkgEstimation.py
Author: Alejandro Gomez Espinosa
Email: alejandro.gomez@cern.ch
Description: Bkg estimation. Check for options at the end.
'''

from ROOT import *
import time, os, math, sys, copy
from array import array
import argparse
from collections import OrderedDict
#from histoLabels import labels, labelAxis, finalLabels
import CMS_lumi as CMS_lumi
import tdrstyle as tdrstyle
from DrawHistogram import rootHistograms

####gReset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)
gSystem.Load(os.getenv('CMSSW_BASE')+'/lib/'+os.getenv('SCRAM_ARCH')+'/libHiggsAnalysisCombinedLimit.so')

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



######################################################
### mass decorrelation functions
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
######################################################

######################################################
### Functions for rhalphabet
######################################################
def buildPolynomialArray( label0, label1, iNVar0, iNVar1, pXMin, pXMax ):
    """docstring for buildPolynomialArray"""
    polyArray = []
    for i0 in range(iNVar0+1):
        for i1 in range(iNVar1+1):
            pVar = label0+str(i0)+label1+str(i1)
            pRooVar = RooRealVar(pVar, pVar, 0.0, pXMin, pXMax)
            polyArray.append(pRooVar)
    return polyArray


def buildRooPolyArray( iPt, maxPolyPt, iMass, maxPolyMass, lUnity, iVars ):
    """docstring for buildRooPolyArray"""

    print( '-'*20, "MYINFO - buildRooPolyArray")
    # print len(iVars);
    striPt = str(int(iPt))
    striMass = str(int(iMass))

    lPt = RooConstVar( "Var_Pt_"+striPt+"_"+striMass, "Var_Pt_"+striPt+"_"+striMass, iPt )
    lMass = RooConstVar( "Var_Mass_"+striPt+"_"+striMass, "Var_Mass_"+striPt+"_"+striMass, iMass )
    lMassArray = RooArgList()
    lNCount = 0
    for pRVar in range(0, maxPolyMass+1):
        lTmpArray = RooArgList()
        for pVar in range(0, maxPolyPt+1):
            if lNCount == 0: lTmpArray.add(lUnity)  # for the very first constant (e.g. p0r0), just set that to 1
            else: lTmpArray.add(iVars[lNCount])
            lNCount = lNCount + 1
        pLabel = "Var_Pol_Bin_"+striPt+"_"+striMass+"_"+str(pRVar)#+suffix
        pPol = RooPolyVar(pLabel , pLabel , lPt, lTmpArray)
        #pPol.Print()
        lMassArray.add(pPol)

    lLabel = "Var_MassPol_Bin_"+striPt+"_"+striMass#+suffix
    lMassPol = RooPolyVar(lLabel , lLabel , lMass, lMassArray)
    #lMassPol.Print()
    return lMassPol


def generate_bernstein_string(n):
    # x = @(n+1)
    monomials = []
    for v in xrange(0, n+1):
            normalization = 1. * math.factorial(n) / (math.factorial(v) * math.factorial(n - v))
            monomials.append("({} * @{} * (@{}**{}) * ((1.-@{})**{}))".format(normalization, v, n+1, v, n+1, n-v))
    return " + ".join(monomials)

def buildRooPolyRhoArrayBernsteinExp( iPt, maxPolyPt, iRho, maxPolyRho, iQCD, iZero, iVars ):

    print( '-'*20, "MYINFO - buildRooPolyArrayBernsteinExp")

    striPt = str(int(iPt))
    striRho = str(int(iRho))
    lPt = RooConstVar("Var_Pt_"+striPt+"_"+striRho, "Var_Pt_"+striPt+"_"+striRho, (iPt))
    lPt_rescaled = RooConstVar("Var_Pt_rescaled_"+striPt+"_"+striRho, "Var_Pt_rescaled_"+striPt+"_"+striRho, ((iPt - float(rhalPtList[0])) / (float(rhalPtList[-1]) - float(rhalPtList[0]))))
    lRho = RooConstVar("Var_Rho_"+striPt+"_"+striRho, "Var_Rho_"+striPt+"_"+striRho, iRho )
    lRho_rescaled = RooConstVar("Var_Rho_rescaled_"+striPt+"_"+striRho,
"Var_Rho_rescaled_"+striPt+"_"+striRho, ((iRho - (-6)) / ((-2) - (-6))))

    ptPolyString = generate_bernstein_string(maxPolyPt)
    rhoPolyString = generate_bernstein_string(maxPolyRho)

    lRhoArray = RooArgList()
    lNCount = 0
    for pRVar in range(0, maxPolyRho + 1):
        lTmpArray = RooArgList()
        for pVar in range(0, maxPolyPt + 1):
            #if lNCount == 0:
            #    lTmpArray.add(iQCD)  # for the very first constant (e.g. p0r0), just set that to 1
            #else:
            print "lNCount = " + str(lNCount)
            lTmpArray.add(iVars[lNCount])
            print "iVars[lNCount]: ", iVars[lNCount]
            print "iVars[lNCount]"
            iVars[lNCount].Print()
            lNCount = lNCount + 1
        pLabel = "Var_Pol_Bin_exp_"+striPt+"_"+striRho+"_"+str(pRVar)
        lTmpArray.add(lPt_rescaled)
        print "lTmpArray: "
        lTmpArray.Print()
        pPol = RooFormulaVar(pLabel, pLabel, ptPolyString, lTmpArray)
        print "pPol:"
        pPol.Print("V")
        lRhoArray.add(pPol)

    lLabel = "Var_RhoPol_Bin_exp_"+striPt+"_"+striRho
    lRhoArray.add(lRho_rescaled)
    print "lRhoArray: "
    #lRhoArray.Print()
    lRhoPol = RooFormulaVar(lLabel, lLabel, 'exp('+rhoPolyString+')', lRhoArray)
    print('exp('+rhoPolyString+')')
    return lRhoPol
######################################################

def accessHistos( nameOfHisto, listOfFiles, minMass, maxMass, rebinMass ):
    """docstring for accessHistos"""

    histos = OrderedDict()
    for isam in listOfFiles:
        for side in ['Fail', 'Pass']:
            for ivar in [ 'Mass' ]: #, 'MassPt', 'RhoPt', 'RhoPtMass' ]:
                newName = nameOfHisto.replace('___', ivar+'_').replace('__', '_'+side)
                try:
                    histos[ isam+ivar+side ] = listOfFiles[ isam ][0].Get( 'tthbb13/'+newName )
                    histos[ isam+ivar+side ].Scale( listOfFiles[ isam ][1] )
                except TypeError: histos[ isam+ivar+side ] = listOfFiles[ isam ].Get( 'tthbb13/'+newName )
                histos[ isam+ivar+side ].SetTitle(isam+ivar+side)
                if ivar=='Mass':
                    histos[ isam+ivar+side ].Rebin(rebinMass)
                    for ibin in range(1, histos[isam+ivar+side].GetNbinsX()+1):
                        iCenter = histos[isam+ivar+side].GetXaxis().GetBinCenter(ibin)
                        if (iCenter<minMass) or (iCenter>maxMass):
                            histos[ isam+ivar+side ].SetBinContent(ibin, 0)
                            histos[ isam+ivar+side ].SetBinError(ibin, 0)
                try: histos[ ivar+side ].Add( histos[ isam+ivar+side ].Clone() )
                except (KeyError, AttributeError) as e: histos[ ivar+side ] = histos[ isam+ivar+side ].Clone()

            ### Making the 1D plots binned in Pt
            if ivar.endswith('Pt'):
                for ptbin in range(len(rhalPtList)-1):
                    histos[ ivar+side+rhalPtList[ptbin] ] = histos[ ivar+side ].ProjectionX( ivar+side+rhalPtList[ptbin], int(rhalPtList[ptbin]), int(rhalPtList[ptbin+1]) )
                    histos[ ivar+side+rhalPtList[ptbin] ].Rebin(2)
    return histos

######################################################
### Main bkg estimation
######################################################
def BkgEstimation( name, xmin, xmax, rebinX, axisX='', axisY='', labX=0.92, labY=0.50 ):
    """Bkg Estimation with rhalphabet method based on https://github.com/DAZSLE/ZPrimePlusJet/blob/35ca072541e8bf9ebbddca523658aad81fea97bc/fitting/rhalphabet_builder.py#L28"""

    ### Opening plots
    dataHistos = accessHistos( name, dataFiles, xmin, xmax, rebinX )
    bkgHistos = accessHistos( name, bkgFiles, xmin, xmax, rebinX )
    sigHistos = accessHistos( name, signalFiles, xmin, xmax, rebinX )
    ##############################

    ### Initializing RooFit variables
    MSD = RooRealVar( 'msd', 'msd', xmin, xmax )
    MSD.Print()
    #MSD.setBins( 5 )
    PT = RooRealVar( 'pt', 'pt', 0, 1500 )
    #PT.setBins( 1500 )
    RHO = RooFormulaVar( "rho", "log(msd*msd/pt/pt)", RooArgList( MSD, PT ) )
    #RHO = RooRealVar( "rho", "rho", -6., -4. )
    EFF = RooRealVar( "veff", "veff", 0.5, 0., 1.0)
    QCDEFF = RooRealVar( "qcdeff", "qcdeff", 0.01, 0., 10.)
    DM = RooRealVar("dm","dm", 0.,-10,10)
    SHIFT = RooFormulaVar( "shift", "msd-dm", RooArgList( MSD, DM ) )

    rooDict = OrderedDict()     ## dict of roofit objects

    ##############################
    ### Alphabet
    QCDEFF.setVal( bkgHistos['MassPass'].Integral()/bkgHistos['MassFail'].Integral() )
    QCDEFF.setConstant(True)
    QCDEFF.Print()

    ### polynomial
    rooDict[ 'a0' ] = RooRealVar('a0', 'a0', 0.01, -10, 10 )
    rooDict[ 'a1' ] = RooRealVar('a1', 'a1', 0.001, -10, 10 )
    rooDict[ 'a2' ] = RooRealVar('a2', 'a2', 0.0001, -10, 10 )
    rooDict[ 'a3' ] = RooRealVar('a3', 'a3', 0.00001, -10, 10 )
    #rooDict[ 'a4' ] = RooRealVar('a4', 'a4', 0.00001, -10, 10 )
    #rooDict[ 'a5' ] = RooRealVar('a5', 'a5', 0.000001, -10, 10 )
    polyArgList = RooArgList( rooDict['a0'], rooDict['a1'], rooDict['a2'], rooDict['a3'] )

    rooDict[ 'bkg_fail_bins' ] = RooArgList( )
    rooDict[ 'bkg_pass_bins' ] = RooArgList( )
    for ibin in range(1, bkgHistos['MassFail'].GetNbinsX()+1):

        ### Fail workspace
        iCont = bkgHistos['MassFail'].GetBinContent(ibin)
        iContErr = bkgHistos['MassFail'].GetBinError(ibin)
        #rooDict[ 'bkg_fail_bin'+str(ibin) ] = RooRealVar( 'bkg_fail_bin'+str(ibin), 'bkg_fail_bin'+str(ibin), 0., -100, 100 )
        #rooDict[ 'bkg_fail_bin'+str(ibin)+'_In' ] = RooRealVar( 'bkg_fail_bin'+str(ibin)+'_In', 'bkg_fail_bin'+str(ibin)+'_In', iCont )
        #rooDict[ 'bkg_fail_bin'+str(ibin)+'_In' ].setConstant(True)
        #rooDict[ 'bkg_fail_bin'+str(ibin)+'_unc' ] = RooRealVar( 'bkg_fail_bin'+str(ibin)+'_unc', 'bkg_fail_bin'+str(ibin)+'_unc', iContErr )
        #rooDict[ 'bkg_fail_bin'+str(ibin)+'_unc' ].setConstant(True)
        #rooDict[ 'bkg_fail_bin'+str(ibin)+'_func' ] = RooFormulaVar( 'bkg_fail_bin'+str(ibin)+'_func', 'bkg_fail_bin'+str(ibin)+'_func', '@1*pow(@2,@0)', RooArgList(rooDict[ 'bkg_fail_bin'+str(ibin) ], rooDict[ 'bkg_fail_bin'+str(ibin)+'_In' ], rooDict[ 'bkg_fail_bin'+str(ibin)+'_unc' ]))
        #rooDict[ 'bkg_fail_bins' ].add( rooDict[ 'bkg_fail_bin'+str(ibin)+'_func' ] )
        rooDict[ 'bkg_fail_bin'+str(ibin) ] = RooRealVar( 'bkg_fail_bin'+str(ibin), 'bkg_fail_bin'+str(ibin), iCont, max(iCont-(5*iContErr),0), max(iCont+(5*iContErr),0) )
        rooDict[ 'bkg_fail_bin'+str(ibin) ].Print()
        rooDict[ 'bkg_fail_bins' ].add( rooDict[ 'bkg_fail_bin'+str(ibin) ] )

        ### Pass workspace
        iCenter = bkgHistos['MassFail'].GetXaxis().GetBinCenter(ibin)
        rooDict[ 'Var_Mass_bin'+str(ibin) ] = RooConstVar('Var_Mass_bin'+str(ibin), 'Var_Mass_bin'+str(ibin), iCenter)
        rooDict[ 'poly_bin'+str(ibin) ] = RooPolyVar("poly_bin"+str(ibin),"poly_bin"+str(ibin), rooDict[ 'Var_Mass_bin'+str(ibin) ], polyArgList )
        #rooDict[ 'poly_bin'+str(ibin) ] = RooBernstein("poly_bin"+str(ibin),"poly_bin"+str(ibin), rooDict[ 'Var_Mass_bin'+str(ibin) ], polyArgList )
        rooDict[ 'poly_bin'+str(ibin) ].Print()
        rooDict[ 'bkg_pass_bin'+str(ibin) ] = RooFormulaVar( 'bkg_pass_bin'+str(ibin), 'bkg_pass_bin'+str(ibin), "@0*max(@1,0)*@2", RooArgList( rooDict[ 'bkg_fail_bin'+str(ibin) ], rooDict[ 'poly_bin'+str(ibin) ], QCDEFF ) )
        rooDict[ 'bkg_pass_bin'+str(ibin) ].Print()
        rooDict[ 'bkg_pass_bins' ].add( rooDict[ 'bkg_pass_bin'+str(ibin) ] )

    rooDict[ 'bkg_pass_bins' ].Print()
    rooDict[ 'bkg_pass' ] = RooParametricHist( 'bkg_pass', 'bkg_pass', MSD, rooDict[ 'bkg_pass_bins' ], bkgHistos['MassFail'] )
    rooDict[ 'bkg_pass' ].Print()
    rooDict[ 'bkg_pass_norm' ] = RooAddition( 'bkg_pass_norm', 'bkg_pass_norm', rooDict[ 'bkg_pass_bins' ] )
    rooDict[ 'bkg_fail_bins' ].Print()
    rooDict[ 'bkg_fail' ] = RooParametricHist( 'bkg_fail', 'bkg_fail', MSD, rooDict[ 'bkg_fail_bins' ], bkgHistos['MassFail'] )
    rooDict[ 'bkg_fail' ].Print()
    rooDict[ 'bkg_fail_norm' ] = RooAddition( 'bkg_fail_norm', 'bkg_fail_norm', rooDict[ 'bkg_fail_bins' ] )

    WS_fail = RooWorkspace("WS_fail")
    WS_pass = RooWorkspace("WS_pass")
    getattr(WS_fail, 'import')(rooDict['bkg_fail'], RooFit.RecycleConflictNodes() ) #, RooFit.RenameAllVariablesExcept('_', 'msd'))
    getattr(WS_fail, 'import')(rooDict['bkg_fail_norm'], RooFit.RecycleConflictNodes() ) #, RooFit.RenameAllVariablesExcept('_', 'msd'))
    WS_fail.Print('V')
    getattr(WS_pass, 'import')(rooDict['bkg_pass'], RooFit.RecycleConflictNodes() ) #, RooFit.RenameAllVariablesExcept('_', 'msd'))
    getattr(WS_pass, 'import')(rooDict['bkg_pass_norm'], RooFit.RecycleConflictNodes() ) #, RooFit.RenameAllVariablesExcept('_', 'msd'))
    WS_pass.Print('V')
    WS_fail.writeToFile( 'alphabetWS.root' )
    WS_pass.writeToFile( 'alphabetWS.root', False )

    ### data signal workspace
    #bkgHistos['PseudoDataPass'] = bkgHistos['MassPass'].Clone()
    #bkgHistos['PseudoDataPass'].Reset()
    #bkgHistos['PseudoDataPass'].SetTitle('PseudoDataPass')
    #bkgHistos['PseudoDataPass'].FillRandom( bkgHistos['MassPass'], int(bkgHistos['MassPass'].Integral()) )
    rooDict[ 'data_obs_pass' ] = RooDataHist("data_obs_pass","data_obs_pass", RooArgList( MSD ), bkgHistos['MassPass'] )
    rooDict[ 'data_obs_fail' ] = RooDataHist("data_obs_fail","data_obs_fail", RooArgList( MSD ), bkgHistos['MassFail'] )
    rooDict[ 'signal_pass' ] = RooDataHist("signal_pass","signal_pass", RooArgList( MSD ), sigHistos['MassPass'] )
    rooDict[ 'signal_fail' ] = RooDataHist("signal_fail","signal_fail", RooArgList( MSD ), sigHistos['MassFail'] )
    WS_data = RooWorkspace("WS_data")
    getattr(WS_data,'import')(rooDict[ 'data_obs_pass' ] )
    getattr(WS_data,'import')(rooDict[ 'data_obs_fail' ] )
    getattr(WS_data,'import')(rooDict[ 'signal_pass' ] )
    getattr(WS_data,'import')(rooDict[ 'signal_fail' ] )
    WS_data.writeToFile( 'alphabetWS_base.root', False )
    WS_data.Print()


    datacard = open('datacard.txt', 'w')
    datacard.write("imax 2 number of bins \n")
    datacard.write("jmax * number of processes minus 1 \n")
    datacard.write("kmax * number of nuisance parameters \n")
    datacard.write("-------------------------------\n")
    datacard.write("shapes *           fail     alphabetWS_base.root WS_data:$PROCESS_fail\n")
    datacard.write("shapes *           pass     alphabetWS_base.root WS_data:$PROCESS_pass\n")
    datacard.write("shapes bkg         fail     alphabetWS.root WS_fail:$PROCESS_fail\n")
    datacard.write("shapes bkg         pass     alphabetWS.root WS_pass:$PROCESS_pass\n")
    datacard.write("-------------------------------\n")
    datacard.write("bin           pass  fail\n")
    datacard.write("observation   -1    -1\n")
    datacard.write("-------------------------------\n")
    datacard.write("bin           fail        fail      pass      pass\n")
    datacard.write("process       bkg         signal    bkg       signal\n")
    datacard.write("process       1           0         1         0\n")
    datacard.write('rate          1           -1        1         -1\n')
    datacard.write("-------------------------------\n")
    datacard.write("# lumi    lnN     1.025         -     \n")
    datacard.write("qcdeff flatParam\n")
    for q, k in rooDict.iteritems():
        if q.startswith('a'): datacard.write(q+"    flatParam\n")
        if q.startswith('bkg_fail_bin') and not q.endswith(('func', 'In', 'unc', 's')):
        #if q.endswith(('func')):
            datacard.write(q+"    flatParam\n")
    datacard.close()
    ##############################

    sys.exit(0)
    ### Loop over pt bins
    print( '-'*20, "MYINFO - number of pt bins: ", len(rhalPtList))
    for k, ptbin in enumerate(rhalPtList):
        if ptbin.endswith(rhalPtList[-1]): continue  ### last
        print( '-'*20, "MYINFO - pt bin number: ", k)

        ### Converting TH1 into list
        #hbins_inPtBin = []
        #hpass_inPtBin = []
        #hfail_inPtBin = []
        #for ibin in range(bkgHistos['MassPtPass'+ptbin].GetNbinsX()):
        #    hbins_inPtBin.append( bkgHistos['MassPtPass'+ptbin].GetBinLowEdge(ibin) )
        #    hpass_inPtBin.append( bkgHistos['MassPtPass'+ptbin].GetBinContent(ibin) )
        #    hfail_inPtBin.append( bkgHistos['MassPtFail'+ptbin].GetBinContent(ibin) )

        #################################################################
        ### Make RooDataset, RooPdfs, and histograms
        ### In principle this can be extended for diff bkgs
        cats = RooCategory( "sample", "sample" )
        cats.defineType("pass",1)
        cats.defineType("fail",0)
        rooDict[ 'PassBkg'+ptbin ] = RooDataHist("bkg_pass_"+ptbin,"bkg_pass_"+ptbin, RooArgList( MSD ), bkgHistos['MassPtPass'+ptbin] )
        rooDict[ 'FailBkg'+ptbin ] = RooDataHist("bkg_fail_"+ptbin,"bkg_fail_"+ptbin, RooArgList( MSD ), bkgHistos['MassPtFail'+ptbin] )
        rooDict[ 'Bkg'+ptbin ] = RooDataHist("comb_bkg_"+ptbin,"comb_bkg_"+ptbin, RooArgList( MSD ), RooFit.Index(cats), RooFit.Import( "pass", rooDict['PassBkg'+ptbin] ), RooFit.Import( "fail", rooDict['FailBkg'+ptbin] ) )

        ### Normalization: RooExtendPdfs are coupled via their normalizations, N*eff or N*(1-eff).
        totalN = bkgHistos['MassPtPass'+ptbin].Integral()+bkgHistos['MassPtFail'+ptbin].Integral()
        rooDict[ 'bkgMC_total_norm_'+ptbin ] = RooRealVar( "bkgMC_norm"+ptbin, "bkgMC_norm"+ptbin, totalN, 0., 5*totalN )
        rooDict[ 'bkgMC_pass_norm_'+ptbin ] = RooFormulaVar( "bkgMC_fpass"+ptbin, "bkgMC_norm"+ptbin+"*(veff)", RooArgList( rooDict['bkgMC_total_norm_'+ptbin], EFF ) )
        rooDict[ 'bkgMC_fail_norm_'+ptbin ] = RooFormulaVar( "bkgMC_fqail"+ptbin, "bkgMC_norm"+ptbin+"*(1-veff)", RooArgList( rooDict['bkgMC_total_norm_'+ptbin], EFF ) )

        ### Shapes
        rooDict[ 'bkgMC_pass_'+ptbin ] = RooDataHist("bkgMC_pass_"+ptbin,"bkgMC_pass_"+ptbin, RooArgList( MSD ), bkgHistos['MassPtPass'+ptbin] )
        rooDict[ 'bkgMC_fail_'+ptbin ] = RooDataHist("bkgMC_fail_"+ptbin,"bkgMC_fail_"+ptbin, RooArgList( MSD ), bkgHistos['MassPtFail'+ptbin] )
        rooDict[ 'bkgMC_passh_'+ptbin ] = RooHistPdf( 'bkgMC_passh_'+ptbin, 'bkgMC_passh_'+ptbin, RooArgList(SHIFT), RooArgList(MSD), rooDict['bkgMC_pass_'+ptbin], 0 )
        rooDict[ 'bkgMC_failh_'+ptbin ] = RooHistPdf( 'bkgMC_failh_'+ptbin, 'bkgMC_failh_'+ptbin, RooArgList(SHIFT), RooArgList(MSD), rooDict['bkgMC_fail_'+ptbin], 0 )

        ### extended likelihood from normalization and shape above
        rooDict[ 'bkgMC_passe_'+ptbin ] = RooExtendPdf( 'bkgMC_passe_'+ptbin, 'bkgMC_passe_'+ptbin, rooDict['bkgMC_passh_'+ptbin], rooDict['bkgMC_pass_norm_'+ptbin] )
        rooDict[ 'bkgMC_passe_'+ptbin ].Print()
        rooDict[ 'bkgMC_faile_'+ptbin ] = RooExtendPdf( 'bkgMC_faile_'+ptbin, 'bkgMC_faile_'+ptbin, rooDict['bkgMC_failh_'+ptbin], rooDict['bkgMC_fail_norm_'+ptbin] )
        rooDict[ 'bkgMC_faile_'+ptbin ].Print()


        ### Add all bkg in RooAddpdf
        ### needed if differnt bkg components
        rooDict[ 'totalMC_pdf_pass'+ptbin ] = RooAddPdf( 'totalMC_pass'+ptbin, 'totalMC_pass'+ptbin, RooArgList( rooDict[ 'bkgMC_passe_'+ptbin ] ) )
        rooDict[ 'totalMC_pdf_fail'+ptbin ] = RooAddPdf( 'totalMC_fail'+ptbin, 'totalMC_fail'+ptbin, RooArgList( rooDict[ 'bkgMC_faile_'+ptbin ] ) )

        ### Make RooSimultaneous
        rooDict[ 'total_simulpdf'+ptbin ] = RooSimultaneous( 'tot'+ptbin, 'tot'+ptbin, cats )
        rooDict[ 'total_simulpdf'+ptbin ].addPdf( rooDict[ 'totalMC_pdf_pass'+ptbin ], 'pass' )
        rooDict[ 'total_simulpdf'+ptbin ].addPdf( rooDict[ 'totalMC_pdf_fail'+ptbin ], 'fail' )
        rooDict[ 'total_simulpdf'+ptbin ].Print()


        #################################################################
        ### Make Rhalphabet
        meanPtBin = (float(rhalPtList[k+1]) + float(ptbin))/2
        PT.setVal(meanPtBin)
        print( '-'*20, "MYINFO - this pt bin value: ", meanPtBin)

        ### Build polynomial
        maxPolyPt = 0
        maxPolyRho = 0
        rooDict[ 'polyArray'+ptbin ] = buildPolynomialArray( 'p', 'r', maxPolyPt, maxPolyRho, -30, 30 )
        print( '-'*20, "MYINFO - polynomial_variables: ", rooDict[ 'polyArray'+ptbin ])

        ### Now build the function
        lUnity = RooConstVar("unity","unity",1.)
        lZero  = RooConstVar("lZero","lZero",0.)

        for massbin in range(bkgHistos['MassPtPass'+ptbin].GetNbinsX()):
            if bkgHistos['MassPtPass'+ptbin].GetXaxis().GetBinLowEdge(massbin) < 50: continue  ### skipping low mass
            MSD.setVal( bkgHistos['MassPtPass'+ptbin].GetXaxis().GetBinCenter(massbin) )

            #rooDict[ 'lPass'+ptbin+str(massbin) ] = buildRooPolyArray( PT.getVal(), maxPolyPt, MSD.getVal(), maxPolyRho, lUnity, rooDict[ 'polyArray'+ptbin ])
            rooDict[ 'roopolyarray'+ptbin+str(massbin) ] = buildRooPolyRhoArrayBernsteinExp( PT.getVal(), maxPolyPt, MSD.getVal(), maxPolyRho, lUnity, lZero, rooDict[ 'polyArray'+ptbin ])
            #rooDict[ 'roopolyarray'+ptbin+str(massbin) ].Print()
            #sys.exit(0)

            fail_bin_content = bkgHistos[ 'MassPtFail'+ptbin ].GetBinContent(massbin)
            #print fail_bin_content, bkgHistos[ 'MassPtFail'+ptbin ].GetBinCenter(massbin)

        pass_workspace = RooWorkspace('w_pass_cat'+ptbin)
        fail_workspace = RooWorkspace('w_fail_cat'+ptbin)
        #getattr(pass_workspace, 'import')(pass_rparh, RooFit.RecycleConflictNodes(), r.RooFit.RenameAllVariablesExcept(self._suffix.replace('_',''),'x'))
        #getattr(pass_workspace, 'import')(pass_norm, r.RooFit.RecycleConflictNodes(), r.RooFit.RenameAllVariablesExcept(self._suffix.replace('_',''),'x'))


        '''
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

        outputFileName = name.replace('__', '_RhoPt'+ptbin+'_')+'_PassFailPlots_'+args.version+'.'+args.ext
        if args.log: outputFileName = outputFileName.replace('Plots','Plots_Log')
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

        outputFileName = name.replace('__', '_Pt'+ptbin+'_')+'_PassFailPlots_'+args.version+'.'+args.ext
        if args.log: outputFileName = outputFileName.replace('Plots','Plots_Log')
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

        outputFileName = name.replace('__', '_Final'+ptbin+'_')+'_PassFailPlots_'+args.version+'.'+args.ext
        if args.log: outputFileName = outputFileName.replace('Plots','Plots_Log')
        print('Processing.......', outputFileName)
        canvas['bkgEst'+ptbin].SaveAs( 'Plots/'+ outputFileName )

        '''
        ######################


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

        VER = args.version.split('_')[1] if '_' in args.version else args.version
        bkgFiles, signalFiles, dataFiles = rootHistograms( VER, args.lumi, '_boosted' )

	plotList = [
                [ 'leadAK8Jet___2J2WdeltaRTau21__', 'Higgs candidate mass [GeV]', 50, 250, 1, False ],
                ]

        #massDecorrelation( 'leadAK8JetRhoPtHbb_2JdeltaR2WTau21DDT_boostedHiggs' )
	for i in plotList:
            BkgEstimation( i[0], i[2], i[3], i[4], axisX=i[1])
