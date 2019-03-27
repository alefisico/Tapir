#!/usr/bin/env python
'''
File: DrawHistogram.py
Author: Alejandro Gomez Espinosa
Email: alejandro.gomez@cern.ch
Description: My Draw histograms. Check for options at the end.
'''

#from ROOT import TFile, TH1F, THStack, TCanvas, TMath, gROOT, gPad
from ROOT import *
import time, os, math, sys, copy
from array import array
import argparse
from collections import OrderedDict
import subprocess
#from histoLabels import labels, labelAxis, finalLabels
import CMS_lumi as CMS_lumi
import tdrstyle as tdrstyle
#from commonFunctions import *

####gROOT.Reset()
gROOT.SetBatch()
gROOT.ForceStyle()
tdrstyle.setTDRStyle()
gStyle.SetOptStat(0)

xline = array('d', [0,2000])
yline = array('d', [1,1])
line = TGraph(2, xline, yline)
line.SetLineColor(kRed)

jetMassHTlabY = 0.20
jetMassHTlabX = 0.85
kfactor = 0.032

ttbarComp = OrderedDict()
ttbarComp['ttbarPlusB'] = [ 'tt+b', kRed+4 ]
ttbarComp['ttbarPlus2B'] = [ 'tt+2b', kRed+3 ]
ttbarComp['ttbarPlusBBbar'] = [ 'tt+bb', kRed+2 ]
ttbarComp['ttbarPlusCCbar'] = [ 'tt+cc', kRed-1 ]
ttbarComp['ttbarOther'] = [ 'tt+light', kRed-2 ]

selection = {}
selection['sl_presel'] = [ 'nlep > 0', 'nJets > 3', 'nDeepCSVM > 1' ]

def setSelection( listSel, xMin=0.65, yMax=0.65, align='right' ):

    for i in range( len( listSel ) ):
        textBox=TLatex()
        textBox.SetNDC()
        textBox.SetTextSize(0.04)
        if 'right' in align: textBox.SetTextAlign(31)
        textBox.SetTextFont(62) ### 62 is bold, 42 is normal
        textBox.DrawLatex(xMin, yMax, listSel[i])
        yMax = yMax -0.05


def stackPlots( nameInRoot, label, xmin, xmax, rebinX, ymin, ymax, labX, labY, log, moveCMSlogo=False, fitRatio=False ):
	"""docstring for stacked plot"""

	outputFileName = nameInRoot+'_'+args.cut+'_stackPlots_'+args.version+'.'+args.ext
	print 'Processing.......', outputFileName

	#if (labY < 0.5) and ( labX < 0.5 ): legend=TLegend(0.20,0.50,0.50,0.62)
	#elif (labX < 0.5): legend=TLegend(0.20,0.75,0.50,0.87)
	legend=TLegend(0.75,0.60,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)

	histos = {}
        for idataLabel, idata in dataFiles.iteritems():
            try:
                histos[ 'Data' ].Add( idata.Get( 'data__'+args.cut+'__'+nameInRoot ) )
            except (KeyError, AttributeError) as e:
                histos[ 'Data' ] = idata.Get( 'data__'+args.cut+'__'+nameInRoot )
	if rebinX > 1: histos[ 'Data' ].Rebin( rebinX )
	hData = histos[ 'Data' ].Clone()
	legend.AddEntry( hData, 'DATA' , 'ep' )

        hBkgStack = THStack('stackHisto', 'hBkg')
	hBkg = histos[ 'Data' ].Clone()
	hBkg.Reset()
        for isamLabel, isam in bkgFiles.iteritems():
            if 'TT' in isamLabel:
                for flaLabel, flaInfo in ttbarComp.iteritems():
                    histos[ flaLabel ] = isam[0].Get( flaLabel+'__'+args.cut+'__'+nameInRoot )
                    histos[ flaLabel ].Scale( isam[1]*kfactor )
                    histos[ flaLabel ].SetFillStyle( 1001 )
                    histos[ flaLabel ].SetFillColor( flaInfo[1] )
                    legend.AddEntry( histos[ flaLabel ], flaInfo[0], 'f' )
                    if rebinX > 1: histos[ flaLabel ].Rebin( rebinX )
                    hBkg.Add( histos[ flaLabel ].Clone() )
                    hBkgStack.Add( histos[ flaLabel ].Clone() )
            else:
                histos[ isamLabel ] = isam[0].Get( isamLabel+'__'+args.cut+'__'+nameInRoot )
                histos[ isamLabel ].Scale( isam[1]*kfactor )
                histos[ isamLabel ].SetFillStyle( 1001 )
                histos[ isamLabel ].SetFillColor( flaInfo[1] )
                legend.AddEntry( histos[ isamLabel ], flaInfo[0], 'f' )
                if rebinX > 1: histos[ isamLabel ].Rebin( rebinX )
                hBkg.Add( histos[ isamLabel ].Clone() )
                hBkgStack.Add( histos[ isamLabel ].Clone() )

        for isignalLabel, isig in signalFiles.iteritems():
            hSignal = isig[0].Get( isignalLabel+'__'+args.cut+'__'+nameInRoot )
            hSignal.Scale( isig[1]*kfactor )
            #histos[ isignalLabel ].SetFillStyle( 1001 )
            hSignal.SetLineWidth( 2 )
            hSignal.SetLineColor( isig[3] )
            legend.AddEntry( hSignal, isig[2], 'l' )
            if rebinX > 1: hSignal.Rebin( rebinX )

	hRatio = TGraphAsymmErrors()
	hRatio.Divide( hData, hBkg, 'pois' )

	binWidth = histos['Data'].GetBinWidth(1)
	hData.SetMarkerStyle(8)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	if log: pad1.SetLogy()
	hBkgStack.Draw('hist')
	hData.Draw("same")
	hSignal.Draw("hist same")
	hBkgStack.SetMaximum( ymax ) #(10 if log else 1.4)* max( hBkgStack.GetMaximum(), hBkgStack.GetMaximum() )  )
        hBkgStack.SetMinimum( ymin )
	#hBkgStack.GetYaxis().SetTitleOffset(1.2)
	if xmax: hBkgStack.GetXaxis().SetRangeUser( xmin, xmax )
	#hBkgStack.GetYaxis().SetTitle( 'Normalized' )
	#hBkgStack.GetYaxis().SetTitle( 'Normalized / '+str(int(binWidth))+' GeV' )
	hBkgStack.GetYaxis().SetTitle( ( 'Events / '+str(int(binWidth))+' GeV' if nameInRoot.endswith( ('pt', 'ht') ) else 'Events' ) )

	#CMS_lumi.relPosX = 0.13
	if moveCMSlogo:
		CMS_lumi.cmsTextOffset = 0.1
		CMS_lumi.relPosX = 0.15
	else:
		CMS_lumi.cmsTextOffset = 0.0
		CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	#labelAxis( name, hData, '' )
	legend.Draw()
        setSelection( selection[ args.cut ], labX, labY )

	pad2.cd()
	gStyle.SetOptFit(1)
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	tmpPad2= pad2.DrawFrame(xmin, ( 0.5 if fitRatio else 0.5), xmax,1.5)
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
	if fitRatio:
		fitLine = TF1( 'fitLine', 'pol1', 0, 2 ) #800, 5000)
		hRatio.Fit( 'fitLine', 'MIR')
		fitLine.Draw("same")
		pad2.Update()
		st1 = hRatio.GetListOfFunctions().FindObject("stats")
		st1.SetX1NDC(.65)
		st1.SetX2NDC(.95)
		st1.SetY1NDC(.75)
		st1.SetY2NDC(.95)
		#st1.SetTextColor(kRed)
		pad2.Modified()

	can.SaveAs( 'Plots/'+ outputFileName.replace('Plots', ( 'Fit' if fitRatio else '') ) )
	del can


def plotQuality( nameInRoot, label, xmin, xmax, rebinX, labX, labY, log, moveCMSlogo=False, fitRatio=False ):
	"""docstring for plot"""

	outputFileName = nameInRoot+'_dataQualityPlots_'+args.version+'.'+args.ext
	print 'Processing.......', outputFileName

	histos = {}

        for idataLabel, idata in dataFiles.iteritems():
            try:
                histos[ 'Data' ].Add( idata.Get( 'data__'+args.cut+'__'+nameInRoot ) )
            except (KeyError, AttributeError) as e:
                histos[ 'Data' ] = idata.Get( 'data__'+args.cut+'__'+nameInRoot )

        histos[ 'Bkg' ] = histos[ 'Data' ].Clone()
        histos[ 'Bkg' ].Reset()
        for isamLabel, isam in bkgFiles.iteritems():
            if 'TT' in isamLabel:
                for flaLabel, flaInfo in ttbarComp.iteritems():
                    histos[ flaLabel ] = isam[0].Get( flaLabel+'__'+args.cut+'__'+nameInRoot )
                    histos[ flaLabel ].Scale( isam[1]*kfactor )
                    histos[ 'Bkg' ].Add( histos[ flaLabel ] )
            else:
                histos[ isamLabel ] = isam[0].Get( isamLabel+'__'+args.cut+'__'+nameInRoot )
                histos[ isamLabel ].Scale( isam[1]*kfactor )
                histos[ 'Bkg' ].Add( histos[ isamLabel ] )

	if rebinX > 1:
            histos[ 'Data' ].Rebin( rebinX )
            histos[ 'Bkg' ].Rebin( rebinX )
	hData = histos[ 'Data' ].Clone()
	hBkg = histos[ 'Bkg' ].Clone()

	hRatio = TGraphAsymmErrors()
	hRatio.Divide( hData, hBkg, 'pois' )

	binWidth = histos['Data'].GetBinWidth(1)

	if (labY < 0.5) and ( labX < 0.5 ): legend=TLegend(0.20,0.50,0.50,0.62)
	elif (labX < 0.5): legend=TLegend(0.20,0.75,0.50,0.87)
	else: legend=TLegend(0.70,0.75,0.90,0.87)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)
	legend.AddEntry( hData, 'DATA' , 'ep' )
	legend.AddEntry( hBkg, 'All Bkg', 'lp' )

	hBkg.SetLineColor(kRed-4)
	hBkg.SetLineWidth(2)
	hData.SetMarkerStyle(8)

	tdrStyle.SetPadRightMargin(0.05)
	tdrStyle.SetPadLeftMargin(0.15)
	can = TCanvas('c1', 'c1',  10, 10, 750, 750 )
	pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
	pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
	pad1.Draw()
	pad2.Draw()

	pad1.cd()
	if log: pad1.SetLogy()
	hData.Draw("E")
	hBkg.Draw('hist same')
	hData.SetMaximum( 1.2* max( hData.GetMaximum(), hBkg.GetMaximum() )  )
        if 'pt' in label: hData.SetMinimum( 1 )
	#hData.GetYaxis().SetTitleOffset(1.2)
	if xmax: hData.GetXaxis().SetRangeUser( xmin, xmax )
	#hData.GetYaxis().SetTitle( 'Normalized' )
	#hData.GetYaxis().SetTitle( 'Normalized / '+str(int(binWidth))+' GeV' )
	hData.GetYaxis().SetTitle( ( 'Events / '+str(int(binWidth))+' GeV' if nameInRoot in [ 'massAve', 'HT', 'jet1Pt', 'jet2Pt', 'MET' ] else 'Events' ) )

	#CMS_lumi.relPosX = 0.13
	if moveCMSlogo:
		CMS_lumi.cmsTextOffset = 0.1
		CMS_lumi.relPosX = 0.15
	else:
		CMS_lumi.cmsTextOffset = 0.0
		CMS_lumi.relPosX = 0.13
	CMS_lumi.CMS_lumi(pad1, 4, 0)
	#labelAxis( name, hData, '' )
	legend.Draw()
        setSelection( selection[ args.cut ], labX, labY )

	pad2.cd()
	gStyle.SetOptFit(1)
	pad2.SetGrid()
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	tmpPad2= pad2.DrawFrame(xmin, ( 0.5 if fitRatio else 0.5), xmax,1.5)
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
	if fitRatio:
		fitLine = TF1( 'fitLine', 'pol1', 0, 2 ) #800, 5000)
		hRatio.Fit( 'fitLine', 'MIR')
		fitLine.Draw("same")
		pad2.Update()
		st1 = hRatio.GetListOfFunctions().FindObject("stats")
		st1.SetX1NDC(.65)
		st1.SetX2NDC(.95)
		st1.SetY1NDC(.75)
		st1.SetY2NDC(.95)
		#st1.SetTextColor(kRed)
		pad2.Modified()

	can.SaveAs( 'Plots/'+ outputFileName.replace('Plots', ( 'Fit' if fitRatio else '') ) )
	del can



if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', dest='process', help='Process to draw, example: 1D, 2D, MC.' )
	parser.add_argument('-v', '--version', action='store', default='v0', help='Version: v01, v02.' )
	parser.add_argument('-c', '--cut', action='store', default='sl_presel', help='cut, example: sl+presel' )
	parser.add_argument('-s', '--single', action='store', default='all', help='single histogram, example: massAve_cutDijet.' )
	#parser.add_argument('-c', '--camp', action='store', default='RunIISpring15MiniAODv2-74X', help='Campaign, example: PHYS14.' )
	parser.add_argument('-l', '--lumi', action='store', type=float, default=35870, help='Luminosity, example: 1.' )
	parser.add_argument('-r', '--range', action='store', default='low', dest='RANGE', help='Trigger used, example PFHT800.' )
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
	dataFiles = OrderedDict()
	bkgFiles = OrderedDict()
	signalFiles = OrderedDict()
	CMS_lumi.extraText = "Preliminary"
	CMS_lumi.lumi_13TeV = str( round( (args.lumi/1000.), 2 ) )+" fb^{-1}, 13 TeV, 2018"

	folder = 'root://t3dcachedb03.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/algomez/ttH/Sparsinator/'+args.version

        dataFiles['EGamma_Run2018A'] = TFile.Open(folder+'/EGamma_Run2018A_sparsinator_'+args.version+'.root')
        dataFiles['EGamma_Run2018B'] = TFile.Open(folder+'/EGamma_Run2018B_sparsinator_'+args.version+'.root')
        dataFiles['EGamma_Run2018C'] = TFile.Open(folder+'/EGamma_Run2018C_sparsinator_'+args.version+'.root')
        dataFiles['EGamma_Run2018D'] = TFile.Open(folder+'/EGamma_Run2018D_sparsinator_'+args.version+'.root')
        dataFiles['SingleMuon_Run2018A'] = TFile.Open(folder+'/SingleMuon_Run2018A_sparsinator_'+args.version+'.root')
        dataFiles['SingleMuon_Run2018B'] = TFile.Open(folder+'/SingleMuon_Run2018B_sparsinator_'+args.version+'.root')
        dataFiles['SingleMuon_Run2018C'] = TFile.Open(folder+'/SingleMuon_Run2018C_sparsinator_'+args.version+'.root')
        dataFiles['SingleMuon_Run2018D'] = TFile.Open(folder+'/SingleMuon_Run2018D_sparsinator_'+args.version+'.root')
        bkgFiles[ 'TTSL' ] = [ TFile.Open(folder+'/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_sparsinator_'+args.version+'.root'), args.lumi, 'ttbar' ]

        signalFiles[ 'ttH_hbb' ] = [ TFile.Open(folder+'/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8_sparsinator_'+args.version+'.root'), args.lumi*0.1, 'ttH(bb)', kBlue-4 ]

	taulabX = 0.90
	taulabY = 0.85
	massMinX = 0
	massMaxX = 400

	plotList = [
		##[ '2D', 'Boosted', 'leadMassHT', 'Leading Jet Mass [GeV]', 'HT [GeV]', 0, massMaxX, 1, 100, 1300, 1, jetMassHTlabX, jetMassHTlabY],
		##[ '2DResolved', 'Resolved', 'etas', '#eta_{jj1}', '#eta_{jj2}', -3.0, 3.0, 10, -3.0, 3.0, 10, jetMassHTlabX, jetMassHTlabY],

		[ 'stack', 'jetsByPt_0_pt', 'Leading jet pT [GeV]', 0, 1000, 2, 10, 10e5, 0.70, 0.80, True, False],
		[ 'stack', 'jetsByPt_1_pt', '2nd leading jet pT [GeV]', 0, 1000, 2, 1, 10e5,  0.70, 0.80, True, False],
		[ 'stack', 'jetsByPt_2_pt', '3rd leading jet pT [GeV]', 0, 1000, 2, 1, 10e5,  0.70, 0.80, True, False],
		[ 'stack', 'jetsByPt_3_pt', '4th leading jet pT [GeV]', 0, 1000, 2, 1, 10e5,  0.70, 0.80, True, False],
		[ 'stack', 'jetsByPt_0_eta', 'Leading jet #eta', -2.5, 2.5, 1, 100, 10e6,  0.70, 0.80, True, False],
		[ 'stack', 'jetsByPt_1_eta', '2nd leading jet #eta', -2.5, 2.5, 1, 100, 10e6, 0.70, 0.80, True, False],
		[ 'stack', 'jetsByPt_2_eta', '3rd leading jet #eta', -2.5, 2.5, 1, 100, 10e6, 0.70, 0.80, True, False],
		[ 'stack', 'jetsByPt_3_eta', '4th leading jet #eta', -2.5, 2.5, 1, 100, 10e6, 0.70, 0.80, True, False],
		[ 'stack', 'jetsByPt_0_btagCSV', 'Leading jet deepCSV discriminator', 0, 1, 1, 100, 10e6,  0.70, 0.80, True, False],
		[ 'stack', 'jetsByPt_1_btagCSV', '2nd leading jet deepCSV discriminator', 0, 1, 1, 100, 10e6,  0.70, 0.80, True, False],
		[ 'stack', 'jetsByPt_2_btagCSV', '3rd leading jet deepCSV discriminator', 0, 1, 1, 100, 10e6,  0.70, 0.80, True, False],
		[ 'stack', 'jetsByPt_3_btagCSV', '4th leading jet deepCSV discriminator', 0, 1, 1, 100, 10e6,  0.70, 0.80, True, False],
		[ 'stack', 'leps_0_pt', 'Lepton pT [GeV]', 0, 800, 2, 1, 10e5, 0.70, 0.80, True, False],
		[ 'stack', 'leps_0_eta', 'Lepton #eta', -2.5, 2.5, 1, 100, 10e6,  0.70, 0.80, True, False],
		[ 'stack', 'met_pt', 'MET [GeV]', 0, 500, 2, 10, 10e6, 0.70, 0.80, True, False],
		[ 'stack', 'numJets', 'Number of jets', 2, 14, 1, 1, 10e6, 0.70, 0.80, True, False],
		[ 'stack', 'nBDeepCSVM', 'Number of deepCSVM jets', 1, 7, 1, 10, 10e7, 0.70, 0.80, True, False],
		[ 'stack', 'ht', 'HT [GeV]', 0, 2000, 5, 10, 10e6, 0.70, 0.80, True, False],

		[ 'qual', 'nPVs', 'Number of PV', 0, 100, 1,  0.85, 0.70, False, False],
		[ 'qual', 'numJets', 'Number of jets', 2, 14, 1,  0.85, 0.70, True, False],
		#[ 'qual', 'FatJet_pt_all', 'jet pT [GeV]', 200, 1500, 5,  0.85, 0.70, True, False],
		]

	if 'all' in args.single: Plots = [ x[1:] for x in plotList if ( ( args.process in x[0] ) )  ]
	else: Plots = [ y[1:] for y in plotList if ( ( args.process in y[0] ) and ( y[1] in args.single ) )  ]

	for i in Plots:
            if ( 'qual' in args.process ):
                plotQuality(
                    i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8],
                    fitRatio=args.addFit )
            elif ( 'stack' in args.process ):
                stackPlots(
                    i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10],
                    fitRatio=args.addFit )
