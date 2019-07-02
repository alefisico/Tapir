#!/usr/bin/env python
'''
File: DrawHistogram.py
Author: Alejandro Gomez Espinosa
Email: alejandro.gomez@cern.ch
Description: My Draw histograms. Check for options at the end.
'''

from ROOT import *
import time, os, math, sys, copy
from array import array
import argparse
from collections import OrderedDict
import subprocess
sys.path.insert(0,'..')
import CMS_lumi as CMS_lumi
import tdrstyle as tdrstyle

####gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)


def setSelection( listSel, xMin=0.65, yMax=0.65, align='right' ):

    for i in range( len( listSel ) ):
        textBox=TLatex()
        textBox.SetNDC()
        textBox.SetTextSize(0.04)
        if 'right' in align: textBox.SetTextAlign(31)
        textBox.SetTextFont(62) ### 62 is bold, 42 is normal
        textBox.DrawLatex(xMin, yMax, listSel[i])
        yMax = yMax -0.05



def plotQuality( nameInRoot, name2, nameNewHisto, label, xmin, xmax, rebinX, labX, labY, log, moveCMSlogo=False, fitRatio=False ):
    """docstring for plot"""

    histos = {}

    for iT in [ 'b_pt_eta', 'c_pt_eta', 'l_pt_eta' ]:
        outputFileName = nameInRoot+"_"+iT+'_'+nameNewHisto+'_diffPlots_'+args.version+'.'+args.ext
        print 'Processing.......', outputFileName

        if (labY < 0.5) and ( labX < 0.5 ): legend=TLegend(0.20,0.50,0.50,0.62)
        elif (labX < 0.5): legend=TLegend(0.20,0.75,0.50,0.87)
        else: legend=TLegend(0.70,0.75,0.90,0.87)
        legend.SetFillStyle(0)
        legend.SetTextSize(0.04)

        dummy=10
        for isamLabel, isam in signalFiles.iteritems():
            histos[ isamLabel ] = isam[0].Get( nameInRoot+'_'+iT if isamLabel.startswith('old') else name2+'_'+iT )
            histos[ isamLabel ] = histos[ isamLabel ].ProjectionZ()
            histos[ isamLabel ].Scale(1/histos[ isamLabel ].Integral())
            legend.AddEntry( histos[ isamLabel ], dummy, 'lp' )
            dummy+=1


        hRatio = TGraphAsymmErrors()
        #hRatio.Divide( projXold, projXnew, 'pois' )
        #hRatioStatErr = projXold.Clone()
        #hRatioStatErr.Divide( projXold )
        #hRatioStatErr.SetFillColor(kBlack)
        #hRatioStatErr.SetFillStyle(3004)

        #binWidth = projXold.GetBinWidth(1)
        legend.AddEntry( projXold, 'old' , 'ep' )

        projXold.SetLineColor(kRed-4)
        projXold.SetLineWidth(2)
        projXnew.SetLineColor(kBlue-4)
        projXnew.SetLineWidth(2)
        #projXnew.SetMarkerStyle(8)

        tdrStyle.SetPadRightMargin(0.05)
        tdrStyle.SetPadLeftMargin(0.15)
        can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
        pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
        pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
        pad1.Draw()
        pad2.Draw()

        pad1.cd()
        if log: pad1.SetLogy()
        projXnew.Draw("e")
        projXold.Draw('e same')
        #projXnew.SetMaximum( 1.2* max( projXnew.GetMaximum(), projXold.GetMaximum() )  )
        #if 'pt' in label: projXnew.SetMinimum( 1 )
        #projXnew.GetYaxis().SetTitleOffset(1.2)
        if xmax: projXnew.GetXaxis().SetRangeUser( xmin, xmax )
        #projXnew.GetYaxis().SetTitle( 'Normalized' )
        #projXnew.GetYaxis().SetTitle( 'Normalized / '+str(int(binWidth))+' GeV' )
        #projXnew.GetYaxis().SetTitle( ( 'Events / '+str(int(binWidth))+' GeV' if nameInRoot in [ 'massAve', 'HT', 'jet1Pt', 'jet2Pt', 'MET' ] else 'Events' ) )

        #CMS_lumi.relPosX = 0.13
        if moveCMSlogo:
                CMS_lumi.cmsTextOffset = 0.1
                CMS_lumi.relPosX = 0.15
        else:
                CMS_lumi.cmsTextOffset = 0.0
                CMS_lumi.relPosX = 0.13
        CMS_lumi.CMS_lumi(pad1, 4, 0)
        #labelAxis( name, projXnew, '' )
        legend.Draw()
        ###setSelection( selection[ args.cut ], labX, labY )

        pad2.cd()
        gStyle.SetOptFit(1)
        pad2.SetGrid()
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.3)
        tmpPad2= pad2.DrawFrame(xmin, 0 , xmax,2)
        #labelAxis( name.replace( args.cut, ''), tmpPad2, ( 'softDrop' if 'Puppi' in args.grooming else Groom ) )
        tmpPad2.GetXaxis().SetTitle( label )
        tmpPad2.GetYaxis().SetTitle( "Data/Bkg" )
        tmpPad2.GetYaxis().SetTitleOffset( 0.5 )
        tmpPad2.GetYaxis().CenterTitle()
        tmpPad2.SetLabelSize(0.12, 'x')
        tmpPad2.SetTitleSize(0.12, 'x')
        tmpPad2.SetLabelSize(0.12, 'y')
        tmpPad2.SetTitleSize(0.12, 'y')
        tmpPad2.SetNdivisions(505, 'x')
        tmpPad2.SetNdivisions(505, 'y')
        pad2.Modified()
        hRatio.SetMarkerStyle(8)
        hRatio.Draw('P')
        #hRatioStatErr.Draw('same e2')

        can.SaveAs( 'Plots/'+ outputFileName.replace('Plots', ( 'Fit' if fitRatio else '') ) )
        del can



if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='qual', dest='process', help='Process to draw, example: 1D, 2D, MC.' )
        parser.add_argument('-d', '--decay', action='store', default='SL', dest='ttbarDecay', help='ttbar decay channel: SL, DL' )
	parser.add_argument('-v', '--version', action='store', default='v0', help='Version: v01, v02.' )
	parser.add_argument('-c', '--cut', action='store', default='SL_presel', help='cut, example: sl+presel' )
	parser.add_argument('-s', '--single', action='store', default='all', help='single histogram, example: massAve_cutDijet.' )
	parser.add_argument('-l', '--lumi', action='store', type=float, default=59215, help='Luminosity, example: 1.' )
	parser.add_argument('-e', '--ext', action='store', default='png', help='Extension of plots.' )
	parser.add_argument('-u', '--unc', action='store', default='JES', dest='unc',  help='Type of uncertainty' )
	parser.add_argument('-f', '--final', action='store_true', default=False, dest='final',  help='If plot is final' )
	parser.add_argument('-F', '--addFit', action='store_true', default=False, dest='addFit',  help='Plot fit in ratio plot.' )
	parser.add_argument('-B', '--batchSys', action='store_true',  dest='batchSys', default=False, help='Process: all or single.' )

	try:
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

        if not os.path.exists('Plots/'): os.makedirs('Plots/')
	signalFiles = OrderedDict()
	CMS_lumi.extraText = "Preliminary"
	CMS_lumi.lumi_13TeV = '' #str( round( (args.lumi/1000.), 2 ) )+" fb^{-1}, 13 TeV, 2018"

        #signalFiles[ 'old' ] = [ TFile.Open('../../../MEAnalysis/data/3Dplots.root'), 1, 'Old', kBlue-4 ]
        #signalFiles[ 'new' ] = [ TFile.Open('3DPlots_local2_2017.root'), 1, 'New', kBlue-4 ]
        signalFiles[ '2016' ] = [ TFile.Open('3DPlots_2016.root'), 1, '2016 MC', kBlue-4 ]
        signalFiles[ '2017' ] = [ TFile.Open('3DPlots_2017.root'), 1, '2017 MC', kBlue-4 ]
        signalFiles[ '2018' ] = [ TFile.Open('3DPlots_2018.root'), 1, '2018 MC', kBlue-4 ]

	taulabX = 0.90
	taulabY = 0.85
	massMinX = 0
	massMaxX = 400

	plotList = [
		#[ 'qual', 'btagCSV', 'btagCSVV2', 'pt', 'pt [GeV]', 20, 400, 20, 0.85, 0.70, False, False],
		#[ 'qual', 'btagDeepCSV', 'btagDeepB', 'pt', 'pt [GeV]', 20, 400, 20, 0.85, 0.70, False, False],
		#[ 'qual', 'btagCSV', 'btagCSVV2', 'eta', '#eta', 0, 2.4, 1, 0.85, 0.70, False, False],
		#[ 'qual', 'btagDeepCSV', 'btagDeepB', 'eta', '#eta', 0, 2.4, 1, 0.85, 0.70, False, False],
		[ 'qual', 'btagCSV', 'btagCSVV2', 'bdisc', 'b discriminator CSVv2', 0, 1, 1, 0.85, 0.70, False, False],
		[ 'qual', 'btagDeepCSV', 'btagDeepB', 'bdisc', 'b discriminator deepCSV', 0, 1, 1, 0.85, 0.70, False, False],
		[ 'qual', 'btagDeepFlavB', 'btagDeepFlavB', 'bdisc', 'b discriminator deepFlavorB', 0, 1, 1, 0.85, 0.70, False, False],
		]

	if 'all' in args.single: Plots = [ x[1:] for x in plotList if ( ( args.process in x[0] ) )  ]
	else: Plots = [ y[1:] for y in plotList if ( ( args.process in y[0] ) and ( y[1] in args.single ) )  ]

	for i in Plots:
            plotQuality(
                i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                fitRatio=args.addFit )
