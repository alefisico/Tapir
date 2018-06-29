#OK, Assume that I have found the target efficiency I want to find for my Higgs and top tagger. 
#Scan variables to find point with the efficiency I want and choose the one which also has the highest 
#background rejection rate.

#imports
########################################

import os
import pickle
import socket # to get the hostname
import math
import ROOT
from array import array


import TTH.MEAnalysis.nanoTreeClasses as nanoTreeClasses
import TTH.MEAnalysis.nanoTreeGenClasses as nanoTreeGenClasses
from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf as python_conf

from TTH.Plotting.maren.BDTStudies.BasicBoostedFunctions import *

########################################
# Define Input Files and
# output directory
########################################
                                         
# for the filename: basepath + filename + .root
full_file_names = {}
#for k,v in files.iteritems():
fn = os.environ['FILE_NAMES'].split(' ')
for v in fn:
    full_file_names[v] = v

#full_file_names = {}
#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/May24_NoME/180524_215806/0000/tree_32.root"
#full_file_names["TTH"] = "root://t3dcachedb.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mameinha/tth/May24_NoME/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/May24_NoME/180524_220009/0000/tree_46.root"

"""class Cuts:
    toptagger = {
    "massinf" : 160,
    "masssup" : 280,
    "nsub" : 0.8,
    "frec" : 0.3
    }
    higgstagger = {
    "nsub" : 0.7,
    "bbtag" : 0.4,
    "btagsl" : 0.7
    }"""

#These are the default cuts...
class Cuts:
    toptagger = {
    "massinf" : 85,
    "masssup" : 280,
    "nsub" : 0.97,
    "frec" : 0.47
    }
    higgstagger = {
    "nsub" : 0.7,
    "bbtag" : 0.4,
    "btagsl" : 0.7
    }


cats = ["sl","dl"]
cases = ["H","T","HT"]

results = {}

for i in cats:
    results[i] = {}
    for j in cases:
        results[i][j] = ROOT.TH1F("numbers_{}_{}".format(i,j),"numbers_{}_{}".format(i,j),20,0,20)


for l in full_file_names:
    print full_file_names[l] 
    if "ttH" in full_file_names[l]:
        sample = "ttH"
    elif "TT" in full_file_names[l]:
        sample = "ttjets"


    f = ROOT.TFile.Open(full_file_names[l], "READ")
    ttree = f.Get("nanoAOD/Events") 


    topcuts = Cuts.toptagger
    higgscuts = Cuts.higgstagger

    
    counter  = 0
    for event in ttree :

        #if counter > 20000:
        #    break

        #if counter < 6495:
        #    continue

        if counter%1000 == 0 :
            print "Processing event: ", counter, event.event

        counter += 1
        
        event.Electron = nanoTreeClasses.Electron.make_array(ttree, MC = True)
        event.Muon = nanoTreeClasses.Muon.make_array(ttree, MC = True)
        event.GenParticle = nanoTreeGenClasses.GenParticle.make_array(ttree)
        event.GenHiggsBoson = nanoTreeGenClasses.GenHiggsBoson.make_array(event.GenParticle)
        event.GenTop = nanoTreeGenClasses.GenTop.make_array(event.GenParticle)  
        event.GenHadTop = filter(lambda x: (x.decayMode==1), event.GenTop)
        event.GenBQuarkFromH = nanoTreeGenClasses.GenBQuarkFromHiggs.make_array(event.GenParticle)
        event.GenBQuarkFromTop = nanoTreeGenClasses.GenBQuarkFromTop.make_array(event.GenParticle)
        event.FatjetCA15SoftDrop = JetCollection.make_array(ttree,"FatjetCA15SoftDrop")
        event.FatjetCA15 = JetCollection.make_array(ttree,"FatjetCA15")
        event.FatjetCA15SoftDropSubjets = JetCollection.make_array(ttree,"FatjetCA15SoftDropSubjets")
        event.FatjetAK8 = JetCollection.make_array(ttree,"FatJet")
        event.FatjetAK8Subjets = JetCollection.make_array(ttree,"SubJet")
        event.HTTV2 = JetCollection.make_array(ttree,"HTTV2")
        event.HTTV2Subjets = JetCollection.make_array(ttree,"HTTV2Subjets")
        
        
        GetCategory(event,python_conf)

        #Get event category
        cat = None
        if event.is_sl:
            cat = "sl"
        elif event.is_dl:
            cat = "dl"
        else:
            continue


        ########################################
        #First apply all general cuts on objects
        ########################################



        event.FatjetCA15SoftDrop = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4 and x.mass>50), event.FatjetCA15SoftDrop)
        event.FatjetCA15 = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.FatjetCA15)
        event.HTTV2 = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.HTTV2)
        event.GenHadTop = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.GenHadTop)
        event.GenHiggsBoson = filter(lambda x: (x.pt > 200 and abs(x.eta) < 2.4), event.GenHiggsBoson)

        matched_fatjet = Match_two_lists(
            event.FatjetCA15SoftDrop, 'CA15SD',
            event.FatjetCA15, 'CA15',0.5)

        event.FatjetCA15 =  filter(lambda x: (hasattr(x,"matched_CA15SD")), event.FatjetCA15)

        matched_fatjet = Match_two_lists(
            event.HTTV2, 'HTT',
            event.FatjetCA15SoftDrop, 'CA15SD',0.5)

        event.HTTV2 =  filter(lambda x: (hasattr(x,"matched_CA15SD")), event.HTTV2)
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
                setattr(i,"tau32SD",i.matched_CA15SD.tau32)
            event.HTTV2 = filter(lambda x: (x.drl>1.0 and x.btagmax > 0.1522), event.HTTV2)
        if cat == "dl":
            event.HTTV2 = []

        #Do the higgs now
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



        ########################################
        #Now get all variables of interest
        ########################################

        for i in ["H","T","HT"]:
            results[cat][i].Fill(1,event.Generator_weight)


        #Apply now found cuts for both taggers:
        event.FatjetCA15 = filter(
            lambda x, higgscuts=higgscuts: (
                x.tau21SD < higgscuts["nsub"]
                and x.bbtag > higgscuts["bbtag"]
                and x.btagmin > higgscuts["btagsl"]
            ), event.FatjetCA15
        )


        event.HTTV2 = filter(
            lambda x, topcuts=topcuts: (
                x.tau32SD < topcuts["nsub"]
                and x.mass > topcuts["massinf"]
                and x.mass < topcuts["masssup"]
                and x.frec < topcuts["frec"]
            ), event.HTTV2
        )

        case = None
        if len(event.FatjetCA15) and not len(event.HTTV2):
            case = "H"
        elif len(event.HTTV2) and not len(event.FatjetCA15):
            case = "T"
        elif len(event.FatjetCA15) and len(event.HTTV2):
            case = "HT"

        if case is not None:
            results[cat][case].Fill(2,event.Generator_weight)

        event.FatjetCA15 = sorted(event.FatjetCA15, key=lambda x: x.btagmin, reverse=True)
        event.HTTV2 = sorted(event.HTTV2, key=lambda x: x.frec)

        if case == "H" and event.FatjetCA15[0].matched == 1:
            results[cat][case].Fill(3,event.Generator_weight)

        if case == "T" and event.HTTV2[0].matched == 1:
            results[cat][case].Fill(3,event.Generator_weight)

        if case == "HT" and event.HTTV2[0].matched == 1 and event.FatjetCA15[0].matched == 1:
            results[cat][case].Fill(3,event.Generator_weight)




f.Close()
print counter 
BDTInput = ROOT.TFile("out.root","recreate")
for i in cats:
    for j in cases:
        results[i][j].Write()
BDTInput.Close()