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

#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_42.root"
#full_file_names["TTH2"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/June07_withME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/June07_withME/180607_164153/0000/tree_43.root"
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
criteria = ["hb"]
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

        #if counter > 20000:
        #    break

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.event

        event.Electron = nanoTreeClasses.Electron.make_array(ttree, MC = True)
        event.Muon = nanoTreeClasses.Muon.make_array(ttree, MC = True)
        event.GenParticle = nanoTreeGenClasses.GenParticle.make_array(ttree)
        event.GenBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(event.GenParticle)
        event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
        event.FatjetAK8 = nanoTreeClasses.FatjetAK8.make_array(ttree)
        event.SubjetAK8 = nanoTreeClasses.SubjetAK8.make_array(ttree)
        event.Jet = nanoTreeClasses.Jet.make_array(ttree, MC = True)

        for part in event.GenBQuarkFromH:
            setattr(part,"btag",0)

        for je in event.Jet:
            setattr(je,"btag",je.btagDeepCSV)

        matched_jets = Match_two_lists(
            event.Jet, 'AK4',
            event.GenBQuarkFromH, 'genQuark',0.3) 


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
        event.FatjetAK8 = filter(lambda x: (x.pt > 300 and abs(x.eta) < 2.4), event.FatjetAK8)
        event.GenHiggsBoson = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.GenHiggsBoson)

        for i in event.FatjetAK8:

            subjets = [event.SubjetAK8[i.subJetIdx1].btag,event.SubjetAK8[i.subJetIdx2].btag]
            subjets = sorted(subjets)
            setattr(i,"btagmax",subjets[1])
            setattr(i,"btagmin",subjets[0])
            matched = 0
            for genhiggs in event.GenHiggsBoson:
                if Get_DeltaR_two_objects(i,genhiggs) < 0.6:
                    matched = 1
            setattr(i,"matched",matched)
            setattr(i,"tau21",i.tau2/i.tau1)

        event.FatjetAK8 = filter(lambda x: (x.msoftdrop>50.0), event.FatjetAK8)


        for i in event.FatjetAK8:
            if i.matched == 1:
                subjets = [event.SubjetAK8[i.subJetIdx1],event.SubjetAK8[i.subJetIdx2]]
                matched_gen = Match_two_lists(
                subjets, 'subjetsHiggs',
                event.GenBQuarkFromH, 'genQuark',0.3) 
                for subjet in subjets:
                    if hasattr(subjet,"matched_genQuark"):
                        for var in variables:
                            count[cat]["hb"]["subjet"][var].Fill(getattr(subjet,var) - getattr(subjet.matched_genQuark,var))

        for part in event.GenBQuarkFromH:
            if hasattr(part,"matched_AK4") and (hasattr(part,"matched_subjetsHiggs") or hasattr(part,"matched_subjetsTop")):
                for var in variables:
                    count[cat]["hb"]["jet"][var].Fill(getattr(part.matched_AK4,var) - getattr(part,var))


results = ROOT.TFile("out.root","recreate")
for i in cats:
    for j in criteria:
        for k in jets:
            for l in variables:
                count[i][j][k][l].Write()
 