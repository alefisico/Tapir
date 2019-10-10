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

####gReset()
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

ttbarComp = OrderedDict()
ttbarComp['ttb'] = [ 'tt+b', kRed+4 ]
ttbarComp['tt2b'] = [ 'tt+2b', kRed+3 ]
ttbarComp['ttbb'] = [ 'tt+bb', kRed+2 ]
ttbarComp['ttcc'] = [ 'tt+cc', kRed-1 ]
ttbarComp['ttll'] = [ 'tt+light', kRed-2 ]

selection = {}
selection['SL_presel'] = [ 'SL Preselection' ]
selection['DL_presel'] = [ 'DL Preselection' ]
#selection['SL_presel'] = [ 'nlep > 0', 'nJets > 3', 'nDeepCSVM > 1' ]

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


def stackPlots( nameInRoot, label, xmin, xmax, rebinX, ymin, ymax, labX, labY, log, moveCMSlogo=False, fitRatio=False ):
	"""docstring for stacked plot"""

	outputFileName = nameInRoot+'_'+args.cut+'_stackPlots_'+args.version+'.'+args.ext
	print 'Processing.......', outputFileName

	#if (labY < 0.5) and ( labX < 0.5 ): legend=TLegend(0.20,0.50,0.50,0.62)
	#elif (labX < 0.5): legend=TLegend(0.20,0.75,0.50,0.87)
	legend=TLegend(0.70,0.53,0.90,0.83)
	legend.SetFillStyle(0)
	legend.SetTextSize(0.04)

	histos = {}
        for idataLabel, idata in dataFiles.iteritems():
            try:
                histos[ 'Data' ].Add( idata.Get( args.ttbarDecay+'_'+nameInRoot+'_'+idataLabel+'_Run2018' ) )
            except (KeyError, AttributeError) as e:
                histos[ 'Data' ] = idata.Get( args.ttbarDecay+'_'+nameInRoot+'_'+idataLabel+'_Run2018' )
	if rebinX != 1: histos[ 'Data' ].Rebin( rebinX )
	hData = histos[ 'Data' ].Clone()
	legend.AddEntry( hData, 'DATA' , 'ep' )

        hBkgStack = THStack('stackHisto', 'hBkg')
	hBkg = histos[ 'Data' ].Clone()
	hBkg.Reset()
        tmpHistos = {}
        for isamLabel, isam in bkgFiles.iteritems():
            #numEventsProc = isam[0].Get( 'eventProcessed_'+isamLabel ).GetEntries()
            if 'TT' in isamLabel:
                for flaLabel, flaInfo in ttbarComp.iteritems():
                    tmpHistos[ flaLabel+'_'+isamLabel ] = isam[0].Get( args.ttbarDecay+'_'+nameInRoot+'_'+isamLabel+'_'+flaLabel )
                    tmpHistos[ flaLabel+'_'+isamLabel ].Scale( isam[1] )
                    tmpHistos[ flaLabel+'_'+isamLabel ].SetFillStyle( 1001 )
                    tmpHistos[ flaLabel+'_'+isamLabel ].SetFillColor( flaInfo[1] )
                    hBkg.Add( tmpHistos[ flaLabel+'_'+isamLabel ].Clone() )
                    if rebinX != 1: tmpHistos[ flaLabel+'_'+isamLabel ].Rebin( rebinX )
                    if flaLabel in histos:
                        histos[ flaLabel ].Add(tmpHistos[ flaLabel+'_'+isamLabel ])
                        hBkgStack.Add( histos[ flaLabel ].Clone() )
                    else:
                        histos[ flaLabel ] = tmpHistos[ flaLabel+'_'+isamLabel ]
                        legend.AddEntry( histos[ flaLabel ], flaInfo[0], 'f' )
            else:
                histos[ isamLabel ] = isam[0].Get( args.ttbarDecay+'_'+nameInRoot+'_'+isamLabel )
                histos[ isamLabel ].Scale( isam[1] )
                histos[ isamLabel ].SetFillStyle( 1001 )
                histos[ isamLabel ].SetFillColor( flaInfo[1] )
                legend.AddEntry( histos[ isamLabel ], flaInfo[0], 'f' )
                if rebinX != 1: histos[ isamLabel ].Rebin( rebinX )
                hBkg.Add( histos[ isamLabel ].Clone() )
                hBkgStack.Add( histos[ isamLabel ].Clone() )


        for isignalLabel, isig in signalFiles.iteritems():
            ##numEventsProc = isam[0].Get( 'eventProcessed_'+isamLabel ).GetEntries()
            hSignal = isig[0].Get( args.ttbarDecay+'_'+nameInRoot+'_'+isignalLabel )
            hSignal.Scale( isig[1] )
            #histos[ isignalLabel ].SetFillStyle( 1001 )
            hSignal.SetLineWidth( 2 )
            hSignal.SetLineColor( isig[3] )
            legend.AddEntry( hSignal, isig[2], 'l' )
            if rebinX != 1: hSignal.Rebin( rebinX )

        hBkg.SetFillColor(kBlack)
        hBkg.SetFillStyle(3004)
        legend.AddEntry( hBkg, 'stat', 'f' )

	hRatio = TGraphAsymmErrors()
	hRatio.Divide( hData, hBkg, 'pois' )
	hRatioStatErr = hBkg.Clone()
	hRatioStatErr.Divide( hBkg )
        hRatioStatErr.SetFillColor(kBlack)
        hRatioStatErr.SetFillStyle(3004)


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
        hBkg.Draw('e2 same')
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
        hRatioStatErr.Draw('same e2')
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

	outputFileName = nameInRoot+'_'+args.ttbarDecay+'_dataQualityPlots_'+args.version+'.'+args.ext
	print 'Processing.......', outputFileName

	histos = {}

        for idataLabel, idata in dataFiles.iteritems():
            try:
                histos[ 'Data' ].Add( idata.Get( 'tthbb13/'+nameInRoot ) )
                #histos[ 'Data' ].Add( idata.Get( args.ttbarDecay+'_'+nameInRoot+'_'+idataLabel+'_Run2018' ) )
            except (KeyError, AttributeError) as e:
                #histos[ 'Data' ] = idata.Get( args.ttbarDecay+'_'+nameInRoot+'_'+idataLabel+'_Run2018' )
                #histos[ 'Data' ] = idata.Get( 'tthbb13/'+nameInRoot )
                histos[ 'Data' ] = idata.Get( 'tthbb13/'+nameInRoot.split('Total')[0] )

        histos[ 'Bkg' ] = histos[ 'Data' ].Clone()
        histos[ 'Bkg' ].Reset()
        for isamLabel, isam in bkgFiles.iteritems():
            #numEventsProc = float(isam[0].Get( 'genEventSumw_'+isamLabel ).GetBinContent(1)/isam[0].Get('genEventSumw_'+isamLabel).GetEntries())
#            if 'TT' in isamLabel:
#                for flaLabel, flaInfo in ttbarComp.iteritems():
#                    histos[ flaLabel ] = isam[0].Get( args.ttbarDecay+'_'+nameInRoot+'_'+isamLabel+'_'+flaLabel )
#                    histos[ flaLabel ].Scale( isam[1] )
#                    histos[ 'Bkg' ].Add( histos[ flaLabel ] )
#            else:
            histos[ isamLabel ] = isam[0].Get( 'tthbb13/'+nameInRoot )
            #histos[ isamLabel ] = isam[0].Get( args.ttbarDecay+'_'+nameInRoot+'_'+isamLabel )
            histos[ isamLabel ].Scale( isam[1] )
            histos[ 'Bkg' ].Add( histos[ isamLabel ] )

	if rebinX != 1:
            histos[ 'Data' ].Rebin( rebinX )
            histos[ 'Bkg' ].Rebin( rebinX )
	hData = histos[ 'Data' ].Clone()
	hBkg = histos[ 'Bkg' ].Clone()

	hRatio = TGraphAsymmErrors()
	hRatio.Divide( hData, hBkg, 'pois' )
	hRatioStatErr = hBkg.Clone()
	hRatioStatErr.Divide( hBkg )
        hRatioStatErr.SetFillColor(kBlack)
        hRatioStatErr.SetFillStyle(3004)

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
        #hBkg.SetFillColor(kBlack)
        #hBkg.SetFillStyle(3004)
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
	hBkg.Draw('hist same e2')
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
        #setSelection( selection[ args.ttbarDecay+'_'+args.cut ], labX, labY )

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
        hRatioStatErr.Draw('same e2')
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

def plotSimpleComparison( inFile1, sample, inFile2, sample2, name, rebinX=1, xmin='', xmax='', labX=0.92, labY=0.50, axisX='', axisY='', log=False, ext='png', Norm=False ):
    """"Take two root files, make simple comparison plot"""

    outputFileName = name+'_'+sample+sample2+'_simpleComparisonPlot'+args.version+'.'+ext
    print('Processing.......', outputFileName)

    histo = inFile1.Get( 'tthbb13/'+name )
    if rebinX!=1: histo.Rebin( rebinX )
    histo2 = inFile2.Get( 'tthbb13/'+name )
    if rebinX!=1: histo2.Rebin( rebinX )

    binWidth = histo.GetBinWidth(1)

    legend=TLegend(0.60,0.75,0.90,0.90)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.03)

    #histo.SetFillColor(48)
    histo.SetFillStyle(1001)

    tdrStyle.SetPadRightMargin(0.05)
    canvas[name] = TCanvas('c1', 'c1',  10, 10, 750, 500 )
    if log:
        canvas[name].SetLogy()
        outName = outputFileName.replace('_simplePlot','_Log_simplePlot')
    else: outName = outputFileName

    legend.AddEntry( histo, sample, 'f' )
    legend.AddEntry( histo2, sample2, 'f' )
    if xmax and xmin: histo.GetXaxis().SetRangeUser( xmin, xmax )
    histo.GetYaxis().SetTitleOffset(0.90)
    histo.SetLineColor(kRed)
    histo2.SetLineColor(kBlue)
    histo.DrawNormalized('hist')
    histo2.DrawNormalized('hist same')
    if not axisY: histo.GetYaxis().SetTitle( 'Events / '+str(binWidth) )
    if axisX: histo.GetXaxis().SetTitle( axisX )

    #labelAxis( name, histo, '' )
    legend.Draw()

    canvas[name].SaveAs( 'Plots/'+outName )
    #del can

def plotSignalBkg( name, xmin, xmax, rebinX, axisX='', axisY='', labX=0.92, labY=0.50, log=False,
                      addRatioFit=False, Norm=False, ext='png' ):
    """function to plot s and b histos"""

    outputFileName = name+'_PlusBkg_AnalysisPlots_'+args.version+'.'+ext
    if log: outputFileName = outputFileName.replace('Plots','Plots_Log')
    if Norm: outputFileName = outputFileName.replace('Plots','Plots_Normalized')
    print('Processing.......', outputFileName)

    legend=TLegend(0.60,0.60,0.90,0.90)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)

#	if 'DATA' in args.process:
#		dataHistos = {}
#		dataHistos[ 'DATA' ] = dataFile.Get( nameInRoot+'_JetHT_Run2016'+tmpRegion if args.miniTree else args.boosted+'AnalysisPlots'+('' if 'pruned' in args.grooming else args.grooming)+'/'+nameInRoot  )
#		if 'massAve' in nameInRoot:
#			dataHistos[ 'DATA' ] = dataHistos[ 'DATA' ].Rebin( len( boostedMassAveBins )-1, dataHistos[ 'DATA' ].GetName(), boostedMassAveBins )
#			dataHistos[ 'DATA' ].Scale ( 1, 'width' )
#		elif rebinX > 1: dataHistos[ 'DATA' ] = dataHistos[ 'DATA' ].Rebin( rebinX )
#        legend.AddEntry( dataHistos[ 'DATA' ], 'Data', 'lep' )
#        if Norm: dataHistos[ 'DATA' ].Scale( 1 /dataHistos['DATA'].Integral() )

    bkgHistos = OrderedDict()
    binWidth = 0
    maxList = []
    bkgInMassWindow = 0
    bkgInMassWindowErr = 0
    if len(bkgFiles) > 0:
        for bkgSamples in bkgFiles:
            bkgHistos[ bkgSamples ] = bkgFiles[ bkgSamples ][0].Get( 'tthbb13/'+name )
            bkgHistos[ bkgSamples ].SetTitle(bkgSamples)
            if bkgFiles[ bkgSamples ][1] != 1: bkgHistos[ bkgSamples ].Scale( bkgFiles[ bkgSamples ][1] )
            print(bkgSamples, round(bkgHistos[ bkgSamples ].Integral(), 2) )
            if rebinX > 1: bkgHistos[ bkgSamples ] = bkgHistos[ bkgSamples ].Rebin( rebinX )
            legend.AddEntry( bkgHistos[ bkgSamples ], bkgSamples, 'l' if Norm else 'f' )

            if Norm:
                bkgHistos[ bkgSamples ].SetLineColor( bkgFiles[ bkgSamples ][2] )
                bkgHistos[ bkgSamples ].SetLineWidth( 2 )
                try: bkgHistos[ bkgSamples ].Scale( 1 / bkgHistos[ bkgSamples ].Integral() )
                except ZeroDivisionError: pass
                maxList.append( bkgHistos[ bkgSamples ].GetMaximum() )
            else:
                bkgHistos[ bkgSamples ].SetFillStyle( 1001 )
                bkgHistos[ bkgSamples ].SetFillColor( int(bkgFiles[ bkgSamples ][2]) )

    signalHistos = OrderedDict()
    if len(signalFiles) > 0:
        dummySig=0
        for sigSamples in signalFiles:
            signalHistos[ sigSamples ] = signalFiles[ sigSamples ][0].Get( 'tthbb13/'+name )
            if signalFiles[ sigSamples ][1] != 1: signalHistos[ sigSamples ].Scale( signalFiles[ sigSamples ][1] )
            print(sigSamples, round(signalHistos[ sigSamples ].Integral(), 2) )
            legend.AddEntry( signalHistos[ sigSamples ], sigSamples, 'l' if Norm else 'f' )
#			if 'massAve' in nameInRoot:
#				signalHistos[ sigSamples ].Scale( twoProngSF * antiTau32SF )
#				signalHistos[ sigSamples ] = signalHistos[ sigSamples ].Rebin( len( boostedMassAveBins )-1, signalHistos[ sigSamples ].GetName(), boostedMassAveBins )
#				signalHistos[ sigSamples ].Scale ( 1, 'width' )
#				totalIntegralSig = signalHistos[ sigSamples ].Integral()
#				nEntriesTotalSig = signalHistos[ sigSamples ].GetEntries()
#				totalSF = totalIntegralSig/nEntriesTotalSig
#				windowIntegralSigErr = Double(0)
#				windowIntegralSig = signalHistos[ sigSamples ].IntegralAndError((args.mass-10)/rebinX, (args.mass+10)/rebinX, windowIntegralSigErr )
#				print sigSamples, round(totalIntegralSig,2), nEntriesTotalSig, totalSF
#				print sigSamples, 'in mass window', round(windowIntegralSig,2), ', nEntries', windowIntegralSig/totalSF, windowIntegralSigErr
            if rebinX > 1: signalHistos[ sigSamples ] = signalHistos[ sigSamples ].Rebin( rebinX )
            if Norm:
                signalHistos[ sigSamples ].SetLineColor( signalFiles[ sigSamples ][2] )
                signalHistos[ sigSamples ].SetLineWidth( 3 )
                signalHistos[ sigSamples ].SetLineStyle( 10-dummySig )
                signalHistos[ sigSamples ].Scale( 1 / signalHistos[ sigSamples ].Integral() )
                maxList.append( signalHistos[ sigSamples ].GetMaximum() )
            else:
#				if 'DATA' in args.process:
#					signalHistos[ sigSamples ].SetLineColor( signalFiles[ sigSamples ][3] )
#					signalHistos[ sigSamples ].SetFillColor(0)
#					signalHistos[ sigSamples ].SetLineWidth(3)
#					signalHistos[ sigSamples ].SetLineStyle(2+dummySig)
#				else:
                signalHistos[ sigSamples ].SetFillStyle( 1001 )
                signalHistos[ sigSamples ].SetFillColor( signalFiles[ sigSamples ][2] )
                signalHistos[ sigSamples ].SetLineColor( signalFiles[ sigSamples ][2] )
            binWidth = int(signalHistos[ sigSamples ].GetBinWidth( 1 ))
            dummySig+=8


    hBkg = bkgHistos[next(iter(bkgHistos))].Clone()
    hBkg.Reset()

    if not Norm:

        stackHisto = THStack('stackHisto'+name, 'stack'+name)
        for samples in signalHistos:
            stackHisto.Add( signalHistos[ samples ].Clone() )
        for samples in bkgHistos:
            stackHisto.Add( bkgHistos[ samples ].Clone() )
            hBkg.Add( bkgHistos[ samples ].Clone() )

        canvas[outputFileName] = TCanvas('c1'+name, 'c1'+name,  10, 10, 750, 500 )
        #tdrStyle.SetPadRightMargin(0.05)
        #tdrStyle.SetPadLeftMargin(0.15)
        #pad1 = TPad("pad1", "Fit",0,0.207,1.00,1.00,-1)
        #pad2 = TPad("pad2", "Pull",0,0.00,1.00,0.30,-1);
        #pad1.Draw()
        #pad2.Draw()

        #pad1.cd()
        #if log and not args.final: pad1.SetLogy()
        if log: canvas[outputFileName].SetLogy()
        stackHisto.Draw('hist')

        if xmax: stackHisto.GetXaxis().SetRangeUser( xmin, xmax )
        #stackHisto.SetMaximum( hBkg.GetMaximum()*1.2 )
        stackHisto.GetYaxis().SetTitleOffset( 0.8 )

        #stackHisto.SetMinimum( 0.1 )
        #hBkg.SetFillStyle(0)
        hBkg.SetLineColor(kBlack)
        hBkg.SetLineStyle(1)
        hBkg.SetLineWidth(1)
        #hBkg.SetFillStyle(3004)
        #hBkg.SetFillColor( kRed )
        #hBkg.Draw("same")

        stackHisto.GetYaxis().SetTitle( 'Events / '+str(binWidth)+' GeV' )
        stackHisto.GetXaxis().SetTitle( axisX )

#		if 'DATA' in args.process:
#			dataHistos[ 'DATA' ].SetMarkerStyle(8)
#			dataHistos[ 'DATA' ].Draw('same')
#			CMS_lumi.extraText = ""#"Preliminary"
#			legend.SetNColumns(2)
#			if not 'Tau32' in args.cut:
#				for sample in signalHistos:
#					if 'massAve' in nameInRoot:
#						#lowEdgeWindow = int(int(sample) - ( int( massWidthList[int(sample)])*3 ))
#						#highEdgeWindow = int(int(sample) + ( int( massWidthList[int(sample)])*3 ))
#						tmpResolution = 2*(-1.78 + ( 0.1097 * int(sample)) + ( -0.0002897 * int(sample)*int(sample) ) + ( 3.18e-07 * int(sample)*int(sample)*int(sample)))
#						lowEdgeWindow = int(int(sample) - tmpResolution )
#						highEdgeWindow = int(int(sample) + tmpResolution )
#						signalHistos[ sample ].GetXaxis().SetRangeUser( lowEdgeWindow, highEdgeWindow )
#					signalHistos[ sample ].Draw("hist same")
#		else:

        tmpHisto = {}
        for sample in signalHistos:
            tmpHisto[ sample ] = signalHistos[ sample ].Clone()
            tmpHisto[ sample ].SetFillColor(0)
            tmpHisto[ sample ].SetLineStyle(2)
            tmpHisto[ sample ].SetLineWidth(3)
            tmpHisto[ sample ].Draw("hist same")

        #CMS_lumi.relPosX = 0.14
        CMS_lumi.CMS_lumi( canvas[outputFileName], 4, 0)
        legend.Draw()

#         if not args.final:
# 			pad2.cd()
# 			pad2.SetGrid()
# 			pad2.SetTopMargin(0)
# 			pad2.SetBottomMargin(0.3)

# 			if 'DATA' in args.process:
# 				tmpPad2= pad2.DrawFrame(xmin,0.5,xmax,1.5)
# 				labelAxis( name.replace( args.cut, ''), tmpPad2, ( 'softDrop' if 'Puppi' in args.grooming else args.grooming ) )
# 				tmpPad2.GetYaxis().SetTitle( "Data/Bkg" )
# 				tmpPad2.GetYaxis().SetTitleOffset( 0.5 )
# 				tmpPad2.GetYaxis().CenterTitle()
# 				tmpPad2.SetLabelSize(0.12, 'x')
# 				tmpPad2.SetTitleSize(0.12, 'x')
# 				tmpPad2.SetLabelSize(0.12, 'y')
# 				tmpPad2.SetTitleSize(0.12, 'y')
# 				tmpPad2.SetNdivisions(505, 'x')
# 				tmpPad2.SetNdivisions(505, 'y')
# 				pad2.Modified()
# 				hRatio = TGraphAsymmErrors()
# 				hRatio.Divide( dataHistos[ 'DATA' ], hBkg, 'pois' )
# 				hRatio.SetMarkerStyle(8)
# 				hRatio.Draw('P')

# 			else:
# 				hRatio = signalHistos[ args.mass ].Clone()
# 				hRatio.Reset()
# 				allBkgWindow = 0
# 				allSigWindow = 0
# 				for ibin in range((args.mass-10)/rebinX, (args.mass+10)/rebinX+1 ):
# 					binContSignal = signalHistos[ args.mass ].GetBinContent(ibin)
# 					allSigWindow += binContSignal
# 					binContBkg = hBkg.GetBinContent(ibin)
# 					allBkgWindow += binContBkg
# 					try: value = binContSignal / TMath.Sqrt( binContBkg )
# 					#try: value = binContSignal / TMath.Sqrt( binContSignal + binContBkg )
# 					#try: value = binContSignal / ( binContSignal + binContBkg )
# 					except ZeroDivisionError: continue
# 					hRatio.SetBinContent( ibin, value )
# 				ratioLabel = "S / #sqrt{B}"
# 				print 's/sqrt(B) ', allSigWindow/TMath.Sqrt(allBkgWindow), allSigWindow, allBkgWindow, allSigWindow/allBkgWindow
# 				print '2 ( sqrt(B+S) - sqrt(B) )', 2*( TMath.Sqrt( allBkgWindow+allSigWindow ) - TMath.Sqrt( allBkgWindow ) )

# 				labelAxis( name, hRatio, ( 'softDrop' if 'Puppi' in args.grooming else args.grooming) )
# 				hRatio.GetYaxis().SetTitleOffset(1.2)
# 				hRatio.GetXaxis().SetLabelSize(0.12)
# 				hRatio.GetXaxis().SetTitleSize(0.12)
# 				hRatio.GetYaxis().SetTitle( ratioLabel )
# 				hRatio.GetYaxis().SetLabelSize(0.12)
# 				hRatio.GetYaxis().SetTitleSize(0.12)
# 				hRatio.GetYaxis().SetTitleOffset(0.45)
# 				hRatio.GetYaxis().CenterTitle()
# 				#hRatio.SetMaximum(0.7)
# 				if xmax: hRatio.GetXaxis().SetRangeUser( xmin, xmax )
# 				hRatio.Draw( ("PES" if 'DATA' in args.process else "hist" ) )

# 			if addRatioFit:
# 				tmpFit = TF1( 'tmpFit', 'pol0', 120, 240 )
# 				hRatio.Fit( 'tmpFit', '', '', 120, 240 )
# 				tmpFit.SetLineColor( kGreen )
# 				tmpFit.SetLineWidth( 2 )
# 				tmpFit.Draw("sames")
# 				chi2Test = TLatex( 0.7, 0.8, '#splitline{#chi^{2}/ndF = '+ str( round( tmpFit.GetChisquare(), 2 ) )+'/'+str( int( tmpFit.GetNDF() ) )+'}{p0 = '+ str( round( tmpFit.GetParameter( 0 ), 2 ) ) +' #pm '+str(  round( tmpFit.GetParError( 0 ), 2 ) )+'}' )
# 				chi2Test.SetNDC()
# 				chi2Test.SetTextFont(42) ### 62 is bold, 42 is normal
# 				chi2Test.SetTextSize(0.10)
# 				chi2Test.Draw('same')

# 			if 'DATA' in args.process:
# 				hRatio.GetYaxis().SetNdivisions(505)
# 				line.Draw('same')

        canvas[outputFileName].SaveAs( 'Plots/'+outputFileName )

    else:

        tdrStyle.SetPadRightMargin(0.05)
        canvas[outputFileName]= TCanvas('c1', 'c1', 750, 500 )
        if log: canvas[outputFileName].SetLogy()
        signalHistos[next(iter(signalHistos))].GetYaxis().SetTitleOffset(1.0)
        signalHistos[next(iter(signalHistos))].GetYaxis().SetTitle( ( 'Normalized / '+str(int(binWidth))+' GeV' ) )
        if xmax: signalHistos[next(iter(signalHistos))].GetXaxis().SetRangeUser( xmin, xmax )
        signalHistos[next(iter(signalHistos))].Draw('hist')
        for bkgSamples in bkgHistos: bkgHistos[ bkgSamples ].Draw('hist same')
        if 'DATA' in args.process:
                dataHistos[ 'DATA' ].SetMarkerStyle(8)
                dataHistos[ 'DATA' ].Draw('same')
                CMS_lumi.extraText = ""#"Preliminary"
        #signalHistos[next(iter(signalHistos))].SetMaximum( 1.1 * max( maxList ) )

        if not 'DATA' in args.process: CMS_lumi.lumi_13TeV = ''
        CMS_lumi.relPosX = 0.11
        CMS_lumi.CMS_lumi(canvas[outputFileName], 4, 0)
        legend.Draw()

        canvas[outputFileName].SaveAs( 'Plots/'+outputFileName )
    del canvas[outputFileName]


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proc', action='store', default='1D', dest='process', help='Process to draw, example: 1D, 2D, MC.' )
        parser.add_argument('-d', '--decay', action='store', default='SL', dest='ttbarDecay', help='ttbar decay channel: SL, DL' )
	parser.add_argument('-v', '--version', action='store', default='v0', help='Version: v01, v02.' )
	parser.add_argument('-c', '--cut', action='store', default='presel', help='cut, example: sl+presel' )
	parser.add_argument('-s', '--single', action='store', default='all', help='single histogram, example: massAve_cutDijet.' )
	parser.add_argument('-l', '--lumi', action='store', type=float, default=59215., help='Luminosity, example: 1.' )
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
	CMS_lumi.extraText = "Preliminary"
	CMS_lumi.lumi_13TeV = str( round( (args.lumi/1000.), 2 ) )+" fb^{-1}, 13 TeV, 2017"


        tmp = 'noOrthogonal_' if '_' in args.version else ''
        VER = args.version.split('_')[1] if '_' in args.version else args.version
        bkgFiles["ST_s-channel"] = [ TFile('Rootfiles/'+VER+'/histograms_ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_'+tmp+'boosted.root'), args.lumi*10.3*.3259/9914948.,  40 ]
        bkgFiles["ST_t-channel"] = [ TFile('Rootfiles/'+VER+'/histograms_ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8_'+tmp+'boosted.root'), args.lumi*136.02/5982064.,  41 ]
        bkgFiles["ST_tW_antitop"] = [ TFile('Rootfiles/'+VER+'/histograms_ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*35.85/7745276., 40 ]
        bkgFiles["ST_tW_top"] = [ TFile('Rootfiles/'+VER+'/histograms_ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*35.85/7945242., 40 ]
        bkgFiles["TTTo2L2Nu"] = [ TFile('Rootfiles/'+VER+'/histograms_TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*88.342/283000430.596, 29 ]
        bkgFiles["TTToHadronic"] = [ TFile('Rootfiles/'+VER+'/histograms_TTToHadronic_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*377.96/1647945788.34, 19 ]
        bkgFiles["TTToSemiLeptonic"] = [ TFile('Rootfiles/'+VER+'/histograms_TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*365.46/720253370.04, 27 ]
        bkgFiles["TTWJetsToQQ"] = [ TFile('Rootfiles/'+VER+'/histograms_TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_'+tmp+'boosted.root'), args.lumi*0.3708/811306, 37  ]
        bkgFiles["TTZToQQ"] = [ TFile('Rootfiles/'+VER+'/histograms_TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8_'+tmp+'boosted.root'),  args.lumi*0.6012/750000, 46 ]
        bkgFiles["WW"] = [ TFile('Rootfiles/'+VER+'/histograms_WW_TuneCP5_13TeV-pythia8_'+tmp+'boosted.root'), args.lumi*118.7/7791498, 38 ]
        ##bkgFiles["THW"] = [ TFile('Rootfiles/'+VER+'/histograms_THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8_'+tmp+'boosted.root'), args.lumi*0.1475/4719999., 46 ]
        bkgFiles["TTGJets"] = [ TFile('Rootfiles/'+VER+'/histograms_TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_'+tmp+'boosted.root'), args.lumi*3.697/7349100., 12 ]
        bkgFiles["WJets"] = [ TFile('Rootfiles/'+VER+'/histograms_WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_'+tmp+'boosted.root'), args.lumi*61526.7/33073306., 33 ]
        #bkgFiles[""] = [ TFile('Rootfiles/'+VER+'/'), 1 ]
        #bkgFiles[""] = [ TFile('Rootfiles/'+VER+'/'), 1 ]

        #signalFiles["ttHToNonbb"] = [ TFile('Rootfiles/'+VER+'/histograms_ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), 1 ]
        signalFiles["ttHTobb"] = [ TFile('Rootfiles/'+VER+'/histograms_ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*0.2934045/4216319.32, kRed ]
        #signalFiles["ttHTobb_ttToSemiLep"] = [ TFile('Rootfiles/'+VER+'/histograms_ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8.root'), args.lumi*0.093/9332943,1 ]
        #signalFiles[""] = [ TFile('Rootfiles/'+VER+'/'), 1 ]

        '''
        #bkgFiles[ 'TTToSemiLeptonic' ] = [ TFile.Open('Rootfiles/'+args.version+'/TTToSemiLeptonic_'+args.version+'.root'), args.lumi*(831.76*2*0.6741*0.3259), 'ttbar' ]
        bkgFiles[ 'TTToSemiLeptonic' ] = [ TFile.Open('Rootfiles/'+args.version+'/TTToSemiLeptonic_'+args.version+'.root'), args.lumi*(831.76*2*0.6741*0.3259)/101340000., 'ttbar' ]
        #bkgFiles[ 'TTToSemiLeptonic' ] = [ TFile.Open('Rootfiles/'+args.version+'/TTToSemiLeptonic_'+args.version+'.root'), args.lumi*(831.76*2*0.6741*0.3259)/101550000., 'ttbar' ]
        #bkgFiles[ 'TTTo2L2Nu' ] = [ TFile.Open('Rootfiles/'+args.version+'/TTTo2L2Nu_'+args.version+'.root'), args.lumi*(831.76*0.3259*0.3259), 'ttbar' ]
        #bkgFiles[ 'TTTo2L2Nu' ] = [ TFile.Open('Rootfiles/'+args.version+'/TTTo2L2Nu_'+args.version+'.root'), args.lumi*(831.76*0.3259*0.3259)/63767169., 'ttbar' ]

        if args.ttbarDecay.startswith("DL"):
            dataFiles['EGamma'] = TFile.Open('Rootfiles/'+args.version+'/EGamma_Run2018All_'+args.version+'.root')
            dataFiles['MuonEG'] = TFile.Open('Rootfiles/'+args.version+'/MuonEG_Run2018All_'+args.version+'.root')
            dataFiles['DoubleMuon'] = TFile.Open('Rootfiles/'+args.version+'/DoubleMuon_Run2018All_'+args.version+'.root')

            signalFiles[ 'ttHTobb_ttTo2L2Nu' ] = [ TFile.Open('Rootfiles/'+args.version+'/ttHTobb_ttTo2L2Nu_'+args.version+'.root'), (args.lumi*0.5071 * 0.4176 * 2 * 0.6741 * 0.3259/9524600.)*50, 'ttH(bb) (x50)', kBlue-4 ]
        else:
            #dataFiles['EGamma'] = TFile.Open('Rootfiles/'+args.version+'/EGamma_'+args.version+'.root')
            dataFiles['SingleMuon'] = TFile.Open('Rootfiles/'+args.version+'/SingleMuon_'+args.version+'.root')
            #dataFiles['EGamma'] = TFile.Open('Rootfiles/'+args.version+'/EGamma_Run2018All_'+args.version+'.root')
            #dataFiles['SingleMuon'] = TFile.Open('Rootfiles/'+args.version+'/SingleMuon_Run2018All_'+args.version+'.root')
            #signalFiles[ 'ttHTobb_ttToSemiLep' ] = [ TFile.Open('Rootfiles/'+args.version+'/ttHTobb_ttToSemiLep_'+args.version+'.root'), (args.lumi*0.5071 * 0.4176 * 0.3259* 0.3259/9577300.)*50, 'ttH(bb) (x50)', kBlue-4 ]

#        bkgFiles[ 'ST_s-channel' ] = [ TFile.Open('Rootfiles/'+args.version+'/ST_s-channel_'+args.version+'.root'), (args.lumi*11.36/12441255.), 'Single top', kBlue-4 ]
#        bkgFiles[ 'ST_t-channel_antitop' ] = [ TFile.Open('Rootfiles/'+args.version+'/ST_t-channel_antitop_'+args.version+'.root'), (args.lumi*80.95/74188955.), 'Single top', kBlue-4 ]
#        bkgFiles[ 'ST_t-channel_top' ] = [ TFile.Open('Rootfiles/'+args.version+'/ST_t-channel_top_'+args.version+'.root'), (args.lumi*136.02/144039704.), 'Single top', kBlue-4 ]
#        bkgFiles[ 'ST_tW_antitop' ] = [ TFile.Open('Rootfiles/'+args.version+'/ST_tW_antitop_'+args.version+'.root'), (args.lumi*35.85/7584921.), 'Single top', kBlue-4 ]
#        bkgFiles[ 'ST_tW_top_5f_inclusiveDecays' ] = [ TFile.Open('Rootfiles/'+args.version+'/ST_tW_top_'+args.version+'.root'), (args.lumi*35.85/9549813.), 'Single top', kBlue-4 ]
        '''

	taulabX = 0.90
	taulabY = 0.85
	massMinX = 0
	massMaxX = 400

	plotList = [
		##[ '2D', 'Boosted', 'leadMassHT', 'Leading Jet Mass [GeV]', 'HT [GeV]', 0, massMaxX, 1, 100, 1300, 1, jetMassHTlabX, jetMassHTlabY],
		##[ '2DResolved', 'Resolved', 'etas', '#eta_{jj1}', '#eta_{jj2}', -3.0, 3.0, 10, -3.0, 3.0, 10, jetMassHTlabX, jetMassHTlabY],

		[ 'stack', 'jetsByPt_0_pt', 'Leading jet pT [GeV]', 0, 600, 2, 10, 20e4, 0.90, 0.85, False, False],
		[ 'stack', 'jetsByPt_1_pt', '2nd leading jet pT [GeV]', 0, 1000, 2, 1, 10e5,  0.90, 0.85, True, False],
		[ 'stack', 'jetsByPt_2_pt', '3rd leading jet pT [GeV]', 0, 1000, 2, 1, 10e5,  0.90, 0.85, True, False],
		[ 'stack', 'jetsByPt_3_pt', '4th leading jet pT [GeV]', 0, 1000, 2, 1, 10e5,  0.90, 0.85, True, False],
		[ 'stack', 'jetsByPt_0_eta', 'Leading jet #eta', -2.5, 2.5, 1, 100, 10e6,  0.90, 0.85, True, False],
		[ 'stack', 'jetsByPt_1_eta', '2nd leading jet #eta', -2.5, 2.5, 1, 100, 10e6, 0.90, 0.85, True, False],
		[ 'stack', 'jetsByPt_2_eta', '3rd leading jet #eta', -2.5, 2.5, 1, 100, 10e6, 0.90, 0.85, True, False],
		[ 'stack', 'jetsByPt_3_eta', '4th leading jet #eta', -2.5, 2.5, 1, 100, 10e6, 0.90, 0.85, True, False],
		[ 'stack', 'jetsByPt_0_btag', 'Leading jet deepCSV discriminator', 0, 1, 1, 100, 10e6,  0.90, 0.85, True, False],
		[ 'stack', 'jetsByPt_1_btag', '2nd leading jet deepCSV discriminator', 0, 1, 1, 100, 10e6,  0.90, 0.85, True, False],
		[ 'stack', 'jetsByPt_2_btag', '3rd leading jet deepCSV discriminator', 0, 1, 1, 100, 10e6,  0.90, 0.85, True, False],
		[ 'stack', 'jetsByPt_3_btag', '4th leading jet deepCSV discriminator', 0, 1, 1, 100, 10e6,  0.90, 0.85, True, False],
		[ 'stack', 'lepsByPt_0_pt', 'Leading Lepton pT [GeV]', 0, 800, 2, 1, 10e5, 0.90, 0.85, True, False],
		[ 'stack', 'lepsByPt_0_eta', 'Leading Lepton #eta', -2.5, 2.5, 1, 100, 10e6,  0.90, 0.85, True, False],
		[ 'stack', 'lepsByPt_0_pt', '2nd Leading Lepton pT [GeV]', 0, 800, 2, 1, 10e5, 0.90, 0.85, True, False],
		[ 'stack', 'lepsByPt_0_eta', '2nd Leading Lepton #eta', -2.5, 2.5, 1, 100, 10e6,  0.90, 0.85, True, False],
		[ 'stack', 'met_pt', 'MET [GeV]', 0, 500, 2, 10, 10e6, 0.90, 0.85, True, False],
		[ 'stack', 'met_phi', 'MET #phi]', -3, 3, 1, 10, 10e6, 0.90, 0.85, True, False],
		[ 'stack', 'Wmass', 'W mass [GeV]', 0, 500, 2, 10, 10e6, 0.90, 0.85, True, False],
		#[ 'stack', 'll_mass', 'Dilepton mass [GeV]', 0, 500, 2, 10, 10e6, 0.90, 0.85, True, False],
		[ 'stack', 'njets', 'Number of jets', 2, 14, 1, 1, 10e6, 0.90, 0.85, True, False],
		[ 'stack', 'nleps', 'Number of leptons', 0, 5, 1, 1, 10e6, 0.90, 0.85, True, False],
		[ 'stack', 'nbjets', 'Number of deepCSVM jets', 1, 7, 1, 10, 10e7, 0.90, 0.85, True, False],
		#[ 'stack', 'mem_tth_SL_1w2h2t_p', 'MEM', 0, 0.00001, 1, 100, 10e7, 0.90, 0.85, True, False],
	####	[ 'stack', 'ht', 'HT [GeV]', 0, 2000, 5, 10, 10e6, 0.90, 0.85, True, False],

		[ 'qual', 'nPVs', 'Number of PV', 0, 100, 2,  0.85, 0.70, False, False],
		#[ 'qual', 'numJets', 'Number of jets', 2, 14, 1,  0.85, 0.70, True, False],
		#[ 'qual', 'FatJet_pt_all', 'jet pT [GeV]', 200, 1500, 5,  0.85, 0.70, True, False],
                #[ 'signalBkg', 'HiggsCandMass_WTop', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                ###[ 'signalBkg', 'TopCandMass_WTop', 'W candidate mass [GeV]', 30, 200, 1, False ],
                #[ 'signalBkg', 'HiggsCandMass_TopHiggs', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                ###[ 'signalBkg', 'TopCandMass_TopHiggs', 'W candidate mass [GeV]', 30, 200, 1, False ],
                [ 'signalBkg', 'HiggsCandMass_WHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'WCandMass_WHiggs', 'W candidate mass [GeV]', 30, 200, 2, False ],
                ###[ 'signalBkg', 'TopCandMass_W', 'W candidate mass [GeV]', 30, 200, 1, False ],
                #[ 'signalBkg', 'WCandMass_W', 'W candidate mass [GeV]', 30, 200, 1, False ],
                #[ 'signalBkg', 'HiggsCandMass_PuppiJets', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                #[ 'signalBkg', 'WCandMass_PuppiJets', 'W candidate mass [GeV]', 30, 200, 1, False ],
                #[ 'signalBkg', 'WCandMass', 'W candidate mass [GeV]', 30, 200, 1, False ],
                #[ 'signalBkg', 'boostedHiggsCandMass_boostedW', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'signalBkg', 'tmpHiggsCandPt_boostedHiggs', 'Higgs candidate mass [GeV]', 200, 600, 2, False ],
                [ 'signalBkg', 'HiggsCandMass_2J_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'HiggsCandMass_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'HiggsCandMass_2J2W_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'resolvedWCandMass_2J_boostedHiggs', 'W candidate mass [GeV]', 30, 150, 1, False ],
                [ 'signalBkg', 'HiggsCandMass_2JdeltaRlepW_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'HiggsCandMass_A_2J_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'HiggsCandMass_B_2J_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'HiggsCandMass_C_2J_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'HiggsCandMass_D_2J_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'HiggsCandMass_A_W1B_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'HiggsCandMass_A_W_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'HiggsCandMass_W_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'HiggsCandMass_A_2J2W_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'resolvedWCandMass_2J2W_boostedHiggs', 'W candidate mass [GeV]', 30, 150, 1, False ],

                [ 'signalBkg', 'boostedHiggsCandMass_boostedW', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'WCandMass_boostedW', 'W candidate mass [GeV]', 30, 150, 1, False ],
                [ 'signalBkg', 'resolvedHiggsCandMass_2B_boostedW', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'signalBkg', 'resolvedHiggsCandMass_2BSmallR_boostedW', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'signalBkg', 'noResolvedHiggsCandMass_2BSmallR_boostedW', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'signalBkg', 'lepTopCandMass_2B_boostedW', 'Top candidate mass [GeV]', 100, 250, 2, False ],
                [ 'signalBkg', 'hadTopCandMass_2B_boostedW', 'Top candidate mass [GeV]', 100, 250, 2, False ],

                [ 'simple', 'nCleanPuppiJets_boostedHiggs', 'Number of PUPPI jets', 0, 15, 1, False ],
                [ 'simple', 'nGoodPuppiJets_boostedHiggs', 'Number of PUPPI jets', 0, 15, 1, False ],
                [ 'simple', 'nGoodPuppiBjets_boostedHiggs', 'Number of PUPPI bjets', 0, 15, 1, False ],
                [ 'simple', 'HiggsCandMass_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'HiggsCandMass_2J_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'HiggsCandMass_2JdeltaRlepW_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'resolvedRecWCandMass_2J_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'resolvedWCandMass_2J_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'HiggsCandMass_2J1B_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'HiggsCandMass_2J2B_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'HiggsCandMass_1B_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'HiggsCandMass_2B_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'HiggsCandMass_2J2W_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'deltaRhadWHiggs_2J_boostedHiggs', 'DeltaR', 0, 5, 5, False ],
                [ 'simple', 'deltaRJJ_2J_boostedHiggs', 'DeltaR', 0, 5, 5, False ],
                [ 'simple', 'deltaRlepWHiggs_2J_boostedHiggs', 'DeltaR', 0, 5, 5, False ],
                [ 'simple', 'deltaRlepWhadW_2J_boostedHiggs', 'DeltaR', 0, 5, 5, False ],
                [ 'simple', 'deltaR1BHiggs_2J1B_boostedHiggs', 'DeltaR', 0, 5, 5, False ],
                [ 'simple', 'deltaR1BHiggs_1B_boostedHiggs', 'DeltaR', 0, 5, 5, False ],

                [ 'simple', 'nGoodPuppiJets_boostedW', 'Number of PUPPI jets', 0, 15, 1, False ],
                [ 'simple', 'nGoodPuppiBjets_boostedW', 'Number of PUPPI bjets', 0, 15, 1, False ],
                [ 'simple', 'WCandMass_boostedW', 'W candidate mass [GeV]', 30, 200, 1, False ],
                [ 'simple', 'lepTopCandMass_2B_boostedW', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'hadTopCandMass_2B_boostedW', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'boostedHiggsCandMass_1B_boostedW', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'boostedHiggsCandMass_2B_boostedW', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'boostedHiggsCandMass_2J_boostedW', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'resolvedHiggsCandMass_2B_boostedW', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'resolvedHiggsCandMass_2BdeltaR_boostedW', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'allResolvedHiggsCandMass_2B_boostedW', 'Higgs candidate mass [GeV]', 30, 250, 1, False ],
                [ 'simple', 'deltaR2B_2B_boostedW', 'DeltaR', 0, 5, 5, False ],
		]

	if 'all' in args.single: Plots = [ x[1:] for x in plotList if ( ( args.process in x[0] ) )  ]
	else: Plots = [ y[1:] for y in plotList if ( ( args.process in y[0] ) and ( y[1] in args.single ) )  ]

	for i in Plots:
            if ( 'qual' in args.process ):
                plotQuality(
                    i[0]+"_"+args.cut, i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8],
                    fitRatio=args.addFit )
            elif ( 'stack' in args.process ):
                stackPlots(
                    i[0]+"_"+args.cut, i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10],
                    fitRatio=args.addFit )
            elif ( 'simple' in args.process ):
                plotSimpleComparison( bkgFiles["TTToSemiLeptonic"][0], "TTToSemiLeptonic", signalFiles["ttHTobb"][0], "ttHTobb", i[0], xmin=i[2], xmax=i[3], rebinX=i[4], log=i[5], axisX=i[1] )
            elif ( 'signalBkg' in args.process ):
                plotSignalBkg( i[0], i[2], i[3], i[4], log=args.log, axisX=i[1], Norm=args.norm)
