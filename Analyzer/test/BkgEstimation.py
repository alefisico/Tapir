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
import subprocess
#from histoLabels import labels, labelAxis, finalLabels
import CMS_lumi as CMS_lumi
import tdrstyle as tdrstyle
from DrawHistogram import dataFiles, bkgFiles, signalFiles
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

def BCDHisto( tmpHisto, BHisto, CHisto, DHisto ):
	"""docstring for BCDHisto: simple ABCD, order between B or C does not matter"""

	tmpHisto.Reset()
	#tmpHisto.SetName('NewBkgEst')
	#tmpHisto.SetTitle('NewBkgEst')
	for jbin in range( 0, tmpHisto.GetNbinsX()+1 ):
		Nominal_Side = BHisto.GetBinContent( jbin )
		Side_Nominal = CHisto.GetBinContent( jbin )
		NoSignal = DHisto.GetBinContent( jbin )
		if NoSignal != 0:
			Bkg = Nominal_Side*Side_Nominal/NoSignal
			try: BkgError = Bkg * TMath.Sqrt(
					TMath.Power(( TMath.Sqrt( Nominal_Side ) / Nominal_Side ), 2) +
					TMath.Power(( TMath.Sqrt( Side_Nominal ) / Side_Nominal ), 2) +
					TMath.Power(( TMath.Sqrt( NoSignal ) / NoSignal ), 2) )
			except ZeroDivisionError: BkgError = 0
		else:
			Bkg = 0
			BkgError = 1.8		### Poisson errors for bins with 0 content
		tmpHisto.SetBinContent( jbin, Bkg )
		tmpHisto.SetBinError( jbin, BkgError )
	return tmpHisto
########################################################

def BkgEstimation( name, xmin, xmax, rebinX, axisX='', axisY='', labX=0.92, labY=0.50, log=False, addRatioFit=False, Norm=False, ext='png' ):
    """Bkg Estimation with ABCD method"""

    outputFileName = name+'_BkgEstimationPlots_'+args.version+'.'+ext
    if log: outputFileName = outputFileName.replace('Plots','Plots_Log')
    if Norm: outputFileName = outputFileName.replace('Plots','Plots_Normalized')
    print('Processing.......', outputFileName)

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
            for side in [ 'A', 'B', 'C', 'D']: #, 'Nominal']:
                newName = name.replace('__', '_') if side.endswith('Nominal') else name.replace('__', '_'+side+'_')
                bkgHistos[ bkgSamples+side ] = bkgFiles[ bkgSamples ][0].Get( 'tthbb13/'+newName )
                bkgHistos[ bkgSamples+side ].SetTitle(bkgSamples+side)
                if bkgFiles[ bkgSamples ][1] != 1: bkgHistos[ bkgSamples+side ].Scale( bkgFiles[ bkgSamples ][1] )
                ##print(bkgSamples, bkgHistos[ bkgSamples ].Integral())
                if rebinX > 1: bkgHistos[ bkgSamples+side ] = bkgHistos[ bkgSamples+side ].Rebin( rebinX )
                #legend.AddEntry( bkgHistos[ bkgSamples+side ], bkgSamples, 'l' if Norm else 'f' )
                bkgHistos[ bkgSamples+side ].SetFillStyle( 1001 )
                bkgHistos[ bkgSamples+side ].SetFillColor( int(bkgFiles[ bkgSamples ][2]) )

    signalHistos = OrderedDict()
    if len(signalFiles) > 0:
        dummySig=0
        for sigSamples in signalFiles:
            for side in [ 'A', 'B', 'C', 'D' ]:
                newName = name.replace('__', '_') if side.endswith('Nominal') else name.replace('__', '_'+side+'_')

                signalHistos[ sigSamples+side ] = signalFiles[ sigSamples ][0].Get( 'tthbb13/'+newName )
                if signalFiles[ sigSamples ][1] != 1: signalHistos[ sigSamples+side ].Scale( signalFiles[ sigSamples ][1] )
                ####legend.AddEntry( signalHistos[ sigSamples ], sigSamples, 'l' if Norm else 'f' )
                if rebinX > 1: signalHistos[ sigSamples+side ] = signalHistos[ sigSamples+side ].Rebin( rebinX )
                signalHistos[ sigSamples+side ].SetFillStyle( 1001 )
                signalHistos[ sigSamples+side ].SetFillColor( signalFiles[ sigSamples ][2] )
                signalHistos[ sigSamples+side ].SetLineColor( signalFiles[ sigSamples ][2] )
            binWidth = int(signalHistos[ sigSamples+side ].GetBinWidth( 1 ))
            dummySig+=8


    hBkg = bkgHistos['TTToSemiLeptonicA'].Clone()
    hBkg.Reset()

    ABCDBkgHistos = {}
    for side in [ 'A', 'B', 'C', 'D', 'Nominal' ]:
        newName = name.replace('__', '_') if side.endswith('Nominal') else name.replace('__', '_'+side+'_')
        ABCDBkgHistos[ side ] = hBkg.Clone()
        ABCDBkgHistos[ side ].SetTitle( newName )
        ABCDBkgHistos[ side ].SetName( newName )
        #for samples in signalHistos:
        #    stackHisto.Add( signalHistos[ samples ].Clone() )
        for samples in bkgHistos:
            #stackHisto.Add( bkgHistos[ samples ].Clone() )
            if samples.endswith( side ): ABCDBkgHistos[ side ].Add( bkgHistos[ samples ].Clone() )

    canvas = {}
    for ih in ABCDBkgHistos:
        canvas[ih] = TCanvas('c1'+ih, 'c1'+ih,  10, 10, 750, 500 )
        ABCDBkgHistos[ih].Draw()
        ABCDBkgHistos[ih].GetYaxis().SetTitle( 'Events / '+str(binWidth)+' GeV' )
        ABCDBkgHistos[ih].GetXaxis().SetTitle( axisX )

        #CMS_lumi.relPosX = 0.14
        CMS_lumi.CMS_lumi( canvas[ih], 4, 0)
        canvas[ih].SaveAs( 'Plots/'+name+ih+'_checks.png')

    BkgEstHisto = BCDHisto( ABCDBkgHistos['A'].Clone(), ABCDBkgHistos['B'].Clone(), ABCDBkgHistos['C'].Clone(), ABCDBkgHistos['D'].Clone())

    canvas['bkgEst'] = TCanvas('c1bkgEst', 'c1bkgEst',  10, 10, 750, 500 )
    BkgEstHisto.SetLineColor(kRed)
    ABCDBkgHistos['A'].SetLineColor(kBlue)
    ABCDBkgHistos['C'].SetLineColor(kMagenta)
    BkgEstHisto.DrawNormalized('')
    ABCDBkgHistos['A'].DrawNormalized('same')
    ABCDBkgHistos['C'].DrawNormalized('same')
    ##ABCDBkgHistos['Nominal'].SetLineColor(kMagenta)
    #ABCDBkgHistos['Nominal'].Draw('same')
    BkgEstHisto.SetMaximum( 1.1*max( BkgEstHisto.GetMaximum(), ABCDBkgHistos['Nominal'].GetMaximum(), ABCDBkgHistos['A'].GetMaximum() ) )
    BkgEstHisto.GetYaxis().SetTitle( 'Events / '+str(binWidth)+' GeV' )
    BkgEstHisto.GetXaxis().SetTitle( axisX )
    BkgEstHisto.GetYaxis().SetTitleOffset(0.8)

    legend=TLegend(0.60,0.70,0.90,0.90)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)
    legend.AddEntry( BkgEstHisto, 'Bkg Estimation', 'lep' )
    #legend.AddEntry( ABCDBkgHistos['Nominal'], 'MC samples', 'lep' )
    legend.AddEntry( ABCDBkgHistos['A'], 'MC samples', 'lep' )
    legend.AddEntry( ABCDBkgHistos['C'], 'Region C', 'lep' )
    legend.Draw()

    #CMS_lumi.relPosX = 0.14
    CMS_lumi.CMS_lumi( canvas['bkgEst'], 4, 0)
    canvas['bkgEst'].SaveAs( 'Plots/'+outputFileName )

    del canvas


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
#        bkgFiles["ST_s-channel"] = [ TFile('Rootfiles/'+VER+'/histograms_ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_'+tmp+'boosted.root'), args.lumi*10.3*.3259/9914948.,  43 ]
#        bkgFiles["ST_t-channel"] = [ TFile('Rootfiles/'+VER+'/histograms_ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8_'+tmp+'boosted.root'), args.lumi*136.02/5982064.,  41 ]
#        bkgFiles["ST_tW_antitop"] = [ TFile('Rootfiles/'+VER+'/histograms_ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*35.85/7745276., 40 ]
#        bkgFiles["ST_tW_top"] = [ TFile('Rootfiles/'+VER+'/histograms_ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*35.85/7945242., 40 ]
        bkgFiles["TTTo2L2Nu"] = [ TFile('Rootfiles/'+VER+'/histograms_TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*88.342/283000430.596, 29 ]
        #bkgFiles["TTToSemiLeptonic"] = [ TFile('Rootfiles/'+VER+'/histograms_TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*365.46/720253370.04, 27 ]
        bkgFiles["TTToSemiLeptonic"] = [ TFile('Rootfiles/'+VER+'/histograms_TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*365.46/43732445., 27 ]
        #bkgFiles["TTWJetsToQQ"] = [ TFile('Rootfiles/'+VER+'/histograms_TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_'+tmp+'boosted.root'), args.lumi*0.3708/811306, 37  ]
        #bkgFiles["TTZToQQ"] = [ TFile('Rootfiles/'+VER+'/histograms_TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8_'+tmp+'boosted.root'),  args.lumi*0.6012/750000, 46 ]
        #bkgFiles["WW"] = [ TFile('Rootfiles/'+VER+'/histograms_WW_TuneCP5_13TeV-pythia8_'+tmp+'boosted.root'), args.lumi*118.7/7791498, 38 ]
        ##bkgFiles["THW"] = [ TFile('Rootfiles/'+VER+'/histograms_THW_ctcvcp_5f_Hincl_13TeV_madgraph_pythia8_'+tmp+'boosted.root'), args.lumi*0.1475/4719999., 46 ]
        #bkgFiles["TTGJets"] = [ TFile('Rootfiles/'+VER+'/histograms_TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_'+tmp+'boosted.root'), args.lumi*3.697/7349100., 12 ]
        #bkgFiles["WJets"] = [ TFile('Rootfiles/'+VER+'/histograms_WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8_'+tmp+'boosted.root'), args.lumi*61526.7/33073306., 33 ]
        #bkgFiles[""] = [ TFile('Rootfiles/'+VER+'/'), 1 ]
        #bkgFiles[""] = [ TFile('Rootfiles/'+VER+'/'), 1 ]

        signalFiles["ttHTobb"] = [ TFile('Rootfiles/'+VER+'/histograms_ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*0.2934045/4216319.32, kRed ]
        #signalFiles["ttHToNonbb"] = [ TFile('Rootfiles/'+VER+'/histograms_ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), 1 ]
        ####signalFiles["ttHTobb_ttToSemiLep"] = [ TFile('Rootfiles/'+VER+'/histograms_ttHTobb_ttToSemiLep_M125_TuneCP5_13TeV-powheg-pythia8_'+tmp+'boosted.root'), args.lumi*0.093/9332943, kRed ]
        #signalFiles[""] = [ TFile('Rootfiles/'+VER+'/'), 1 ]


	taulabX = 0.90
	taulabY = 0.85
	massMinX = 0
	massMaxX = 400

	plotList = [
                [ 'HiggsCandMass__boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'HiggsCandMass__2J_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'HiggsCandMass__2J2W_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'HiggsCandMass__2JdeltaR_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'HiggsCandMass__2JdeltaR2W_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                [ 'HiggsCandMass__2JdeltaR2W1B_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                #[ 'HiggsCandMass__W_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                #[ 'HiggsCandMass__W1B_boostedHiggs', 'Higgs candidate mass [GeV]', 30, 250, 2, False ],
                ]


	for i in plotList:
            BkgEstimation( i[0], i[2], i[3], i[4], log=args.log, axisX=i[1], Norm=args.norm)
