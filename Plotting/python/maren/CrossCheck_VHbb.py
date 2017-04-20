#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import pickle
import socket # to get the hostname
import math
import numpy as np

from ROOT import *

if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.CompareDistributionsHelpers import *
else:
    from TTH.Plotting.python.Helpers.CompareDistributionsHelpers import *


########################################
# Define Input Files and
# output directory
########################################

if socket.gethostname() == "t3ui02":
    basepath = 'root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat'
else:
    basepath = 'root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat'
                                         
# for the filename: basepath + filename + .root
full_file_names = {}
#for k,v in files.iteritems():
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = basepath + v

#full_file_names = {}
#full_file_names["v"] = "./testdata.root"


########################################
# Create histograms, saved in file
########################################

Histonames = ["nJet","Jet_pt","Jet_btagCSV","Jet_eta"]

limit = [0,0,0,-3]
limitsup = [12,600,2,3]
nbin = [12,50,50,50]

Histograms  = {}

for i in Histonames:
    m = Histonames.index(i)
    Histograms[i] = ROOT.TH1F("{cat}".format(cat = i),"{cat}".format(cat = i),nbin[m],limit[m],limitsup[m])

 

########################################
# Start program
########################################

filename = {}
#filename["v"] = 'root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/store/user/mameinha/tth/Apr12_v1/SingleMuon/Apr12_v1/170412_122435/0000/tree_10.root'
filename["v"] = "root://cms-xrd-global.cern.ch//store/user/mameinha/tth/Apr09_v1/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/Apr09_v1/170409_111531/0000/tree_1.root"
for l in full_file_names:
    f = ROOT.TFile.Open(full_file_names[l], "READ")
    print f
    ttree = f.Get("vhbb/tree")


    for event in ttree :

        for l in Histonames:

            #Event selection
            if event.json!=1:
                continue

            if (event.HLT_BIT_HLT_IsoMu24_v!=1 and event.HLT_BIT_HLT_IsoTkMu24_v!=1):
                continue


            #Lepton selection
            if event.nselLeptons!=1:
                continue
            if abs(event.selLeptons_pdgId[0])!=13:
                continue
            if event.selLeptons_pt[0]<24:
                continue


            #Calculate number of jets
            nbjets = 0

            for k in range (0,event.nJet):
                if event.Jet_pt[k]>30 and abs(event.Jet_eta[k])<2.4:
                    nbjets+=1


            if l == "nJet":
                Histograms[l].Fill(nbjets)
            else: 
                #Plot some jet variables
                for p in range(0,event.nJet):
                    if event.Jet_pt[p]>30 and abs(event.Jet_eta[p])<2.4:
                        Histograms["Jet_pt"].Fill(getattr(event,"Jet_pt")[p])
                        Histograms["Jet_btagCSV"].Fill(getattr(event,"Jet_btagCSV")[p])
                        Histograms["Jet_eta"].Fill(getattr(event,"Jet_eta")[p])

    
       

results = TFile("CrossCheck_VHbb.root","recreate")
for i in Histonames:
    Histograms[i].Write()

