#!/usr/bin/env python

########################################
# Imports
########################################

import math
import os
import pickle
import socket # to get the hostname

import ROOT

from TTH.Plotting.maren.BDTStudies.BasicBoostedFunctions import *

from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf
import TTH.MEAnalysis.nanoTreeClasses as nanoTreeClasses
import TTH.MEAnalysis.nanoTreeGenClasses as nanoTreeGenClasses

import sklearn
from sklearn.ensemble import GradientBoostingClassifier

import pandas
import root_numpy
import numpy as np

print "Imported numpy"

########################################
# Define Input Files and
# output directory
########################################


# for the filename: basepath + filename + .root
full_file_names = {} 
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v
#SKIP_EVENTS = int(os.environ["SKIP_EVENTS"]) 
#MAX_EVENTS = int(os.environ["MAX_EVENTS"]) 

#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/May24_NoME/180524_215806/0000/tree_32.root"
#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_45.root"

########################################
# Create histograms, saved in file
########################################

cats = ["dl","sl"]
criteria = ["S","Stot","effH","effT","effHT"]
possibilities = ["H","T","HT"]


count = {}


for i in cats:
    count[i]= {}
    for j in criteria:
        count[i][j]= {}
        for k in possibilities:
            count[i][j][k] = ROOT.TH2F("count_{}_{}_{}".format(i,j,k),"count_{}_{}_{}".format(i,j,k),100,0,1,100,0,1)
 

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

    #Now load BDT pickle files
    #Higgs
    f1 = open("BDT_Higgs.pickle", "r")
    higgsBDT = pickle.load(f1)
    #Top
    f2 = open("BDT_Top.pickle", "r")
    topBDT = pickle.load(f2)

    #Here matched means Delta R < 0.8 to generated particle or jet or whatever...

    for event in ttree :
        counter += 1

        #if counter > 5000:
        #    break


        if counter%1000 == 0 :
            print "Processing event: ", counter, event.event


        event.Electron = nanoTreeClasses.Electron.make_array(ttree, MC = True)
        event.Muon = nanoTreeClasses.Muon.make_array(ttree, MC = True)
        event.GenParticle = nanoTreeGenClasses.GenParticle.make_array(ttree)
        event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
        event.GenTop = nanoTreeGenClasses.GenTop.make_array(event.GenParticle)
        event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)
        #event.GenLepTop = filter(lambda x: (x.decayMode==0), event.GenTop)
        event.FatjetCA15SoftDrop = JetCollection.make_array(ttree,"FatjetCA15SoftDrop")
        event.FatjetCA15 = JetCollection.make_array(ttree,"FatjetCA15")
        event.FatjetCA15SoftDropSubjets = JetCollection.make_array(ttree,"FatjetCA15SoftDropSubjets")
        event.HTTV2Subjets = JetCollection.make_array(ttree,"HTTV2Subjets")
        event.HTTV2 = JetCollection.make_array(ttree,"HTTV2")
        event.HTTV2 = MatchFatjets(event.HTTV2,event.FatjetCA15SoftDrop)



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
        event.HTTV2 = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.HTTV2)
        event.GenHadTop = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.GenHadTop)
        event.GenHiggsBoson = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.GenHiggsBoson)
        if cat == "sl":
            for i in event.HTTV2:
                setattr(i,"drl",Get_DeltaR_two_objects(i,event.lep_SL[0]))
                subjets = [event.HTTV2Subjets[i.subJetIdx1].btag,event.HTTV2Subjets[i.subJetIdx2].btag,event.HTTV2Subjets[i.subJetIdx3].btag]
                subjets = sorted(subjets)
                setattr(i,"btagmax",subjets[2])
                setattr(i,"btagsecond",subjets[1])
                matched = 0
                for gentop in event.GenHadTop:
                    if Get_DeltaR_two_objects(i,gentop) < 0.6:
                        matched = 1
                setattr(i,"matched",matched)
            event.HTTV2 = filter(lambda x: (x.drl>1.0 and x.btagmax > 0.1522), event.HTTV2)
            for i in event.HTTV2:
                d = [(i.mass,i.tau32,i.frec)]
                df = pandas.DataFrame(d)               
                a = topBDT.predict_proba(d)
                setattr(i,"bdt",a[0][1])
            event.HTTV2 = sorted(event.HTTV2, key = lambda x: x.bdt, reverse = True)
        elif cat == "dl":
            event.HTTV2 = []

        matched_objectsCA15 = Match_two_lists(
            event.FatjetCA15, 'CA15',
            event.FatjetCA15SoftDrop, 'CA15SD',1.0)

        for i in event.FatjetCA15:

            if hasattr(i,"matched_CA15SD"):
                setattr(i,"softdropmass",i.matched_CA15SD.mass)
                subjets = [event.FatjetCA15SoftDropSubjets[i.matched_CA15SD.subJetIdx1].btag,event.FatjetCA15SoftDropSubjets[i.matched_CA15SD.subJetIdx2].btag]
                subjets = sorted(subjets)
                setattr(i,"btagmax",subjets[1])
                setattr(i,"btagmin",subjets[0])
                matched = 0
                for genhiggs in event.GenHiggsBoson:
                    if Get_DeltaR_two_objects(i,genhiggs) < 0.6:
                        matched = 1
                setattr(i,"matched",matched)
                setattr(i,"tau21SD",i.matched_CA15SD.tau21)
        event.FatjetCA15 = filter(lambda x: (hasattr(x,"matched_CA15SD") and x.softdropmass>50.0), event.FatjetCA15)
        for i in event.FatjetCA15:
            #"mass", "nsub", "bbtag", "btagf", "btags"
            d = [(i.tau21SD,i.bbtag,i.btagmin)]
            df = pandas.DataFrame(d)               
            a = higgsBDT.predict_proba(d)
            setattr(i,"bdt",a[0][1])

        event.FatjetCA15 = sorted(event.FatjetCA15, key = lambda x: x.bdt, reverse = True)

        pos = None
        matchH = -1
        matchT  = -1
        bdtTop = -1
        bdtHiggs = -1
        if len(event.HTTV2): 
            bdtTop = event.HTTV2[0].bdt
            if event.HTTV2[0].matched == 1:
                matchT = 1
            else:
                matchT = 0
        else:
            bdtTop = 0
            matchT = 0
        if len(event.FatjetCA15):
            bdtHiggs = event.FatjetCA15[0].bdt
            if event.FatjetCA15[0].matched == 1:
                matchH = 1
            else:
                matchH = 0
        else:
            bdtHiggs = 0
            matchH = 0

        if len(event.HTTV2) and len(event.FatjetCA15):
            pos = "HT"
        elif len(event.HTTV2) and not len(event.FatjetCA15):
            pos = "T"
        elif len(event.FatjetCA15) and not len(event.HTTV2):
            pos = "H"


        """for a in range(0,101):
            a2 = float(a)/100
            for b in range(0,101):
                b2 = float(b)/100
                count[cat]["Stot"]["HT"].Fill(a2,b2,event.Generator_weight)
                if pos == None:
                    continue
                if bdtTop >= a2 and bdtHiggs >= b2:
                    count[cat]["S"][pos].Fill(a2,b2,event.Generator_weight)
                    if matchT == 1 and matchH == 0:
                        count[cat]["effT"][pos].Fill(a2,b2,event.Generator_weight)
                    if matchH == 1 and matchT == 0:
                        count[cat]["effH"][pos].Fill(a2,b2,event.Generator_weight)
                    if matchT == 1 and matchH  == 1:
                        count[cat]["effHT"][pos].Fill(a2,b2,event.Generator_weight)"""


        for a in range(0,101):
            a2 = float(a)/100
            for b in range(0,101):
                b2 = float(b)/100
                count[cat]["Stot"]["HT"].Fill(a2+0.001,b2+0.001,event.Generator_weight)
                if pos == None:
                    continue
                if bdtTop >= a2 and bdtHiggs >= b2:
                    count[cat]["S"][pos].Fill(a2+0.001,b2+0.001,event.Generator_weight)
                    if matchT == 1 and matchH == 0:
                        count[cat]["effT"][pos].Fill(a2+0.001,b2+0.001,event.Generator_weight)
                    if matchH == 1 and matchT == 0:
                        count[cat]["effH"][pos].Fill(a2+0.001,b2+0.001,event.Generator_weight)
                    if matchT == 1 and matchH  == 1:
                        count[cat]["effHT"][pos].Fill(a2+0.001,b2+0.001,event.Generator_weight)







results = ROOT.TFile("out.root","recreate")
for i in cats:
    for j in criteria:
        for k in possibilities:
            count[i][j][k].Write()
