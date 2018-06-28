#!/usr/bin/env python

########################################
# Imports
########################################

import math
import os
import pickle
import socket # to get the hostname

import ROOT

########################################
# Define Input Files and
# output directory
########################################


# for the filename: basepath + filename + .root
full_file_names = {}
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v



#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_127.root"
#full_file_names["TT"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_45.root"

########################################
# Create histograms, saved in file
########################################


Cat = ROOT.TH2F("Cat","Cat",3,0,3,3,0,3)


######################################
# Run code
########################################

for l in full_file_names:
    f = ROOT.TFile.Open(full_file_names[l], "READ")
    ttree = f.Get("tree")

    print full_file_names[l]


    counter  = 0 

    for event in ttree:
        counter += 1

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.evt

        catgen = event.cat_gen
        catrec = -1
        if event.is_sl:
            catrec = 0
        elif event.is_dl:
            catrec = 1
        elif event.is_fh:
            catrec = 2

        Cat.Fill(catgen,catrec,event.genWeight)


results = ROOT.TFile("out.root","recreate")
Cat.Write()