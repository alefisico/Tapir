#!/usr/bin/env python

########################################
# Imports
########################################

import math
import os
import pickle
import socket # to get the hostname

import ROOT

from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf
import TTH.MEAnalysis.nanoTreeClasses as nanoTreeClasses
import TTH.MEAnalysis.nanoTreeGenClasses as nanoTreeGenClasses
from TTH.Plotting.maren.BDTStudies.BasicBoostedFunctions import *



########################################
# Define Input Files and
# output directory
########################################


# for the filename: basepath + filename + .root
full_file_names = {} 
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v

#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/May24_NoME/180524_215806/0000/tree_32.root"
#full_file_names["TTH2"] = "root://t3dcachedb.psi.ch//pnfspsi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_43.root"
#full_file_names["TTH3"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_44.root"
#full_file_names["TTH4"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_45.root"
#full_file_names["TTH5"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_46.root"
#full_file_names["TTH6"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_47.root"
#full_file_names["TTH7"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_48.root"
#full_file_names["TTH8"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_49.root"
#full_file_names["TTH9"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_50.root"
#full_file_names["TTH10"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_51.root"
#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_45.root"

########################################
# Create histograms, saved in file
########################################

cats = ["dl","sl"]
jet = ["CA15","AK8"]


count = {}


for i in cats:
    count[i] = {}
    for j in jet: 
        count[i][j] = ROOT.TH1F("count_{}_{}".format(i,j),"count_{}_{}".format(i,j),10,0,10)
   
########################################
# Run code
########################################

for l in full_file_names:
    f = ROOT.TFile.Open(full_file_names[l], "READ")
    ttree = f.Get("nanoAOD/Events")

    print full_file_names[l]

    sample = ""
    if "ttH" in full_file_names[l]:
        sample = "ttH"
    elif "TT" in full_file_names[l]:
        sample = "ttjets"


    counter = 0

    for event in ttree :
        counter += 1

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.event

        event.Electron = nanoTreeClasses.Electron.make_array(ttree, MC = True)
        event.Muon = nanoTreeClasses.Muon.make_array(ttree, MC = True)
        event.GenParticle = nanoTreeGenClasses.GenParticle.make_array(ttree)
        event.GenBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(event.GenParticle)
        event.GenWZQuark = nanoTreeGenClasses.GenWZQuark.make_array(event.GenParticle)
        event.GenBQuarkFromTop = nanoTreeGenClasses.GenBQuarkFromTop.make_array(event.GenParticle)
        event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
        event.FatjetCA15SoftDrop = JetCollection.make_array(ttree,"FatjetCA15SoftDrop")
        event.FatjetCA15 = JetCollection.make_array(ttree,"FatjetCA15")
        event.FatjetAK8 = nanoTreeClasses.FatjetAK8.make_array(ttree)
        event.GenISRGluon = nanoTreeGenClasses.GenISRGluon.make_array(event.GenParticle)


        GetCategory(event,python_conf)

        #Get event category
        cat = None
        if event.is_sl:
            cat = "sl"
        elif event.is_dl:
            cat = "dl"
        else:
            continue

        #First apply all general cuts on objects
        event.FatjetCA15SoftDrop = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4 and x.mass>50), event.FatjetCA15SoftDrop)
        event.FatjetCA15 = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.FatjetCA15)
        event.FatjetAK8 = filter(lambda x: (x.pt > 300 and abs(x.eta) < 2.4), event.FatjetAK8)
        event.GenHiggsBoson = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.GenHiggsBoson)

        matched_objectsCA15 = Match_two_lists(
            event.FatjetCA15, 'CA15',
            event.FatjetCA15SoftDrop, 'CA15SD',1.0)

        for i in event.FatjetCA15:

            if hasattr(i,"matched_CA15SD"):
                setattr(i,"softdropmass",i.matched_CA15SD.mass)
                matched = 0
                for genhiggs in event.GenHiggsBoson:
                    if Get_DeltaR_two_objects(i,genhiggs) < 0.6:
                        matched = 1
                setattr(i,"matched",matched)
        event.FatjetCA15 = filter(lambda x: (hasattr(x,"matched_CA15SD") and x.softdropmass>50.0), event.FatjetCA15)

        for i in event.FatjetCA15:
            if i.matched == 1:
                count[cat]["CA15"].Fill(1,event.genWeight)
                for j in event.GenBQuarkFromTop:
                    if Get_DeltaR_two_objects(i,j) < 1.5:
                        count[cat]["CA15"].Fill(2,event.genWeight)
                for j in event.GenWZQuark:
                    if Get_DeltaR_two_objects(i,j) < 1.5:
                        count[cat]["CA15"].Fill(3,event.genWeight)
                for j in event.GenISRGluon:
                    if Get_DeltaR_two_objects(i,j) < 1.5:
                        count[cat]["CA15"].Fill(4,event.genWeight)


        for i in event.FatjetAK8:
            matched = 0
            for genhiggs in event.GenHiggsBoson:
                if Get_DeltaR_two_objects(i,genhiggs) < 0.6:
                    matched = 1
            setattr(i,"matched",matched)
        event.FatjetAK8 = filter(lambda x: (x.msoftdrop>50.0), event.FatjetAK8)

        for i in event.FatjetAK8:
            if i.matched == 1:
                count[cat]["AK8"].Fill(1,event.genWeight)
                for j in event.GenBQuarkFromTop:
                    if Get_DeltaR_two_objects(i,j) < 0.8:
                        count[cat]["AK8"].Fill(2,event.genWeight)
                for j in event.GenWZQuark:
                    if Get_DeltaR_two_objects(i,j) < 0.8:
                        count[cat]["AK8"].Fill(3,event.genWeight)
                for j in event.GenISRGluon:
                    if Get_DeltaR_two_objects(i,j) < 0.8:
                        count[cat]["AK8"].Fill(4,event.genWeight)
       

results = ROOT.TFile("out.root","recreate")
for i in cats:
    for j in jet:
        count[i][j].Write()
 