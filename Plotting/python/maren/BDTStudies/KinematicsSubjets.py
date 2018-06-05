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
#fn = os.environ['FILE_NAMES'].split(' ')
#for v in fn:
#    full_file_names[v] = v

full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/May24_NoME/180524_215806/0000/tree_41.root"
full_file_names["TTH2"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/May24_NoME/180524_215806/0000/tree_32.root"
#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_45.root"

########################################
# Create histograms, saved in file
########################################

cats = ["dl","sl"]
criteria = ["hb","tb","tl"]
jets = ["subjet","jet","object"]
variables = ["pt","eta","phi","mass","btag"]
limits = [100,2,2,100,2]


count = {}


for i in cats:
    count[i] = {}
    for j in criteria:
        count[i][j] = {}
        for k in jets:
            count[i][j][k] = {}
            for l in variables:
                m = variables.index(l)
                count[i][j][k][l] = ROOT.TH1F("count_{}_{}_{}_{}".format(i,j,k,l),"count_{}_{}_{}_{}".format(i,j,k,l),100,-limits[m],limits[m])
 

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

        if counter > 20000:
            break

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.event

        event.Electron = nanoTreeClasses.Electron.make_array(ttree, MC = True)
        event.Muon = nanoTreeClasses.Muon.make_array(ttree, MC = True)
        event.GenParticle = nanoTreeGenClasses.GenParticle.make_array(ttree)
        event.GenBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(event.GenParticle)
        event.GenWZQuark = nanoTreeGenClasses.GenWZQuark.make_array(event.GenParticle)
        event.GenBQuarkFromTop = nanoTreeGenClasses.GenBQuarkFromTop.make_array(event.GenParticle)
        event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
        event.GenTop = nanoTreeGenClasses.GenTop.make_array(event.GenParticle)
        event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)
        event.FatjetCA15SoftDrop = JetCollection.make_array(ttree,"FatjetCA15SoftDrop")
        event.FatjetCA15 = JetCollection.make_array(ttree,"FatjetCA15")
        event.FatjetCA15SoftDropSubjets = JetCollection.make_array(ttree,"FatjetCA15SoftDropSubjets")
        event.HTTV2Subjets = JetCollection.make_array(ttree,"HTTV2Subjets")
        event.HTTV2 = JetCollection.make_array(ttree,"HTTV2")
        event.HTTV2 = MatchFatjets(event.HTTV2,event.FatjetCA15SoftDrop)
        event.Jet = nanoTreeClasses.Jet.make_array(ttree, MC = True)

        for part in event.GenWZQuark + event.GenBQuarkFromH + event.GenBQuarkFromTop:
            setattr(part,"btag",0)

        for je in event.Jet:
            setattr(je,"btag",je.btagDeepCSV)

        matched_jets = Match_two_lists(
            event.Jet, 'AK4',
            event.GenWZQuark + event.GenBQuarkFromH + event.GenBQuarkFromTop, 'genQuark',0.3) 


        GetCategory(event,python_conf)

        SelectJets(event,python_conf)

        event.Jet = event.good_jets

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
            #event.HTTV2 = filter(lambda x: (x.mass>100 and x.mass < 250 and x.frec < 0.4), event.HTTV2)

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
            if i.matched == 1:
                subjets = [event.FatjetCA15SoftDropSubjets[i.matched_CA15SD.subJetIdx1],event.FatjetCA15SoftDropSubjets[i.matched_CA15SD.subJetIdx2]]
                matched_gen = Match_two_lists(
                subjets, 'subjetsHiggs',
                event.GenBQuarkFromH, 'genQuark',0.3) 
                for subjet in subjets:
                    if hasattr(subjet,"matched_genQuark"):
                        for var in variables:
                            count[cat]["hb"]["subjet"][var].Fill(getattr(subjet,var) - getattr(subjet.matched_genQuark,var))

        for i in event.HTTV2:
            if i.matched == 1:
                count[cat]["tb"]["object"]["pt"].Fill(i.pt - event.GenHadTop[0].pt)
                subjets = [event.HTTV2Subjets[i.subJetIdx1],event.HTTV2Subjets[i.subJetIdx2],event.HTTV2Subjets[i.subJetIdx3]]
                sorted(subjets, key=lambda x: x.btag, reverse=True)
                matched_genb = Match_two_lists(
                [subjets[0]], 'subjetsTop',
                event.GenBQuarkFromTop, 'genQuark',0.3) 
                matched_genl = Match_two_lists(
                [subjets[1]] + [subjets[2]], 'subjetsTop',
                event.GenWZQuark, 'genQuark',0.3)                
                for subjet in subjets:
                    if subjet.pt > 30:
                        index = subjets.index(subjet)
                        if hasattr(subjet,"matched_genQuark"):
                            print Get_DeltaR_two_objects(subjet,subjet.matched_genQuark), subjet.pt ,subjet.matched_genQuark.pt
                            print subjets[0].pt, subjets[1].pt, subjets[2].pt
                            for pa in event.GenWZQuark:
                                print pa.pt, "WZ"
                            for pa in event.GenBQuarkFromTop:
                                print pa.pt, "B"
                            for var in variables:
                                if index == 0:
                                    count[cat]["tb"]["subjet"][var].Fill(getattr(subjet,var) - getattr(subjet.matched_genQuark,var))
                                else:
                                    count[cat]["tl"]["subjet"][var].Fill(getattr(subjet,var) - getattr(subjet.matched_genQuark,var))

        for part in event.GenWZQuark:
            if hasattr(part,"matched_AK4") and (hasattr(part,"matched_subjetsHiggs") or hasattr(part,"matched_subjetsTop")):
                for var in variables:
                    count[cat]["tl"]["jet"][var].Fill(getattr(part.matched_AK4,var) - getattr(part,var))
        for part in event.GenBQuarkFromH:
            if hasattr(part,"matched_AK4") and (hasattr(part,"matched_subjetsHiggs") or hasattr(part,"matched_subjetsTop")):
                for var in variables:
                    count[cat]["hb"]["jet"][var].Fill(getattr(part.matched_AK4,var) - getattr(part,var))
        for part in event.GenBQuarkFromTop:
            if hasattr(part,"matched_AK4") and (hasattr(part,"matched_subjetsHiggs") or hasattr(part,"matched_subjetsTop")):
                for var in variables:
                    count[cat]["tb"]["jet"][var].Fill(getattr(part.matched_AK4,var) - getattr(part,var))


results = ROOT.TFile("KinematicsSubjets.root","recreate")
for i in cats:
    for j in criteria:
        for k in jets:
            for l in variables:
                count[i][j][k][l].Write()
 