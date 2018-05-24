#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import math
import os
import pickle
import socket # to get the hostname

import ROOT

def Get_DeltaR_two_objects(obj1_eta, obj1_phi, obj2_eta, obj2_phi ):

        #for obj in [ obj1, obj2 ]:
        #    if not ( hasattr( obj, 'phi' ) or hasattr( obj, 'eta' ) ):
        #        print "Can't calculate Delta R: objects don't have right attributes"
        #        return 0

        pi = math.pi

        del_phi = abs( obj1_phi - obj2_phi )
        if del_phi > pi: del_phi = 2*pi - del_phi

        delR = pow( pow(obj1_eta-obj2_eta,2) + pow(del_phi,2) , 0.5 )

        return delR

########################################
# Define Input Files and
# output directory
########################################

basepath = 'root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat'

# for the filename: basepath + filename + .root
full_file_names = {}
#for k,v in files.iteritems():
#fn = os.environ['FILE_NAMES'].split(' ')
#for v in fn:
#    full_file_names[v] = basepath + v

#full_file_names = {}
full_file_names["VHbb"] = "/mnt/t3nfs01/data01/shome/mameinha/TTH/CMSSW/src/TTH/MEAnalysis/python/Loop_ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8_16/tree.root"
full_file_names["Nano"] = "/mnt/t3nfs01/data01/shome/mameinha/TTH/SwitchNanoAOD/CMSSW/src/TTH/MEAnalysis/python/Loop_ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/tree.root"

#full_file_names["VHbb"] = "~/tth/data/testvhbb.root"
#full_file_names["Nano"] = "~/tth/gc/meanalysis/GC6cf57cffdec2/default/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/job_1_out.root"
#full_file_names = {}
#full_file_names["v"] = "root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/store/user/mameinha/tth/Apr09_v1/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/Apr09_v1/170409_111531/0000/tree_100.root"


########################################
# Create histograms, saved in file
########################################
samples = ["VHbb","Nano"]
genobjects = ["GenBHiggs","GenBTop","GenQW","genHiggs","genTopHad","genTopLep"]
otherstuff = ["nMatch_hb","nMatch_hb_btag","nMatch_tb","nMatch_tb_btag","nMatch_wq","nMatch_wq_btag","jets_matchBfromHadT"]

Cat = {}
GenObject = {}
OtherStuff = {}

ids = []

for i in samples:

    Cat[i] = ROOT.TH1F("Cat_{}".format(i),"Cat_{}".format(i),3,0,3)

    GenObject[i] = {}
    OtherStuff[i] = {}
    for j in genobjects:
        GenObject[i][j] = ROOT.TH1F("{}_{}".format(j,i),"{}_{}".format(j,i),10,0,10)
    for j in otherstuff:
        OtherStuff[i][j] = ROOT.TH1F("{}_{}".format(j,i),"{}_{}".format(j,i),10,0,10)


for l in full_file_names:
    f = ROOT.TFile.Open(full_file_names[l], "READ")
    ttree = f.Get("tree")


    if l == "VHbb":
        sample = "VHbb"
    elif l == "Nano":
        sample = "Nano"

    counter = 0


    for event in ttree :

        if counter%1000 == 0 :
            print counter
        counter += 1

        #if event.cat_gen < 0:
        #    continue

        if sample == "VHbb":
            ids.append(event.evt)
        elif sample == "Nano":
            if not event.evt in ids:
                continue

        Cat[sample].Fill(event.cat_gen)
        try:
            for i in genobjects:
                GenObject[sample][i].Fill(getattr(event,"n{}".format(i)))
            for i in otherstuff:    
                OtherStuff[sample][i].Fill(getattr(event,"{}".format(i)))
        except:
            pass


results = ROOT.TFile("GenSanityCheck.root","recreate")
for i in samples:
    Cat[i].Write()
    for j in genobjects:
        GenObject[i][j].Write()
    for j in otherstuff:
        OtherStuff[i][j].Write()
