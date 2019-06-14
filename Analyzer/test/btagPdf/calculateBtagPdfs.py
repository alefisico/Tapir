#!/usr/bin/env python
####################################
### Script to create a root file with pdfs for diff btag discrminators
### Based on TTH/Plotting/python/christina/btag_pdfs/btag_pdfs.py
####################################

from ROOT import *
import os, argparse
import numpy as np
from collections import OrderedDict
from dbs.apis.dbsClient import DbsApi  ## talk to DBS to get list of files in this dataset
dbsglobal = DbsApi('https://cmsweb.cern.ch/dbs/prod/global/DBSReader')

btaggers = ["btagCSVV2", "btagDeepB", "btagDeepFlavB"]  ## name of btag disc. in nanoAOD

##########################################################
def pdfs(file_names, presel):
    """function to get btag pdfs"""

    # opening root files
    chain = TChain("Events")
    for file_name in file_names:
        print "Adding file "+file_name
        chain.AddFile(file_name)
    print "Chain contains "+str(chain.GetEntries())+" events"

    # initialize output file
    outputFileName = args.output+'_'+args.version+".root"
    output = TFile( outputFileName , "RECREATE")

    # initialize histograms
    allHistos = {}
    for b in btaggers:
        for f in ["b", "c", "l"]:
            allHistos[b+"_"+f+"_Bin0__rec"] = TH1F(b+"_"+f+"_Bin0__rec", b+"_"+f+"_Bin0__rec", 100, 0, 1)
            allHistos[b+"_"+f+"_pt"] = TH1F(b+"_"+f+"_pt", b+"_"+f+"_pt", 6, 20, 400)
            allHistos[b+"_"+f+"_eta"] = TH1F(b+"_"+f+"_eta", b+"_"+f+"_eta", 6, 0, 2.4)
            allHistos[b+"_"+f+"_Bin1__rec"] = TH1F(b+"_"+f+"_Bin1__rec", b+"_"+f+"_Bin1__rec", 100, 0, 1)
            allHistos[b+"_"+f+"_pt_eta"] = TH3F(b+"_"+f+"_pt_eta", b+"_"+f+"_pt_eta", 6, 20, 400, 6, 0, 2.4, 20, 0, 1)
    for h in allHistos: allHistos[h].Sumw2()

    # looping over btag disc.
    for b in btaggers:

        #### For light jets
        lJetSel = presel + TCut('(Jet_hadronFlavour[Iteration$]!=4) && (Jet_hadronFlavour[Iteration$]!=5)')
        chain.Draw("Jet_"+b+":abs(Jet_eta):Jet_pt>>"+b+"_l_pt_eta", lJetSel, 'normgoff' )
        chain.Draw("Jet_pt>>"+b+"_l_pt", lJetSel, 'normgoff' )
        chain.Draw("abs(Jet_eta)>>"+b+"_l_eta", lJetSel, 'normgoff' )
        chain.Draw("Jet_"+b+">>"+b+"_l_Bin0__rec", lJetSel+TCut('abs(Jet_eta[Iteration$])<=1.'), 'normgoff' )
        chain.Draw("Jet_"+b+">>"+b+"_l_Bin1__rec", lJetSel+TCut('abs(Jet_eta[Iteration$])>1.'), 'normgoff' )

        #### For c jets
        cJetSel = presel + TCut('Jet_hadronFlavour[Iteration$]==4')
        chain.Draw("Jet_"+b+":abs(Jet_eta):Jet_pt>>"+b+"_c_pt_eta", cJetSel, 'normgoff' )
        chain.Draw("Jet_pt>>"+b+"_c_pt", cJetSel, 'normgoff' )
        chain.Draw("Jet_eta>>"+b+"_c_eta", cJetSel, 'normgoff' )
        chain.Draw("Jet_"+b+">>"+b+"_c_Bin0__rec", cJetSel+TCut('abs(Jet_eta[Iteration$])<=1.'), 'normgoff' )
        chain.Draw("Jet_"+b+">>"+b+"_c_Bin1__rec", cJetSel+TCut('abs(Jet_eta[Iteration$])>1.'), 'normgoff' )

        #### For b jets
        bJetSel = presel + TCut('Jet_hadronFlavour[Iteration$]==5')
        chain.Draw("Jet_"+b+":abs(Jet_eta):Jet_pt>>"+b+"_b_pt_eta", bJetSel, 'normgoff' )
        chain.Draw("Jet_pt>>"+b+"_b_pt", bJetSel, 'normgoff' )
        chain.Draw("Jet_eta>>"+b+"_b_eta", bJetSel, 'normgoff' )
        chain.Draw("Jet_"+b+">>"+b+"_b_Bin0__rec", bJetSel+TCut('abs(Jet_eta[Iteration$])<=1.'), 'normgoff' )
        chain.Draw("Jet_"+b+">>"+b+"_b_Bin1__rec", bJetSel+TCut('abs(Jet_eta[Iteration$])>1.'), 'normgoff' )

    output.Write()
    print 'Writing output file: '+ outputFileName
    output.Close()


#################################################################################
if __name__ == '__main__':

    usage = 'usage: %prog [options]'

    parser = argparse.ArgumentParser()
    parser.add_argument( '-s', '--singleFile', action='store_true', dest='singleFile', default=False, help='Run one file at the time (true) or the whole dataset (false)' )
    parser.add_argument( '-i', '--inputFile', action='store', dest='inputFile', default='/store/user/algomez/ttH/nanoPostMEAnalysis/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_tthbb13_PostProcMEAnalysis_withME_102X_v02p1/190426_153044/0000/tree_115.root', help='Input file if singleFile=True' )
    parser.add_argument( '-d', '--dataset', action='store', dest='dataset', default='ttHTobb', help='Type of sample' )
    parser.add_argument( '-o', '--output', action='store', dest='output', default='3DPlots', help='Name of output file (wo root extension)' )
    parser.add_argument( '-v', '--version', action='store', default='2017', dest='version', help='Version of the analysis' )

    try: args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    ##### Samples
    allSamples = {}
    allSamples['TTToSemiLeptonic_2016'] = ['/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16NanoAODv4-PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6-v1/NANOAODSIM', dbsglobal ]
    allSamples['TTToSemiLeptonic_2017'] = ['/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv4-PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/NANOAODSIM', dbsglobal ]
    allSamples['TTToSemiLeptonic_2018'] = ['/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAOD-102X_upgrade2018_realistic_v15-v1/NANOAODSIM', dbsglobal ]

    ##### Selection
    presel = TCut('(Jet_pt[Iteration$]>20) && (abs(Jet_eta[Iteration$])<2.4) && (Jet_jetId[Iteration$]>0)')

    for isam in allSamples:
        if args.version in isam:
            fileDictList = allSamples[isam][1].listFiles( dataset=allSamples[isam][0], validFileOnly=1 )
            file_names= [ 'root://cms-xrd-global.cern.ch/'+dic['logical_file_name'] for dic in fileDictList ]
            #file_names= [ 'nano102x_on_mini102x_2018_mc_NANO_573.root' ]
            pdfs( file_names[:5], presel)

